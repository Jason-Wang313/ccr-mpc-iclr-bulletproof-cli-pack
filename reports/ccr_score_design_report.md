# CCR Score Design Report

## Status

Preliminary design and current implementation audit. The repository has hand-weighted CCR, single-feature calibrated ablations, and preliminary logistic/isotonic/random-forest validation diagnostics. These learned risk models are not yet used as final planner baselines.

## Current CCR Features

- Counterfactual regret CVaR across dynamics particles or trained ensemble members.
- Violation probability across particles.
- Violation-tail and negative-margin-tail scores.
- Rank instability across model-specific candidate rankings.
- First-action disagreement across sampled candidates.
- Cost uncertainty as a non-CCR comparison feature.

## Current Implemented Variants

- `ccr_mpc`: combined calibrated gate using CCR, violation, and margin scores.
- `ccr_no_calibration`: uncalibrated CCR penalty.
- `calibration_no_ccr`: calibrated uncertainty-only gate.
- `disagreement_only`: calibrated rank-instability gate.
- `regret_only`: calibrated regret-CVaR gate.
- `violation_tail_only`: calibrated violation-tail gate.
- `conformal_risk_non_ccr`: calibrated non-CCR violation-rate score.

## Evidence So Far

- Original focused surrogate suite: `tables/summary_by_method.csv`
- Trained-dynamics Stage A: `tables/trained_dynamics_stage_a_summary_by_method.csv`
- Trained-dynamics Stage-B pilot: `tables/trained_dynamics_stage_b_pilot_summary_by_method.csv`
- Reliability plot: `figures/risk_reliability.png`
- Dynamics calibration diagnostic: `figures/prediction_calibration_vs_control_risk.png`
- Preliminary risk-model validation: `logs/risk_model_validation.csv`
- Executed-rollout calibration split: `logs/executed_rollout_calibration_split.csv`

## Preliminary Risk-Model Finding

On available calibration diagnostics, multi-feature learned risk models beat the hand-weighted combined score on Brier score:

- Focused surrogate calibration samples: `random_forest_all_features` Brier 0.0258, versus `single_combined` Brier 0.2071.
- Trained Stage-A calibration samples: `random_forest_all_features` Brier 0.0460, versus `single_combined` Brier 0.2344.

This is not a held-out Stage-B claim. It means the max-out path should treat learned risk-model selection as a serious baseline rather than assuming the current hand-weighted CCR score is final.

## Executed-Rollout Split Finding

On the Stage-A selected-rollout split, validation-selected held-out score choices most often select `violation_tail` (35 of 76 selected rows), followed by `combined` (19), `regret_cvar` (12), `pred_risk` (5), and `pred_violation_rate` (5). Held-out accepted step-violation rates average 0.0146 at alpha 0.05 and 0.0201 at alpha 0.10/0.15/0.20, but accepted plan-failure rates remain high at roughly 0.22-0.24.

This supports validation selection over a fixed hand-weighted score and warns against claiming episode-level safety from step-level executed-rollout calibration.

## Stage-B Pilot Finding

In the held-out trained-dynamics Stage-B pilot, CCR-MPC improves violation over vanilla MPPI and uncalibrated CCR, but `conformal_prediction_mpc` and `conformal_risk_non_ccr` are safer at higher cost, while CVaR/RA-MPPI and robust MPC are lower cost with slightly higher violation. This reinforces the need for validation-selected learned risk models and tuned baseline sweeps before final paper claims.

## Missing For Max-Out

- Planner integration for logistic/isotonic/random-forest risk models.
- Gradient-boosting risk model when available.
- Validation-set model selection before held-out testing.
- Fresh held-out Stage-B/Stage-C evaluation after selecting the risk model.

## Claim Boundary

Current evidence supports CCR as a useful decision-risk score family in bounded runs. It also shows that the hand-weighted combined score should not be treated as the final or strongest risk estimator without validation-selected learned risk models.
