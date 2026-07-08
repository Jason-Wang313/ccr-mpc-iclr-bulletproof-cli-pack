# Domain Validation Report

## Status

Higher-dimensional CPU domain prototypes were added and smoke-validated. They are not yet integrated into the main MPC experiment runner.

## Domains

- `cartpole_safety`: D1b cartpole safety envelope; state_dim=4; action_dim=1; shifts=cart_mass, pole_mass, friction
- `dynamic_bicycle_4d`: D2 4D dynamic bicycle; state_dim=4; action_dim=2; shifts=friction, steering_bias, actuator_delay
- `planar_quadrotor_6d`: D3 6D planar quadrotor; state_dim=6; action_dim=2; shifts=wind, payload_mass, motor_strength
- `pushing_contact_4d`: D4 quasi-static pushing/contact; state_dim=4; action_dim=2; shifts=object_mass, table_friction, contact_point_bias

## Aggregate Validation

| domain              | level   |   violation_rate |   min_margin_mean |   final_state_norm_mean |
|:--------------------|:--------|-----------------:|------------------:|------------------------:|
| cartpole_safety     | L0      |           1.0000 |           -4.6552 |                 14.4822 |
| cartpole_safety     | L1      |           1.0000 |           -4.4135 |                 12.8277 |
| cartpole_safety     | L2      |           1.0000 |           -4.5128 |                 11.8349 |
| cartpole_safety     | L3      |           1.0000 |           -4.5842 |                 11.2180 |
| dynamic_bicycle_4d  | L0      |           0.0000 |            0.5198 |                  6.5665 |
| dynamic_bicycle_4d  | L1      |           0.0000 |            0.5521 |                  6.5188 |
| dynamic_bicycle_4d  | L2      |           0.0000 |            0.5779 |                  6.4732 |
| dynamic_bicycle_4d  | L3      |           0.0000 |            0.5975 |                  6.4329 |
| planar_quadrotor_6d | L0      |           0.0000 |            0.6581 |                  1.2223 |
| planar_quadrotor_6d | L1      |           0.0000 |            0.3420 |                  2.0849 |
| planar_quadrotor_6d | L2      |           1.0000 |           -0.3032 |                  3.7540 |
| planar_quadrotor_6d | L3      |           1.0000 |           -0.8689 |                  5.1507 |
| pushing_contact_4d  | L0      |           0.0000 |            0.1691 |                  1.3898 |
| pushing_contact_4d  | L1      |           0.0000 |            0.1662 |                  1.2172 |
| pushing_contact_4d  | L2      |           0.0000 |            0.1717 |                  1.1405 |
| pushing_contact_4d  | L3      |           0.0000 |            0.1790 |                  1.0949 |

## Artifacts

- `src/domains/high_dimensional.py`
- `logs/domain_validation_metrics.csv`
- `figures/domain_schematic_cartpole_safety.png`
- `figures/domain_schematic_dynamic_bicycle_4d.png`
- `figures/domain_schematic_planar_quadrotor_6d.png`
- `figures/domain_schematic_pushing_contact_4d.png`

## Limitation

These domains are CPU prototypes for the next experiment stage. The current paper results still use the original simplified domains and trained Stage-A runner.
