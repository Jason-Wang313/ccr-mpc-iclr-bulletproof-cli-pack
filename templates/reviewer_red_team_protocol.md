# Reviewer Red-Team Protocol

Run this after experiments and before polishing.

## Fatal-Rejection Simulation

Answer each question with artifact paths, not prose alone.

1. Why is this not RA-MPPI/CVaR MPPI with a new score?
2. Why is this not conformal risk control applied to a controller?
3. Why is this not ensemble variance plus a threshold?
4. Where does prediction calibration fail while CCR succeeds?
5. Does safety come from freezing, fallback, or useful decisions?
6. Which baselines received the same horizon, action-sample budget, training data, calibration data, and tuning effort?
7. What fails under the strongest OOD shift, and does the limitations section admit it?
8. Which claims would break if the exchangeability assumption fails?
9. Which citations were manually verified, and which were removed?
10. Can a reviewer reproduce the main figures from a clean checkout?

## Output

Create `reports/reviewer_red_team_report.md` with:

- fatal unresolved issues;
- high-risk wording to narrow;
- missing artifacts;
- final claims to drop;
- final claims safe to keep.
