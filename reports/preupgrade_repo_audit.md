# CCR-MPC Pre-Upgrade Repository Audit

## Audit Date

2026-07-07

## Current Goal

Execute the local `FINAL_AGENT_PROMPT_CCR_MPC_ICLR_MAXOUT.md` brief as an honest upgrade path from the existing bounded CPU package toward a stronger ICLR submission package.

## Repository State Verified

- Repository: `https://github.com/Jason-Wang313/ccr-mpc-iclr-bulletproof-cli-pack`
- Local path: `C:\Users\wangz\Downloads\ccr_mpc_iclr_bulletproof_cli_pack`
- Branch status before this audit: `main...origin/main`, clean and already up to date.
- Baseline verifier command: `python scripts\verify_pack.py --smoke`
- Baseline verifier result: `PACK VERIFY PASSED: 0 warning(s)`.
- Existing manuscript: `paper/CCR_MPC_paper.tex`
- Existing PDF: `paper/CCR_MPC_paper.pdf`
- Existing claim ledger: `reports/claim_ledger.csv`
- Existing manifest: `reports/final_artifact_manifest.json`

## Current Run Scope

Verified from `configs/execution_config.json`, `reports/experiment_results_summary.md`, and `paper/CCR_MPC_paper.tex`:

- Closed-loop runs: 1026
- Planning-step predictions: 20862
- Domains: 6 simplified CPU domains
- Methods/ablations: 19
- Seeds: 0,1,2
- OOD levels: L0,L1,L2
- Candidate budget: 32
- Dynamics particles: 7 unless method-specific
- Calibration contexts: 36 per domain/OOD pair
- Target risk: alpha = 0.15
- Focused run time reported by artifact: 216.9 seconds

## Exact Existing Limitations

The current paper already states the following material limitations:

- Experiments are simplified low-dimensional CPU surrogates, not high-fidelity robot simulation or hardware.
- Dynamics particles are synthetic learned-model surrogates, not neural dynamics models trained from raw robot data.
- Theory is limited to a stylized one-step separation, finite-threshold split calibration, and sampled accepted-candidate optimality.
- The exchangeability assumption for calibration is fragile under online distribution shift.
- The focused run is 1026 closed-loop runs, not the full 57000-row max-out matrix.
- CCR-MPC ties the lowest aggregate violation tier but does not dominate CVaR/RA-MPPI or conformal-prediction MPC in cost.

## Current Strongest Baselines

Verified from `tables/summary_by_method.csv`:

- `cvar_ra_mppi`: violation rate 0.0042087542, cost 28.6502721
- `conformal_prediction_mpc`: violation rate 0.0042087542, cost 29.6708674
- `robust_mpc`: violation rate 0.0050505051, cost 28.6856717
- `oracle_mpc`: cost 28.5380544, violation rate 0.0062663674
- `conformal_risk_non_ccr`: cost 28.5487710, violation rate 0.0050505051

CCR-MPC verified row:

- `ccr_mpc`: violation rate 0.0042087542, cost 29.4113151

## Claims Too Weak For Strong ICLR Acceptance

- The current empirical claim is bounded to simplified CPU settings.
- The current dynamics evidence does not show trained learned-dynamics ensembles.
- The current theorem package is useful but narrow and still needs human theorem review.
- The current method comparison shows safety improvement over vanilla and some ablations, but not clear Pareto dominance over the strongest risk-aware/conformal baselines.
- The current max-out matrix exists as a plan but has not been executed.

## Missing Max-Out Artifacts At Phase-0 Start

At the start of this execution, the local repo did not contain verified artifacts for:

- `reports/theorem_A_separation.md`
- `reports/theorem_B_calibration.md`
- `reports/theorem_C_safe_cost.md`
- `reports/theorem_D_shift_calibration.md`
- `models/` or `artifacts/models/` trained learned-dynamics ensembles
- `reports/dynamics_training_report.md`
- `logs/dynamics_prediction_metrics.csv`
- `figures/prediction_calibration_vs_control_risk.*`
- Higher-fidelity 4D dynamic bicycle, 6D planar quadrotor, and richer contact-pushing domains
- Risk-estimator validation table `logs/risk_model_validation.csv`
- `reports/ccr_score_design_report.md`
- `configs/baseline_sweeps.yaml`
- `tables/baseline_tuning_summary.csv`
- Full Stage B or Stage C max-out execution over the requested factors
- `reports/acceptance_critical_result_gate.md`
- `reports/final_submission_readiness.md` beyond this Phase-0 gate
- `reports/final_claim_ledger.csv` beyond the copied bounded-claim seed
- `paper/iclr_submission.pdf` beyond the seeded bounded manuscript

