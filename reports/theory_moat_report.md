# CCR-MPC Theory Moat Report

## Status

This execution produced bounded formal theorem statements for the paper package. The statements are intentionally narrow and still require human theorem review before external submission.

## Theorem 1: Separation Of Prediction Calibration And Control Risk

Claim: for a constrained one-dimensional one-step MPC problem, two learned dynamics models can have identical one-step prediction loss on a training distribution away from the constraint boundary while inducing different MPC actions near the boundary. Under an evaluation distribution with mass on the boundary state, the closed-loop violation risk can differ by a constant.

Proof: use true dynamics x+ = x+u with constraint x+ <= 0. At evaluation state x0 = -eta/2, include a safe candidate u_s = -eta/2 and a risky candidate u_r = eta. The true risky transition violates. Let f_a equal the true dynamics. Let f_b equal the true dynamics outside the boundary neighborhood and subtract eta inside it. A training distribution with no mass in the boundary neighborhood gives identical one-step loss for f_a and f_b. A one-step MPC objective with a large predicted-violation penalty makes f_a choose the safe candidate, while f_b predicts both candidates as safe and chooses the risky candidate because it is closer to the target boundary. An evaluation distribution with mass rho on x0 yields violation-risk gap at least rho.

Evidence link: `figures/prediction_error_vs_control_risk.png` and the `synthetic_separation` rows in `logs/results.jsonl`.

## Theorem 2: Split CCR Calibration

Claim: for a finite threshold set, if calibration and test candidate contexts are exchangeable and labels are bounded, a split-calibrated CCR threshold controls accepted-candidate failure frequency up to a Hoeffding/union-bound finite-sample slack.

Proof: for any fixed threshold, the accepted-candidate failure rate is a bounded empirical mean conditional on acceptance. Hoeffding's inequality upper-bounds the conditional failure probability by empirical failure plus sqrt(log(2|T|/delta)/(2n_tau)). A union bound makes the inequality simultaneous over the finite threshold set T. Since the selected threshold is chosen from this set using split calibration labels, the simultaneous bound applies to it.

Implementation link: `skeleton/ccr_mpc.py::RiskCalibrator`.

## Theorem 3: Safe-Cost Optimality Over Sampled Candidates

Claim: given a calibrated acceptable set, CCR-MPC selects the minimum predicted mean-cost candidate inside that set. Its sampled-candidate cost is therefore no worse than any other accepted sampled candidate under the same score threshold.

Proof: if the accepted set is nonempty, the selection rule is an argmin over the adjusted predicted cost on that accepted set. Any comparison to a continuous safe optimum must pass through candidate-sampling error, model-prediction error, and calibration-threshold error; no stronger continuous-control global optimality is claimed.

## Limitations

- The theorem statements are narrow and should be checked by a human theorem reviewer before submission.
- The exchangeability condition is strong under online distribution shift.
- The CPU domains are simplified surrogates, not full robot physics.
