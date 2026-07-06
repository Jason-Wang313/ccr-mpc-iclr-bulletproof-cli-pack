# Prior-Work Distinction Report

This bounded execution now includes `paper/references.bib` and `reports/citation_verification.md`. Before external submission, re-export BibTeX from publisher pages where available and check capitalization against the target venue style.

## Risk-Aware MPPI / CVaR MPPI

The implemented `cvar_ra_mppi` baseline optimizes an upper-tail cost/violation objective. CCR-MPC differs by scoring whether plausible learned dynamics particles change the planner-level regret, violation tail, rank, and first action, then calibrating that score to observed failures.

## Conformal Risk / Decision / Prediction Baselines

The implemented conformal baselines calibrate non-CCR scores: predicted violation rate, prediction uncertainty, margin tails, and rank instability. The paper should claim only the bounded distinction supported by artifacts: CCR-MPC improves over vanilla and uncalibrated CCR, while conformal prediction and non-CCR conformal risk remain strong alternatives in the focused suite.

## Robust MPC And Domain Randomization

The robust and domain-randomized baselines use more conservative model sets or worst-case objectives. CCR-MPC is positioned as a decision-risk filter over sampled candidates, not as a replacement for robust control in all settings.

## System Identification

The `sysid_mpc` baseline receives a partially shifted model center. This is a simplified adaptation proxy, not a full online identification method.

## Scope Guard

Do not claim first safe MPC, first conformal planning, first risk-aware MPPI, or foundation dynamics models.
