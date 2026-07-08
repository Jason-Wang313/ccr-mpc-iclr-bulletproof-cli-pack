# Risk Model Validation Report

## Status

Preliminary validation on available calibration-sample logs. These results are for model-selection diagnostics only and are not held-out Stage-B test claims.

## Summary

```json
{
  "sources": [
    "focused_surrogate",
    "trained_stage_a"
  ],
  "rows": 18,
  "best_by_brier": [
    {
      "source": "focused_surrogate",
      "risk_model": "random_forest_all_features",
      "brier": 0.025802080214361877,
      "roc_auc": 0.9938422877382022,
      "ece": 0.01987175480175527
    },
    {
      "source": "focused_surrogate",
      "risk_model": "single_violation_rate",
      "brier": 0.029520473738484935,
      "roc_auc": 0.9882987877880874,
      "ece": 0.02635660933927068
    },
    {
      "source": "focused_surrogate",
      "risk_model": "logistic_all_features",
      "brier": 0.0298605601717982,
      "roc_auc": 0.9912950214506635,
      "ece": 0.0378559380861693
    },
    {
      "source": "trained_stage_a",
      "risk_model": "logistic_all_features",
      "brier": 0.05303133329170463,
      "roc_auc": 0.9732800203097233,
      "ece": 0.0358104662324603
    },
    {
      "source": "trained_stage_a",
      "risk_model": "random_forest_all_features",
      "brier": 0.0549968529306394,
      "roc_auc": 0.9696369636963698,
      "ece": 0.04309502678351593
    },
    {
      "source": "trained_stage_a",
      "risk_model": "single_violation_rate",
      "brier": 0.06458426700349623,
      "roc_auc": 0.9403274942878903,
      "ece": 0.06599481612090678
    }
  ]
}
```

## Artifacts

- `logs/risk_model_validation.csv`
- `scripts/validate_risk_models.py`

## Limitation

The current validation samples are calibration diagnostics, not a locked held-out benchmark. Final claims require validation-selected risk models evaluated on fresh held-out Stage-B/Stage-C runs.
