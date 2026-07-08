# Calibration Report

## Setup

Each domain/OOD pair used sampled calibration contexts. Candidate sequences were evaluated under learned dynamics particles and under the true shifted simulator. Split calibrators were fit for CCR combined score, uncertainty, predicted violation, rank instability, regret CVaR, violation tail, and negative margin tail.

## Aggregate Calibration Metrics

- CCR-MPC mean ECE: 0.2575
- Non-CCR conformal risk mean ECE: 0.2542
- Step-level prediction rows: 20862
- Calibration sample rows saved: 3888

## Reliability Figure

See `figures/risk_reliability.png`.

## Executed-Rollout Split

A new held-out Stage-A split is reported in `reports/executed_rollout_calibration_split.md`.
It calibrates thresholds on executed selected rollouts from seeds 0-2, selects scores on seed 3, and reports held-out seed 4.

Validation-selected held-out averages:

- Alpha 0.05: mean accept rate 0.9811, accepted step-violation rate 0.0146, accepted plan-failure rate 0.2211.
- Alpha 0.10/0.15/0.20: mean accept rate 0.9994, accepted step-violation rate 0.0201, accepted plan-failure rate 0.2378.

This supports a narrower step-level executed-rollout calibration diagnostic. It does not yet establish episode-level plan-failure control.

## Limitation

Risk predictions are calibrated on sampled candidate contexts and Stage-A executed rollouts from the same simplified simulator family. This is weaker than a deployment guarantee under arbitrary online shift, and the new executed-rollout split still shows high accepted plan-failure rates.
