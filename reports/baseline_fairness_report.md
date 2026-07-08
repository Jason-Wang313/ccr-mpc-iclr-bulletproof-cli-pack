# Baseline Fairness Report

## Status

Preliminary. The focused surrogate suite and trained-dynamics Stage-A suite include all listed methods under matched candidate budgets within each suite, but the max-out baseline tuning requirement is not complete.

## What Is Matched

- Within the original focused suite, all methods share the configured domain/OOD/seed grid and candidate budget unless method-specific oracle, system-ID proxy, or domain-randomized particles are part of the method definition.
- Within trained-dynamics Stage A, all non-oracle methods use the same trained Torch MLP ensemble candidate evaluator on D0/D1, levels L0-L2, seeds 0-4, 24 candidates, and 24 calibration contexts per domain/level.
- `oracle_mpc` uses the true simulator candidate evaluator in both suites and is reported as an oracle reference, not a fair deployable baseline.

## What Is Not Yet Fair Enough For Final Claims

- Trained Stage A does not yet implement specialized trained-dynamics versions of `domain_randomized_mpc` or `sysid_mpc`; those method names currently run through the shared trained evaluator except for their existing selection rules.
- Hyperparameter sweeps in `configs/baseline_sweeps.yaml` are specified but not fully executed.
- Baseline winners are not hidden: in trained Stage A, conformal prediction/risk gates reach zero aggregate violation at higher cost/freezing, and CCR-MPC does not dominate them.

## Current Evidence

- Focused surrogate suite: `tables/summary_by_method.csv`
- Trained-dynamics Stage A: `tables/trained_dynamics_stage_a_summary_by_method.csv`
- Sweep plan: `configs/baseline_sweeps.yaml`
- Tuning summary: `tables/baseline_tuning_summary.csv`

## Final-Submission Requirement

Before claiming superiority, execute validation-selected sweeps under matched budgets, then freeze hyperparameters before the held-out Stage B/Stage C test runs.

