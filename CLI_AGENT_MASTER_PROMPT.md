# CLI Agent Master Prompt: ICLR CCR-MPC Bulletproof Plan

You are a CLI research/coding agent executing the ICLR paper plan:

# Prediction Uncertainty Is Not Control Risk:
## Counterfactual Risk Calibration for Learned-Dynamics MPC

Short name: CCR-MPC / CCR-MPPI.

## Mission

Build a theory-first, CPU-reproducible ICLR submission package.

The paper must prove and demonstrate:
1. Prediction calibration/uncertainty does not imply closed-loop control-risk calibration.
2. Counterfactual control risk (CCR) is a planner-level risk score based on regret/violation instability across plausible learned dynamics models.
3. CCR can be calibrated to observed closed-loop violation/failure risk.
4. CCR-MPC/CCR-MPPI improves safety-performance tradeoffs under dynamics shift compared with hard baselines.
5. Experiments are broad enough to make the result non-toy without requiring GPU.

## First commands

Before implementing, run:

```bash
python scripts/verify_pack.py --smoke
```

On Windows PowerShell, this wrapper is available:

```powershell
.\scripts\run_pack_checks.ps1
```

Treat verifier failures as blockers unless they are explicitly about the absence
of completed experiment reports.

## Completion protocol

When all non-hardware jobs are done:
1. Create `reports/claim_ledger.csv` from `templates/claim_ledger.csv`.
2. Create `reports/readiness_gate_report.md` from `templates/readiness_gate_report.md`.
3. Create `reports/ICLR_CCR_MPC_COMPLETE.md`.
4. Create `reports/final_artifact_manifest.json`.
5. Run `python scripts/verify_pack.py --smoke`.
6. Print exactly:

ICLR CCR-MPC COMPLETE: bounded theory proofs, counterfactual-risk algorithms, calibration code, CPU experiment suite, baselines, ablations, plots, paper manuscript, related-work audit, and reviewer-defense reports are finished. All claims are backed by generated artifacts. Human review is required before submission.

Then stop.

## Forbidden

- Do not claim foundation dynamics models unless actually implemented.
- Do not compare to large GPU-heavy methods unless a fair baseline is run or explicitly scoped as not comparable.
- Do not hide conformal risk control, conformal decision theory, RA-MPPI, chance-constrained MPPI, uncertainty-aware MPC, safe MPC, SODA-like fallback, or domain randomization.
- Do not make the paper look like "ensemble variance + conformal threshold".
- Do not report only reward.
- Do not generate fake citations.
- Do not mark work complete without generated plots/tables/logs.
- Do not keep a claim unless it has an artifact row in `reports/claim_ledger.csv`.
- Do not leave metric-name drift between CSV configs, JSON logs, plots, and tables.

## Required artifacts

Theory:
- theorem statements
- bounded proofs for the stated assumptions
- synthetic construction demonstrating separation
- assumptions and limitations

Code:
- dynamics ensemble/particles
- planner implementations: MPPI main, CEM-MPC secondary
- CCR score computation
- calibration layer
- risk-aware planner
- baselines
- experiment runner
- logging/metrics/plots

Experiments:
- synthetic separation system
- classic constrained control systems
- kinematic/dynamic car
- planar quadrotor
- quasi-static pushing/contact
- secondary planner generality
- ablations
- OOD severity sweeps
- calibration sample-size sweeps
- seed/confidence interval analysis

Paper:
- ICLR-style abstract
- introduction
- related work
- theorem section
- method
- experiments
- limitations
- reviewer attack closure appendix

Evidence ledger:
- every headline claim
- exact evidence artifact paths
- tested scope and compute budget
- strongest alternative explanation
- limitation or narrowed wording
