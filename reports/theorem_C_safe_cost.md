# Theorem C: Safe-Cost Optimality Among Calibrated Accepted Candidates

## Status

Supported for sampled candidate sets under a fixed calibrated risk gate. This is an argmin property of the implemented decision rule, not a global optimal-control theorem.

## Statement

Given a sampled candidate set, learned-dynamics particles, CCR scores, a calibrated threshold tau, and predicted adjusted costs, CCR-MPC selects the minimum predicted-cost candidate among candidates whose score is accepted by the calibrated gate. If no candidate is accepted, the fallback is the lowest predicted-risk candidate.

## Proof Sketch

Let U be the sampled candidate set and A_tau be the accepted subset. If A_tau is nonempty, the implementation computes predicted costs for every candidate and masks non-accepted candidates. It returns argmin over the masked cost vector. Therefore the selected candidate has predicted cost no larger than any other accepted sampled candidate under the same threshold and candidate set.

## Gap Decomposition

Any comparison to a continuous safe optimum requires additional terms:

- sampling error: the best continuous control may not appear in the sampled candidate set;
- model error: learned-dynamics predicted costs may differ from true closed-loop costs;
- calibration threshold error: the accepted set depends on finite calibration data and score quality;
- fallback error: when no candidate is accepted, the decision minimizes predicted risk rather than accepted-set cost.

## Matching Artifacts

- `skeleton/ccr_mpc.py` (`select_action`)
- `paper/iclr_submission.tex`
- `reports/theory_moat_report.md`
- `tables/summary_by_method.csv`

## Limitation

The result justifies the sampled selection rule. It does not prove global optimality, asymptotic MPC stability, or robot safety.

