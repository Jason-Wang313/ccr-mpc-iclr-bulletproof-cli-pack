# Counterfactual Control Risk ICLR Bulletproof Execution Pack

Date: 2026-07-06

Final committed paper direction:

# Prediction Uncertainty Is Not Control Risk:
## Counterfactual Risk Calibration for Learned-Dynamics MPC

Short name: **CCR-MPC** / **CCR-MPPI**

This is a **theory-first, CPU-reproducible ICLR plan**, not a robot-paper plan.

Main thesis:
> Learned dynamics can be prediction-calibrated yet decision-unsafe. We define counterfactual control risk (CCR): planner-level regret/violation instability across plausible learned dynamics models. We calibrate CCR to observed closed-loop failure risk and use it inside MPC/MPPI to make safer decisions under dynamics shift without becoming blindly conservative.

## What the CLI agent must do

1. Read `CLI_AGENT_MASTER_PROMPT.md`.
2. Run the pack verifier before editing:

```powershell
.\scripts\run_pack_checks.ps1
```

or:

```bash
bash scripts/run_pack_checks.sh
```

3. Execute phases in `tasks.yaml` order.
4. Maintain `reports/claim_ledger.csv` from `templates/claim_ledger.csv`.
5. Finish all non-hardware deliverables:
   - bounded theory statements/proofs under stated assumptions
   - synthetic separation experiments
   - CCR-MPC/CCR-MPPI implementation
   - all baselines
   - bounded focused CPU experiment suite plus max-out matrix
   - calibration/risk/evaluation scripts
   - plot generation
   - paper manuscript
   - related-work audit
   - reviewer-defense matrix
   - reproducibility package
6. Create:
   - `reports/ICLR_CCR_MPC_COMPLETE.md`
   - `reports/final_artifact_manifest.json`
7. Print exactly:

```text
ICLR CCR-MPC COMPLETE: bounded theory proofs, counterfactual-risk algorithms, calibration code, CPU experiment suite, baselines, ablations, plots, paper manuscript, related-work audit, and reviewer-defense reports are finished. All claims are backed by generated artifacts. Human review is required before submission.
```

## Core rule

Do not claim "foundation dynamics models" unless the experiments actually include a broad/generalist dynamics model. The safe title uses **learned dynamics models**, not "foundation dynamics models".

## Completion gate

The completion message is forbidden until:

- `scripts/verify_pack.py --smoke` passes;
- every required report in `tasks.yaml` exists under `reports/`;
- `reports/final_artifact_manifest.json` validates against `schemas/artifact_manifest_schema.json`;
- every hashed artifact listed in `reports/final_artifact_manifest.json` exists and matches its SHA-256 digest;
- every headline paper claim has a supported row in `reports/claim_ledger.csv`;
- every claim-ledger evidence path exists;
- `configs/execution_config.json` separates actual focused-run settings from plots-only regeneration metadata;
- `logs/results.jsonl` covers all required domains, methods, seeds, OOD levels, and metrics;
- all citations and related-work claims are verified from primary sources.

## Main files

- `COUNTERFACTUAL_CONTROL_RISK_MASTER_PLAN.md`: full plan.
- `CLI_AGENT_MASTER_PROMPT.md`: paste this into the CLI agent.
- `THEORY_MOAT_PLAN.md`: proof strategy and theorem checklist.
- `EXPERIMENT_MAXOUT_PLAN.md`: every experiment required.
- `REVIEWER_ATTACK_CLOSURE_MATRIX.md`: attack -> defense -> artifact.
- `PRIOR_WORK_DISTINCTION_MEMO.md`: how to distinguish from RA-MPPI, conformal risk, conformal decision, safe MPC, etc.
- `BASELINES_ABLATIONS_CHECKLIST.md`: all baselines and ablations.
- `matrices/experiment_matrix_maxout.csv`: maxed CPU experiment grid.
- `tasks.yaml`: machine-readable execution graph.
- `schemas/*.json`: result logging schemas.
- `skeleton/*.py`: pseudocode/skeletons for agent implementation.
- `scripts/verify_pack.py`: structural verifier and smoke-test entrypoint.
- `scripts/run_pack_checks.ps1` / `scripts/run_pack_checks.sh`: cross-platform check wrappers.
- `templates/claim_ledger.csv`: claim-to-artifact ledger required before completion.
- `templates/readiness_gate_report.md`: final reviewer-risk gate before completion.
- `paper/CCR_MPC_paper.tex`: compiled LaTeX manuscript source.
- `paper/CCR_MPC_paper.pdf`: compiled manuscript PDF.
- `paper/references.bib`: verified BibTeX bibliography.
- `logs/`, `tables/`, and `figures/`: generated focused CPU run artifacts.
- `reports/claim_ledger.csv`: bounded claim-to-evidence ledger.
- `reports/citation_verification.md`: primary-source citation audit.
