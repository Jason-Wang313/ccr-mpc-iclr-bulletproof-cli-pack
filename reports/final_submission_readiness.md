# Final Submission Readiness Gate

## Status

Not final-submission-ready as of 2026-07-07.

## Verified Starting Point

- `python scripts\verify_pack.py --smoke` passes with `PACK VERIFY PASSED: 0 warning(s)`.
- `paper/iclr_submission.tex` has been seeded from the bounded manuscript `paper/CCR_MPC_paper.tex`.
- `reports/final_claim_ledger.csv` has been seeded from `reports/claim_ledger.csv`.
- Theorem-specific reports A/B/C have been added as bounded proof reports.
- CPU-trained Torch MLP dynamics ensembles have been added as diagnostics.
- Trained-dynamics Stage A has been executed on D0/D1 with all 19 methods, L0-L2, and seeds 0-4.
- Preliminary risk-model validation has been generated for single-feature, logistic, isotonic, and random-forest score models.
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
- Theorem-specific reports A/B/C are present, but theorem D is not implemented and A/B/C still require human theorem review.
- No high-fidelity or higher-dimensional upgraded domains are present.
- Stage-A trained-dynamics artifacts are present; Stage B and Stage C max-out execution artifacts are not.
- The acceptance-critical result gate exists and currently rejects a broad superiority claim.
- Preliminary baseline sweep configuration and tuning summary exist, but validation-selected sweeps have not been executed.
- Learned risk models are validated diagnostically, but not yet integrated into the planner or tested on held-out Stage B/C runs.
- No final citation re-audit has been performed for the max-out manuscript.
- No updated verifier enforces the new max-out artifacts.

## Claim Posture Allowed Right Now

Allowed:

- Prediction-space uncertainty is an incomplete proxy for control risk in the current bounded suite.
- CCR-MPC improves violation rate over vanilla MPPI and uncalibrated CCR in the focused run.
- CCR-MPC improves violation rate over vanilla MPPI and uncalibrated CCR in trained-dynamics Stage A.
- CCR-MPC ties the lowest aggregate violation rate tier in the focused run.
- The current evidence is CPU-reproducible and bounded.

Not allowed:

- Hardware safety.
- Broad robotics generality.
- Dominance over CVaR/RA-MPPI or conformal-prediction MPC.
- Claims that trained neural learned-dynamics results establish broad superiority.
- Claims that the 57000-row max-out matrix was executed.

## Next Required Step

Expand the trained-dynamics runner beyond D0/D1, add executed-rollout calibration, and execute validation-selected baseline sweeps before strengthening the paper. Stage-A results are mixed: CCR-MPC improves over vanilla/uncalibrated CCR, but conformal and robust baselines remain stronger on some aggregate metrics.
