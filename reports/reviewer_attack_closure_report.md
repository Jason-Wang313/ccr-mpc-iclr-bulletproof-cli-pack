# Reviewer Attack Closure Report

## Fatal Attacks Addressed By Generated Artifacts

- "Just ensemble uncertainty": compare `ensemble_uncertainty_penalty`, `prediction_calibrated_penalty`, `calibration_no_ccr`, and `ccr_mpc` in `tables/summary_by_method.csv`.
- "Just RA-MPPI/CVaR": compare `cvar_ra_mppi` and `ccr_mpc`.
- "Just conformal risk control": compare `conformal_risk_non_ccr`, `conformal_decision_baseline`, and CCR variants.
- "Safe but useless": inspect cost, freezing rate, fallback rate, and safety-performance figure.
- "MPPI-specific": inspect `secondary_planner` domain using `CEM-MPC`.

## Remaining High-Risk Reviewer Complaints

- The domains are simplified surrogates; this is not hardware evidence.
- The formal theory is narrow: one-step separation, finite-threshold split calibration, and sampled-set optimality only.
- Citation metadata has been checked and recorded, but final venue-style BibTeX should be re-exported before submission.
- Hyperparameter sensitivity exists but is not yet a full 57,000-row max-out matrix execution.

## Wording To Use

Use: "In a bounded CPU suite of simplified learned-dynamics MPC tasks..."

Avoid: "solves safe robot control", "foundation dynamics models", "general control-risk calibration", or "hardware-ready".
