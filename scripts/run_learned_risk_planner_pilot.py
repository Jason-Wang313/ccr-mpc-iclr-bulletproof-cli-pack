#!/usr/bin/env python3
"""Run a held-out planner pilot with executed-rollout learned risk models."""

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
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "skeleton"))

from ccr_mpc import CCRConfig, ccr_score  # noqa: E402
from execute_paper_cpu_study import (  # noqa: E402
    LEVEL_SEVERITY,
    TARGET_RISK,
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
from run_trained_dynamics_stage_a import (  # noqa: E402
    TrainedDynamicsBundle,
    calibrate_trained_domain_level,
    evaluate_candidates_trained,
    load_trained_bundle,
    normalize,
    parse_list,
    safe_artifact_tag,
    summarize,
    write_jsonl,
)


FEATURE_NAMES = [
    "combined",
    "regret_cvar",
    "violation_tail",
    "rank_instability",
    "uncertainty",
    "pred_violation_rate",
]
LEARNED_METHODS = {"learned_risk_executed_rf", "learned_risk_executed_logistic", "learned_risk_executed_selected"}
BASELINE_METHODS = {
    "vanilla_mppi",
    "robust_mpc",
    "cvar_ra_mppi",
    "conformal_prediction_mpc",
    "conformal_risk_non_ccr",
    "ccr_no_calibration",
    "ccr_mpc",
    "oracle_mpc",
}


class LearnedRiskModels:
    def __init__(
        self,
        models: Mapping[str, object],
        selected_name: str,
        thresholds: Mapping[str, float],
        validation_rows: Sequence[Mapping[str, object]],
        label: str,
    ) -> None:
        self.models = dict(models)
        self.selected_name = selected_name
        self.thresholds = dict(thresholds)
        self.validation_rows = list(validation_rows)
        self.label = label

    def resolve(self, method: str) -> Tuple[str, object, float]:
        if method == "learned_risk_executed_rf":
            name = "random_forest"
        elif method == "learned_risk_executed_logistic":
            name = "logistic"
        elif method == "learned_risk_executed_selected":
            name = self.selected_name
        else:
            raise ValueError(method)
        return name, self.models[name], self.thresholds[name]


def candidate_features(costs: np.ndarray, violations: np.ndarray, margins: np.ndarray, actions: np.ndarray) -> np.ndarray:
    cfg = CCRConfig(alpha=TARGET_RISK, cvar_quantile=0.80)
    features = ccr_score(costs, violations, margins, cfg, actions)
    cost_uncertainty = normalize(np.std(costs, axis=0))
    columns = [
        normalize(features["combined"]),
        normalize(features["regret_cvar"]),
        normalize(features["violation_tail"]),
        normalize(features["rank_instability"]),
        cost_uncertainty,
        np.asarray(features["violation_rate"], dtype=float),
    ]
    return np.column_stack(columns)


def candidate_feature_summary(feature_matrix: np.ndarray, idx: int) -> Dict[str, float]:
    return {name: float(feature_matrix[idx, col]) for col, name in enumerate(FEATURE_NAMES)}


def predict_risk(model: object, feature_matrix: np.ndarray) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return np.asarray(model.predict_proba(feature_matrix)[:, 1], dtype=float)
    pred = np.asarray(model.predict(feature_matrix), dtype=float)
    return np.clip(pred, 0.0, 1.0)


def select_threshold(pred: np.ndarray, labels: np.ndarray, alpha: float) -> Dict[str, float]:
    order = np.argsort(pred)
    best = {
        "threshold": float(np.min(pred) - 1e-9) if len(pred) else 0.0,
        "accept_rate": 0.0,
        "accepted_failure_rate": 0.0,
        "accepted_count": 0.0,
    }
    for threshold in np.unique(pred[order]):
        accepted = pred <= float(threshold)
        count = int(np.sum(accepted))
        if count == 0:
            continue
        failure = float(np.mean(labels[accepted]))
        row = {
            "threshold": float(threshold),
            "accept_rate": float(np.mean(accepted)),
            "accepted_failure_rate": failure,
            "accepted_count": float(count),
        }
        if failure <= alpha and row["accept_rate"] >= best["accept_rate"]:
            best = row
    return best


def model_metrics(name: str, model: object, x: np.ndarray, y: np.ndarray, alpha: float) -> Dict[str, object]:
    pred = predict_risk(model, x)
    threshold = select_threshold(pred, y, alpha)
    has_both = len(set(float(v) for v in y)) == 2
    return {
        "risk_model": name,
        "n": int(len(y)),
        "positive_rate": float(np.mean(y)) if len(y) else 0.0,
        "brier": float(brier_score_loss(y, np.clip(pred, 1e-6, 1.0 - 1e-6))) if len(y) else float("nan"),
        "roc_auc": float(roc_auc_score(y, pred)) if has_both else float("nan"),
        **threshold,
    }


def fit_learned_risk_models(step_log: Path, label: str, alpha: float, selected_override: str = "auto") -> LearnedRiskModels:
    df = pd.read_csv(step_log)
    missing = [name for name in FEATURE_NAMES + [label, "seed"] if name not in df.columns]
    if missing:
        raise ValueError(f"missing columns in {step_log}: {missing}")

    train = df[df["seed"].isin([0, 1, 2])].copy()
    validation = df[df["seed"] == 3].copy()
    test = df[df["seed"] == 4].copy()
    if train.empty or validation.empty:
        raise ValueError("Stage-A step log must include train seeds 0-2 and validation seed 3")

    x_train = train[FEATURE_NAMES].to_numpy(dtype=float)
    y_train = train[label].to_numpy(dtype=float)
    x_validation = validation[FEATURE_NAMES].to_numpy(dtype=float)
    y_validation = validation[label].to_numpy(dtype=float)
    x_test = test[FEATURE_NAMES].to_numpy(dtype=float) if not test.empty else x_validation
    y_test = test[label].to_numpy(dtype=float) if not test.empty else y_validation

    models: Dict[str, object] = {
        "logistic": make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=1000, class_weight="balanced", random_state=313),
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=240,
            min_samples_leaf=8,
            class_weight="balanced_subsample",
            random_state=313,
            n_jobs=-1,
        ),
    }
    for model in models.values():
        model.fit(x_train, y_train)

    validation_rows: List[Dict[str, object]] = []
    thresholds: Dict[str, float] = {}
    for name, model in models.items():
        validation_row = {
            "split": "validation_seed_3",
            **model_metrics(name, model, x_validation, y_validation, alpha),
        }
        test_row = {
            "split": "heldout_seed_4",
            **model_metrics(name, model, x_test, y_test, alpha),
        }
        validation_rows.extend([validation_row, test_row])
        thresholds[name] = float(validation_row["threshold"])

    if selected_override == "auto":
        selectable = [row for row in validation_rows if row["split"] == "validation_seed_3"]
        selectable.sort(key=lambda row: (float(row["brier"]), -float(row["accept_rate"])))
        selected_name = str(selectable[0]["risk_model"])
    else:
        if selected_override not in models:
            raise ValueError(f"unknown selected risk model override: {selected_override}")
        selected_name = selected_override
    return LearnedRiskModels(models, selected_name, thresholds, validation_rows, label)


