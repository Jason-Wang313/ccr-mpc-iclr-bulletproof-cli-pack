# Codex Handoff

## Current Goal

Execute the local max-out prompt `C:\Users\wangz\Downloads\FINAL_AGENT_PROMPT_CCR_MPC_ICLR_MAXOUT.md` against the CCR-MPC repository while keeping claims honest.

## Repo Facts Verified

- Repo path: `C:\Users\wangz\Downloads\ccr_mpc_iclr_bulletproof_cli_pack`
- Remote: `https://github.com/Jason-Wang313/ccr-mpc-iclr-bulletproof-cli-pack.git`
- Baseline before edits was up to date with `origin/main`.
- Existing focused CPU suite remains 1026 closed-loop runs and 20862 planning-step predictions.
- Existing verifier now passes after this continuation checkpoint: `PACK VERIFY PASSED: 0 warning(s)`.
- Manifest now verifies 140 artifact entries after the closed-loop-selected learned-risk pilot.
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
  - `reports/theorem_D_shift_calibration.md` (sketch/diagnostic only)
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
- Added trained-dynamics Stage-B pilot outputs:
  - `logs/trained_dynamics_stage_b_pilot_results.jsonl`
  - `logs/trained_dynamics_stage_b_pilot_results_flat.csv`
  - `logs/trained_dynamics_stage_b_pilot_step_predictions.csv`
  - `logs/trained_dynamics_stage_b_pilot_calibration_samples.csv`
  - `configs/trained_dynamics_stage_b_pilot_config.json`
  - `tables/trained_dynamics_stage_b_pilot_summary_by_method.csv`
  - `tables/trained_dynamics_stage_b_pilot_summary_by_domain_method.csv`
  - `reports/trained_dynamics_stage_b_pilot_report.md`
- Added learned-risk planner pilot outputs:
  - `scripts/run_learned_risk_planner_pilot.py`
  - `scripts/plot_learned_risk_pilot.py`
  - `logs/learned_risk_stage_b_pilot_results.jsonl`
  - `logs/learned_risk_stage_b_pilot_results_flat.csv`
  - `logs/learned_risk_stage_b_pilot_step_predictions.csv`
  - `logs/learned_risk_stage_b_pilot_calibration_samples.csv`
  - `configs/learned_risk_stage_b_pilot_config.json`
  - `tables/learned_risk_stage_b_pilot_summary_by_method.csv`
  - `tables/learned_risk_stage_b_pilot_summary_by_domain_method.csv`
  - `tables/learned_risk_stage_b_pilot_risk_model_selection.csv`
  - `reports/learned_risk_stage_b_pilot_report.md`
  - `figures/learned_risk_stage_b_pilot_pareto.png`
- Added closed-loop-selected learned-risk planner pilot outputs:
  - `logs/learned_risk_closedloop_stage_b_pilot_results.jsonl`
  - `logs/learned_risk_closedloop_stage_b_pilot_results_flat.csv`
  - `logs/learned_risk_closedloop_stage_b_pilot_step_predictions.csv`
  - `logs/learned_risk_closedloop_stage_b_pilot_calibration_samples.csv`
  - `configs/learned_risk_closedloop_stage_b_pilot_config.json`
  - `tables/learned_risk_closedloop_stage_b_pilot_summary_by_method.csv`
  - `tables/learned_risk_closedloop_stage_b_pilot_summary_by_domain_method.csv`
  - `tables/learned_risk_closedloop_stage_b_pilot_risk_model_selection.csv`
  - `reports/learned_risk_closedloop_stage_b_pilot_report.md`
  - `figures/learned_risk_closedloop_stage_b_pilot_pareto.png`
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
- Added executed-rollout calibration split:
  - `scripts/evaluate_executed_rollout_calibration_split.py`
  - `logs/executed_rollout_calibration_split.csv`
  - `tables/executed_rollout_calibration_selection.csv`
  - `reports/executed_rollout_calibration_split.md`
- Added shifted-calibration diagnostic:
  - `scripts/evaluate_shift_weighted_calibration.py`
  - `logs/shift_weighted_calibration.csv`
  - `reports/shift_weighted_calibration_report.md`
  - `reports/theorem_D_shift_calibration.md`
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
- `python scripts\run_trained_dynamics_stage_a.py --domains all --levels L0,L1,L2,L3 --seeds 5,6,7,8,9 --methods vanilla_mppi,robust_mpc,cvar_ra_mppi,conformal_prediction_mpc,conformal_risk_non_ccr,ccr_no_calibration,ccr_mpc,oracle_mpc --candidates 32 --calibration-contexts 32 --artifact-tag trained_dynamics_stage_b_pilot`: completed 960 trained-dynamics Stage-B pilot episodes in 858.89 seconds.
- `python scripts\run_learned_risk_planner_pilot.py`: completed 1200 learned-risk planner pilot episodes in 1755.27 seconds.
- `python scripts\plot_learned_risk_pilot.py`: wrote `figures/learned_risk_stage_b_pilot_pareto.png`.
- `python scripts\run_learned_risk_planner_pilot.py --seeds 15,16,17,18,19 --methods vanilla_mppi,cvar_ra_mppi,conformal_prediction_mpc,conformal_risk_non_ccr,ccr_mpc,learned_risk_executed_logistic,learned_risk_executed_selected,oracle_mpc --artifact-tag learned_risk_closedloop_stage_b_pilot --selected-risk-model logistic`: completed 960 closed-loop-selected learned-risk pilot episodes in 682.59 seconds.
- `python scripts\plot_learned_risk_pilot.py --artifact-tag learned_risk_closedloop_stage_b_pilot`: wrote `figures/learned_risk_closedloop_stage_b_pilot_pareto.png`.
- `python scripts\validate_risk_models.py`: wrote 18 risk-model validation rows.
- `python scripts\compare_calibration_label_sources.py`: wrote 27 calibration-label-source ablation rows.
- `python scripts\evaluate_executed_rollout_calibration_split.py`: wrote 1596 split evaluation rows and 76 validation-selected held-out rows.
- `python scripts\evaluate_shift_weighted_calibration.py`: wrote 144 shifted-calibration diagnostic rows.
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
- Trained Stage-B pilot aggregate rows:
  - Vanilla MPPI: cost 28.2276, violation 0.0199
  - CCR-MPC: cost 28.7881, violation 0.0114
  - CVaR/RA-MPPI: cost 28.2926, violation 0.0129
  - Conformal prediction MPC: cost 30.7194, violation 0.0034
  - Conformal risk non-CCR: cost 31.9752, violation 0.0042
  - Oracle MPC: cost 28.2406, violation 0.0049
