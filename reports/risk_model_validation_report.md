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
      "risk_model": "random_forest_all_features",
      "brier": 0.04595054951419268,
      "roc_auc": 0.9744872187605913,
      "ece": 0.021763235511367395
    },
    {
      "source": "trained_stage_a",
      "risk_model": "logistic_all_features",
      "brier": 0.04843039333423672,
      "roc_auc": 0.9721245470187971,
      "ece": 0.026934154716539135
    },
    {
      "source": "trained_stage_a",
      "risk_model": "single_violation_rate",
      "brier": 0.05937567790359488,
      "roc_auc": 0.9350982219673071,
      "ece": 0.06292037515605499
    }
  ]
}
```

## Artifacts

- `logs/risk_model_validation.csv`
- `scripts/validate_risk_models.py`

## Limitation

The current validation samples are calibration diagnostics, not a locked held-out benchmark. Final claims require validation-selected risk models evaluated on fresh held-out Stage-B/Stage-C runs.
