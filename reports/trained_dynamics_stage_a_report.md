# Trained-Dynamics Stage-A Report

## Status

This Stage-A run uses trained Torch MLP dynamics ensembles inside the planner candidate evaluator for D0-D5.
It is a real integration checkpoint, but it is not the final max-out run and does not replace the original focused-suite evidence.

## Scope

- Domains: all
- Methods: all
- Levels: L0,L1,L2,L3
- Seeds: 0,1,2,3,4
- Candidate budget: 24
- Calibration contexts per domain/level: 24
- Runtime seconds: 2266.87

## Key Aggregate Rows

- Vanilla MPPI: cost=28.6862, violation=0.0255
- CCR-MPC: cost=29.3156, violation=0.0166
- CVaR/RA-MPPI: cost=28.7424, violation=0.0234
- Conformal prediction MPC: cost=37.4319, violation=0.0019

## Artifacts

- `logs/trained_dynamics_stage_a_results.jsonl`
- `logs/trained_dynamics_stage_a_results_flat.csv`
- `logs/trained_dynamics_stage_a_step_predictions.csv`
- `tables/trained_dynamics_stage_a_summary_by_method.csv`
- `tables/trained_dynamics_stage_a_summary_by_domain_method.csv`
- `configs/trained_dynamics_stage_a_config.json`

## Limitations

- This remains a Stage-A CPU run with the repository's simplified domains; it is not a high-fidelity robot simulation suite.
- The calibration labels are still simulator candidate labels, not executed-rollout calibration.
- Method names such as `sysid_mpc` and `domain_randomized_mpc` are run through the trained-model candidate evaluator in this integration checkpoint unless the method is `oracle_mpc`; they are not yet full tuned specialized baselines.
- No strong-superiority claim is allowed from this Stage-A run alone.
