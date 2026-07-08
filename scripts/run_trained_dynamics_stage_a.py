#!/usr/bin/env python3
"""Run Stage-A CCR-MPC experiments using trained Torch dynamics ensembles.

The original focused suite uses parameter-particle surrogates. This script is a
separate evidence path: it loads the trained MLP ensembles from `artifacts/models`
and uses them inside the planner candidate evaluator for D0/D1 Stage-A runs.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "skeleton"))

from execute_paper_cpu_study import (  # noqa: E402
    LEVEL_SEVERITY,
    METHODS,
    TARGET_RISK,
    CalibrationBundle,
    DomainSpec,
    aggregate_oracle_regret,
    calibration_metrics,
    constraint_eval,
    domain_specs,
    evaluate_candidates,
    flatten_result,
    sample_action_sequences,
    select_candidate,
    sha256_file,
    sha256_text,
    stable_seed,
    step_cost,
    step_dynamics,
    true_params,
)
from ccr_mpc import CCRConfig, RiskCalibrator, ccr_score  # noqa: E402
from train_learned_dynamics_cpu import DeltaMLP  # noqa: E402


class TrainedDynamicsBundle:
    def __init__(
        self,
        domain: str,
        models: Sequence[DeltaMLP],
        normalizer: Mapping[str, np.ndarray],
        artifact_path: Path,
    ) -> None:
        self.domain = domain
        self.models = list(models)
        self.normalizer = dict(normalizer)
        self.artifact_path = artifact_path
        self.artifact_hash = sha256_file(artifact_path)


def parse_list(value: str, default: Sequence[str]) -> List[str]:
    if value == "all":
        return list(default)
    return [part.strip() for part in value.split(",") if part.strip()]


def load_trained_bundle(spec: DomainSpec) -> TrainedDynamicsBundle:
    path = ROOT / "artifacts" / "models" / f"{spec.name}_torch_mlp_ensemble.pt"
    if not path.exists():
        raise FileNotFoundError(f"missing trained dynamics artifact: {path}")
    payload = torch.load(path, map_location="cpu", weights_only=False)
    width = int(payload.get("hidden_width", 32))
    models: List[DeltaMLP] = []
    for state_dict in payload["state_dicts"]:
        model = DeltaMLP(width=width)
        model.load_state_dict(state_dict)
        model.eval()
        models.append(model)
    normalizer = {key: np.asarray(value, dtype=float) for key, value in payload["normalizer"].items()}
    return TrainedDynamicsBundle(spec.name, models, normalizer, path)


def predict_next_batch(model: DeltaMLP, states: np.ndarray, actions: np.ndarray, bundle: TrainedDynamicsBundle) -> np.ndarray:
    x = np.column_stack([states[:, 0], states[:, 1], actions])
    norm = bundle.normalizer
    x_n = (x - norm["x_mean"]) / norm["x_std"]
    with torch.no_grad():
        delta_n = model(torch.tensor(x_n, dtype=torch.float32)).cpu().numpy()
    delta = delta_n * norm["y_std"] + norm["y_mean"]
    return states + delta


def evaluate_candidates_trained(
    bundle: TrainedDynamicsBundle,
    state: np.ndarray,
    action_sequences: np.ndarray,
    spec: DomainSpec,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    k_count = len(bundle.models)
    n_count = action_sequences.shape[0]
    horizon = action_sequences.shape[1]
    actions = action_sequences[:, :, 0]
    costs = np.zeros((k_count, n_count), dtype=float)
    violations = np.zeros((k_count, n_count), dtype=float)
    margins = np.zeros((k_count, n_count), dtype=float)

    for model_idx, model in enumerate(bundle.models):
        states = np.repeat(np.asarray(state, dtype=float)[None, :], n_count, axis=0)
        min_margin = spec.safe_limit - np.abs(states[:, 0])
        target_error = states[:, 0] - spec.target
        violation = np.maximum(0.0, np.abs(states[:, 0]) - spec.safe_limit)
        cost = 2.8 * target_error**2 + 0.35 * states[:, 1] ** 2 + 42.0 * violation**2
        for h in range(horizon):
            u = np.clip(actions[:, h], -spec.action_limit, spec.action_limit)
            states = predict_next_batch(model, states, u, bundle)
            margin = spec.safe_limit - np.abs(states[:, 0])
            min_margin = np.minimum(min_margin, margin)
            target_error = states[:, 0] - spec.target
            violation = np.maximum(0.0, np.abs(states[:, 0]) - spec.safe_limit)
            cost += 2.8 * target_error**2 + 0.35 * states[:, 1] ** 2 + 0.05 * u**2 + 42.0 * violation**2
        cost += 4.0 * (states[:, 0] - spec.target) ** 2
        costs[model_idx, :] = cost
        violations[model_idx, :] = (min_margin < 0.0).astype(float)
        margins[model_idx, :] = min_margin
    return costs, violations, margins


def normalize(values: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    lo = np.nanmin(values)
    hi = np.nanmax(values)
    if not np.isfinite(lo) or not np.isfinite(hi) or hi - lo <= eps:
        return np.zeros_like(values, dtype=float)
    return (values - lo) / (hi - lo + eps)


def calibrate_trained_domain_level(
    spec: DomainSpec,
    level: str,
    bundle: TrainedDynamicsBundle,
    contexts: int,
    candidates: int,
    alpha: float,
) -> CalibrationBundle:
    rng = np.random.default_rng(stable_seed("trained_stage_a_calibration", spec.name, level))
    true = true_params(spec, level)
    cfg = CCRConfig(alpha=alpha, cvar_quantile=0.80)
    score_lists: Dict[str, List[float]] = {
        "combined": [],
        "uncertainty": [],
        "violation_rate": [],
        "rank_instability": [],
        "regret_cvar": [],
        "violation_tail": [],
        "negative_margin_tail": [],
    }
    failures: List[float] = []
    rows: List[Dict[str, float]] = []

    for context_idx in range(contexts):
        center = np.array([spec.target, 0.0], dtype=float)
        state = center + rng.normal(0.0, [0.42 * spec.safe_limit, 0.30], size=2)
        state[0] = np.clip(state[0], -0.92 * spec.safe_limit, 0.92 * spec.safe_limit)
        actions = sample_action_sequences(state, spec, rng, candidates, spec.planner)
        costs, violations, margins = evaluate_candidates_trained(bundle, state, actions, spec)
        true_costs, true_violations, _ = evaluate_candidates([true], state, actions, spec)
        features = ccr_score(costs, violations, margins, cfg, actions)
        arrays = {
            "combined": normalize(features["combined"]),
            "uncertainty": normalize(np.std(costs, axis=0)),
            "violation_rate": np.asarray(features["violation_rate"]),
            "rank_instability": normalize(features["rank_instability"]),
            "regret_cvar": normalize(features["regret_cvar"]),
            "violation_tail": normalize(features["violation_tail"]),
            "negative_margin_tail": normalize(features["negative_margin_tail"]),
        }
        for candidate_idx in range(actions.shape[0]):
            failure = float(true_violations[0, candidate_idx] > 0.0)
            failures.append(failure)
            for key, arr in arrays.items():
                score_lists[key].append(float(arr[candidate_idx]))
            if context_idx < 12:
                rows.append(
                    {
                        "domain": spec.name,
                        "level": level,
                        "context": float(context_idx),
                        "candidate": float(candidate_idx),
                        "true_failure": failure,
                        "true_cost": float(true_costs[0, candidate_idx]),
                        "combined": float(arrays["combined"][candidate_idx]),
                        "uncertainty": float(arrays["uncertainty"][candidate_idx]),
                        "violation_rate": float(arrays["violation_rate"][candidate_idx]),
                        "rank_instability": float(arrays["rank_instability"][candidate_idx]),
                        "regret_cvar": float(arrays["regret_cvar"][candidate_idx]),
                        "violation_tail": float(arrays["violation_tail"][candidate_idx]),
                    }
                )

    failure_arr = np.asarray(failures, dtype=float)
    calibrators = {
        key: RiskCalibrator(confidence_delta=0.10).fit(np.asarray(scores, dtype=float), failure_arr)
        for key, scores in score_lists.items()
    }
    return CalibrationBundle(calibrators=calibrators, rows=rows)


def run_episode_trained(
    spec: DomainSpec,
    method: str,
    level: str,
    seed: int,
    calibrators: Mapping[str, RiskCalibrator],
    bundle: TrainedDynamicsBundle,
    num_candidates: int,
    alpha: float,
    code_hash: str,
) -> Tuple[Dict[str, object], List[Dict[str, object]]]:
    init_rng = np.random.default_rng(stable_seed("trained_stage_a_init", spec.name, level, seed))
    plan_rng = np.random.default_rng(stable_seed("trained_stage_a_planner", spec.name, level, method, seed))
    noise_rng = np.random.default_rng(stable_seed("trained_stage_a_noise", spec.name, level, seed))
    state = np.array(
        [
            spec.init_pos + init_rng.normal(0.0, spec.init_std),
            spec.init_vel + init_rng.normal(0.0, spec.init_std * 0.5),
        ],
        dtype=float,
    )
    true = true_params(spec, level)
    total_cost = 0.0
    actions_taken: List[float] = []
    step_failures: List[float] = []
    plan_failures: List[float] = []
    pred_risks: List[float] = []
    pred_errors: List[float] = []
    feature_rows: List[Dict[str, object]] = []
    fallback_count = 0
    compute_times: List[float] = []

    for step_idx in range(spec.steps):
        t0 = time.perf_counter()
        actions = sample_action_sequences(state, spec, plan_rng, num_candidates, spec.planner)
        if method == "oracle_mpc":
            costs, violations, margins = evaluate_candidates([true], state, actions, spec)
        else:
            costs, violations, margins = evaluate_candidates_trained(bundle, state, actions, spec)
        idx, pred_risk, fallback, feature_summary = select_candidate(
            method, costs, violations, margins, actions, calibrators, alpha, spec, state
        )
        true_costs, true_violations, _ = evaluate_candidates([true], state, actions, spec)
        compute_times.append(1000.0 * (time.perf_counter() - t0))

        action = float(actions[idx, 0, 0])
        model_nexts = np.stack(
            [
                predict_next_batch(model, state.reshape(1, 2), np.array([action]), bundle)[0]
                for model in bundle.models
            ],
            axis=0,
        )
        true_next_det = step_dynamics(state, action, true, spec, noisy=False)
        pred_errors.append(float(np.linalg.norm(model_nexts.mean(axis=0) - true_next_det)))
        next_state = step_dynamics(state, action, true, spec, rng=noise_rng, noisy=True)
        violation, margin = constraint_eval(next_state.reshape(1, 2), spec)

        total_cost += step_cost(next_state, action, spec)
        actions_taken.append(action)
        step_failures.append(float(violation > 0.0))
        plan_failures.append(float(true_violations[0, idx] > 0.0))
        pred_risks.append(pred_risk)
        if fallback:
            fallback_count += 1
        feature_rows.append(
            {
                "domain": spec.name,
                "method": method,
                "level": level,
                "seed": seed,
                "step": step_idx,
                "pred_risk": pred_risk,
                "plan_failure": float(true_violations[0, idx] > 0.0),
                "step_violation": float(violation > 0.0),
                "action": action,
                "state_pos": float(state[0]),
                "state_vel": float(state[1]),
                "next_pos": float(next_state[0]),
                "true_plan_cost": float(true_costs[0, idx]),
                "margin": float(margin),
                "fallback": float(fallback),
                **feature_summary,
            }
        )
        state = next_state

    cal = calibration_metrics(pred_risks, plan_failures)
    run_id = sha256_text(f"trained-stage-a:{spec.name}:{method}:{level}:{seed}")[:16]
    violation_rate = float(np.mean(step_failures))
    result = {
        "run_id": run_id,
        "domain": spec.name,
        "method": method,
        "seed": seed,
        "task": spec.label,
        "ood_shift": {"name": spec.shift_name, "level": level, "severity": LEVEL_SEVERITY[level]},
        "planner": spec.planner,
        "dynamics_model": "oracle" if method == "oracle_mpc" else "trained_torch_mlp_ensemble",
        "metrics": {
            "reward": float(-total_cost),
            "cost": float(total_cost),
            "violation_rate": violation_rate,
            "observed_risk": float(np.max(step_failures)),
            "target_risk": alpha,
            "ece": cal["ece"],
            "brier": cal["brier"],
            "log_loss": cal["log_loss"],
            "freezing_rate": float(np.mean(np.abs(actions_taken) < 0.05 * spec.action_limit)),
            "compute_ms": float(np.mean(compute_times)),
            "oracle_regret": 0.0,
            "fallback_rate": float(fallback_count / spec.steps),
            "decision_disagreement": float(np.mean([row["rank_instability"] for row in feature_rows])),
            "empirical_coverage": float(1.0 - violation_rate),
            "prediction_error": float(np.mean(pred_errors)),
        },
        "artifacts": {
            "config_path": "configs/trained_dynamics_stage_a_config.json",
            "log_path": "logs/trained_dynamics_stage_a_results.jsonl",
            "plot_paths": [],
            "model_hash": bundle.artifact_hash[:16],
            "code_hash": code_hash,
        },
    }
    return result, feature_rows


def write_jsonl(path: Path, rows: Iterable[Mapping[str, object]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    def sem(values: pd.Series) -> float:
        return float(np.std(values, ddof=1) / math.sqrt(len(values))) if len(values) > 1 else 0.0

    return df.groupby("method", as_index=False).agg(
        cost_mean=("cost", "mean"),
        cost_sem=("cost", sem),
        violation_rate_mean=("violation_rate", "mean"),
        violation_rate_sem=("violation_rate", sem),
        observed_risk_mean=("observed_risk", "mean"),
        compute_ms_mean=("compute_ms", "mean"),
        prediction_error_mean=("prediction_error", "mean"),
        freezing_rate_mean=("freezing_rate", "mean"),
        fallback_rate_mean=("fallback_rate", "mean"),
    )


def write_reports(df: pd.DataFrame, summary: pd.DataFrame, args: argparse.Namespace, elapsed_s: float) -> None:
    reports_dir = ROOT / "reports"
    tables_dir = ROOT / "tables"
    reports_dir.mkdir(exist_ok=True)
    tables_dir.mkdir(exist_ok=True)
    summary_path = tables_dir / "trained_dynamics_stage_a_summary_by_method.csv"
    summary.to_csv(summary_path, index=False)
    domain_path = tables_dir / "trained_dynamics_stage_a_summary_by_domain_method.csv"
    df.groupby(["domain", "method"], as_index=False).agg(
        cost_mean=("cost", "mean"),
        violation_rate_mean=("violation_rate", "mean"),
        prediction_error_mean=("prediction_error", "mean"),
    ).to_csv(domain_path, index=False)

    ccr = summary[summary["method"] == "ccr_mpc"]
    cvar = summary[summary["method"] == "cvar_ra_mppi"]
    conf = summary[summary["method"] == "conformal_prediction_mpc"]
    vanilla = summary[summary["method"] == "vanilla_mppi"]
    def row_text(row: pd.DataFrame) -> str:
        if row.empty:
            return "missing"
        r = row.iloc[0]
        return f"cost={float(r['cost_mean']):.4f}, violation={float(r['violation_rate_mean']):.4f}"

    report = [
        "# Trained-Dynamics Stage-A Report",
        "",
        "## Status",
        "",
        "This Stage-A run uses trained Torch MLP dynamics ensembles inside the planner candidate evaluator for D0/D1.",
        "It is a real integration checkpoint, but it is not the final max-out run and does not replace the original focused-suite evidence.",
        "",
        "## Scope",
        "",
        f"- Domains: {args.domains}",
        f"- Methods: {args.methods}",
        f"- Levels: {args.levels}",
        f"- Seeds: {args.seeds}",
        f"- Candidate budget: {args.candidates}",
        f"- Calibration contexts per domain/level: {args.calibration_contexts}",
        f"- Runtime seconds: {elapsed_s:.2f}",
        "",
        "## Key Aggregate Rows",
        "",
        f"- Vanilla MPPI: {row_text(vanilla)}",
        f"- CCR-MPC: {row_text(ccr)}",
        f"- CVaR/RA-MPPI: {row_text(cvar)}",
        f"- Conformal prediction MPC: {row_text(conf)}",
        "",
        "## Artifacts",
        "",
        "- `logs/trained_dynamics_stage_a_results.jsonl`",
        "- `logs/trained_dynamics_stage_a_results_flat.csv`",
        "- `logs/trained_dynamics_stage_a_step_predictions.csv`",
        "- `tables/trained_dynamics_stage_a_summary_by_method.csv`",
        "- `tables/trained_dynamics_stage_a_summary_by_domain_method.csv`",
        "- `configs/trained_dynamics_stage_a_config.json`",
        "",
        "## Limitations",
        "",
        "- Only D0/D1 Stage-A domains are included.",
        "- The calibration labels are still simulator candidate labels, not executed-rollout calibration.",
        "- Method names such as `sysid_mpc` and `domain_randomized_mpc` are run through the trained-model candidate evaluator in this integration checkpoint unless the method is `oracle_mpc`; they are not yet full tuned specialized baselines.",
        "- No strong-superiority claim is allowed from this Stage-A run alone.",
    ]
    (reports_dir / "trained_dynamics_stage_a_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    integration = [
        "# Trained-Dynamics Planner Integration",
        "",
        "## What Changed",
        "",
        "`scripts/run_trained_dynamics_stage_a.py` loads `artifacts/models/*_torch_mlp_ensemble.pt` and uses the learned models to roll out sampled MPC candidates. Candidate costs, violation indicators, margins, CCR features, and calibrated gates are computed from trained ensemble predictions rather than parameter-particle surrogates.",
        "",
        "## What Remains",
        "",
        "The original focused suite still uses the parameter-particle runner. The trained-dynamics runner is separate so the old artifact hashes and claims remain reproducible.",
        "",
        "## Next Integration Step",
        "",
        "Promote `trained_torch_mlp_ensemble` to a first-class `--model-source` option in `scripts/execute_paper_cpu_study.py` once Stage-A behavior is stable.",
    ]
    (reports_dir / "trained_dynamics_planner_integration.md").write_text("\n".join(integration) + "\n", encoding="utf-8")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage-A trained-dynamics CCR-MPC experiments.")
    parser.add_argument("--domains", default="synthetic_separation,classic_control")
    parser.add_argument("--methods", default="all")
    parser.add_argument("--levels", default="L0,L1,L2")
    parser.add_argument("--seeds", default="0,1,2,3,4")
    parser.add_argument("--candidates", type=int, default=24)
    parser.add_argument("--calibration-contexts", type=int, default=24)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    start = time.perf_counter()
    torch.set_num_threads(max(1, min(4, torch.get_num_threads())))
    all_domains = domain_specs()
    domain_names = parse_list(args.domains, [spec.name for spec in all_domains])
    method_names = parse_list(args.methods, METHODS)
    levels = parse_list(args.levels, list(LEVEL_SEVERITY))
    seeds = [int(part) for part in parse_list(args.seeds, [])]
    selected_domains = [spec for spec in all_domains if spec.name in domain_names]
    missing_domains = sorted(set(domain_names) - {spec.name for spec in selected_domains})
    missing_methods = sorted(set(method_names) - set(METHODS))
    missing_levels = sorted(set(levels) - set(LEVEL_SEVERITY))
    if missing_domains:
        raise ValueError(f"unknown domains: {missing_domains}")
    if missing_methods:
        raise ValueError(f"unknown methods: {missing_methods}")
    if missing_levels:
        raise ValueError(f"unknown levels: {missing_levels}")

    code_hash = sha256_file(Path(__file__))
    bundles = {spec.name: load_trained_bundle(spec) for spec in selected_domains}
    calibration_cache: Dict[Tuple[str, str], CalibrationBundle] = {}
    calibration_rows: List[Dict[str, float]] = []
    for spec in selected_domains:
        for level in levels:
            bundle = bundles[spec.name]
            calibration = calibrate_trained_domain_level(
                spec,
                level,
                bundle,
                args.calibration_contexts,
                max(18, args.candidates // 2),
                TARGET_RISK,
            )
            calibration_cache[(spec.name, level)] = calibration
            calibration_rows.extend(calibration.rows)
            print(f"calibrated trained {spec.name}/{level}")

    results: List[Dict[str, object]] = []
    step_rows: List[Dict[str, object]] = []
    total_jobs = len(selected_domains) * len(levels) * len(seeds) * len(method_names)
    job_idx = 0
    for spec in selected_domains:
        bundle = bundles[spec.name]
        for level in levels:
            calibrators = calibration_cache[(spec.name, level)].calibrators
            for seed in seeds:
                for method in method_names:
                    job_idx += 1
                    result, rows = run_episode_trained(
                        spec,
                        method,
                        level,
                        seed,
                        calibrators,
                        bundle,
                        args.candidates,
                        TARGET_RISK,
                        code_hash,
                    )
                    results.append(result)
                    step_rows.extend(rows)
                    if job_idx % 25 == 0 or job_idx == total_jobs:
                        print(f"completed {job_idx}/{total_jobs}")

    logs_dir = ROOT / "logs"
    configs_dir = ROOT / "configs"
    logs_dir.mkdir(exist_ok=True)
    configs_dir.mkdir(exist_ok=True)
    write_jsonl(logs_dir / "trained_dynamics_stage_a_results.jsonl", results)
    flat = pd.DataFrame([flatten_result(row) for row in results])
    flat = aggregate_oracle_regret(flat)
    flat.to_csv(logs_dir / "trained_dynamics_stage_a_results_flat.csv", index=False)
    pd.DataFrame(step_rows).to_csv(logs_dir / "trained_dynamics_stage_a_step_predictions.csv", index=False)
    pd.DataFrame(calibration_rows).to_csv(logs_dir / "trained_dynamics_stage_a_calibration_samples.csv", index=False)
    summary = summarize(flat)
    elapsed_s = time.perf_counter() - start
    write_reports(flat, summary, args, elapsed_s)

    config = {
        "created_utc": pd.Timestamp.utcnow().isoformat(),
        "execution_record_type": "trained_dynamics_stage_a",
        "args": vars(args),
        "run_settings": {
            "domains": [spec.name for spec in selected_domains],
            "methods": method_names,
            "levels": levels,
            "seeds": seeds,
            "num_candidates": args.candidates,
            "calibration_contexts": args.calibration_contexts,
            "target_risk": TARGET_RISK,
        },
        "execution_seconds": elapsed_s,
        "domains": [asdict(spec) for spec in selected_domains],
        "model_source": "trained_torch_mlp_ensemble",
        "model_artifacts": {
            name: {
                "path": bundle.artifact_path.relative_to(ROOT).as_posix(),
                "sha256": bundle.artifact_hash,
            }
            for name, bundle in bundles.items()
        },
        "code_hash": code_hash,
    }
    (configs_dir / "trained_dynamics_stage_a_config.json").write_text(json.dumps(config, indent=2, sort_keys=True), encoding="utf-8")
    print(f"wrote trained Stage-A results in {elapsed_s:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
