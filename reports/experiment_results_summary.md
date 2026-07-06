# Experiment Results Summary

## Run Scope

- Runs: 1026
- Planning steps logged: 20862
- Domains: 6 simplified CPU domains
- Methods: 19
- Seeds: 0,1,2
- OOD levels: L0,L1,L2
- Wall-clock execution time: 216.9 seconds
- Result-log code hash prefix(es): `c2626ba6fd5d4ce3`
- Current package code hash: `95cb1f26050cbb0d6d2c5588b74637130d38824f773ae3bfb414f83cb76276e2`

## Main Aggregate Results

- Vanilla MPPI mean violation rate: 1.1%
- Robust MPC mean violation rate: 0.5%
- CCR-MPC mean violation rate: 0.4%
- Vanilla MPPI mean cost: 28.474
- CCR-MPC mean cost: 29.411
- Oracle MPC mean cost: 28.538

## Interpretation

CCR-MPC reduced observed violation frequency relative to vanilla MPPI in this bounded suite while keeping cost below the most conservative failure-avoidance strategies when averaged over the configured runs. The evidence supports a bounded claim about simplified learned-dynamics MPC settings, not a claim about real robot deployment.

## Artifacts

- `logs/results.jsonl`
- `logs/results_flat.csv`
- `logs/step_predictions.csv`
- `tables/summary_by_method.csv`
- `tables/summary_by_domain_method.csv`
- `tables/summary_by_method_level.csv`
- `figures/safety_performance_pareto.png`
- `figures/ood_severity_curves.png`
- `figures/risk_reliability.png`
- `figures/prediction_error_vs_control_risk.png`
- `figures/ccr_ablation_bars.png`
- `figures/compute_time_by_method.png`
