# Learned-Risk Planner Pilot

## Status

This pilot trains logistic and random-forest risk models on executed selected rollouts from Stage-A seeds 0-2, selects the model and threshold on seed 3, checks seed 4, then uses the learned risk model inside MPC candidate selection on fresh held-out seeds.

## Scope

- Domains: all
- Methods: vanilla_mppi,cvar_ra_mppi,conformal_prediction_mpc,conformal_risk_non_ccr,ccr_no_calibration,ccr_mpc,learned_risk_executed_logistic,learned_risk_executed_rf,learned_risk_executed_selected,oracle_mpc
- Levels: L0,L1,L2,L3
- Seeds: 10,11,12,13,14
- Candidate budget: 32
- Calibration contexts per domain/level for baseline gates: 24
- Executed-rollout risk label: `plan_failure`
- Selected risk model: `random_forest`
- Runtime seconds: 1755.27

## Key Aggregate Rows

- Learned selected risk: cost=28.3511, violation=0.0266
- Learned RF risk: cost=28.3376, violation=0.0240
- Learned logistic risk: cost=28.3399, violation=0.0084
- CCR-MPC: cost=28.8994, violation=0.0088
- CVaR/RA-MPPI: cost=28.3659, violation=0.0065
- Conformal prediction MPC: cost=36.9413, violation=0.0008
- Vanilla MPPI: cost=28.2824, violation=0.0154

## Method Ranking

| method                         |   cost_mean |   violation_rate_mean |   observed_risk_mean |   freezing_rate_mean |
|:-------------------------------|------------:|----------------------:|---------------------:|---------------------:|
| conformal_prediction_mpc       |     36.9413 |                0.0008 |               0.0167 |               0.4372 |
| conformal_risk_non_ccr         |     34.2117 |                0.0020 |               0.0417 |               0.3677 |
| oracle_mpc                     |     28.2872 |                0.0063 |               0.0917 |               0.1492 |
| cvar_ra_mppi                   |     28.3659 |                0.0065 |               0.0750 |               0.1446 |
| learned_risk_executed_logistic |     28.3399 |                0.0084 |               0.0917 |               0.1348 |
| ccr_mpc                        |     28.8994 |                0.0088 |               0.0917 |               0.1182 |
| vanilla_mppi                   |     28.2824 |                0.0154 |               0.1583 |               0.1436 |
| ccr_no_calibration             |     28.5639 |                0.0206 |               0.1750 |               0.1206 |
| learned_risk_executed_rf       |     28.3376 |                0.0240 |               0.1917 |               0.1396 |
| learned_risk_executed_selected |     28.3511 |                0.0266 |               0.2083 |               0.1429 |

## Interpretation

The learned logistic risk model is the useful result in this pilot: it slightly improves over CCR-MPC on both mean cost and mean violation rate. However, the random-forest model has the best validation Brier score and is therefore selected by the current validation rule, yet it performs worse when deployed inside the planner. This means learned risk-model integration is promising, but validation Brier alone is not a sufficient model-selection rule for closed-loop planning.

See `figures/learned_risk_stage_b_pilot_pareto.png`.

## Risk Model Selection

| split             | risk_model    |    n |   positive_rate |   brier |   roc_auc |   threshold |   accept_rate |   accepted_failure_rate |   accepted_count |
|:------------------|:--------------|-----:|----------------:|--------:|----------:|------------:|--------------:|------------------------:|-----------------:|
| validation_seed_3 | logistic      | 9272 |          0.2513 |  0.0454 |    0.9724 |      0.9999 |        0.8804 |                  0.1499 |        8163.0000 |
| heldout_seed_4    | logistic      | 9272 |          0.2377 |  0.0472 |    0.9719 |      0.9999 |        0.8968 |                  0.1500 |        8315.0000 |
| validation_seed_3 | random_forest | 9272 |          0.2513 |  0.0395 |    0.9810 |      0.9961 |        0.8790 |                  0.1482 |        8150.0000 |
| heldout_seed_4    | random_forest | 9272 |          0.2377 |  0.0409 |    0.9784 |      0.9961 |        0.8968 |                  0.1500 |        8315.0000 |

## Artifacts

- `logs/learned_risk_stage_b_pilot_results.jsonl`
- `logs/learned_risk_stage_b_pilot_results_flat.csv`
- `logs/learned_risk_stage_b_pilot_step_predictions.csv`
- `tables/learned_risk_stage_b_pilot_summary_by_method.csv`
- `tables/learned_risk_stage_b_pilot_summary_by_domain_method.csv`
- `tables/learned_risk_stage_b_pilot_risk_model_selection.csv`
- `figures/learned_risk_stage_b_pilot_pareto.png`
- `configs/learned_risk_stage_b_pilot_config.json`

## Limitation

The learned risk models are trained from previously executed selected rollouts, not from a newly randomized Stage-B calibration collection. Applying those models to every sampled candidate is a distribution-shifted use of selected-action labels. Treat this as a real planner-integration pilot, not a final learned-risk claim.
