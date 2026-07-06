# Baselines and Ablations Checklist

## Hard baselines

- Vanilla MPPI/MPC
- Robust/conservative MPC
- Raw ensemble uncertainty penalty
- Prediction-calibrated uncertainty penalty
- CVaR / RA-MPPI-style
- Chance-constrained MPC-style
- Conformal prediction-set MPC
- Conformal risk control with non-CCR score
- Conformal decision/planning baseline
- SODA-like OOD detector + fallback
- Domain-randomized dynamics + MPC
- System ID / online adaptation + MPC
- Oracle dynamics + MPC

## Ablations

- CCR no calibration
- calibration no CCR
- planner disagreement only
- regret only
- violation-tail only
- no task conditioning
- no OOD features
- no online recalibration
- no fallback
- weighted calibration off
- open-loop calibration instead of closed-loop calibration
- MPPI only vs CEM-MPC secondary

Machine-readable method names:
- `ccr_no_calibration`
- `calibration_no_ccr`
- `disagreement_only`
- `regret_only`
- `violation_tail_only`

## Fairness rules

- Equal planning horizon where applicable.
- Equal action-sample budget.
- Equal dynamics training data.
- Equal calibration set size.
- Report compute overhead.
- Tune baselines reasonably and document sweep ranges.