def select_learned_candidate(
    method: str,
    costs: np.ndarray,
    violations: np.ndarray,
    margins: np.ndarray,
    actions: np.ndarray,
    learned: LearnedRiskModels,
) -> Tuple[int, float, bool, Dict[str, float]]:
    name, model, threshold = learned.resolve(method)
    feature_matrix = candidate_features(costs, violations, margins, actions)
    mean_cost = costs.mean(axis=0)
    risk = predict_risk(model, feature_matrix)
    acceptable = risk <= threshold
    fallback = False
    if np.any(acceptable):
        idx = int(np.argmin(np.where(acceptable, mean_cost, np.inf)))
    else:
        idx = int(np.argmin(risk + 0.03 * normalize(mean_cost)))
        fallback = True
    summary = candidate_feature_summary(feature_matrix, idx)
    summary["learned_risk_model"] = 0.0 if name == "logistic" else 1.0
    return idx, float(np.clip(risk[idx], 0.0, 1.0)), fallback, summary


def run_episode(
    spec,
    method: str,
    level: str,
    seed: int,
    calibrators,
    bundle: TrainedDynamicsBundle,
    learned: LearnedRiskModels,
    num_candidates: int,
    alpha: float,
    code_hash: str,
    artifact_tag: str,
) -> Tuple[Dict[str, object], List[Dict[str, object]]]:
    init_rng = np.random.default_rng(stable_seed("learned_risk_init", spec.name, level, seed))
    plan_rng = np.random.default_rng(stable_seed("learned_risk_planner", spec.name, level, method, seed))
    noise_rng = np.random.default_rng(stable_seed("learned_risk_noise", spec.name, level, seed))
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

        if method in LEARNED_METHODS:
            idx, pred_risk, fallback, feature_summary = select_learned_candidate(
                method, costs, violations, margins, actions, learned
            )
        else:
            idx, pred_risk, fallback, feature_summary = select_candidate(
                method, costs, violations, margins, actions, calibrators, alpha, spec, state
            )
        true_costs, true_violations, _ = evaluate_candidates([true], state, actions, spec)
        compute_times.append(1000.0 * (time.perf_counter() - t0))

        action = float(actions[idx, 0, 0])
        model_nexts = np.stack(
            [
                model_predict_next(model, state, action, bundle)
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
    run_id = sha256_text(f"{artifact_tag}:{spec.name}:{method}:{level}:{seed}")[:16]
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
            "config_path": f"configs/{artifact_tag}_config.json",
            "log_path": f"logs/{artifact_tag}_results.jsonl",
            "plot_paths": [],
            "model_hash": bundle.artifact_hash[:16],
            "code_hash": code_hash,
        },
    }
    return result, feature_rows


