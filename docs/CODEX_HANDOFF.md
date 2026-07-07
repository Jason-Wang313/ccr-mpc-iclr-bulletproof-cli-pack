# Codex Handoff

## Current Goal

Execute the local max-out prompt `C:\Users\wangz\Downloads\FINAL_AGENT_PROMPT_CCR_MPC_ICLR_MAXOUT.md` against the CCR-MPC repository while keeping claims honest.

## Repo Facts Verified

- Repo path: `C:\Users\wangz\Downloads\ccr_mpc_iclr_bulletproof_cli_pack`
- Remote: `https://github.com/Jason-Wang313/ccr-mpc-iclr-bulletproof-cli-pack.git`
- Baseline before edits was up to date with `origin/main`.
- Existing focused CPU suite remains 1026 closed-loop runs and 20862 planning-step predictions.
- Existing verifier now passes after edits: `PACK VERIFY PASSED: 0 warning(s)`.
- Manifest now verifies 73 artifact entries.
- New `paper/iclr_submission.tex` and `paper/iclr_submission.pdf` are seeded from the bounded manuscript, not a final max-out rewrite.
- New trained dynamics artifacts are diagnostic and are not yet integrated into the MPC experiment runner.

## Files Changed Or Added

- Added `paper/iclr_submission.tex` and `paper/iclr_submission.pdf` as seeded submission branch artifacts.
- Added `reports/preupgrade_repo_audit.md` and `reports/final_submission_readiness.md` to record current readiness and gaps.
- Added `reports/final_claim_ledger.csv` as a seed copy of the bounded claim ledger.
- Added theorem reports:
  - `reports/theorem_A_separation.md`
  - `reports/theorem_B_calibration.md`
  - `reports/theorem_C_safe_cost.md`
- Added `reports/acceptance_critical_result_gate.md`, which rejects broad superiority claims under current results.
- Added `scripts/train_learned_dynamics_cpu.py`.
- Added trained Torch MLP ensemble artifacts under `artifacts/models/`.
- Added `logs/dynamics_prediction_metrics.csv`.
- Added `reports/dynamics_training_report.md`.
- Added figures:
  - `figures/prediction_calibration_vs_control_risk.png`
  - `figures/theorem_separation_visualization.png`
- Updated `reports/final_artifact_manifest.json` with new hashes.
- Updated `scripts/verify_pack.py` to allow `logs/dynamics_prediction_metrics.csv` as a tracked log.
- Added this handoff at `docs/CODEX_HANDOFF.md`.

## Commands And Results

- `git pull --ff-only`: already up to date.
- `python scripts\verify_pack.py --smoke`: passed before edits.
- `pdflatex`/`bibtex`/`pdflatex`/`pdflatex` on `paper/iclr_submission.tex`: produced `paper/iclr_submission.pdf`; LaTeX scratch files were removed.
- `python scripts\train_learned_dynamics_cpu.py`: trained six Torch MLP ensembles and wrote dynamics metrics/report/figure.
- Final `python scripts\verify_pack.py --smoke`: `PACK VERIFY PASSED: 0 warning(s)`.

## Experiment Artifacts And Results

- Existing focused CCR-MPC result remains unchanged: CCR-MPC mean violation rate 0.0042087542 and mean cost 29.4113151 in `tables/summary_by_method.csv`.
- `cvar_ra_mppi` matches the same aggregate violation rate with lower mean cost 28.6502721.
- New learned dynamics diagnostics:
  - L0 mean one-step MSE: 0.000004
  - L1 mean one-step MSE: 0.000090
  - L2 mean one-step MSE: 0.000282
  - L0 mean interval90 coverage: 0.643779
  - L1 mean interval90 coverage: 0.249834
  - L2 mean interval90 coverage: 0.175170

## Known Failures Or Bugs

- No verifier failures remain.
- `latexmk` could not run because MiKTeX lacks Perl; direct `pdflatex`/`bibtex` worked.
- The max-out prompt is not complete. The final max-out completion message has not been printed and must not be printed yet.

## Open Questions

- Whether to push the new artifacts to the public GitHub repo: UNKNOWN.
- Whether the next execution should integrate trained dynamics into the MPC runner or first implement higher-fidelity domains: UNKNOWN.
- Whether to run Stage B max-out matrix after planner integration: UNKNOWN.

## Next Recommended Steps

1. Decide whether to commit and push this verified upgrade checkpoint.
2. Integrate the trained dynamics ensembles into the planner as a selectable model source.
3. Add `reports/ccr_score_design_report.md`, `configs/baseline_sweeps.yaml`, and `tables/baseline_tuning_summary.csv`.
4. Add executed-rollout calibration versus simulator-oracle full-candidate-label ablation.
5. Run a small Stage A with trained dynamics before attempting Stage B.

Safe to clear after handoff is updated.
