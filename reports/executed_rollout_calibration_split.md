# Executed-Rollout Calibration Split

## Status

Stage-A selected-rollout data were split by seed: calibration seeds 0-2, validation seed 3, and held-out test seed 4.
Thresholds are fit only on executed selected rollouts, then the risk score is selected on validation performance and reported on the held-out test split.

## Summary

```json
{
  "test_selected_by_alpha": [
    {
      "alpha": 0.05,
      "mean_accept_rate": 0.9811259706643657,
      "mean_accepted_step_violation_rate": 0.014568175989622357,
      "mean_accepted_plan_failure_rate": 0.22107703585398833,
      "mean_brier_step": 0.05725127880620461
    },
    {
      "alpha": 0.1,
      "mean_accept_rate": 0.9993528904227782,
      "mean_accepted_step_violation_rate": 0.02006860739600717,
      "mean_accepted_plan_failure_rate": 0.23779432077088,
      "mean_brier_step": 0.049876913792162025
    },
    {
      "alpha": 0.15,
      "mean_accept_rate": 0.9993528904227782,
      "mean_accepted_step_violation_rate": 0.02006860739600717,
      "mean_accepted_plan_failure_rate": 0.23779432077088,
      "mean_brier_step": 0.049876913792162025
    },
    {
      "alpha": 0.2,
      "mean_accept_rate": 0.9993528904227782,
      "mean_accepted_step_violation_rate": 0.02006860739600717,
      "mean_accepted_plan_failure_rate": 0.23779432077088,
      "mean_brier_step": 0.049876913792162025
    }
  ],
  "selected_score_counts": [
    {
      "score": "violation_tail",
      "count": 35
    },
    {
      "score": "combined",
      "count": 19
    },
    {
      "score": "regret_cvar",
      "count": 12
    },
    {
      "score": "pred_violation_rate",
      "count": 5
    },
    {
      "score": "pred_risk",
      "count": 5
    }
  ]
}
```

## Selected Held-Out Rows

| method                        |   alpha | score               |   accept_rate |   accepted_step_violation_rate |   accepted_plan_failure_rate |   brier_step |
|:------------------------------|--------:|:--------------------|--------------:|-------------------------------:|-----------------------------:|-------------:|
| calibration_no_ccr            |  0.0500 | pred_violation_rate |        0.8320 |                         0.0000 |                       0.0172 |       0.1110 |
| ccr_mpc                       |  0.0500 | combined            |        1.0000 |                         0.0143 |                       0.2725 |       0.0175 |
| ccr_no_calibration            |  0.0500 | pred_risk           |        1.0000 |                         0.0205 |                       0.2807 |       0.0215 |
| chance_constrained_mpc        |  0.0500 | pred_risk           |        0.8217 |                         0.0000 |                       0.1446 |       0.1368 |
| conformal_decision_baseline   |  0.0500 | violation_tail      |        1.0000 |                         0.0287 |                       0.2090 |       0.0902 |
| conformal_prediction_mpc      |  0.0500 | violation_tail      |        1.0000 |                         0.0000 |                       0.1578 |       0.0328 |
| conformal_risk_non_ccr        |  0.0500 | violation_tail      |        1.0000 |                         0.0000 |                       0.2029 |       0.0471 |
| cvar_ra_mppi                  |  0.0500 | combined            |        1.0000 |                         0.0225 |                       0.2869 |       0.0479 |
| disagreement_only             |  0.0500 | violation_tail      |        1.0000 |                         0.0369 |                       0.2111 |       0.0963 |
| domain_randomized_mpc         |  0.0500 | regret_cvar         |        0.9939 |                         0.0124 |                       0.2825 |       0.0314 |
| ensemble_uncertainty_penalty  |  0.0500 | violation_tail      |        1.0000 |                         0.0246 |                       0.3340 |       0.1393 |
| oracle_mpc                    |  0.0500 | combined            |        0.9980 |                         0.0041 |                       0.3306 |       0.0640 |
| prediction_calibrated_penalty |  0.0500 | violation_tail      |        1.0000 |                         0.0348 |                       0.2971 |       0.1025 |
| regret_only                   |  0.0500 | violation_tail      |        1.0000 |                         0.0020 |                       0.0594 |       0.0287 |
| robust_mpc                    |  0.0500 | regret_cvar         |        0.9980 |                         0.0041 |                       0.2895 |       0.0138 |
| soda_like_fallback            |  0.0500 | pred_violation_rate |        1.0000 |                         0.0225 |                       0.0410 |       0.0102 |
| sysid_mpc                     |  0.0500 | combined            |        0.9980 |                         0.0308 |                       0.3614 |       0.0728 |
| vanilla_mppi                  |  0.0500 | regret_cvar         |        1.0000 |                         0.0184 |                       0.3504 |       0.0198 |
| violation_tail_only           |  0.0500 | violation_tail      |        1.0000 |                         0.0000 |                       0.0717 |       0.0041 |
| calibration_no_ccr            |  0.1000 | violation_tail      |        1.0000 |                         0.0574 |                       0.1824 |       0.0902 |
| ccr_mpc                       |  0.1000 | combined            |        1.0000 |                         0.0143 |                       0.2725 |       0.0175 |
| ccr_no_calibration            |  0.1000 | pred_risk           |        1.0000 |                         0.0205 |                       0.2807 |       0.0215 |
| chance_constrained_mpc        |  0.1000 | combined            |        1.0000 |                         0.0471 |                       0.2971 |       0.0175 |
| conformal_decision_baseline   |  0.1000 | violation_tail      |        1.0000 |                         0.0287 |                       0.2090 |       0.0902 |

## Artifacts

- `logs/executed_rollout_calibration_split.csv`
- `tables/executed_rollout_calibration_selection.csv`
- `logs/trained_dynamics_stage_a_step_predictions.csv`

## Limitation

This is a held-out split over existing Stage-A selected rollouts, not a freshly collected Stage-B calibration/test protocol. It should guide risk-score selection, but final claims still require locked hyperparameters and fresh held-out Stage-B or Stage-C execution.
