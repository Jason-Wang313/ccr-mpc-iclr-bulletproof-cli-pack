# CCR-MPC Paper Artifact Index

The primary manuscript is now the compiled LaTeX paper:

- `paper/CCR_MPC_paper.tex`
- `paper/CCR_MPC_paper.pdf`
- `paper/references.bib`

## Bounded Abstract

Across 6 simplified CPU domains, 19 methods/ablations, three OOD levels, and seeds 0,1,2, CCR-MPC reduced mean closed-loop violation rate from 1.1% for vanilla MPPI to 0.4%, with mean cost 29.411 versus 28.474 for vanilla and 28.538 for oracle MPC. CCR-MPC tied the lowest aggregate violation rate in this suite but did not dominate CVaR/RA-MPPI or conformal-prediction MPC in cost. The supported claim is bounded: calibrated counterfactual decision-risk features can improve safety over vanilla and uncalibrated learned-dynamics MPC in these simplified sampled-planning settings.

## Main Evidence

- `tables/summary_by_method.csv`
- `figures/safety_performance_pareto.png`
- `figures/ccr_ablation_bars.png`
- `reports/claim_ledger.csv`
- `reports/citation_verification.md`

## Non-Negotiable Scope

The experiments are low-dimensional CPU surrogates. The theory covers a stylized one-step separation, finite-threshold split calibration, and optimality over sampled accepted candidates, not broad robot safety. Calibration assumes candidate-context exchangeability within the simplified simulator family. The system-ID baseline is a proxy, not a full adaptive identification method. The current run does not include high-fidelity contact simulation, real robots, or a complete 57,000-row max-out matrix.
