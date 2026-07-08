# Calibration Label Source Ablation

## Status

This diagnostic compares simulator full-candidate labels with labels from actually executed selected rollouts in the trained Stage-A run.

## Summary

```json
{
  "rows": 27,
  "main_ablation": [
    {
      "label_source": "simulator_full_candidate_labels_oracle",
      "score": "violation_rate",
      "label": "true_failure",
      "n": 5184,
      "positive_rate": 0.37982253086419754,
      "brier": 0.054097128858996715,
      "roc_auc": 0.9380764999008742,
      "ece": 0.05605612673611121
    },
    {
      "label_source": "executed_rollout_calibration_main",
      "score": "pred_risk",
      "label": "step_violation",
      "n": 46360,
      "positive_rate": 0.02385677308024159,
      "brier": 0.15776291687802457,
      "roc_auc": 0.7143474114483881,
      "ece": 0.23788319260873472
    },
    {
      "label_source": "simulator_full_candidate_labels_oracle",
      "score": "violation_tail",
      "label": "true_failure",
      "n": 5184,
      "positive_rate": 0.37982253086419754,
      "brier": 0.1832558063281605,
      "roc_auc": 0.7618116576768843,
      "ece": 0.1832551728395062
    },
    {
      "label_source": "selected_candidate_plan_label",
      "score": "pred_risk",
      "label": "plan_failure",
      "n": 46360,
      "positive_rate": 0.24706643658326144,
      "brier": 0.18544971933720827,
      "roc_auc": 0.6543529449758908,
      "ece": 0.1848034345850197
    },
    {
      "label_source": "simulator_full_candidate_labels_oracle",
      "score": "combined",
      "label": "true_failure",
      "n": 5184,
      "positive_rate": 0.37982253086419754,
      "brier": 0.23311817347094055,
      "roc_auc": 0.6934336808399556,
      "ece": 0.15116991039333996
    },
    {
      "label_source": "simulator_full_candidate_labels_oracle",
      "score": "regret_cvar",
      "label": "true_failure",
      "n": 5184,
      "positive_rate": 0.37982253086419754,
      "brier": 0.3290994494575835,
      "roc_auc": 0.4835778833189713,
      "ece": 0.26634847973394665
    },
    {
      "label_source": "simulator_full_candidate_labels_oracle",
      "score": "uncertainty",
      "label": "true_failure",
      "n": 5184,
      "positive_rate": 0.37982253086419754,
      "brier": 0.33474701250093064,
      "roc_auc": 0.4888870810154597,
      "ece": 0.272915081561629
    },
    {
      "label_source": "simulator_full_candidate_labels_oracle",
      "score": "rank_instability",
      "label": "true_failure",
      "n": 5184,
      "positive_rate": 0.37982253086419754,
      "brier": 0.3711628400488542,
      "roc_auc": 0.4914213860719851,
      "ece": 0.3365276936411336
    }
  ]
}
```

## Interpretation

Simulator full-candidate labels give dense candidate-level supervision. Executed-rollout labels are more realistic but only cover selected actions under the deployed planner distribution.

## Artifacts

- `logs/calibration_label_source_ablation.csv`
- `logs/trained_dynamics_stage_a_calibration_samples.csv`
- `logs/trained_dynamics_stage_a_step_predictions.csv`

## Limitation

This is an offline diagnostic from Stage-A logs. A final main setting should collect a dedicated executed-rollout calibration split before held-out Stage-B/Stage-C testing.
