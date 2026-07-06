# Prior Work Distinction Memo

## Dangerous prior-work buckets

### Risk-aware MPPI / CVaR-MPPI

Existing work uses CVaR/tail-risk objectives for safer MPPI. Do not claim first risk-aware MPPI.

Distinction:
CCR-MPC measures planner instability/regret across plausible learned dynamics models and calibrates that to observed closed-loop failure risk. Risk is decision-space, not just cost-tail or collision risk.

### Dynamic risk-aware / chance-constrained MPPI

Existing work handles predicted collision risk, dynamic obstacles, and chance constraints.

Distinction:
CCR-MPC targets learned-dynamics-induced control failure: tracking failure, saturation, instability, constraint violation, OOD dynamics, task failure.

### Conformal prediction for planning

Existing work uses conformal prediction sets/regions to support safe planning.

Distinction:
CCR-MPC does not merely calibrate future states. It calibrates a planner-level counterfactual regret/violation score induced by learned dynamics particles.

### Conformal Risk Control / Conformal Decision Theory

Existing work gives general risk-control/decision-calibration tools.

Distinction:
Use these as tools/baselines. Novelty is the control-specific CCR score and its use inside receding-horizon learned-dynamics MPC.

### Uncertainty-aware MPC / GP-MPC / safe MPC

Existing work penalizes uncertainty or propagates confidence sets.

Distinction:
Raw uncertainty may be unrelated to closed-loop decision risk. CCR focuses on whether plausible dynamics models would make the planner choose different/high-regret actions.

### SODA-like OOD fallback

Existing work detects unreliable dynamics and triggers fallback.

Distinction:
CCR-MPC shapes decisions before fallback; it measures counterfactual planner regret, not just OOD detection.

## Must-cite/must-compare categories

The agent must verify exact citations before final writing:
- risk-aware MPPI / CVaR MPPI
- chance-constrained/risk-calibrated MPPI
- conformal prediction for safe planning
- conformal risk control
- conformal decision theory
- safe learning-based MPC
- uncertainty-aware MPC
- model-based RL with MPC
- learned dynamics ensemble uncertainty
- control-aware representations/MPC at ICLR
- Dreamer/BMPC/BS-MPC only as broad ICLR precedent, not direct baselines unless run fairly

## Related-work wording

Use:
"These works calibrate prediction sets, cost tails, collision probabilities, or OOD monitors. We calibrate counterfactual planner regret/violation induced by learned dynamics uncertainty, and use it directly to select MPC actions."

Do not use:
"We are the first safe/risk-aware/conformal MPC method."
