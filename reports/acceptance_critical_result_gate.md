# Acceptance-Critical Result Gate

## Status

Current gate result: do not claim broad empirical superiority.

## Evidence Checked

- `tables/summary_by_method.csv`
- `tables/trained_dynamics_stage_a_summary_by_method.csv`
- `reports/experiment_results_summary.md`
- `reports/trained_dynamics_stage_a_report.md`
- `reports/trained_dynamics_stage_b_pilot_report.md`
- `reports/learned_risk_stage_b_pilot_report.md`
- `reports/learned_risk_closedloop_stage_b_pilot_report.md`
- `paper/iclr_submission.tex`
- `reports/preupgrade_repo_audit.md`

## Where CCR-MPC Wins

- CCR-MPC improves mean violation rate over vanilla MPPI in the focused CPU suite: 0.0042087542 versus 0.0114104003.
- CCR-MPC improves mean violation rate over uncalibrated CCR: 0.0042087542 versus 0.0112233446.
- CCR-MPC has much lower mean cost than highly conservative fallbacks such as `soda_like_fallback` and `violation_tail_only`.
- In trained-dynamics Stage A on D0-D5 with L0-L3, CCR-MPC improves aggregate violation over vanilla MPPI: 0.0165741 versus 0.0254798.
- In trained-dynamics Stage A, CCR-MPC improves aggregate violation over uncalibrated CCR: 0.0165741 versus 0.0259049.
- In the trained-dynamics Stage-B pilot, CCR-MPC improves aggregate violation over vanilla MPPI: 0.0113636 versus 0.0198611.
- In the trained-dynamics Stage-B pilot, CCR-MPC improves aggregate violation over uncalibrated CCR: 0.0113636 versus 0.0154419.
- In the learned-risk planner pilot, `learned_risk_executed_logistic` slightly improves over CCR-MPC in both violation and cost: violation 0.0083670 versus 0.0087837, cost 28.3399 versus 28.8994.
- In the closed-loop-selected learned-risk pilot, `learned_risk_executed_selected` improves over vanilla MPPI: violation 0.0177862 versus 0.0227020.
- The executed-rollout calibration split keeps validation-selected held-out accepted step-violation rates below 0.05 on average for all tested alpha values.

## Where CCR-MPC Ties

- CCR-MPC ties `cvar_ra_mppi` and `conformal_prediction_mpc` at the lowest aggregate violation rate in the focused suite: 0.0042087542.
- CCR-MPC ties the low observed-risk tier in the aggregate results.

## Where CCR-MPC Loses

- `cvar_ra_mppi` has lower mean cost than CCR-MPC at the same aggregate violation rate: 28.6502721 versus 29.4113151.
- `conformal_risk_non_ccr` has lower mean cost and only slightly higher violation rate in the aggregate table.
- `oracle_mpc` and vanilla MPPI have lower mean costs, although with different safety tradeoffs.
- In trained-dynamics Stage A, `conformal_prediction_mpc`, `conformal_risk_non_ccr`, and `violation_tail_only` achieve lower aggregate violation than CCR-MPC at higher cost/freezing.
- In trained-dynamics Stage A, `robust_mpc` has lower cost and slightly lower aggregate violation than CCR-MPC.
- In trained-dynamics Stage A, the `domain_randomized_mpc` row is lower cost but slightly higher violation than CCR-MPC; it is not yet a fully faithful domain-randomized learned-model baseline.
- In the trained-dynamics Stage-B pilot, `conformal_prediction_mpc`, `conformal_risk_non_ccr`, and `oracle_mpc` have lower aggregate violation than CCR-MPC.
- In the trained-dynamics Stage-B pilot, `cvar_ra_mppi` and `robust_mpc` have lower mean cost than CCR-MPC with only slightly higher violation.
- In the learned-risk planner pilot, conformal prediction, conformal risk, oracle, and CVaR remain safer than the learned logistic risk planner.
- The validation-selected learned risk model is random forest by Brier score, but its closed-loop violation is worse than vanilla MPPI in this pilot: 0.0266498 versus 0.0154293.
- In the closed-loop-selected learned-risk pilot, CCR-MPC, CVaR/RA-MPPI, conformal prediction, conformal risk, and oracle MPC all have lower violation than the selected learned-risk planner.
- The executed-rollout calibration split still has high accepted plan-failure rates, averaging roughly 0.22-0.24 across alpha settings.

## Allowed Paper Claim

The current paper should claim bounded diagnostic insight about decision-risk calibration in simplified learned-dynamics MPC settings. It may claim improvement over vanilla MPPI and uncalibrated CCR in the focused and trained Stage-A runs, but it must state that stronger conformal/robust baselines can match or beat CCR-MPC on these aggregate metrics.

## Disallowed Paper Claim

The current evidence does not support a strong-superiority claim over CVaR/RA-MPPI, conformal-prediction MPC, or all conformal/risk-aware baselines. It also does not support claiming that learned risk-model selection is solved, even after a closed-loop-selected logistic deployment.

## Max-Out Requirement Before Stronger Claim

A stronger ICLR submission now needs broader trained-dynamics planner integration, main-runner integration of the new higher-dimensional domain prototypes, validation-selected baseline sweeps, fresh Stage-B executed-rollout calibration, and Stage B/Stage C experiments. If those still show ties or losses, the paper should remain a diagnostic or mixed-result paper.
