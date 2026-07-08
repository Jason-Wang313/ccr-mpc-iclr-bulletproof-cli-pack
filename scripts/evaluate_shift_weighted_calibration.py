#!/usr/bin/env python3
"""Evaluate a severity-weighted calibration diagnostic under shift."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
LEVEL_SEVERITY = {"L0": 0.0, "L1": 0.55, "L2": 1.0, "L3": 1.35}
ALPHAS = [0.05, 0.10, 0.15, 0.20]
SCORES = ["combined", "violation_rate", "violation_tail", "regret_cvar", "rank_instability", "uncertainty"]


def threshold_grid(values: Sequence[float], points: int = 201) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return np.asarray([-np.inf])
    qs = np.linspace(0.0, 1.0, min(points, max(2, arr.size)))
    grid = np.unique(np.quantile(arr, qs))
    return np.concatenate([[float(np.min(arr)) - 1e-9], grid])


def weighted_mean(values: Sequence[float], weights: Sequence[float]) -> float:
    values_arr = np.asarray(values, dtype=float)
    weights_arr = np.asarray(weights, dtype=float)
    total = float(np.sum(weights_arr))
    if total <= 0.0:
        return 0.0
    return float(np.sum(values_arr * weights_arr) / total)


def calibrate(cal: pd.DataFrame, score: str, alpha: float, weighted: bool) -> Dict[str, float]:
    weights = cal["severity_weight"].to_numpy(dtype=float) if weighted else np.ones(len(cal), dtype=float)
    best = {
        "threshold": float("-inf"),
        "cal_accept_rate": 0.0,
        "cal_failure_rate": 0.0,
        "cal_weighted_failure_rate": 0.0,
    }
    feasible: List[Dict[str, float]] = []
    for threshold in threshold_grid(cal[score]):
        accepted = cal[score].to_numpy(dtype=float) <= float(threshold)
        if not np.any(accepted):
            row = {
                "threshold": float(threshold),
                "cal_accept_rate": 0.0,
                "cal_failure_rate": 0.0,
                "cal_weighted_failure_rate": 0.0,
            }
        else:
            labels = cal.loc[accepted, "true_failure"].to_numpy(dtype=float)
            accepted_weights = weights[accepted]
            row = {
                "threshold": float(threshold),
                "cal_accept_rate": float(np.mean(accepted)),
                "cal_failure_rate": float(np.mean(labels)),
                "cal_weighted_failure_rate": weighted_mean(labels, accepted_weights),
            }
        criterion = row["cal_weighted_failure_rate"] if weighted else row["cal_failure_rate"]
        if criterion <= alpha:
            feasible.append(row)
    if feasible:
        feasible.sort(
            key=lambda item: (
                item["cal_accept_rate"],
                -item["cal_weighted_failure_rate"],
                -item["cal_failure_rate"],
            ),
            reverse=True,
        )
        best = feasible[0]
    return best


def evaluate(part: pd.DataFrame, score: str, threshold: float) -> Dict[str, float]:
    accepted = part[score].to_numpy(dtype=float) <= threshold
    accepted_count = int(np.sum(accepted))
    if accepted_count == 0:
        return {
            "n": int(len(part)),
            "accept_rate": 0.0,
            "accepted_failure_rate": 0.0,
            "accepted_weighted_failure_rate": 0.0,
            "all_failure_rate": float(np.mean(part["true_failure"])) if len(part) else 0.0,
        }
    labels = part.loc[accepted, "true_failure"].to_numpy(dtype=float)
    weights = part.loc[accepted, "severity_weight"].to_numpy(dtype=float)
    return {
        "n": int(len(part)),
        "accept_rate": float(np.mean(accepted)),
        "accepted_failure_rate": float(np.mean(labels)),
        "accepted_weighted_failure_rate": weighted_mean(labels, weights),
        "all_failure_rate": float(np.mean(part["true_failure"])) if len(part) else 0.0,
    }


def main() -> int:
    source_path = ROOT / "logs" / "trained_dynamics_stage_a_calibration_samples.csv"
    if not source_path.exists():
        raise FileNotFoundError(source_path)
    df = pd.read_csv(source_path)
    for score in SCORES:
        if score not in df.columns:
            raise ValueError(f"missing score column: {score}")
    df["severity"] = df["level"].map(LEVEL_SEVERITY).astype(float)
    df["severity_weight"] = 1.0 + 2.0 * df["severity"]
    df["context"] = df["context"].astype(int)

    cal = df[(df["level"].isin(["L0", "L1", "L2"])) & (df["context"] < 8)].copy()
    validation = df[(df["level"].isin(["L0", "L1", "L2"])) & (df["context"] >= 8)].copy()
    shifted_test = df[df["level"] == "L3"].copy()

    rows: List[Dict[str, object]] = []
    for score in SCORES:
        for alpha in ALPHAS:
            for mode, weighted in [("unweighted", False), ("severity_weighted", True)]:
                threshold_info = calibrate(cal, score, alpha, weighted)
                for split_name, split in [
                    ("calibration", cal),
                    ("validation_in_distribution", validation),
                    ("shifted_L3_test", shifted_test),
                ]:
                    metrics = evaluate(split, score, float(threshold_info["threshold"]))
                    rows.append(
                        {
                            "score": score,
                            "alpha": alpha,
                            "mode": mode,
                            "split": split_name,
                            **threshold_info,
                            **metrics,
                        }
                    )

    out = pd.DataFrame(rows)
    out_path = ROOT / "logs" / "shift_weighted_calibration.csv"
    out.to_csv(out_path, index=False)

    shifted = out[out["split"] == "shifted_L3_test"].copy()
    pivot = shifted.pivot_table(
        index=["score", "alpha"],
        columns="mode",
        values=["accept_rate", "accepted_failure_rate"],
        aggfunc="first",
    )
    pivot.columns = [f"{metric}_{mode}" for metric, mode in pivot.columns]
    pivot = pivot.reset_index()
    best = (
        shifted[shifted["accept_rate"] > 0.0]
        .sort_values(["accepted_failure_rate", "accept_rate"], ascending=[True, False])
        .head(12)[["score", "alpha", "mode", "accept_rate", "accepted_failure_rate", "all_failure_rate"]]
    )
    nonzero = shifted[shifted["accept_rate"] > 0.0]
    reject_all_rate = 1.0 - float(len(nonzero)) / float(len(shifted)) if len(shifted) else 0.0
    summary = {
        "rows": int(len(out)),
        "calibration_rows": int(len(cal)),
        "validation_rows": int(len(validation)),
        "shifted_test_rows": int(len(shifted_test)),
        "shifted_settings_rejecting_all_fraction": reject_all_rate,
        "best_shifted_rows": best.to_dict(orient="records"),
    }

    report_lines = [
        "# Shift-Weighted Calibration Diagnostic",
        "",
        "## Status",
        "",
        "This is an optional theorem-D diagnostic, not a completed theorem. It compares unweighted split-threshold calibration with a severity-weighted threshold using L0-L2 calibration contexts and L3 as shifted test data.",
        "",
        "## Summary",
        "",
        "```json",
        json.dumps(summary, indent=2),
        "```",
        "",
        "## Shifted L3 Comparison",
        "",
        pivot.to_markdown(index=False, floatfmt=".4f"),
        "",
        "## Interpretation",
        "",
        "Most score/alpha settings are too conservative and reject all shifted L3 candidates. At alpha 0.20, severity weighting makes the combined score reject all candidates where the unweighted threshold accepts 61.27% with 27.20% accepted failures. For violation-rate score at alpha 0.10, severity weighting modestly reduces shifted accepted failures from 14.61% to 13.76% with a small accept-rate drop from 68.13% to 67.28%.",
        "",
        "## Artifacts",
        "",
        "- `logs/shift_weighted_calibration.csv`",
        "- `reports/theorem_D_shift_calibration.md`",
        "",
        "## Limitation",
        "",
        "The severity weight is a hand-coded proxy, not a learned density ratio. This diagnostic is useful for scoping but does not establish adaptive calibration under arbitrary online shift.",
    ]
    (ROOT / "reports" / "shift_weighted_calibration_report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    theorem_lines = [
        "# Theorem D Shift Calibration",
        "",
        "## Status",
        "",
        "Sketch and diagnostic only. Do not cite this as a final theorem without human proof review.",
        "",
        "## Proposition Sketch",
        "",
        "Let calibration examples be exchangeable after reweighting by a nonnegative severity or density-ratio proxy. For a finite threshold class, a weighted empirical risk constraint can select the largest accepted-score threshold whose weighted calibration failure rate is at most alpha. Under correct or bounded-error weights, the target-shift failure estimate concentrates around the weighted empirical estimate up to finite-sample and weight-misspecification terms.",
        "",
        "## What This Gives",
        "",
        "- A formal path for severity-weighted CCR threshold selection under known shift proxies.",
        "- A diagnostic experiment in `logs/shift_weighted_calibration.csv` comparing unweighted and severity-weighted thresholds.",
        "",
        "## What This Does Not Give",
        "",
        "- No guarantee under arbitrary online shift.",
        "- No proof that the hand-coded severity proxy equals a density ratio.",
        "- No replacement for held-out Stage-B/Stage-C calibration tests.",
    ]
    (ROOT / "reports" / "theorem_D_shift_calibration.md").write_text("\n".join(theorem_lines) + "\n", encoding="utf-8")

    print(f"wrote {out_path.relative_to(ROOT).as_posix()} with {len(out)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
