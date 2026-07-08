# Trained-Dynamics Stage-A Report

## Status

This Stage-A run uses trained Torch MLP dynamics ensembles inside the planner candidate evaluator for D0/D1.
It is a real integration checkpoint, but it is not the final max-out run and does not replace the original focused-suite evidence.

## Scope

- Domains: synthetic_separation,classic_control
- Methods: all
- Levels: L0,L1,L2
- Seeds: 0,1,2,3,4
- Candidate budget: 24
- Calibration contexts per domain/level: 24
- Runtime seconds: 502.83

## Key Aggregate Rows

- Vanilla MPPI: cost=32.0396, violation=0.0315
- CCR-MPC: cost=32.8436, violation=0.0185
- CVaR/RA-MPPI: cost=32.1963, violation=0.0315
- Conformal prediction MPC: cost=39.8974, violation=0.0000

## Artifacts

- `logs/trained_dynamics_stage_a_results.jsonl`
- `logs/trained_dynamics_stage_a_results_flat.csv`
- `logs/trained_dynamics_stage_a_step_predictions.csv`
- `tables/trained_dynamics_stage_a_summary_by_method.csv`
- `tables/trained_dynamics_stage_a_summary_by_domain_method.csv`
- `configs/trained_dynamics_stage_a_config.json`

## Limitations

- Only D0/D1 Stage-A domains are included.
- The calibration labels are still simulator candidate labels, not executed-rollout calibration.
- Method names such as `sysid_mpc` and `domain_randomized_mpc` are run through the trained-model candidate evaluator in this integration checkpoint unless the method is `oracle_mpc`; they are not yet full tuned specialized baselines.
- No strong-superiority claim is allowed from this Stage-A run alone.