## Artifacts Added During This Execution

- `paper/iclr_submission.tex`
- `paper/iclr_submission.pdf`
- `reports/final_claim_ledger.csv`
- `reports/final_submission_readiness.md`
- `reports/preupgrade_repo_audit.md`
- `reports/theorem_A_separation.md`
- `reports/theorem_B_calibration.md`
- `reports/theorem_C_safe_cost.md`
- `reports/acceptance_critical_result_gate.md`
- `scripts/train_learned_dynamics_cpu.py`
- `artifacts/models/*_torch_mlp_ensemble.pt`
- `artifacts/models/training_summary.json`
- `logs/dynamics_prediction_metrics.csv`
- `reports/dynamics_training_report.md`
- `figures/prediction_calibration_vs_control_risk.png`
- `figures/theorem_separation_visualization.png`
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
- `configs/baseline_sweeps.yaml`
- `tables/baseline_tuning_summary.csv`
- `reports/baseline_fairness_report.md`
- `reports/ccr_score_design_report.md`
- `scripts/validate_risk_models.py`
- `logs/risk_model_validation.csv`
- `reports/risk_model_validation_report.md`
- `scripts/compare_calibration_label_sources.py`
- `logs/calibration_label_source_ablation.csv`
- `reports/calibration_label_source_ablation.md`
- `src/domains/high_dimensional.py`
- `scripts/validate_domain_upgrades.py`
- `logs/domain_validation_metrics.csv`
- `reports/domain_validation_report.md`
- `figures/domain_schematic_cartpole_safety.png`
- `figures/domain_schematic_dynamic_bicycle_4d.png`
- `figures/domain_schematic_planar_quadrotor_6d.png`
- `figures/domain_schematic_pushing_contact_4d.png`

## Still Missing After This Execution

- Trained learned-dynamics ensembles are integrated into a separate Stage-A runner, but not yet into the original focused-suite runner as a first-class model-source option.
- The theorem-specific reports still require human theorem review.
- No optional theorem D weighted/adaptive shift-calibration proof or experiment has been implemented.
- Higher-dimensional CPU domain prototypes now exist and pass smoke validation, but they are not integrated into the main MPC result suite or trained Stage-A experiments.
- Risk-estimator validation exists as a preliminary calibration diagnostic, but learned risk models are not yet integrated into the planner.
- Full validation-selected baseline sweeps remain missing.
- A calibration-label source ablation exists, but a dedicated executed-rollout calibration split before held-out testing remains missing.
- Full Stage B or Stage C max-out execution remains missing.
- `paper/iclr_submission.tex` remains a seeded bounded manuscript rather than a rewritten max-out submission.

## Plan To Close Each Gap

1. Theory: split the existing `theory_moat_report.md` into theorem-specific reports, strengthen assumptions and proof statements, and downgrade any incomplete proof to proposition/sketch.
2. Learned dynamics: implement CPU training data generation plus bootstrapped model fitting; prefer PyTorch CPU if present, otherwise use sklearn or NumPy fallback.
3. Domains: replace current two-state surrogates with verified state definitions for D1-D4 while preserving the old surrogates as regression tests.
4. CCR score: add calibrated/logistic/isotonic/tree-based risk estimators when dependencies are available; compare them against single-feature scores.
5. Calibration: separate executed-rollout calibration from simulator-oracle candidate labels and report both.
6. Baselines: add a sweep config, tuned ranges, and a baseline fairness report; keep any baseline wins visible.
7. Experiments: run Stage A first, then a bounded Stage B subset, then record any skipped max-out rows explicitly.
8. Result gate: write `acceptance_critical_result_gate.md` before strengthening manuscript claims.
9. Citations: reverify related work from primary sources before final writing.
10. Manuscript: only upgrade `paper/iclr_submission.tex` after evidence exists; until then it remains a seeded bounded draft.

## Current Phase-0 Decision

The repository is clean and verified as a bounded CPU package plus new Phase-1/Phase-2 diagnostic, Stage-A trained-dynamics, and higher-dimensional domain-prototype artifacts. It is not yet a max-out ICLR submission package. The final completion message from `FINAL_AGENT_PROMPT_CCR_MPC_ICLR_MAXOUT.md` must not be printed until broader trained-dynamics integration, main-runner domain integration, executed-rollout calibration, validation-selected baseline sweeps, max-out experiment artifacts, citation audit, claim ledger, final PDF, and an updated verifier all pass.
