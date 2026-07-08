# Codex Handoff

## Current Goal

Execute the local max-out prompt `C:\Users\wangz\Downloads\FINAL_AGENT_PROMPT_CCR_MPC_ICLR_MAXOUT.md` against the CCR-MPC repository while keeping claims honest.

## Repo Facts Verified

- Repo path: `C:\Users\wangz\Downloads\ccr_mpc_iclr_bulletproof_cli_pack`
- Remote: `https://github.com/Jason-Wang313/ccr-mpc-iclr-bulletproof-cli-pack.git`
- Baseline before edits was up to date with `origin/main`.
- Existing focused CPU suite remains 1026 closed-loop runs and 20862 planning-step predictions.
- Existing verifier now passes after this continuation checkpoint: `PACK VERIFY PASSED: 0 warning(s)`.
- Manifest now verifies 102 artifact entries.
- New `paper/iclr_submission.tex` and `paper/iclr_submission.pdf` are seeded from the bounded manuscript, not a final max-out rewrite.
- New trained dynamics artifacts are diagnostic in the original focused suite and integrated in the separate Stage-A runner `scripts/run_trained_dynamics_stage_a.py`.

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
- Added trained-dynamics Stage-A runner and outputs:
  - `scripts/run_trained_dynamics_stage_a.py`
  - `logs/trained_dynamics_stage_a_results.jsonl`
  - `logs/trained_dynamics_stage_a_results_flat.csv`
  - `logs/trained_dynamics_stage_a_step_predictions.csv`
  - `logs/trained_dynamics_stage_a_calibration_samples.csv`
  - `configs/trained_dynamics_stage_a_config.json`
  - `tables/trained_dynamics_stage_a_summary_by_method.csv`
  - `tables/trained_dynamics_stage_a_summary_by_domain_method.csv`
  - `reports/trained_dynamics_stage_a_report.md`
  - `reports/trained_dynamics_planner_integration.md`
- Added preliminary baseline/score scaffolds:
  - `configs/baseline_sweeps.yaml`
  - `tables/baseline_tuning_summary.csv`
  - `reports/baseline_fairness_report.md`
  - `reports/ccr_score_design_report.md`
- Added preliminary risk-model validation:
  - `scripts/validate_risk_models.py`
  - `logs/risk_model_validation.csv`
  - `reports/risk_model_validation_report.md`
- Added calibration-label-source ablation:
  - `scripts/compare_calibration_label_sources.py`
  - `logs/calibration_label_source_ablation.csv`
  - `reports/calibration_label_source_ablation.md`
- Added higher-dimensional domain prototypes and validation:
  - `src/domains/high_dimensional.py`
  - `scripts/validate_domain_upgrades.py`
  - `logs/domain_validation_metrics.csv`
  - `reports/domain_validation_report.md`
  - `figures/domain_schematic_cartpole_safety.png`
  - `figures/domain_schematic_dynamic_bicycle_4d.png`
  - `figures/domain_schematic_planar_quadrotor_6d.png`
  - `figures/domain_schematic_pushing_contact_4d.png`
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
- `python scripts\run_trained_dynamics_stage_a.py --domains synthetic_separation --levels L0 --methods vanilla_mppi,ccr_mpc,oracle_mpc --seeds 0 --candidates 12 --calibration-contexts 4`: smoke run passed.
- `python scripts\run_trained_dynamics_stage_a.py --domains all --levels L0,L1,L2,L3 --seeds 0,1,2,3,4 --candidates 24 --calibration-contexts 24`: completed 2280 trained-dynamics Stage-A episodes in 2266.87 seconds.
- `python scripts\validate_risk_models.py`: wrote 18 risk-model validation rows.
- `python scripts\compare_calibration_label_sources.py`: wrote 27 calibration-label-source ablation rows.
- `python scripts\validate_domain_upgrades.py`: wrote domain validation metrics and four domain schematic figures.
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
- Expanded trained Stage-A aggregate rows:
  - Vanilla MPPI: cost 28.6862, violation 0.0255
  - CCR-MPC: cost 29.3156, violation 0.0166
  - CVaR/RA-MPPI: cost 28.7424, violation 0.0234
  - Conformal prediction MPC: cost 37.4319, violation 0.0019
- Preliminary risk validation:
  - Focused surrogate best Brier: random forest all features, 0.0258
  - Trained Stage-A best Brier: random forest all features, 0.0460
- Calibration-label-source ablation:
  - Simulator full-candidate violation-rate label Brier: 0.0541
  - Executed-rollout step-violation label Brier: 0.1578
- Higher-dimensional domain prototype smoke validation:
  - Cartpole safety: violation rate 1.0000 at L0-L3 under the simple validation policy, so it needs controller/domain tuning before main experiments.
  - Dynamic bicycle 4D: violation rate 0.0000 at L0-L3, likely too easy in this smoke policy.
  - Planar quadrotor 6D: violation rate 0.0000 at L0/L1 and 1.0000 at L2/L3, useful as a severity stress test.
  - Pushing contact 4D: violation rate 0.0000 at L0-L3, likely too easy in this smoke policy.

## Known Failures Or Bugs

- No verifier failures remain.
- `latexmk` could not run because MiKTeX lacks Perl; direct `pdflatex`/`bibtex` worked.
- The max-out prompt is not complete. The final max-out completion message has not been printed and must not be printed yet.
- Trained Stage-A results are mixed and do not support broad superiority.
- Higher-dimensional domains are prototypes only; they are not integrated into the main MPC runner or trained Stage-A runner.

## Open Questions

- Whether to integrate trained dynamics into the original focused runner before Stage B: UNKNOWN.
- Whether to tune the new higher-dimensional domains first or integrate them as stress tests with current policies: UNKNOWN.
- Whether to run Stage B max-out matrix after planner/domain integration: UNKNOWN.

## Next Recommended Steps

1. Commit and push this verified continuation checkpoint.
2. Promote trained dynamics to a first-class `--model-source` option in the original runner, or keep the separate runner and integrate the higher-dimensional domain prototypes there.
3. Add a dedicated executed-rollout calibration split instead of relying only on offline Stage-A diagnostics.
4. Execute validation-selected baseline sweeps from `configs/baseline_sweeps.yaml`.
5. Run Stage B only after trained-domain baselines, domain difficulty, and calibration are stable.

Safe to clear after handoff is updated.
