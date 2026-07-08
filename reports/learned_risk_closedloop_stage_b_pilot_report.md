# Learned-Risk Planner Pilot

## Status

This pilot trains logistic and random-forest risk models on executed selected rollouts from Stage-A seeds 0-2, selects or overrides the deployment model, then uses the learned risk model inside MPC candidate selection on fresh held-out seeds.

## Scope

- Domains: all
- Methods: vanilla_mppi,cvar_ra_mppi,conformal_prediction_mpc,conformal_risk_non_ccr,ccr_mpc,learned_risk_executed_logistic,learned_risk_executed_selected,oracle_mpc
- Levels: L0,L1,L2,L3
- Seeds: 15,16,17,18,19
- Candidate budget: 32
- Calibration contexts per domain/level for baseline gates: 24
- Executed-rollout risk label: `plan_failure`
- Selected risk model: `logistic`
- Selection mode: `logistic`
- Runtime seconds: 682.59

## Key Aggregate Rows

- Learned selected risk: cost=28.5961, violation=0.0178
- Learned RF risk: missing
- Learned logistic risk: cost=28.6301, violation=0.0208
- CCR-MPC: cost=29.1271, violation=0.0139
- CVaR/RA-MPPI: cost=28.5823, violation=0.0115
- Conformal prediction MPC: cost=37.2538, violation=0.0015
- Vanilla MPPI: cost=28.5251, violation=0.0227

## Method Ranking

| method                         |   cost_mean |   violation_rate_mean |   observed_risk_mean |   freezing_rate_mean |
|:-------------------------------|------------:|----------------------:|---------------------:|---------------------:|
| conformal_prediction_mpc       |     37.2538 |                0.0015 |               0.0083 |               0.4481 |
| conformal_risk_non_ccr         |     34.5116 |                0.0019 |               0.0167 |               0.3820 |
| oracle_mpc                     |     28.5442 |                0.0064 |               0.0750 |               0.1505 |
| cvar_ra_mppi                   |     28.5823 |                0.0115 |               0.0917 |               0.1410 |
| ccr_mpc                        |     29.1271 |                0.0139 |               0.1000 |               0.1172 |
| learned_risk_executed_selected |     28.5961 |                0.0178 |               0.1417 |               0.1369 |
| learned_risk_executed_logistic |     28.6301 |                0.0208 |               0.1250 |               0.1383 |
| vanilla_mppi                   |     28.5251 |                0.0227 |               0.1833 |               0.1499 |

## Interpretation

This is the strongest next-level check I can run locally without pretending a proxy metric is enough. The closed-loop-selected logistic risk model improves over vanilla MPPI on fresh seeds 15-19, but it does not beat CCR-MPC, CVaR/RA-MPPI, conformal risk, conformal prediction, or oracle MPC on violation rate. The result closes the easy learned-risk selection loophole: the problem is not just that Brier selected the wrong model; even the closed-loop-selected logistic deployment remains below the strongest baselines in this setting.

See `figures/learned_risk_closedloop_stage_b_pilot_pareto.png`.

## Risk Model Selection

| split             | risk_model    |    n |   positive_rate |   brier |   roc_auc |   threshold |   accept_rate |   accepted_failure_rate |   accepted_count |
|:------------------|:--------------|-----:|----------------:|--------:|----------:|------------:|--------------:|------------------------:|-----------------:|
| validation_seed_3 | logistic      | 9272 |          0.2513 |  0.0454 |    0.9724 |      0.9999 |        0.8804 |                  0.1499 |        8163.0000 |
| heldout_seed_4    | logistic      | 9272 |          0.2377 |  0.0472 |    0.9719 |      0.9999 |        0.8968 |                  0.1500 |        8315.0000 |
| validation_seed_3 | random_forest | 9272 |          0.2513 |  0.0395 |    0.9810 |      0.9961 |        0.8790 |                  0.1482 |        8150.0000 |
| heldout_seed_4    | random_forest | 9272 |          0.2377 |  0.0409 |    0.9784 |      0.9961 |        0.8968 |                  0.1500 |        8315.0000 |

## Artifacts

- `logs/learned_risk_closedloop_stage_b_pilot_results.jsonl`
- `logs/learned_risk_closedloop_stage_b_pilot_results_flat.csv`
- `logs/learned_risk_closedloop_stage_b_pilot_step_predictions.csv`
- `tables/learned_risk_closedloop_stage_b_pilot_summary_by_method.csv`
- `tables/learned_risk_closedloop_stage_b_pilot_summary_by_domain_method.csv`
- `tables/learned_risk_closedloop_stage_b_pilot_risk_model_selection.csv`
- `figures/learned_risk_closedloop_stage_b_pilot_pareto.png`
- `configs/learned_risk_closedloop_stage_b_pilot_config.json`

## Limitation

The learned risk models are trained from previously executed selected rollouts, not from a newly randomized Stage-B calibration collection. Applying those models to every sampled candidate is a distribution-shifted use of selected-action labels. Treat this as a real planner-integration pilot, not a final learned-risk claim.
