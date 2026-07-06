# CCR-MPC ICLR Readiness Gate Report

Complete this file before creating `reports/ICLR_CCR_MPC_COMPLETE.md`.

## Gate 1: Claim Ledger

- [ ] `reports/claim_ledger.csv` exists.
- [ ] Every abstract/introduction headline claim has a row.
- [ ] Every result claim points to logs, tables, figures, and configs.
- [ ] Every efficiency/scalability claim includes hardware, wall-clock, samples, seeds, and implementation caveats.
- [ ] Every broad wording choice is narrowed to the tested scope.

## Gate 2: Theory

- [ ] Separation theorem has assumptions, construction, proof sketch, and synthetic experiment mapping.
- [ ] Finite-sample calibration theorem states exchangeability or weighted-shift assumptions.
- [ ] Safe-cost optimality theorem states sampled-candidate and calibration-error terms.
- [ ] Any skipped theorem is explicitly labeled as future work or removed from claims.

## Gate 3: Experiments

- [ ] D0 synthetic separation validates the negative result.
- [ ] D1-D4 CPU domains have logs, plots, seeds, and confidence intervals.
- [ ] D5 secondary planner shows the CCR layer is not MPPI-only.
- [ ] Every required baseline has a fair tuning range and equal budget where applicable.
- [ ] OOD severity, calibration size, horizon, ensemble size, and alpha sweeps are present.

## Gate 4: Calibration And Safety

- [ ] Reliability diagrams, ECE, Brier, log loss, observed risk, and target risk are reported.
- [ ] Freezing/fallback rates are reported so safety is not hiding useless conservatism.
- [ ] Failure-mode breakdown ties limitations to observed failures.

## Gate 5: Related Work And Citations

- [ ] RA-MPPI/CVaR MPPI, chance-constrained MPC, conformal risk/decision/planning, robust/safe MPC, OOD fallback, domain randomization, and sysID/adaptation are addressed.
- [ ] All citation metadata is verified from primary sources.
- [ ] No generated or guessed citation remains.

## Gate 6: Reproducibility

- [ ] `scripts/verify_pack.py --smoke` passes.
- [ ] `scripts/run_minimal.sh`, `scripts/run_full_cpu.sh`, and `scripts/reproduce_main_figures.sh` exist in the completed implementation.
- [ ] `reports/final_artifact_manifest.json` lists hashes for code, configs, logs, plots, paper, reports, and claim ledger.

## Decision

- [ ] Ready to print the completion message.
- [ ] Not ready: list blocking gaps below.
