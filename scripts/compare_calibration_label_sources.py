#!/usr/bin/env python3
"""Compare simulator candidate-label and executed-rollout calibration sources."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np
import pandas as pd
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score


ROOT = Path(__file__).resolve().parents[1]


def normalize(values: Sequence[float]) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    lo = np.nanmin(arr)
    hi = np.nanmax(arr)
    if not np.isfinite(lo) or not np.isfinite(hi) or hi - lo <= 1e-12:
        return np.zeros_like(arr)
    return (arr - lo) / (hi - lo)


def ece(pred: np.ndarray, obs: np.ndarray, bins: int = 10) -> float:
    pred = np.clip(np.asarray(pred, dtype=float), 1e-6, 1.0 - 1e-6)
    obs = np.asarray(obs, dtype=float)
    out = 0.0
    edges = np.linspace(0.0, 1.0, bins + 1)
    for lo, hi in zip(edges[:-1], edges[1:]):
        mask = (pred >= lo) & (pred < hi if hi < 1.0 else pred <= hi)
        if np.any(mask):
            out += float(np.mean(mask)) * abs(float(np.mean(pred[mask]) - np.mean(obs[mask])))
    return out


def metrics(source: str, score_name: str, label_name: str, score: Sequence[float], label: Sequence[float]) -> Dict[str, object]:
    pred = np.clip(normalize(score), 1e-6, 1.0 - 1e-6)
    obs = np.asarray(label, dtype=float)
    both = len(set(float(v) for v in obs)) == 2
    return {
        "label_source": source,
        "score": score_name,
        "label": label_name,
        "n": int(len(obs)),
        "positive_rate": float(np.mean(obs)) if len(obs) else 0.0,
        "roc_auc": float(roc_auc_score(obs, pred)) if both else float("nan"),
        "brier": float(brier_score_loss(obs, pred)) if len(obs) else float("nan"),
        "log_loss": float(log_loss(obs, pred, labels=[0, 1])) if len(obs) else float("nan"),
        "ece": float(ece(pred, obs)) if len(obs) else float("nan"),
    }


def main() -> int:
    rows: List[Dict[str, object]] = []

    cal_path = ROOT / "logs" / "trained_dynamics_stage_a_calibration_samples.csv"
    step_path = ROOT / "logs" / "trained_dynamics_stage_a_step_predictions.csv"
    if not cal_path.exists() or not step_path.exists():
        raise FileNotFoundError("trained Stage-A calibration and step logs are required")

    cal = pd.read_csv(cal_path)
    step = pd.read_csv(step_path)

    for score in ["combined", "violation_rate", "violation_tail", "regret_cvar", "rank_instability", "uncertainty"]:
        if score in cal.columns:
            rows.append(metrics("simulator_full_candidate_labels_oracle", score, "true_failure", cal[score], cal["true_failure"]))

    rows.append(metrics("executed_rollout_calibration_main", "pred_risk", "step_violation", step["pred_risk"], step["step_violation"]))
    rows.append(metrics("selected_candidate_plan_label", "pred_risk", "plan_failure", step["pred_risk"], step["plan_failure"]))

    for method, part in step.groupby("method"):
        rows.append(metrics(f"executed_rollout_by_method:{method}", "pred_risk", "step_violation", part["pred_risk"], part["step_violation"]))

    out = pd.DataFrame(rows)
    out_path = ROOT / "logs" / "calibration_label_source_ablation.csv"
    out.to_csv(out_path, index=False)

    main_rows = out[out["label_source"].isin(["simulator_full_candidate_labels_oracle", "executed_rollout_calibration_main", "selected_candidate_plan_label"])]
    best = main_rows.sort_values(["brier", "ece"], ascending=[True, True]).head(8)
    report = {
        "rows": int(len(out)),
        "main_ablation": best[["label_source", "score", "label", "n", "positive_rate", "brier", "roc_auc", "ece"]].to_dict(orient="records"),
    }
    lines = [
        "# Calibration Label Source Ablation",
        "",
        "## Status",
        "",
        "This diagnostic compares simulator full-candidate labels with labels from actually executed selected rollouts in the trained Stage-A run.",
        "",
        "## Summary",
        "",
        "```json",
        json.dumps(report, indent=2),
        "```",
        "",
        "## Interpretation",
        "",
        "Simulator full-candidate labels give dense candidate-level supervision. Executed-rollout labels are more realistic but only cover selected actions under the deployed planner distribution.",
        "",
        "## Artifacts",
        "",
        "- `logs/calibration_label_source_ablation.csv`",
        "- `logs/trained_dynamics_stage_a_calibration_samples.csv`",
        "- `logs/trained_dynamics_stage_a_step_predictions.csv`",
        "",
        "## Limitation",
        "",
        "This is an offline diagnostic from Stage-A logs. A final main setting should collect a dedicated executed-rollout calibration split before held-out Stage-B/Stage-C testing.",
    ]
    (ROOT / "reports" / "calibration_label_source_ablation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out_path.relative_to(ROOT).as_posix()} with {len(out)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
