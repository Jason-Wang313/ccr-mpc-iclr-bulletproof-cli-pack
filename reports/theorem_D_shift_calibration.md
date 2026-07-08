# Theorem D Shift Calibration

## Status

Sketch and diagnostic only. Do not cite this as a final theorem without human proof review.

## Proposition Sketch

Let calibration examples be exchangeable after reweighting by a nonnegative severity or density-ratio proxy. For a finite threshold class, a weighted empirical risk constraint can select the largest accepted-score threshold whose weighted calibration failure rate is at most alpha. Under correct or bounded-error weights, the target-shift failure estimate concentrates around the weighted empirical estimate up to finite-sample and weight-misspecification terms.

## What This Gives

- A formal path for severity-weighted CCR threshold selection under known shift proxies.
- A diagnostic experiment in `logs/shift_weighted_calibration.csv` comparing unweighted and severity-weighted thresholds.

## What This Does Not Give

- No guarantee under arbitrary online shift.
- No proof that the hand-coded severity proxy equals a density ratio.
- No replacement for held-out Stage-B/Stage-C calibration tests.
