# Final Submission Readiness Gate

## Status

Not final-submission-ready as of 2026-07-07.

## Verified Starting Point

- `python scripts\verify_pack.py --smoke` passes with `PACK VERIFY PASSED: 0 warning(s)`.
- `paper/iclr_submission.tex` has been seeded from the bounded manuscript `paper/CCR_MPC_paper.tex`.
- `reports/final_claim_ledger.csv` has been seeded from `reports/claim_ledger.csv`.
- Theorem-specific reports A/B/C have been added as bounded proof reports.
- CPU-trained Torch MLP dynamics ensembles have been added as diagnostics.
- The current evidence supports a bounded CPU decision-calibration paper, not a strong empirical superiority paper.

## Passing Evidence Already Present

- Runnable CPU study with 1026 closed-loop runs.
- Six simplified domains and nineteen methods/ablations.
- Tables, figures, logs, and claim ledger for the focused run.
- Honest limitations in the manuscript.
- Existing citation metadata report and related-work distinctions.
- Existing verifier checks schemas, manifest hashes, result coverage, table consistency, smoke tests, and packaging cleanliness.

## Blocking Gates

- Trained learned-dynamics ensemble artifacts are present, but they are not yet integrated into the MPC experiment runner.
- Theorem-specific reports A/B/C are present, but theorem D is not implemented and A/B/C still require human theorem review.
- No high-fidelity or higher-dimensional upgraded domains are present.
- No Stage B or Stage C max-out execution artifacts are present.
- The acceptance-critical result gate exists and currently rejects a broad superiority claim.
- No verified baseline sweep configuration or tuning summary exists yet.
- No final citation re-audit has been performed for the max-out manuscript.
- No updated verifier enforces the new max-out artifacts.

## Claim Posture Allowed Right Now

Allowed:

- Prediction-space uncertainty is an incomplete proxy for control risk in the current bounded suite.
- CCR-MPC improves violation rate over vanilla MPPI and uncalibrated CCR in the focused run.
- CCR-MPC ties the lowest aggregate violation rate tier in the focused run.
- The current evidence is CPU-reproducible and bounded.

Not allowed:

- Hardware safety.
- Broad robotics generality.
- Dominance over CVaR/RA-MPPI or conformal-prediction MPC.
- Claims about trained neural learned-dynamics ensembles.
- Claims that the 57000-row max-out matrix was executed.

## Next Required Step

Implement the Phase-1/Phase-2 evidence path before strengthening the paper: theorem-specific reports plus trained learned-dynamics data/model/metrics artifacts. The seeded submission branch should remain conservative until those artifacts exist.
