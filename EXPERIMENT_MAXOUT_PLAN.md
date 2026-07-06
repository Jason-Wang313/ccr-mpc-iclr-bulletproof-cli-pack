# Experiment Max-Out Plan

## Principle

No GPU is acceptable only if the paper wins through theory, controlled experiments, and broad CPU-reproducible evidence.

## Domains

### D0: synthetic separation system

Purpose:
- visualize and validate Theorem 1.

Required:
- two learned models with similar prediction error/calibration;
- different MPC actions near boundary;
- failure of raw uncertainty;
- success of CCR.

### D1: classic constrained control

Systems:
- double integrator with obstacle/constraint;
- pendulum with safety envelope;
- cartpole with angle/position constraint;
- acrobot with unsafe region.

OOD shifts:
- mass/length/friction;
- actuator gain;
- latency;
- noise.

### D2: dynamic bicycle/agile car

Tasks:
- lane keeping;
- track following;
- obstacle avoidance;
- aggressive cornering.

Shifts:
- friction coefficient;
- steering bias;
- actuator latency;
- payload/mass;
- sensor noise;
- speed cap.

### D3: planar quadrotor

Tasks:
- waypoint tracking;
- obstacle avoidance;
- narrow passage;
- landing/tracking under disturbance.

Shifts:
- wind;
- payload;
- motor strength;
- latency;
- mass/battery variation;
- sensor noise.

### D4: quasi-static pushing/contact

Tasks:
- push object to target;
- push around obstacle;
- rotate object;
- contact-rich path.

Shifts:
- object mass;
- friction;
- contact point uncertainty;
- table surface;
- actuation noise.

### D5: secondary planner generality

Use same risk layer with:
- CEM-MPC
- shooting MPC
Main method remains MPPI.

## Baselines

Mandatory:
1. vanilla MPPI/MPC
2. robust/conservative MPC
3. raw ensemble uncertainty penalty
4. prediction-calibrated uncertainty penalty
5. CVaR/RA-MPPI-style
6. chance-constrained MPC-style
7. conformal prediction-set MPC
8. conformal risk control with non-CCR score
9. conformal decision/planning baseline
10. SODA-like OOD fallback
11. domain-randomized dynamics + MPC
12. sysID/adaptation + MPC
13. oracle dynamics + MPC
14. CCR no calibration
15. calibration no CCR
16. planner disagreement only
17. regret only (`regret_only`)
18. violation tail only (`violation_tail_only`)

## Metrics

- reward/cost
- closed-loop violation rate
- target risk vs observed risk
- ECE / calibration error for trajectory risk
- Brier score and log loss for failure prediction
- safety-performance Pareto
- freezing/conservatism rate
- computation time per step
- calibration sample efficiency
- OOD severity curves
- fallback rate
- regret vs oracle dynamics
- decision disagreement across dynamics particles
- empirical coverage of calibration theorem

## Required ablations

- number of dynamics particles K
- number of action samples N
- planning horizon H
- calibration set size
- risk threshold alpha
- OOD severity
- risk features included/excluded
- online recalibration on/off
- fallback on/off
- weighted calibration on/off
- task-conditioned risk on/off
- closed-loop vs open-loop calibration

## Seeds

Minimum:
- 10 seeds per main experiment
- 20 seeds for synthetic/theorem demo if cheap
- confidence intervals everywhere

## Reproducibility

Agent must create:
- `scripts/run_minimal.sh`
- `scripts/run_full_cpu.sh`
- `scripts/reproduce_main_figures.sh`
- config files for every figure
- raw logs
- plot scripts
- manifest with git/hash/configs
