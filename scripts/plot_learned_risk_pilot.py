#!/usr/bin/env python3
"""Plot learned-risk planner pilot safety/cost tradeoffs."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    summary_path = ROOT / "tables" / "learned_risk_stage_b_pilot_summary_by_method.csv"
    df = pd.read_csv(summary_path)
    df = df.sort_values(["violation_rate_mean", "cost_mean"])
    labels = {
        "conformal_prediction_mpc": "Conf. pred.",
        "conformal_risk_non_ccr": "Conf. risk",
        "oracle_mpc": "Oracle",
        "cvar_ra_mppi": "CVaR",
        "learned_risk_executed_logistic": "Learned logistic",
        "ccr_mpc": "CCR-MPC",
        "vanilla_mppi": "Vanilla",
        "ccr_no_calibration": "CCR no calib.",
        "learned_risk_executed_rf": "Learned RF",
        "learned_risk_executed_selected": "Validation-selected",
    }
    colors = [
        "#2f6f9f" if "learned_risk" in method else "#767676" if method != "ccr_mpc" else "#b24b4b"
        for method in df["method"]
    ]
    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    ax.scatter(df["cost_mean"], 100.0 * df["violation_rate_mean"], s=90, c=colors, edgecolor="black", linewidth=0.6)
    for _, row in df.iterrows():
        ax.annotate(
            labels.get(row["method"], row["method"]),
            (row["cost_mean"], 100.0 * row["violation_rate_mean"]),
            xytext=(5, 4),
            textcoords="offset points",
            fontsize=8,
        )
    ax.set_xlabel("Mean cost")
    ax.set_ylabel("Mean violation rate (%)")
    ax.set_title("Learned-risk planner pilot: safety/cost tradeoff")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    out = ROOT / "figures" / "learned_risk_stage_b_pilot_pareto.png"
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, dpi=180)
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
