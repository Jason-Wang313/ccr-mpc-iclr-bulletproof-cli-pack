#!/usr/bin/env python3
"""Evaluate held-out calibration from executed Stage-A rollouts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

import numpy as np
import pandas as pd
from sklearn.metrics import brier_score_loss, roc_auc_score


ROOT = Path(__file__).resolve().parents[1]
ALPHAS = [0.05, 0.10, 0.15, 0.20]
SCORES = [
    "pred_risk",
    "combined",
    "pred_violation_rate",
    "violation_tail",
    "regret_cvar",
    "rank_instability",
    "uncertainty",
]


def finite_series(values: Sequence[float]) -> np.ndarray:
    return np.asarray(values, dtype=float)[np.isfinite(np.asarray(values, dtype=float))]


def threshold_grid(values: Sequence[float], points: int = 201) -> np.ndarray:
    arr = finite_series(values)
    if arr.size == 0:
        return np.asarray([-np.inf])
    qs = np.linspace(0.0, 1.0, min(points, max(2, arr.size)))
    grid = np.unique(np.quantile(arr, qs))
    below_min = np.nanmin(arr) - max(1e-9, 1e-9 * abs(float(np.nanmin(arr))))
    return np.concatenate([[below_min], grid])


def normalize_with_calibration(values: Sequence[float], cal_values: Sequence[float]) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    cal = finite_series(cal_values)
    if cal.size == 0:
        return np.full_like(arr, 0.5, dtype=float)
    lo = float(np.nanmin(cal))
    hi = float(np.nanmax(cal))
    if hi - lo <= 1e-12:
        return np.full_like(arr, 0.5, dtype=float)
    return np.clip((arr - lo) / (hi - lo), 1e-6, 1.0 - 1e-6)


def ece(pred: np.ndarray, obs: np.ndarray, bins: int = 10) -> float:
    pred = np.clip(np.asarray(pred, dtype=float), 1e-6, 1.0 - 1e-6)
    obs = np.asarray(obs, dtype=float)
    total = 0.0
    edges = np.linspace(0.0, 1.0, bins + 1)
    for lo, hi in zip(edges[:-1], edges[1:]):
        mask = (pred >= lo) & (pred < hi if hi < 1.0 else pred <= hi)
        if np.any(mask):
            total += float(np.mean(mask)) * abs(float(np.mean(pred[mask]) - np.mean(obs[mask])))
    return total


def calibrate_threshold(cal: pd.DataFrame, score: str, alpha: float) -> Dict[str, float]:
    best = {
        "threshold": float("-inf"),
        "cal_accept_rate": 0.0,
        "cal_accepted_step_violation_rate": 0.0,
        "cal_accepted_count": 0.0,
    }
    feasible: List[Dict[str, float]] = []
    for threshold in threshold_grid(cal[score]):
        accepted = cal[score].to_numpy(dtype=float) <= float(threshold)
        accepted_count = int(np.sum(accepted))
        if accepted_count == 0:
            row = {
                "threshold": float(threshold),
                "cal_accept_rate": 0.0,
                "cal_accepted_step_violation_rate": 0.0,
                "cal_accepted_count": 0.0,
            }
        else:
            row = {
                "threshold": float(threshold),
                "cal_accept_rate": float(np.mean(accepted)),
                "cal_accepted_step_violation_rate": float(np.mean(cal.loc[accepted, "step_violation"])),
                "cal_accepted_count": float(accepted_count),
            }
        if row["cal_accepted_step_violation_rate"] <= alpha:
            feasible.append(row)
    if feasible:
        feasible.sort(
            key=lambda item: (
                item["cal_accept_rate"],
                -item["cal_accepted_step_violation_rate"],
                item["threshold"],
            ),
            reverse=True,
        )
        best = feasible[0]
    return best


def eval_split(part: pd.DataFrame, cal: pd.DataFrame, score: str, threshold: float) -> Dict[str, float]:
    pred = normalize_with_calibration(part[score], cal[score])
    labels = part["step_violation"].to_numpy(dtype=float)
    accepted = part[score].to_numpy(dtype=float) <= threshold
    accepted_count = int(np.sum(accepted))
    out = {
        "n": int(len(part)),
        "accept_count": accepted_count,
        "accept_rate": float(np.mean(accepted)) if len(part) else float("nan"),
        "all_step_violation_rate": float(np.mean(labels)) if len(part) else float("nan"),
        "all_plan_failure_rate": float(np.mean(part["plan_failure"])) if len(part) else float("nan"),
        "accepted_step_violation_rate": float(np.mean(part.loc[accepted, "step_violation"])) if accepted_count else 0.0,
        "accepted_plan_failure_rate": float(np.mean(part.loc[accepted, "plan_failure"])) if accepted_count else 0.0,
        "brier_step": float(brier_score_loss(labels, pred)) if len(part) else float("nan"),
        "ece_step": float(ece(pred, labels)) if len(part) else float("nan"),
    }
    out["roc_auc_step"] = (
        float(roc_auc_score(labels, pred)) if len(set(float(v) for v in labels)) == 2 else float("nan")
    )
    return out


def split_by_seed(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    seeds = sorted(int(seed) for seed in df["seed"].dropna().unique())
    if len(seeds) >= 5:
        cal_seeds = seeds[:3]
        validation_seeds = [seeds[3]]
        test_seeds = seeds[4:]
    elif len(seeds) >= 3:
        cal_seeds = seeds[:-2]
        validation_seeds = [seeds[-2]]
        test_seeds = [seeds[-1]]
    else:
        raise ValueError("at least three seeds are required for executed-rollout calibration split")
    return {
        "calibration": df[df["seed"].isin(cal_seeds)].copy(),
        "validation": df[df["seed"].isin(validation_seeds)].copy(),
        "test": df[df["seed"].isin(test_seeds)].copy(),
    }


def selected_rows(rows: pd.DataFrame) -> pd.DataFrame:
    selections: List[pd.Series] = []
    validation = rows[rows["split"] == "validation"].copy()
    for (method, alpha), part in validation.groupby(["method", "alpha"]):
        feasible = part[part["accepted_step_violation_rate"] <= alpha].copy()
        if feasible.empty:
            feasible = part.copy()
            feasible["_feasible"] = 0
        else:
            feasible["_feasible"] = 1
        feasible = feasible.sort_values(
            by=["_feasible", "accept_rate", "brier_step", "ece_step"],
            ascending=[False, False, True, True],
        )
        chosen = feasible.iloc[0]
        test_match = rows[
            (rows["split"] == "test")
            & (rows["method"] == method)
            & (rows["alpha"] == alpha)
            & (rows["score"] == chosen["score"])
        ]
        if not test_match.empty:
            selections.append(test_match.iloc[0])
    return pd.DataFrame(selections)


def aggregate_selected(selection: pd.DataFrame) -> Dict[str, object]:
    if selection.empty:
        return {}
    by_alpha = (
        selection.groupby("alpha", as_index=False)
        .agg(
            mean_accept_rate=("accept_rate", "mean"),
            mean_accepted_step_violation_rate=("accepted_step_violation_rate", "mean"),
            mean_accepted_plan_failure_rate=("accepted_plan_failure_rate", "mean"),
            mean_brier_step=("brier_step", "mean"),
        )
        .sort_values("alpha")
    )
    score_counts = selection["score"].value_counts().rename_axis("score").reset_index(name="count")
    return {
        "test_selected_by_alpha": by_alpha.to_dict(orient="records"),
        "selected_score_counts": score_counts.to_dict(orient="records"),
    }


def main() -> int:
    step_path = ROOT / "logs" / "trained_dynamics_stage_a_step_predictions.csv"
    if not step_path.exists():
        raise FileNotFoundError(step_path)

    df = pd.read_csv(step_path)
    missing = [score for score in SCORES if score not in df.columns]
    if missing:
        raise ValueError(f"missing score columns: {missing}")

    split_frames = split_by_seed(df)
    rows: List[Dict[str, object]] = []
    for method, method_df in df.groupby("method"):
        method_splits = {name: frame[frame["method"] == method].copy() for name, frame in split_frames.items()}
        cal = method_splits["calibration"]
        if cal.empty:
            continue
        for score in SCORES:
            for alpha in ALPHAS:
                threshold_info = calibrate_threshold(cal, score, alpha)
                threshold = float(threshold_info["threshold"])
                for split_name, split_df in method_splits.items():
                    metrics = eval_split(split_df, cal, score, threshold)
                    row: Dict[str, object] = {
                        "method": method,
                        "score": score,
                        "alpha": alpha,
                        "split": split_name,
                        "threshold": threshold,
                        **threshold_info,
                        **metrics,
                    }
                    rows.append(row)

    out = pd.DataFrame(rows)
    out_path = ROOT / "logs" / "executed_rollout_calibration_split.csv"
    out.to_csv(out_path, index=False)

    selection = selected_rows(out)
    selection_path = ROOT / "tables" / "executed_rollout_calibration_selection.csv"
    selection.to_csv(selection_path, index=False)

    summary = aggregate_selected(selection)
    preview = selection[
        [
            "method",
            "alpha",
            "score",
            "accept_rate",
            "accepted_step_violation_rate",
            "accepted_plan_failure_rate",
            "brier_step",
        ]
    ].sort_values(["alpha", "method"]).head(24)

    lines = [
        "# Executed-Rollout Calibration Split",
        "",
        "## Status",
        "",
        "Stage-A selected-rollout data were split by seed: calibration seeds 0-2, validation seed 3, and held-out test seed 4.",
        "Thresholds are fit only on executed selected rollouts, then the risk score is selected on validation performance and reported on the held-out test split.",
        "",
        "## Summary",
        "",
        "```json",
        json.dumps(summary, indent=2),
        "```",
        "",
        "## Selected Held-Out Rows",
        "",
        preview.to_markdown(index=False, floatfmt=".4f"),
        "",
        "## Artifacts",
        "",
        "- `logs/executed_rollout_calibration_split.csv`",
        "- `tables/executed_rollout_calibration_selection.csv`",
        "- `logs/trained_dynamics_stage_a_step_predictions.csv`",
        "",
        "## Limitation",
        "",
        "This is a held-out split over existing Stage-A selected rollouts, not a freshly collected Stage-B calibration/test protocol. It should guide risk-score selection, but final claims still require locked hyperparameters and fresh held-out Stage-B or Stage-C execution.",
    ]
    report_path = ROOT / "reports" / "executed_rollout_calibration_split.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"wrote {out_path.relative_to(ROOT).as_posix()} with {len(out)} rows")
    print(f"wrote {selection_path.relative_to(ROOT).as_posix()} with {len(selection)} selected rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
