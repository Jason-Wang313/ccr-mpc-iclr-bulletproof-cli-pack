# Acceptance-Critical Result Gate

## Status

Current gate result: do not claim broad empirical superiority.

## Evidence Checked

- `tables/summary_by_method.csv`
- `reports/experiment_results_summary.md`
- `paper/iclr_submission.tex`
- `reports/preupgrade_repo_audit.md`

## Where CCR-MPC Wins

- CCR-MPC improves mean violation rate over vanilla MPPI in the focused CPU suite: 0.0042087542 versus 0.0114104003.
- CCR-MPC improves mean violation rate over uncalibrated CCR: 0.0042087542 versus 0.0112233446.
- CCR-MPC has much lower mean cost than highly conservative fallbacks such as `soda_like_fallback` and `violation_tail_only`.

## Where CCR-MPC Ties

- CCR-MPC ties `cvar_ra_mppi` and `conformal_prediction_mpc` at the lowest aggregate violation rate in the focused suite: 0.0042087542.
- CCR-MPC ties the low observed-risk tier in the aggregate results.

## Where CCR-MPC Loses

- `cvar_ra_mppi` has lower mean cost than CCR-MPC at the same aggregate violation rate: 28.6502721 versus 29.4113151.
- `conformal_risk_non_ccr` has lower mean cost and only slightly higher violation rate in the aggregate table.
- `oracle_mpc` and vanilla MPPI have lower mean costs, although with different safety tradeoffs.

## Allowed Paper Claim

The current paper should claim matched low violation rate and diagnostic insight about decision-risk calibration in simplified learned-dynamics MPC settings. It may claim improvement over vanilla MPPI and uncalibrated CCR in the focused suite.

## Disallowed Paper Claim

The current evidence does not support a strong-superiority claim over CVaR/RA-MPPI, conformal-prediction MPC, or all conformal/risk-aware baselines.

## Max-Out Requirement Before Stronger Claim

A stronger ICLR submission needs trained learned-dynamics planner integration, higher-fidelity domains, tuned baseline sweeps, executed-rollout calibration, and Stage B/Stage C experiments. If those still show ties or losses, the paper should remain a diagnostic or mixed-result paper.

