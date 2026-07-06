# Completion Checklist

The CLI agent may only print the completion message if all are true:

## Theory
- [ ] separation theorem statement
- [ ] bounded proof under stated assumptions
- [ ] finite-sample CCR calibration theorem
- [ ] safe-cost optimality theorem
- [ ] online shifted calibration theorem explicitly out of scope with reason

## Code
- [ ] CCR score implementation
- [ ] calibration implementation
- [ ] MPPI implementation
- [ ] secondary planner implementation
- [ ] all baselines
- [ ] all domains
- [ ] logging schema
- [ ] plotting scripts

## Experiments
- [ ] D0 synthetic separation
- [ ] classic control
- [ ] car
- [ ] quadrotor
- [ ] pushing/contact
- [ ] secondary planner
- [ ] OOD severity sweeps
- [ ] calibration sample-size sweeps
- [ ] all baselines
- [ ] ablations
- [ ] confidence intervals

## Paper
- [ ] abstract
- [ ] intro
- [ ] related work
- [ ] theory section
- [ ] method
- [ ] experiments
- [ ] limitations
- [ ] appendix outline

## Reports
- [ ] prior-work audit
- [ ] reviewer attack closure
- [ ] calibration report
- [ ] plot/table manifest
- [ ] claim ledger with one row per headline claim
- [ ] readiness gate report
- [ ] final artifact manifest

## Verification
- [ ] `python scripts/verify_pack.py --smoke` passes
- [ ] result logs use metric names from `schemas/result_schema.json`
- [ ] final manifest validates against `schemas/artifact_manifest_schema.json`
- [ ] every final citation has primary-source metadata verified
- [ ] no broad "foundation dynamics" claim appears unless actually implemented

Completion message:
ICLR CCR-MPC COMPLETE: bounded theory proofs, counterfactual-risk algorithms, calibration code, CPU experiment suite, baselines, ablations, plots, paper manuscript, related-work audit, and reviewer-defense reports are finished. All claims are backed by generated artifacts. Human review is required before submission.
