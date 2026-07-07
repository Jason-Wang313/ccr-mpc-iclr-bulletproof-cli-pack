# Theorem B: Finite-Sample Decision-Risk Calibration

## Status

Supported as a finite-threshold split-calibration guarantee under exchangeability. This report narrows the claim to accepted sampled candidates and does not claim hardware safety or online adaptive validity under arbitrary shift.

## Random Variable

The calibrated random variable is a candidate-context pair:

- context: state, domain, OOD level, sampled candidate set, and learned-dynamics particles;
- candidate: one sampled action sequence from that context;
- score: CCR or a baseline risk score computed before observing the candidate outcome;
- label: observed candidate failure under the calibration outcome definition.

In the current focused suite the main label is a simulator-evaluated planned-trajectory failure label. This should be replaced or paired with executed-rollout calibration for a stronger submission.

## Candidate-Level Guarantee

For a finite threshold set T and exchangeable calibration/test candidate-context examples, choose a threshold tau from T using split calibration. For any fixed tau, let A_tau be the accepted calibration candidates and let n_tau be their count. With bounded failure labels in [0, 1], Hoeffding's inequality gives a one-sided upper confidence bound on accepted-candidate failure frequency. A union bound over T makes the bound hold simultaneously for every threshold in T, including the selected tau.

## What Is Guaranteed

- Candidate-level accepted-set failure frequency under the same exchangeable sampling process.
- The guarantee applies to the selected finite threshold because the simultaneous bound covers all thresholds considered.
- The guarantee is finite-sample and distribution-free under the stated exchangeability assumption.

## What Is Not Guaranteed

- Step-level or episode-level safety without an additional reduction.
- Validity under nonexchangeable online shift.
- Safety for continuous action spaces beyond the sampled candidate set.
- Validity for a threshold not included in the finite threshold set unless an additional continuous-score argument is supplied.

## Matching Artifacts

- `skeleton/ccr_mpc.py` (`RiskCalibrator`)
- `reports/calibration_report.md`
- `logs/calibration_samples.csv`
- `figures/risk_reliability.png`
- `paper/iclr_submission.tex`

## Needed Upgrade

For the max-out submission, add an executed-rollout calibration setting and report it separately from simulator-oracle full-candidate labels.

