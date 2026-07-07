#!/usr/bin/env python3
"""Train lightweight CPU learned-dynamics ensembles for CCR-MPC diagnostics.

This script is intentionally separate from the focused planner run. It produces
trained model artifacts and prediction metrics, but does not claim that the main
CCR-MPC results already use these learned models.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from torch import nn

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "scripts"))

from execute_paper_cpu_study import (  # noqa: E402
    LEVEL_SEVERITY,
    DomainSpec,
    domain_specs,
    pid_action,
    stable_seed,
    step_dynamics,
    true_params,
)


class DeltaMLP(nn.Module):
    def __init__(self, width: int = 32) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, width),
            nn.Tanh(),
            nn.Linear(width, width),
            nn.Tanh(),
            nn.Linear(width, 2),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def policy_action(state: np.ndarray, spec: DomainSpec, rng: np.random.Generator, mode: str) -> float:
    if mode == "random":
        return float(rng.uniform(-spec.action_limit, spec.action_limit))
    if mode == "nominal":
        return float(np.clip(pid_action(state, spec) + rng.normal(0.0, 0.12 * spec.action_limit), -spec.action_limit, spec.action_limit))
    exploratory = pid_action(state, spec, scale=0.65) + rng.normal(0.0, 0.45 * spec.action_limit)
    exploratory += 0.25 * spec.action_limit * math.sin(float(state[0]) * 3.0)
    return float(np.clip(exploratory, -spec.action_limit, spec.action_limit))


def generate_transition_data(
    spec: DomainSpec,
    level: str,
    seed: int,
    trajectories: int,
    steps: int,
    noisy: bool,
) -> Tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    params = true_params(spec, level)
    inputs: List[np.ndarray] = []
    targets: List[np.ndarray] = []
    modes = ["random", "nominal", "exploratory"]

    for traj_idx in range(trajectories):
        mode = modes[traj_idx % len(modes)]
        state = np.array(
            [
                spec.init_pos + rng.normal(0.0, 0.55 * spec.safe_limit),
                spec.init_vel + rng.normal(0.0, 0.35),
            ],
            dtype=float,
        )
        state[0] = float(np.clip(state[0], -0.95 * spec.safe_limit, 0.95 * spec.safe_limit))
        for _ in range(steps):
            action = policy_action(state, spec, rng, mode)
            next_state = step_dynamics(state, action, params, spec, rng=rng, noisy=noisy)
            inputs.append(np.array([state[0], state[1], action], dtype=float))
            targets.append(next_state - state)
            state = next_state
            if abs(float(state[0])) > 1.6 * spec.safe_limit:
                state[0] = float(np.sign(state[0]) * 0.75 * spec.safe_limit)
                state[1] *= 0.2

    return np.stack(inputs, axis=0), np.stack(targets, axis=0)


def standardize(x: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = x.mean(axis=0)
    std = x.std(axis=0)
    std = np.where(std < 1e-6, 1.0, std)
    return (x - mean) / std, mean, std


def train_member(
    train_x: np.ndarray,
    train_y: np.ndarray,
    seed: int,
    epochs: int,
    batch_size: int,
    width: int,
) -> DeltaMLP:
    torch.manual_seed(seed)
    model = DeltaMLP(width=width)
    opt = torch.optim.AdamW(model.parameters(), lr=2e-3, weight_decay=1e-4)
    x_t = torch.tensor(train_x, dtype=torch.float32)
    y_t = torch.tensor(train_y, dtype=torch.float32)
    n = x_t.shape[0]
    generator = torch.Generator().manual_seed(seed)
    for _ in range(epochs):
        order = torch.randperm(n, generator=generator)
        for start in range(0, n, batch_size):
            idx = order[start : start + batch_size]
            pred = model(x_t[idx])
            loss = torch.mean((pred - y_t[idx]) ** 2)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
    return model


def ensemble_predict(
    models: Sequence[DeltaMLP],
    x: np.ndarray,
    x_mean: np.ndarray,
    x_std: np.ndarray,
    y_mean: np.ndarray,
    y_std: np.ndarray,
) -> np.ndarray:
    x_n = (x - x_mean) / x_std
    x_t = torch.tensor(x_n, dtype=torch.float32)
    preds: List[np.ndarray] = []
    with torch.no_grad():
        for model in models:
            pred_delta = model(x_t).cpu().numpy() * y_std + y_mean
            preds.append(pred_delta + x[:, :2])
    return np.stack(preds, axis=0)


def rollout_mse(
    models: Sequence[DeltaMLP],
    spec: DomainSpec,
    level: str,
    normalizer: Mapping[str, np.ndarray],
    seed: int,
    rollouts: int,
) -> float:
    rng = np.random.default_rng(seed)
    params = true_params(spec, level)
    sq_errors: List[float] = []
    for i in range(rollouts):
        state_true = np.array(
            [
                spec.init_pos + rng.normal(0.0, 0.45 * spec.safe_limit),
                spec.init_vel + rng.normal(0.0, 0.25),
            ],
            dtype=float,
        )
        state_pred = state_true.copy()
        mode = ["random", "nominal", "exploratory"][i % 3]
        for _ in range(spec.horizon):
            action = policy_action(state_true, spec, rng, mode)
            state_true = step_dynamics(state_true, action, params, spec, rng=rng, noisy=False)
            inp = np.array([[state_pred[0], state_pred[1], action]], dtype=float)
            pred_all = ensemble_predict(models, inp, **normalizer)
            state_pred = pred_all.mean(axis=0)[0]
            sq_errors.append(float(np.mean((state_pred - state_true) ** 2)))
    return float(np.mean(sq_errors))


def evaluate_models(
    models: Sequence[DeltaMLP],
    spec: DomainSpec,
    level: str,
    normalizer: Mapping[str, np.ndarray],
    seed: int,
    samples: int,
    rollouts: int,
) -> Dict[str, float]:
    x_eval, y_eval = generate_transition_data(spec, level, seed, max(4, samples // spec.steps), spec.steps, noisy=False)
    x_eval = x_eval[:samples]
    true_next = x_eval[:, :2] + y_eval[:samples]
    preds = ensemble_predict(models, x_eval, **normalizer)
    mean_pred = preds.mean(axis=0)
    std_pred = preds.std(axis=0)
    one_step_mse = float(np.mean((mean_pred - true_next) ** 2))
    lower = mean_pred - 1.645 * (std_pred + 1e-8)
    upper = mean_pred + 1.645 * (std_pred + 1e-8)
    coverage = float(np.mean((true_next >= lower) & (true_next <= upper)))
    disagreement = float(np.mean(np.linalg.norm(std_pred, axis=1)))
    r_mse = rollout_mse(models, spec, level, normalizer, seed + 17, rollouts)
    return {
        "one_step_mse": one_step_mse,
        "rollout_mse": r_mse,
        "interval90_coverage": coverage,
        "model_disagreement": disagreement,
    }


def control_risk_lookup() -> Dict[Tuple[str, str], float]:
    path = ROOT / "logs" / "results_flat.csv"
    if not path.exists():
        return {}
    df = pd.read_csv(path)
    grouped = df.groupby(["domain", "level"])["violation_rate"].mean()
    return {(str(domain), str(level)): float(value) for (domain, level), value in grouped.items()}


def write_report(metrics: pd.DataFrame, args: argparse.Namespace) -> None:
    report_path = ROOT / "reports" / "dynamics_training_report.md"
    by_level = metrics.groupby("level")[["one_step_mse", "rollout_mse", "interval90_coverage", "model_disagreement"]].mean()
    lines = [
        "# Dynamics Training Report",
        "",
        "## Status",
        "",
        "This run trained bootstrapped Torch MLP one-step dynamics ensembles on CPU for each existing CCR-MPC domain.",
        "These artifacts are diagnostic evidence only: the current focused CCR-MPC planner results still use the original parameter-particle surrogate models.",
        "",
        "## Training Configuration",
        "",
        f"- Ensemble size: {args.ensemble_size}",
        f"- Training trajectories per domain: {args.train_trajectories}",
        f"- Training steps per trajectory: {args.train_steps}",
        f"- Epochs per ensemble member: {args.epochs}",
        f"- Hidden width: {args.width}",
        "- Training level: L0 nominal dynamics",
        "- Evaluation levels: L0, L1, L2 when present",
        "",
        "## Aggregate Metrics",
        "",
        by_level.to_markdown(floatfmt=".6f"),
        "",
        "## Artifacts",
        "",
        "- `artifacts/models/*_torch_mlp_ensemble.pt`",
        "- `logs/dynamics_prediction_metrics.csv`",
        "- `figures/prediction_calibration_vs_control_risk.png`",
        "",
        "## Limitations",
        "",
        "- Models are trained on the existing simplified 2D domains, not high-fidelity robot simulators.",
        "- The trained ensembles are not yet wired into the MPC experiment runner.",
        "- The coverage metric is an ensemble-spread interval diagnostic, not a formal conformal guarantee.",
    ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def plot_calibration_vs_risk(metrics: pd.DataFrame) -> None:
    fig_path = ROOT / "figures" / "prediction_calibration_vs_control_risk.png"
    plot_df = metrics.dropna(subset=["existing_focus_violation_rate"]).copy()
    plot_df["coverage_error"] = (0.90 - plot_df["interval90_coverage"]).abs()

    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    for level, part in plot_df.groupby("level"):
        ax.scatter(part["coverage_error"], part["existing_focus_violation_rate"], label=level, s=58, alpha=0.85)
        for _, row in part.iterrows():
            ax.annotate(str(row["domain"]).replace("_", "\n"), (row["coverage_error"], row["existing_focus_violation_rate"]), fontsize=7, alpha=0.75)
    ax.set_xlabel("Prediction interval calibration error |0.90 - coverage|")
    ax.set_ylabel("Existing focused-run control violation rate")
    ax.set_title("Prediction Calibration Diagnostic vs Control Risk")
    ax.grid(True, alpha=0.25)
    ax.legend(title="OOD level")
    fig.tight_layout()
    fig.savefig(fig_path, dpi=180)
    plt.close(fig)


def save_models(
    spec: DomainSpec,
    models: Sequence[DeltaMLP],
    normalizer: Mapping[str, np.ndarray],
    args: argparse.Namespace,
) -> Path:
    model_dir = ROOT / "artifacts" / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    path = model_dir / f"{spec.name}_torch_mlp_ensemble.pt"
    payload = {
        "domain": asdict(spec),
        "model_class": "DeltaMLP",
        "train_level": "L0",
        "ensemble_size": args.ensemble_size,
        "hidden_width": args.width,
        "normalizer": {key: value.tolist() for key, value in normalizer.items()},
        "state_dicts": [model.state_dict() for model in models],
    }
    torch.save(payload, path)
    return path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train CPU learned dynamics ensembles for CCR-MPC diagnostics.")
    parser.add_argument("--ensemble-size", type=int, default=5)
    parser.add_argument("--train-trajectories", type=int, default=48)
    parser.add_argument("--train-steps", type=int, default=18)
    parser.add_argument("--eval-samples", type=int, default=320)
    parser.add_argument("--eval-rollouts", type=int, default=48)
    parser.add_argument("--epochs", type=int, default=70)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--width", type=int, default=32)
    parser.add_argument("--domains", default="all")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    torch.set_num_threads(max(1, min(4, torch.get_num_threads())))
    selected_names = None if args.domains == "all" else {part.strip() for part in args.domains.split(",") if part.strip()}
    specs = [spec for spec in domain_specs() if selected_names is None or spec.name in selected_names]
    if not specs:
        raise ValueError("no domains selected")

    risk_by_domain_level = control_risk_lookup()
    rows: List[Dict[str, object]] = []
    model_paths: List[Path] = []

    for spec in specs:
        seed = stable_seed("torch_dynamics_train", spec.name)
        x_raw, y_raw = generate_transition_data(spec, "L0", seed, args.train_trajectories, args.train_steps, noisy=True)
        x_train, x_mean, x_std = standardize(x_raw)
        y_train, y_mean, y_std = standardize(y_raw)
        normalizer = {"x_mean": x_mean, "x_std": x_std, "y_mean": y_mean, "y_std": y_std}
        rng = np.random.default_rng(seed)
        models: List[DeltaMLP] = []
        for member_idx in range(args.ensemble_size):
            boot_idx = rng.integers(0, x_train.shape[0], size=x_train.shape[0])
            model = train_member(
                x_train[boot_idx],
                y_train[boot_idx],
                seed + 1009 * (member_idx + 1),
                args.epochs,
                args.batch_size,
                args.width,
            )
            models.append(model)
        model_paths.append(save_models(spec, models, normalizer, args))

        for level in LEVEL_SEVERITY:
            metrics = evaluate_models(
                models,
                spec,
                level,
                normalizer,
                stable_seed("torch_dynamics_eval", spec.name, level),
                args.eval_samples,
                args.eval_rollouts,
            )
            rows.append(
                {
                    "domain": spec.name,
                    "level": level,
                    "model_class": "torch_mlp_delta_ensemble",
                    "ensemble_size": args.ensemble_size,
                    "train_samples": int(x_train.shape[0]),
                    "eval_samples": args.eval_samples,
                    "one_step_mse": metrics["one_step_mse"],
                    "rollout_mse": metrics["rollout_mse"],
                    "interval90_coverage": metrics["interval90_coverage"],
                    "model_disagreement": metrics["model_disagreement"],
                    "existing_focus_violation_rate": risk_by_domain_level.get((spec.name, level), float("nan")),
                    "model_artifact": model_paths[-1].relative_to(ROOT).as_posix(),
                }
            )
        print(f"trained {spec.name}: {model_paths[-1].relative_to(ROOT).as_posix()}")

    logs_dir = ROOT / "logs"
    logs_dir.mkdir(exist_ok=True)
    metrics_df = pd.DataFrame(rows)
    metrics_df.to_csv(logs_dir / "dynamics_prediction_metrics.csv", index=False)
    plot_calibration_vs_risk(metrics_df)
    write_report(metrics_df, args)

    summary = {
        "domains": [spec.name for spec in specs],
        "model_artifacts": [path.relative_to(ROOT).as_posix() for path in model_paths],
        "metrics": "logs/dynamics_prediction_metrics.csv",
        "report": "reports/dynamics_training_report.md",
        "figure": "figures/prediction_calibration_vs_control_risk.png",
    }
    (ROOT / "artifacts" / "models" / "training_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print("wrote logs/dynamics_prediction_metrics.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
