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

## Limitation

Risk predictions are calibrated on sampled candidate contexts from the same simplified simulator family. This is weaker than a deployment guarantee under arbitrary online shift.
