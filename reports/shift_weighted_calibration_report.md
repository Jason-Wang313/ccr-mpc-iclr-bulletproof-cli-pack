# Shift-Weighted Calibration Diagnostic

## Status

This is an optional theorem-D diagnostic, not a completed theorem. It compares unweighted split-threshold calibration with a severity-weighted threshold using L0-L2 calibration contexts and L3 as shifted test data.

## Summary

```json
{
  "rows": 144,
  "calibration_rows": 2592,
  "validation_rows": 1296,
  "shifted_test_rows": 1296,
  "shifted_settings_rejecting_all_fraction": 0.8541666666666666,
  "best_shifted_rows": [
    {
      "score": "violation_rate",
      "alpha": 0.1,
      "mode": "severity_weighted",
      "accept_rate": 0.6728395061728395,
      "accepted_failure_rate": 0.13761467889908258,
      "all_failure_rate": 0.4182098765432099
    },
    {
      "score": "violation_rate",
      "alpha": 0.1,
      "mode": "unweighted",
      "accept_rate": 0.6813271604938271,
      "accepted_failure_rate": 0.14609286523216308,
      "all_failure_rate": 0.4182098765432099
    },
    {
      "score": "violation_rate",
      "alpha": 0.15,
      "mode": "unweighted",
      "accept_rate": 0.6813271604938271,
      "accepted_failure_rate": 0.14609286523216308,
      "all_failure_rate": 0.4182098765432099
    },
    {
      "score": "violation_rate",
      "alpha": 0.15,
      "mode": "severity_weighted",
      "accept_rate": 0.6813271604938271,
      "accepted_failure_rate": 0.14609286523216308,
      "all_failure_rate": 0.4182098765432099
    },
    {
      "score": "violation_rate",
      "alpha": 0.2,
      "mode": "unweighted",
      "accept_rate": 0.6813271604938271,
      "accepted_failure_rate": 0.14609286523216308,
      "all_failure_rate": 0.4182098765432099
    },
    {
      "score": "violation_rate",
      "alpha": 0.2,
      "mode": "severity_weighted",
      "accept_rate": 0.6813271604938271,
      "accepted_failure_rate": 0.14609286523216308,
      "all_failure_rate": 0.4182098765432099
    },
    {
      "score": "combined",
      "alpha": 0.2,
      "mode": "unweighted",
      "accept_rate": 0.6126543209876543,
      "accepted_failure_rate": 0.27204030226700254,
      "all_failure_rate": 0.4182098765432099
    }
  ]
}
```

## Shifted L3 Comparison

| score            |   alpha |   accept_rate_severity_weighted |   accept_rate_unweighted |   accepted_failure_rate_severity_weighted |   accepted_failure_rate_unweighted |
|:-----------------|--------:|--------------------------------:|-------------------------:|------------------------------------------:|-----------------------------------:|
| combined         |  0.0500 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| combined         |  0.1000 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| combined         |  0.1500 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| combined         |  0.2000 |                          0.0000 |                   0.6127 |                                    0.0000 |                             0.2720 |
| rank_instability |  0.0500 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| rank_instability |  0.1000 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| rank_instability |  0.1500 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| rank_instability |  0.2000 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| regret_cvar      |  0.0500 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| regret_cvar      |  0.1000 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| regret_cvar      |  0.1500 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| regret_cvar      |  0.2000 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| uncertainty      |  0.0500 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| uncertainty      |  0.1000 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| uncertainty      |  0.1500 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| uncertainty      |  0.2000 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| violation_rate   |  0.0500 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| violation_rate   |  0.1000 |                          0.6728 |                   0.6813 |                                    0.1376 |                             0.1461 |
| violation_rate   |  0.1500 |                          0.6813 |                   0.6813 |                                    0.1461 |                             0.1461 |
| violation_rate   |  0.2000 |                          0.6813 |                   0.6813 |                                    0.1461 |                             0.1461 |
| violation_tail   |  0.0500 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| violation_tail   |  0.1000 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| violation_tail   |  0.1500 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |
| violation_tail   |  0.2000 |                          0.0000 |                   0.0000 |                                    0.0000 |                             0.0000 |

## Interpretation

Most score/alpha settings are too conservative and reject all shifted L3 candidates. At alpha 0.20, severity weighting makes the combined score reject all candidates where the unweighted threshold accepts 61.27% with 27.20% accepted failures. For violation-rate score at alpha 0.10, severity weighting modestly reduces shifted accepted failures from 14.61% to 13.76% with a small accept-rate drop from 68.13% to 67.28%.

## Artifacts

- `logs/shift_weighted_calibration.csv`
- `reports/theorem_D_shift_calibration.md`

## Limitation

The severity weight is a hand-coded proxy, not a learned density ratio. This diagnostic is useful for scoping but does not establish adaptive calibration under arbitrary online shift.