- Learned-risk planner pilot aggregate rows:
  - Learned logistic risk: cost 28.3399, violation 0.0084
  - CCR-MPC: cost 28.8994, violation 0.0088
  - CVaR/RA-MPPI: cost 28.3659, violation 0.0065
  - Conformal prediction MPC: cost 36.9413, violation 0.0008
  - Vanilla MPPI: cost 28.2824, violation 0.0154
  - Validation-selected learned risk picked random forest by validation Brier, but had cost 28.3511 and violation 0.0266.
- Closed-loop-selected learned-risk pilot aggregate rows:
  - Learned selected logistic risk: cost 28.5961, violation 0.0178
  - Learned logistic risk: cost 28.6301, violation 0.0208
  - CCR-MPC: cost 29.1271, violation 0.0139
  - CVaR/RA-MPPI: cost 28.5823, violation 0.0115
  - Conformal prediction MPC: cost 37.2538, violation 0.0015
  - Vanilla MPPI: cost 28.5251, violation 0.0227
- Preliminary risk validation:
  - Focused surrogate best Brier: random forest all features, 0.0258
  - Trained Stage-A best Brier: random forest all features, 0.0460
- Calibration-label-source ablation:
  - Simulator full-candidate violation-rate label Brier: 0.0541
  - Executed-rollout step-violation label Brier: 0.1578
- Executed-rollout calibration split:
  - Alpha 0.05 held-out selected mean accept rate: 0.9811
  - Alpha 0.05 held-out accepted step-violation rate: 0.0146
  - Alpha 0.05 held-out accepted plan-failure rate: 0.2211
  - Alpha 0.10/0.15/0.20 held-out accepted step-violation rate: 0.0201
  - Alpha 0.10/0.15/0.20 held-out accepted plan-failure rate: 0.2378
  - Most selected score: `violation_tail` with 35 of 76 selected rows.
- Shift-weighted calibration diagnostic:
  - L3 shifted test all-failure rate: 0.4182
  - 85.42% of score/alpha settings reject all shifted L3 candidates.
  - For violation-rate score at alpha 0.10, severity weighting changes accept rate 0.6813 to 0.6728 and accepted failure 0.1461 to 0.1376.
- Higher-dimensional domain prototype smoke validation:
  - Cartpole safety: violation rate 1.0000 at L0-L3 under the simple validation policy, so it needs controller/domain tuning before main experiments.
  - Dynamic bicycle 4D: violation rate 0.0000 at L0-L3, likely too easy in this smoke policy.
  - Planar quadrotor 6D: violation rate 0.0000 at L0/L1 and 1.0000 at L2/L3, useful as a severity stress test.
  - Pushing contact 4D: violation rate 0.0000 at L0-L3, likely too easy in this smoke policy.

## Known Failures Or Bugs

- No verifier failures remain.
- `latexmk` could not run because MiKTeX lacks Perl; direct `pdflatex`/`bibtex` worked.
- The max-out prompt is not complete. The final max-out completion message has not been printed and must not be printed yet.
- Trained Stage-A and Stage-B pilot results are mixed and do not support broad superiority.
- Learned logistic risk integration is promising in one held-out pilot, but validation-Brier model selection failed and closed-loop-selected logistic still lost to CCR-MPC/CVaR/conformal baselines on fresh seeds 15-19.
- Higher-dimensional domains are prototypes only; they are not integrated into the main MPC runner or trained Stage-A runner.
- The executed-rollout calibration split supports step-level diagnostics only; accepted plan-failure rates remain too high for an episode-level guarantee.
- Theorem D is only a sketch plus diagnostic; the severity weight is hand-coded and often too conservative.

## Open Questions

- Whether to integrate trained dynamics into the original focused runner before Stage B: UNKNOWN.
- Whether to tune the new higher-dimensional domains first or integrate them as stress tests with current policies: UNKNOWN.
- Whether to run Stage B max-out matrix after planner/domain integration: UNKNOWN.

## Next Recommended Steps

1. Commit and push this verified continuation checkpoint.
2. Promote trained dynamics to a first-class `--model-source` option in the original runner, or keep the separate runner and integrate the higher-dimensional domain prototypes there.
3. Run a fresh Stage-B calibration/test split after planner/domain integration; do not rely only on the Stage-A split.
4. Treat learned-risk integration as explored but not solved; next improvement likely needs better calibration data collection, not only another selector.
5. Execute validation-selected baseline sweeps from `configs/baseline_sweeps.yaml`.

Safe to clear after handoff is updated.
