# Theorem A: Separation Of Prediction Metrics And Control Risk

## Status

Constructive theorem supported for a stylized one-step constrained MPC system. This is not a broad robotics safety theorem.

## Statement

For any epsilon > 0 and any rho in (0, 1], there is a deterministic one-dimensional constrained control problem, a training distribution, an evaluation distribution, two learned dynamics models, and a two-candidate one-step MPC planner such that the models have arbitrarily similar prediction loss on the training distribution while inducing different first actions and a violation-risk gap of at least rho on the evaluation distribution.

## Construction

- State: scalar x.
- Action candidates: safe action u_s and risky action u_r.
- True dynamics: x+ = x + u.
- Constraint: x+ <= 0.
- Evaluation state: x0 = -eta / 2.
- Safe action: u_s = -eta / 2, yielding x+ = -eta.
- Risky action: u_r = eta, yielding x+ = eta / 2 and violating the constraint.
- Model f_a: equals the true dynamics.
- Model f_b: equals the true dynamics on the training-distribution support, but is locally optimistic near x0 for u_r and predicts the risky transition below the constraint boundary.
- Training distribution: places no mass in the local boundary neighborhood where f_b differs from f_a.
- Evaluation distribution: places mass rho at x0.

Because the models match on the training support, their prediction loss gap on that support can be made zero, and therefore at most epsilon. Because the planner evaluates candidates near the boundary, f_a rejects u_r while f_b predicts u_r as feasible and can choose it when the objective prefers approaching the target boundary. The induced violation-risk gap is at least rho.

## Decision Boundary

The decision boundary is the set of model predictions for which the risky candidate crosses the constraint threshold x+ = 0. A small local prediction change near this boundary flips the first action even if prediction loss is unchanged on the training distribution.

## Why Prediction Calibration Fails Here

Prediction calibration on the training distribution does not constrain behavior in the planner-relevant boundary neighborhood when that neighborhood has no training mass. The risk object is therefore decision-conditional: whether candidate ranking and constraint feasibility change under plausible learned dynamics.

## Matching Artifacts

- `figures/theorem_separation_visualization.png`
- `paper/iclr_submission.tex`
- `reports/theory_moat_report.md`
- `logs/results.jsonl` rows with `domain=synthetic_separation`

## Limitation

The theorem is deliberately narrow. It isolates a mechanism; it does not prove that CCR-MPC is safe for arbitrary nonlinear continuous-control systems.

