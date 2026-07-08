# Trained-Dynamics Planner Integration

## What Changed

`scripts/run_trained_dynamics_stage_a.py` loads `artifacts/models/*_torch_mlp_ensemble.pt` and uses the learned models to roll out sampled MPC candidates. Candidate costs, violation indicators, margins, CCR features, and calibrated gates are computed from trained ensemble predictions rather than parameter-particle surrogates.

## What Remains

The original focused suite still uses the parameter-particle runner. The trained-dynamics runner is separate so the old artifact hashes and claims remain reproducible.

## Next Integration Step

Promote `trained_torch_mlp_ensemble` to a first-class `--model-source` option in `scripts/execute_paper_cpu_study.py` once Stage-A behavior is stable.
