# Prediction Uncertainty Is Not Control Risk
## Counterfactual Risk Calibration for Learned-Dynamics MPC

Short name: CCR-MPC / CCR-MPPI.

## Final paper identity

This is not a "controller tuning" paper. It is a decision-calibration paper for learned-dynamics control.

Main claim:
> Prediction-space uncertainty is not the object that controllers need. A planner needs decision-space risk: whether plausible learned dynamics models would make it choose a different, high-regret, or violating action.

## Abstract target

Learned dynamics models are often evaluated by prediction error or prediction calibration, but closed-loop control decisions depend on how model uncertainty changes the planner's selected action. We show theoretically and empirically that prediction calibration does not imply control-risk calibration. We introduce counterfactual control risk (CCR), a planner-level score measuring regret and violation instability across plausible learned dynamics models. We calibrate this score using finite-sample risk-control tools and integrate it into MPC/MPPI to choose actions that are low-risk under dynamics uncertainty without becoming uniformly conservative. Across synthetic systems, classic constrained control, vehicle dynamics, planar quadrotors, and contact-rich pushing, CCR-MPC controls observed violation rates under dynamics shift while preserving task performance better than raw uncertainty penalties, risk-aware MPPI, conformal prediction/planning baselines, conservative MPC, domain randomization, and system-ID baselines.

## Why this is ICLR-shaped

The paper contributes:
1. a negative theory result about prediction calibration vs control-risk calibration;
2. a new decision-risk statistic: counterfactual control regret;
3. finite-sample calibration/coverage guarantee for closed-loop risk;
4. a general MPC/MPPI instantiation;
5. broad CPU-reproducible experiments.

The ML object is not "a robot controller"; it is calibrated decision-making with learned dynamics models.

## Core definitions

### Plausible dynamics set

`F = {f_1, ..., f_K}` from:
- bootstrapped ensembles
- dropout particles
- posterior samples
- perturbed learned models
- local residual models
- OOD-shifted model particles in synthetic tests

### Planner candidate set

For each state `x_t`, sample action sequences:
`U = {u_1, ..., u_N}`.

Evaluate each `u_j` under each `f_i`:
`J_i(u_j)` and `Violation_i(u_j)`.

### Counterfactual control regret

For each model particle `f_i`, define:
`u_i* = argmin_{u in U} J_i(u)`.

Regret matrix:
`R_ij = J_i(u_j) - J_i(u_i*)`.

Candidate CCR score for candidate `u_j`:
- quantile over i of `R_ij`;
- CVaR over i of `R_ij`;
- violation rate over i;
- action-rank instability;
- first-action disagreement;
- constraint-margin tail.

### Calibrated CCR

Use calibration data from closed-loop rollouts:
features -> observed violation/task failure.

Calibrate CCR scores to target risk alpha:
- conformal/risk-control thresholding
- split calibration
- weighted/adaptive calibration for shift
- bootstrap uncertainty estimates

### CCR-MPC / CCR-MPPI

Modify MPC/MPPI:
1. sample candidate sequences;
2. evaluate under dynamics particles;
3. compute CCR features;
4. apply calibrated risk threshold or penalty;
5. select low-cost action among risk-acceptable candidates;
6. fallback if no acceptable candidate exists;
7. optionally update calibration online.

## Required theory

### Theorem 1: separation theorem

Prediction calibration / low one-step error does not imply low control risk.

Construct a low-dimensional constrained system where two learned models have identical or arbitrarily close prediction error/calibration on a data distribution but induce arbitrarily different MPC decisions and violation risk.

### Theorem 2: finite-sample CCR risk guarantee

Given exchangeable calibration rollouts and monotone violation loss, calibrated CCR threshold controls future violation frequency at level alpha plus finite-sample term.

### Theorem 3: safe-cost optimality

Among sampled candidate sequences satisfying the calibrated risk constraint, CCR-MPC selects a trajectory whose cost is close to the best low-risk sampled trajectory up to sampling/calibration error.

### Optional Theorem 4: shifted/weighted calibration

Under weighted exchangeability or bounded density-ratio shift, weighted CCR calibration controls target-domain risk.

## Required experimental conclusion

Main message:
> Prediction uncertainty and prediction calibration fail as proxies for closed-loop control risk. CCR provides a better calibrated decision-risk signal and improves safety-performance tradeoffs.

## Required domains

Minimum:
1. synthetic separation system
2. constrained classic control
3. dynamic bicycle / agile car
4. planar quadrotor
5. quasi-static pushing/contact

Optional if time:
6. simple locomotion/point-foot system
7. dynamic obstacle environment
8. noisy state-estimation system

## Required baselines

1. Vanilla MPPI/MPC
2. conservative/robust MPC
3. raw ensemble uncertainty penalty
4. prediction-calibrated uncertainty penalty
5. CVaR / RA-MPPI-style baseline
6. chance-constrained MPC-style baseline
7. conformal prediction-set MPC
8. conformal risk control with non-CCR score
9. conformal decision/planning baseline
10. SODA-like OOD detector + fallback
11. domain-randomized learned dynamics + MPC
12. system-ID/adaptation + MPC
13. oracle dynamics + MPC
14. CCR without calibration
15. calibration without counterfactual regret
16. planner disagreement only
17. regret only without violation features

## Required plots

1. prediction error vs control risk scatter
2. prediction calibration vs decision calibration
3. risk calibration reliability diagram
4. safety-performance Pareto
5. OOD severity curves
6. calibration set size curves
7. ensemble size sensitivity
8. horizon length sensitivity
9. compute time per step
10. ablation bar charts
11. failure mode breakdown
12. synthetic theorem visualization

## Required writing posture

Do not claim:
- first risk-aware MPC
- first conformal planning
- first learned MPC
- first safe MPC
- foundation dynamics models unless implemented

Do claim:
- prediction uncertainty is not control risk;
- CCR is a planner-level decision-risk statistic;
- finite-sample calibration makes the risk layer principled;
- CCR-MPC improves risk-performance tradeoffs in learned-dynamics MPC under shift.

## Success bar

Weak version = reject:
- no theorem;
- two toy experiments;
- only vanilla baselines;
- looks like ensemble penalty plus conformal threshold.

Strong version = plausible strong accept:
- separation theorem;
- finite-sample calibration theorem;
- broad CPU domains;
- hard prior-work baselines;
- exact calibration metrics;
- reproducible code and logs;
- clean writing.
