# Theory Moat Plan

## Goal

Make the paper impossible to dismiss as a heuristic uncertainty penalty.

## Theorem 1: Separation of Prediction Calibration and Control-Risk Calibration

### Statement target

There exists a constrained dynamical system, a data distribution, and two learned models `f_a`, `f_b` such that:

1. `f_a` and `f_b` have identical or arbitrarily close one-step prediction error on the data distribution.
2. `f_a` and `f_b` have identical or arbitrarily close prediction calibration under standard prediction metrics.
3. When embedded in MPC with the same cost/constraint and horizon, they induce different first actions.
4. The closed-loop violation probability under one induced policy can be arbitrarily larger than under the other.

### Construction sketch

Use a low-dimensional state with a constraint boundary. Put most data mass away from the decision boundary, so prediction error/calibration are dominated by harmless regions. Construct a small model mismatch near the boundary that flips the MPC argmin. The flipped action crosses a safety boundary with high probability.

### Artifact required

- formal theorem statement
- proof
- plot of system and decision boundary
- synthetic experiment exactly matching theorem

## Theorem 2: Finite-Sample CCR Calibration

### Statement target

Given calibration rollouts `(S_i, L_i)`, where `S_i` is CCR score of selected planned trajectory and `L_i` is observed violation/task-failure loss, choose a threshold or risk mapping by split calibration. Under exchangeability:

`Pr(observed violation of future selected plan) <= alpha + finite_sample_term`

or expected monotone loss is controlled at level alpha.

### Important

If directly using Conformal Risk Control, cite it and state that the novelty is the CCR score, not the generic calibration machinery.

### Artifact required

- theorem statement
- proof with assumptions
- empirical coverage validation

## Theorem 3: Safe-Cost Optimality Among Sampled Rollouts

### Statement target

Let `U_safe` be candidate action sequences satisfying the calibrated risk constraint. CCR-MPC selects a sequence with cost within epsilon of the best sampled risk-acceptable sequence, where epsilon is due to sampling, score estimation, and calibration error.

### Artifact required

- theorem statement
- proof
- empirical safety-performance Pareto showing not just conservative

## Optional Theorem 4: Weighted Shift Calibration

### Statement target

Under bounded density ratio or weighted exchangeability, weighted CCR calibration controls target-domain violation risk.

### Artifact required

- theorem statement
- proof sketch
- OOD severity experiment with and without weighting

## Theory quality checklist

- Define all random variables.
- Make clear what is calibrated: closed-loop violation/failure, not prediction residual.
- Do not overclaim global nonlinear control safety.
- Separate open-loop rollout risk from receding-horizon closed-loop risk.
- State limitations of exchangeability assumptions.
