# Final Submission Readiness Gate

## Status

Not final-submission-ready as of 2026-07-08.

## Verified Starting Point

- `python scripts\verify_pack.py --smoke` passes with `PACK VERIFY PASSED: 0 warning(s)`.
- `paper/iclr_submission.tex` has been seeded from the bounded manuscript `paper/CCR_MPC_paper.tex`.
- `reports/final_claim_ledger.csv` has been seeded from `reports/claim_ledger.csv`.
- Theorem-specific reports A/B/C have been added as bounded proof reports; theorem D has been added only as a sketch plus shifted-calibration diagnostic.
- CPU-trained Torch MLP dynamics ensembles have been added as diagnostics.
- Trained-dynamics Stage A has been executed on D0-D5 with all 19 methods, L0-L3, and seeds 0-4.
- Preliminary risk-model validation has been generated for single-feature, logistic, isotonic, and random-forest score models.
- A calibration-label-source ablation has been generated comparing simulator full-candidate labels with executed-rollout labels.
- A held-out executed-rollout calibration split has been generated from Stage-A selected rollouts.
- Higher-dimensional CPU domain prototypes have been added and smoke-validated, but are not integrated into the main MPC result suite.
- A trained-dynamics Stage-B pilot has been executed on D0-D5, L0-L3, held-out seeds 5-9, 8 key methods, candidate budget 32, and 32 calibration contexts.
- A learned-risk planner pilot has been executed on D0-D5, L0-L3, held-out seeds 10-14, 10 methods, and candidate budget 32.
- A closed-loop-selected learned-risk pilot has been executed on D0-D5, L0-L3, held-out seeds 15-19, 8 methods, and candidate budget 32.
- The current evidence supports a bounded CPU decision-calibration paper, not a strong empirical superiority paper.

## Passing Evidence Already Present

- Runnable CPU study with 1026 closed-loop runs.
- Six simplified domains and nineteen methods/ablations.
- Tables, figures, logs, and claim ledger for the focused run.
- Honest limitations in the manuscript.
- Existing citation metadata report and related-work distinctions.
- Existing verifier checks schemas, manifest hashes, result coverage, table consistency, smoke tests, and packaging cleanliness.

## Blocking Gates

- Trained learned-dynamics ensembles are integrated into a separate Stage-A runner, but not yet into the original focused-suite runner as a first-class `--model-source` option.
- Theorem-specific reports A/B/C are present, and theorem D is a sketch/diagnostic only; all theorem reports still require human theorem review.
- Higher-dimensional CPU domain prototypes are present and smoke-validated, but not integrated into the main MPC runner or Stage-A trained-dynamics experiments.
- Expanded Stage-A trained-dynamics artifacts and a Stage-B pilot are present; full Stage B and Stage C max-out execution artifacts are not.
- The acceptance-critical result gate exists and currently rejects a broad superiority claim.
- Preliminary baseline sweep configuration and tuning summary exist, but validation-selected sweeps have not been executed.
- Learned risk models are now integrated into held-out planner pilots, including a closed-loop-selected logistic variant; the fresh closed-loop-selected pilot still does not beat CCR-MPC, CVaR/RA-MPPI, conformal risk, or conformal prediction on violation rate.
- No final citation re-audit has been performed for the max-out manuscript.
- The verifier permits the new tracked diagnostic logs and manifest-hashes the new artifacts, but it does not yet require Stage B/Stage C max-out coverage or fresh held-out calibration splits.

## Claim Posture Allowed Right Now

Allowed:

- Prediction-space uncertainty is an incomplete proxy for control risk in the current bounded suite.
- CCR-MPC improves violation rate over vanilla MPPI and uncalibrated CCR in the focused run.
- CCR-MPC improves violation rate over vanilla MPPI and uncalibrated CCR in trained-dynamics Stage A.
- CCR-MPC improves violation rate over vanilla MPPI and uncalibrated CCR in the trained-dynamics Stage-B pilot.
- The learned logistic risk planner slightly improves over CCR-MPC in the learned-risk pilot: violation 0.0084 versus 0.0088 and cost 28.3399 versus 28.8994.
- The closed-loop-selected logistic risk planner improves over vanilla MPPI on seeds 15-19: violation 0.0178 versus 0.0227.
- CCR-MPC ties the lowest aggregate violation rate tier in the focused run.
- The current evidence is CPU-reproducible and bounded.

Not allowed:

- Hardware safety.
- Broad robotics generality.
- Dominance over CVaR/RA-MPPI or conformal-prediction MPC.
- Claims that trained neural learned-dynamics results establish broad superiority.
- Claims that learned risk models are solved; Brier selection failed, and closed-loop-selected logistic still lost to stronger baselines on fresh seeds 15-19.
- Claims that the 57000-row max-out matrix was executed.

## Next Required Step

Integrate the higher-dimensional domain prototypes into the planner suite, add a fresh Stage-B executed-rollout calibration/test split, and execute validation-selected baseline sweeps before strengthening the paper. Expanded Stage-A, Stage-B pilot, learned-risk pilot, and closed-loop-selected learned-risk pilot results are mixed: CCR-MPC and learned logistic risk improve over vanilla/uncalibrated CCR in some settings, but conformal, oracle, violation-tail, and robust/CVaR-style baselines remain stronger on some aggregate safety or cost metrics.
