# Dynamics Training Report

## Status

This run trained bootstrapped Torch MLP one-step dynamics ensembles on CPU for each existing CCR-MPC domain.
These artifacts are diagnostic evidence only: the current focused CCR-MPC planner results still use the original parameter-particle surrogate models.

## Training Configuration

- Ensemble size: 5
- Training trajectories per domain: 48
- Training steps per trajectory: 18
- Epochs per ensemble member: 70
- Hidden width: 32
- Training level: L0 nominal dynamics
- Evaluation levels: L0, L1, L2 when present

## Aggregate Metrics

| level   |   one_step_mse |   rollout_mse |   interval90_coverage |   model_disagreement |
|:--------|---------------:|--------------:|----------------------:|---------------------:|
| L0      |       0.000004 |      0.000084 |              0.643779 |             0.001249 |
| L1      |       0.000090 |      0.001808 |              0.249834 |             0.001370 |
| L2      |       0.000282 |      0.005710 |              0.175170 |             0.001414 |

## Artifacts

- `artifacts/models/*_torch_mlp_ensemble.pt`
- `logs/dynamics_prediction_metrics.csv`
- `figures/prediction_calibration_vs_control_risk.png`

## Limitations

- Models are trained on the existing simplified 2D domains, not high-fidelity robot simulators.
- The trained ensembles are not yet wired into the MPC experiment runner.
- The coverage metric is an ensemble-spread interval diagnostic, not a formal conformal guarantee.