def model_predict_next(model, state: np.ndarray, action: float, bundle: TrainedDynamicsBundle) -> np.ndarray:
    from run_trained_dynamics_stage_a import predict_next_batch

    return predict_next_batch(model, state.reshape(1, 2), np.array([action]), bundle)[0]


def write_report(
    artifact_tag: str,
    flat: pd.DataFrame,
    summary: pd.DataFrame,
    learned: LearnedRiskModels,
    args: argparse.Namespace,
    elapsed_s: float,
) -> None:
    reports_dir = ROOT / "reports"
    tables_dir = ROOT / "tables"
    reports_dir.mkdir(exist_ok=True)
    tables_dir.mkdir(exist_ok=True)
    summary.to_csv(tables_dir / f"{artifact_tag}_summary_by_method.csv", index=False)
    flat.groupby(["domain", "method"], as_index=False).agg(
        cost_mean=("cost", "mean"),
        violation_rate_mean=("violation_rate", "mean"),
        prediction_error_mean=("prediction_error", "mean"),
    ).to_csv(tables_dir / f"{artifact_tag}_summary_by_domain_method.csv", index=False)
    pd.DataFrame(learned.validation_rows).to_csv(tables_dir / f"{artifact_tag}_risk_model_selection.csv", index=False)

    def row_text(method: str) -> str:
        row = summary[summary["method"] == method]
        if row.empty:
            return "missing"
        data = row.iloc[0]
        return f"cost={float(data['cost_mean']):.4f}, violation={float(data['violation_rate_mean']):.4f}"

    sorted_rows = summary.sort_values(["violation_rate_mean", "cost_mean"])[
        ["method", "cost_mean", "violation_rate_mean", "observed_risk_mean", "freezing_rate_mean"]
    ]
    lines = [
        "# Learned-Risk Planner Pilot",
        "",
        "## Status",
        "",
        "This pilot trains logistic and random-forest risk models on executed selected rollouts from Stage-A seeds 0-2, selects or overrides the deployment model, then uses the learned risk model inside MPC candidate selection on fresh held-out seeds.",
        "",
        "## Scope",
        "",
        f"- Domains: {args.domains}",
        f"- Methods: {args.methods}",
        f"- Levels: {args.levels}",
        f"- Seeds: {args.seeds}",
        f"- Candidate budget: {args.candidates}",
        f"- Calibration contexts per domain/level for baseline gates: {args.calibration_contexts}",
        f"- Executed-rollout risk label: `{args.risk_label}`",
        f"- Selected risk model: `{learned.selected_name}`",
        f"- Selection mode: `{args.selected_risk_model}`",
        f"- Runtime seconds: {elapsed_s:.2f}",
        "",
        "## Key Aggregate Rows",
        "",
        f"- Learned selected risk: {row_text('learned_risk_executed_selected')}",
        f"- Learned RF risk: {row_text('learned_risk_executed_rf')}",
        f"- Learned logistic risk: {row_text('learned_risk_executed_logistic')}",
        f"- CCR-MPC: {row_text('ccr_mpc')}",
        f"- CVaR/RA-MPPI: {row_text('cvar_ra_mppi')}",
        f"- Conformal prediction MPC: {row_text('conformal_prediction_mpc')}",
        f"- Vanilla MPPI: {row_text('vanilla_mppi')}",
        "",
        "## Method Ranking",
        "",
        sorted_rows.to_markdown(index=False, floatfmt=".4f"),
        "",
        "## Risk Model Selection",
        "",
        pd.DataFrame(learned.validation_rows).to_markdown(index=False, floatfmt=".4f"),
        "",
        "## Artifacts",
        "",
        f"- `logs/{artifact_tag}_results.jsonl`",
        f"- `logs/{artifact_tag}_results_flat.csv`",
        f"- `logs/{artifact_tag}_step_predictions.csv`",
        f"- `tables/{artifact_tag}_summary_by_method.csv`",
        f"- `tables/{artifact_tag}_summary_by_domain_method.csv`",
        f"- `tables/{artifact_tag}_risk_model_selection.csv`",
        f"- `configs/{artifact_tag}_config.json`",
        "",
        "## Limitation",
        "",
        "The learned risk models are trained from previously executed selected rollouts, not from a newly randomized Stage-B calibration collection. Applying those models to every sampled candidate is a distribution-shifted use of selected-action labels. Treat this as a real planner-integration pilot, not a final learned-risk claim.",
    ]
    (reports_dir / f"{artifact_tag}_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run learned-risk planner pilot.")
    parser.add_argument("--domains", default="all")
    parser.add_argument("--levels", default="L0,L1,L2,L3")
    parser.add_argument("--seeds", default="10,11,12,13,14")
    parser.add_argument(
        "--methods",
        default=(
            "vanilla_mppi,cvar_ra_mppi,conformal_prediction_mpc,conformal_risk_non_ccr,"
            "ccr_no_calibration,ccr_mpc,learned_risk_executed_logistic,"
            "learned_risk_executed_rf,learned_risk_executed_selected,oracle_mpc"
        ),
    )
    parser.add_argument("--candidates", type=int, default=32)
    parser.add_argument("--calibration-contexts", type=int, default=24)
    parser.add_argument("--artifact-tag", default="learned_risk_stage_b_pilot")
    parser.add_argument("--risk-label", default="plan_failure", choices=["plan_failure", "step_violation"])
    parser.add_argument("--selected-risk-model", default="auto", choices=["auto", "logistic", "random_forest"])
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    artifact_tag = safe_artifact_tag(args.artifact_tag)
    start = time.perf_counter()
    torch.set_num_threads(max(1, min(4, torch.get_num_threads())))

    learned = fit_learned_risk_models(
        ROOT / "logs" / "trained_dynamics_stage_a_step_predictions.csv",
        args.risk_label,
        TARGET_RISK,
        args.selected_risk_model,
    )

    all_domains = domain_specs()
    domain_names = parse_list(args.domains, [spec.name for spec in all_domains])
    method_names = parse_list(args.methods, [])
    levels = parse_list(args.levels, list(LEVEL_SEVERITY))
    seeds = [int(part) for part in parse_list(args.seeds, [])]
    valid_methods = BASELINE_METHODS | LEARNED_METHODS
    selected_domains = [spec for spec in all_domains if spec.name in domain_names]
    missing_domains = sorted(set(domain_names) - {spec.name for spec in selected_domains})
    missing_methods = sorted(set(method_names) - valid_methods)
    missing_levels = sorted(set(levels) - set(LEVEL_SEVERITY))
    if missing_domains:
        raise ValueError(f"unknown domains: {missing_domains}")
    if missing_methods:
        raise ValueError(f"unknown methods: {missing_methods}")
    if missing_levels:
        raise ValueError(f"unknown levels: {missing_levels}")

    code_hash = sha256_file(Path(__file__))
    bundles = {spec.name: load_trained_bundle(spec) for spec in selected_domains}
    calibration_cache = {}
    calibration_rows: List[Dict[str, float]] = []
    for spec in selected_domains:
        for level in levels:
            calibration = calibrate_trained_domain_level(
                spec,
                level,
                bundles[spec.name],
                args.calibration_contexts,
                max(18, args.candidates // 2),
                TARGET_RISK,
            )
            calibration_cache[(spec.name, level)] = calibration
            calibration_rows.extend(calibration.rows)
            print(f"calibrated baseline gates {spec.name}/{level}")

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
                    result, rows = run_episode(
                        spec,
                        method,
                        level,
                        seed,
                        calibrators,
                        bundle,
                        learned,
                        args.candidates,
                        TARGET_RISK,
                        code_hash,
                        artifact_tag,
                    )
                    results.append(result)
                    step_rows.extend(rows)
                    if job_idx % 25 == 0 or job_idx == total_jobs:
                        print(f"completed {job_idx}/{total_jobs}")

    logs_dir = ROOT / "logs"
    configs_dir = ROOT / "configs"
    logs_dir.mkdir(exist_ok=True)
    configs_dir.mkdir(exist_ok=True)
    write_jsonl(logs_dir / f"{artifact_tag}_results.jsonl", results)
    flat = pd.DataFrame([flatten_result(row) for row in results])
    flat = aggregate_oracle_regret(flat)
    flat.to_csv(logs_dir / f"{artifact_tag}_results_flat.csv", index=False)
    pd.DataFrame(step_rows).to_csv(logs_dir / f"{artifact_tag}_step_predictions.csv", index=False)
    pd.DataFrame(calibration_rows).to_csv(logs_dir / f"{artifact_tag}_calibration_samples.csv", index=False)
    summary = summarize(flat)
    elapsed_s = time.perf_counter() - start
    write_report(artifact_tag, flat, summary, learned, args, elapsed_s)

    config = {
        "created_utc": pd.Timestamp.utcnow().isoformat(),
        "execution_record_type": artifact_tag,
        "args": vars(args),
        "run_settings": {
            "domains": [spec.name for spec in selected_domains],
            "methods": method_names,
            "levels": levels,
            "seeds": seeds,
            "num_candidates": args.candidates,
            "calibration_contexts": args.calibration_contexts,
            "target_risk": TARGET_RISK,
            "risk_label": args.risk_label,
            "selected_risk_model": learned.selected_name,
            "selected_risk_model_mode": args.selected_risk_model,
            "feature_names": FEATURE_NAMES,
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
        "risk_model_selection": learned.validation_rows,
        "code_hash": code_hash,
    }
    (configs_dir / f"{artifact_tag}_config.json").write_text(json.dumps(config, indent=2, sort_keys=True), encoding="utf-8")
    print(f"wrote {artifact_tag} results in {elapsed_s:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
