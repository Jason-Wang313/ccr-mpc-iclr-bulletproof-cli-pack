# Trained Dynamics Stage B Pilot Report

## Status

This tagged run uses trained Torch MLP dynamics ensembles inside the planner candidate evaluator for the selected domains.
It is a real integration checkpoint, but it is not the final max-out run and does not replace the original focused-suite evidence.

## Scope

- Domains: all
- Methods: vanilla_mppi,robust_mpc,cvar_ra_mppi,conformal_prediction_mpc,conformal_risk_non_ccr,ccr_no_calibration,ccr_mpc,oracle_mpc
- Levels: L0,L1,L2,L3
- Seeds: 5,6,7,8,9
- Candidate budget: 32
- Calibration contexts per domain/level: 32
- Runtime seconds: 858.89

## Key Aggregate Rows

- Vanilla MPPI: cost=28.2276, violation=0.0199
- CCR-MPC: cost=28.7881, violation=0.0114
- CVaR/RA-MPPI: cost=28.2926, violation=0.0129
- Conformal prediction MPC: cost=30.7194, violation=0.0034

## Artifacts

- `logs/trained_dynamics_stage_b_pilot_results.jsonl`
- `logs/trained_dynamics_stage_b_pilot_results_flat.csv`
- `logs/trained_dynamics_stage_b_pilot_step_predictions.csv`
- `tables/trained_dynamics_stage_b_pilot_summary_by_method.csv`
- `tables/trained_dynamics_stage_b_pilot_summary_by_domain_method.csv`
- `configs/trained_dynamics_stage_b_pilot_config.json`

## Limitations

- This remains a CPU run with the repository's simplified domains; it is not a high-fidelity robot simulation suite.
- The calibration labels are still simulator candidate labels, not executed-rollout calibration.
- Method names such as `sysid_mpc` and `domain_randomized_mpc` are run through the trained-model candidate evaluator in this integration checkpoint unless the method is `oracle_mpc`; they are not yet full tuned specialized baselines.
- No strong-superiority claim is allowed from this tagged run alone.
