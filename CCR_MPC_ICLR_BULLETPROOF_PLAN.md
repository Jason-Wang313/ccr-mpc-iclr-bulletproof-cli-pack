# Counterfactual Control Risk ICLR Bulletproof Execution Pack

Date: 2026-07-06

Final committed paper direction:

# Prediction Uncertainty Is Not Control Risk:
## Counterfactual Risk Calibration for Learned-Dynamics MPC

Short name: **CCR-MPC** / **CCR-MPPI**

This is a **theory-first, CPU-reproducible ICLR plan**, not a robot-paper plan.

Main thesis:
> Learned dynamics can be prediction-calibrated yet decision-unsafe. We define counterfactual control risk (CCR): planner-level regret/violation instability across plausible learned dynamics models. We calibrate CCR to observed closed-loop failure risk and use it inside MPC/MPPI to make safer decisions under dynamics shift without becoming blindly conservative.

## What the CLI agent must do

1. Read `CLI_AGENT_MASTER_PROMPT.md`.
2. Run the pack verifier before editing:

```powershell
.\scripts\run_pack_checks.ps1
```

or:

```bash
bash scripts/run_pack_checks.sh
```

3. Execute phases in `tasks.yaml` order.
4. Maintain `reports/claim_ledger.csv` from `templates/claim_ledger.csv`.
5. Finish all non-hardware deliverables:
   - bounded theory statements/proofs under stated assumptions
   - synthetic separation experiments
   - CCR-MPC/CCR-MPPI implementation
   - all baselines
   - bounded focused CPU experiment suite plus max-out matrix
   - calibration/risk/evaluation scripts
   - plot generation
   - paper manuscript
   - related-work audit
   - reviewer-defense matrix
   - reproducibility package
6. Create:
   - `reports/ICLR_CCR_MPC_COMPLETE.md`
   - `reports/final_artifact_manifest.json`
7. Print exactly:

```text
ICLR CCR-MPC COMPLETE: bounded theory proofs, counterfactual-risk algorithms, calibration code, CPU experiment suite, baselines, ablations, plots, paper manuscript, related-work audit, and reviewer-defense reports are finished. All claims are backed by generated artifacts. Human review is required before submission.
```

## Core rule

Do not claim "foundation dynamics models" unless the experiments actually include a broad/generalist dynamics model. The safe title uses **learned dynamics models**, not "foundation dynamics models".

## Completion gate

The completion message is forbidden until:

- `scripts/verify_pack.py --smoke` passes;
- every required report in `tasks.yaml` exists under `reports/`;
- `reports/final_artifact_manifest.json` validates against `schemas/artifact_manifest_schema.json`;
- every headline paper claim has a row in `reports/claim_ledger.csv`;
- all citations and related-work claims are verified from primary sources.

## Main files

- `COUNTERFACTUAL_CONTROL_RISK_MASTER_PLAN.md`: full plan.
- `CLI_AGENT_MASTER_PROMPT.md`: paste this into the CLI agent.
- `THEORY_MOAT_PLAN.md`: proof strategy and theorem checklist.
- `EXPERIMENT_MAXOUT_PLAN.md`: every experiment required.
- `REVIEWER_ATTACK_CLOSURE_MATRIX.md`: attack -> defense -> artifact.
- `PRIOR_WORK_DISTINCTION_MEMO.md`: how to distinguish from RA-MPPI, conformal risk, conformal decision, safe MPC, etc.
- `BASELINES_ABLATIONS_CHECKLIST.md`: all baselines and ablations.
- `matrices/experiment_matrix_maxout.csv`: maxed CPU experiment grid.
- `tasks.yaml`: machine-readable execution graph.
- `schemas/*.json`: result logging schemas.
- `skeleton/*.py`: pseudocode/skeletons for agent implementation.
- `scripts/verify_pack.py`: structural verifier and smoke-test entrypoint.
- `scripts/run_pack_checks.ps1` / `scripts/run_pack_checks.sh`: cross-platform check wrappers.
- `templates/claim_ledger.csv`: claim-to-artifact ledger required before completion.
- `templates/readiness_gate_report.md`: final reviewer-risk gate before completion.


---

# CLI Agent Master Prompt: ICLR CCR-MPC Bulletproof Plan

You are a CLI research/coding agent executing the ICLR paper plan:

# Prediction Uncertainty Is Not Control Risk:
## Counterfactual Risk Calibration for Learned-Dynamics MPC

Short name: CCR-MPC / CCR-MPPI.

## Mission

Build a theory-first, CPU-reproducible ICLR submission package.

The paper must prove and demonstrate:
1. Prediction calibration/uncertainty does not imply closed-loop control-risk calibration.
2. Counterfactual control risk (CCR) is a planner-level risk score based on regret/violation instability across plausible learned dynamics models.
3. CCR can be calibrated to observed closed-loop violation/failure risk.
4. CCR-MPC/CCR-MPPI improves safety-performance tradeoffs under dynamics shift compared with hard baselines.
5. Experiments are broad enough to make the result non-toy without requiring GPU.

## First commands

Before implementing, run:

```bash
python scripts/verify_pack.py --smoke
```

On Windows PowerShell, this wrapper is available:

```powershell
.\scripts\run_pack_checks.ps1
```

Treat verifier failures as blockers unless they are explicitly about the absence
of completed experiment reports.

## Completion protocol

When all non-hardware jobs are done:
1. Create `reports/claim_ledger.csv` from `templates/claim_ledger.csv`.
2. Create `reports/readiness_gate_report.md` from `templates/readiness_gate_report.md`.
3. Create `reports/ICLR_CCR_MPC_COMPLETE.md`.
4. Create `reports/final_artifact_manifest.json`.
5. Run `python scripts/verify_pack.py --smoke`.
6. Print exactly:

ICLR CCR-MPC COMPLETE: bounded theory proofs, counterfactual-risk algorithms, calibration code, CPU experiment suite, baselines, ablations, plots, paper manuscript, related-work audit, and reviewer-defense reports are finished. All claims are backed by generated artifacts. Human review is required before submission.

Then stop.

## Forbidden

- Do not claim foundation dynamics models unless actually implemented.
- Do not compare to large GPU-heavy methods unless a fair baseline is run or explicitly scoped as not comparable.
- Do not hide conformal risk control, conformal decision theory, RA-MPPI, chance-constrained MPPI, uncertainty-aware MPC, safe MPC, SODA-like fallback, or domain randomization.
- Do not make the paper look like "ensemble variance + conformal threshold".
- Do not report only reward.
- Do not generate fake citations.
- Do not mark work complete without generated plots/tables/logs.
- Do not keep a claim unless it has an artifact row in `reports/claim_ledger.csv`.
- Do not leave metric-name drift between CSV configs, JSON logs, plots, and tables.

## Required artifacts

Theory:
- theorem statements
- bounded proofs under stated assumptions
- synthetic construction demonstrating separation
- assumptions and limitations

Code:
- dynamics ensemble/particles
- planner implementations: MPPI main, CEM-MPC secondary
- CCR score computation
- calibration layer
- risk-aware planner
- baselines
- experiment runner
- logging/metrics/plots

Experiments:
- synthetic separation system
- classic constrained control systems
- kinematic/dynamic car
- planar quadrotor
- quasi-static pushing/contact
- secondary planner generality
- ablations
- OOD severity sweeps
- calibration sample-size sweeps
- seed/confidence interval analysis

Paper:
- ICLR-style abstract
- introduction
- related work
- theorem section
- method
- experiments
- limitations
- reviewer attack closure appendix

Evidence ledger:
- every headline claim
- exact evidence artifact paths
- tested scope and compute budget
- strongest alternative explanation
- limitation or narrowed wording


---

# Prediction Uncertainty Is Not Control Risk
## Counterfactual Risk Calibration for Learned-Dynamics MPC

Short name: CCR-MPC / CCR-MPPI.

## Final paper identity

This is not a "controller tuning" paper. It is a decision-calibration paper for learned-dynamics control.

Main claim:
> Prediction-space uncertainty is not the object that controllers need. A planner needs decision-space risk: whether plausible learned dynamics models would make it choose a different, high-regret, or violating action.

## Abstract target

Learned dynamics models are often evaluated by prediction error or prediction calibration, but closed-loop control decisions depend on how model uncertainty changes the planner's selected action. We show theoretically and empirically that prediction calibration does not imply control-risk calibration. We introduce counterfactual control risk (CCR), a planner-level score measuring regret and violation instability across plausible learned dynamics models. We calibrate this score using finite-sample risk-control tools and integrate it into MPC/MPPI to choose actions that are low-risk under dynamics uncertainty without becoming uniformly conservative. Across synthetic systems, classic constrained control, vehicle dynamics, planar quadrotors, and contact-rich pushing, CCR-MPC controls observed violation rates under dynamics shift while preserving task performance better than raw uncertainty penalties, risk-aware MPPI, conformal prediction/planning baselines, conservative MPC, domain randomization, and system-ID baselines.

## Why this is ICLR-shaped

The paper contributes:
1. a negative theory result about prediction calibration vs control-risk calibration;
2. a new decision-risk statistic: counterfactual control regret;
3. finite-sample calibration/coverage guarantee for closed-loop risk;
4. a general MPC/MPPI instantiation;
5. broad CPU-reproducible experiments.

The ML object is not "a robot controller"; it is calibrated decision-making with learned dynamics models.

## Core definitions

### Plausible dynamics set

`F = {f_1, ..., f_K}` from:
- bootstrapped ensembles
- dropout particles
- posterior samples
- perturbed learned models
- local residual models
- OOD-shifted model particles in synthetic tests

### Planner candidate set

For each state `x_t`, sample action sequences:
`U = {u_1, ..., u_N}`.

Evaluate each `u_j` under each `f_i`:
`J_i(u_j)` and `Violation_i(u_j)`.

### Counterfactual control regret

For each model particle `f_i`, define:
`u_i* = argmin_{u in U} J_i(u)`.

Regret matrix:
`R_ij = J_i(u_j) - J_i(u_i*)`.

Candidate CCR score for candidate `u_j`:
- quantile over i of `R_ij`;
- CVaR over i of `R_ij`;
- violation rate over i;
- action-rank instability;
- first-action disagreement;
- constraint-margin tail.

### Calibrated CCR

Use calibration data from closed-loop rollouts:
features -> observed violation/task failure.

Calibrate CCR scores to target risk alpha:
- conformal/risk-control thresholding
- split calibration
- weighted/adaptive calibration for shift
- bootstrap uncertainty estimates

### CCR-MPC / CCR-MPPI

Modify MPC/MPPI:
1. sample candidate sequences;
2. evaluate under dynamics particles;
3. compute CCR features;
4. apply calibrated risk threshold or penalty;
5. select low-cost action among risk-acceptable candidates;
6. fallback if no acceptable candidate exists;
7. optionally update calibration online.

## Required theory

### Theorem 1: separation theorem

Prediction calibration / low one-step error does not imply low control risk.

Construct a low-dimensional constrained system where two learned models have identical or arbitrarily close prediction error/calibration on a data distribution but induce arbitrarily different MPC decisions and violation risk.

### Theorem 2: finite-sample CCR risk guarantee

Given exchangeable calibration rollouts and monotone violation loss, calibrated CCR threshold controls future violation frequency at level alpha plus finite-sample term.

### Theorem 3: safe-cost optimality

Among sampled candidate sequences satisfying the calibrated risk constraint, CCR-MPC selects a trajectory whose cost is close to the best low-risk sampled trajectory up to sampling/calibration error.

### Optional Theorem 4: shifted/weighted calibration

Under weighted exchangeability or bounded density-ratio shift, weighted CCR calibration controls target-domain risk.

## Required experimental conclusion

Main message:
> Prediction uncertainty and prediction calibration fail as proxies for closed-loop control risk. CCR provides a better calibrated decision-risk signal and improves safety-performance tradeoffs.

## Required domains

Minimum:
1. synthetic separation system
2. constrained classic control
3. dynamic bicycle / agile car
4. planar quadrotor
5. quasi-static pushing/contact

Optional if time:
6. simple locomotion/point-foot system
7. dynamic obstacle environment
8. noisy state-estimation system

## Required baselines

1. Vanilla MPPI/MPC
2. conservative/robust MPC
3. raw ensemble uncertainty penalty
4. prediction-calibrated uncertainty penalty
5. CVaR / RA-MPPI-style baseline
6. chance-constrained MPC-style baseline
7. conformal prediction-set MPC
8. conformal risk control with non-CCR score
9. conformal decision/planning baseline
10. SODA-like OOD detector + fallback
11. domain-randomized learned dynamics + MPC
12. system-ID/adaptation + MPC
13. oracle dynamics + MPC
14. CCR without calibration
15. calibration without counterfactual regret
16. planner disagreement only
17. regret only without violation features

## Required plots

1. prediction error vs control risk scatter
2. prediction calibration vs decision calibration
3. risk calibration reliability diagram
4. safety-performance Pareto
5. OOD severity curves
6. calibration set size curves
7. ensemble size sensitivity
8. horizon length sensitivity
9. compute time per step
10. ablation bar charts
11. failure mode breakdown
12. synthetic theorem visualization

## Required writing posture

Do not claim:
- first risk-aware MPC
- first conformal planning
- first learned MPC
- first safe MPC
- foundation dynamics models unless implemented

Do claim:
- prediction uncertainty is not control risk;
- CCR is a planner-level decision-risk statistic;
- finite-sample calibration makes the risk layer principled;
- CCR-MPC improves risk-performance tradeoffs in learned-dynamics MPC under shift.

## Success bar

Weak version = reject:
- no theorem;
- two toy experiments;
- only vanilla baselines;
- looks like ensemble penalty plus conformal threshold.

Strong version = plausible strong accept:
- separation theorem;
- finite-sample calibration theorem;
- broad CPU domains;
- hard prior-work baselines;
- exact calibration metrics;
- reproducible code and logs;
- clean writing.


---

# Theory Moat Plan

## Goal

Make the paper impossible to dismiss as a heuristic uncertainty penalty.

## Theorem 1: Separation of Prediction Calibration and Control-Risk Calibration

### Statement target

There exists a constrained dynamical system, a data distribution, and two learned models `f_a`, `f_b` such that:

1. `f_a` and `f_b` have identical or arbitrarily close one-step prediction error on the data distribution.
2. `f_a` and `f_b` have identical or arbitrarily close prediction calibration under standard prediction metrics.
3. When embedded in MPC with the same cost/constraint and horizon, they induce different first actions.
4. The closed-loop violation probability under one induced policy can be arbitrarily larger than under the other.

### Construction sketch

Use a low-dimensional state with a constraint boundary. Put most data mass away from the decision boundary, so prediction error/calibration are dominated by harmless regions. Construct a small model mismatch near the boundary that flips the MPC argmin. The flipped action crosses a safety boundary with high probability.

### Artifact required

- formal theorem statement
- proof
- plot of system and decision boundary
- synthetic experiment exactly matching theorem

## Theorem 2: Finite-Sample CCR Calibration

### Statement target

Given calibration rollouts `(S_i, L_i)`, where `S_i` is CCR score of selected planned trajectory and `L_i` is observed violation/task-failure loss, choose a threshold or risk mapping by split calibration. Under exchangeability:

`Pr(observed violation of future selected plan) <= alpha + finite_sample_term`

or expected monotone loss is controlled at level alpha.

### Important

If directly using Conformal Risk Control, cite it and state that the novelty is the CCR score, not the generic calibration machinery.

### Artifact required

- theorem statement
- proof with assumptions
- empirical coverage validation

## Theorem 3: Safe-Cost Optimality Among Sampled Rollouts

### Statement target

Let `U_safe` be candidate action sequences satisfying the calibrated risk constraint. CCR-MPC selects a sequence with cost within epsilon of the best sampled risk-acceptable sequence, where epsilon is due to sampling, score estimation, and calibration error.

### Artifact required

- theorem statement
- proof
- empirical safety-performance Pareto showing not just conservative

## Optional Theorem 4: Weighted Shift Calibration

### Statement target

Under bounded density ratio or weighted exchangeability, weighted CCR calibration controls target-domain violation risk.

### Artifact required

- theorem statement
- proof sketch
- OOD severity experiment with and without weighting

## Theory quality checklist

- Define all random variables.
- Make clear what is calibrated: closed-loop violation/failure, not prediction residual.
- Do not overclaim global nonlinear control safety.
- Separate open-loop rollout risk from receding-horizon closed-loop risk.
- State limitations of exchangeability assumptions.


---

# Experiment Max-Out Plan

## Principle

No GPU is acceptable only if the paper wins through theory, controlled experiments, and broad CPU-reproducible evidence.

## Domains

### D0: synthetic separation system

Purpose:
- visualize and validate Theorem 1.

Required:
- two learned models with similar prediction error/calibration;
- different MPC actions near boundary;
- failure of raw uncertainty;
- success of CCR.

### D1: classic constrained control

Systems:
- double integrator with obstacle/constraint;
- pendulum with safety envelope;
- cartpole with angle/position constraint;
- acrobot with unsafe region.

OOD shifts:
- mass/length/friction;
- actuator gain;
- latency;
- noise.

### D2: dynamic bicycle/agile car

Tasks:
- lane keeping;
- track following;
- obstacle avoidance;
- aggressive cornering.

Shifts:
- friction coefficient;
- steering bias;
- actuator latency;
- payload/mass;
- sensor noise;
- speed cap.

### D3: planar quadrotor

Tasks:
- waypoint tracking;
- obstacle avoidance;
- narrow passage;
- landing/tracking under disturbance.

Shifts:
- wind;
- payload;
- motor strength;
- latency;
- mass/battery variation;
- sensor noise.

### D4: quasi-static pushing/contact

Tasks:
- push object to target;
- push around obstacle;
- rotate object;
- contact-rich path.

Shifts:
- object mass;
- friction;
- contact point uncertainty;
- table surface;
- actuation noise.

### D5: secondary planner generality

Use same risk layer with:
- CEM-MPC
- shooting MPC
Main method remains MPPI.

## Baselines

Mandatory:
1. vanilla MPPI/MPC
2. robust/conservative MPC
3. raw ensemble uncertainty penalty
4. prediction-calibrated uncertainty penalty
5. CVaR/RA-MPPI-style
6. chance-constrained MPC-style
7. conformal prediction-set MPC
8. conformal risk control with non-CCR score
9. conformal decision/planning baseline
10. SODA-like OOD fallback
11. domain-randomized dynamics + MPC
12. sysID/adaptation + MPC
13. oracle dynamics + MPC
14. CCR no calibration
15. calibration no CCR
16. planner disagreement only
17. regret only (`regret_only`)
18. violation tail only (`violation_tail_only`)

## Metrics

- reward/cost
- closed-loop violation rate
- target risk vs observed risk
- ECE / calibration error for trajectory risk
- Brier score and log loss for failure prediction
- safety-performance Pareto
- freezing/conservatism rate
- computation time per step
- calibration sample efficiency
- OOD severity curves
- fallback rate
- regret vs oracle dynamics
- decision disagreement across dynamics particles
- empirical coverage of calibration theorem

## Required ablations

- number of dynamics particles K
- number of action samples N
- planning horizon H
- calibration set size
- risk threshold alpha
- OOD severity
- risk features included/excluded
- online recalibration on/off
- fallback on/off
- weighted calibration on/off
- task-conditioned risk on/off
- closed-loop vs open-loop calibration

## Seeds

Minimum:
- 10 seeds per main experiment
- 20 seeds for synthetic/theorem demo if cheap
- confidence intervals everywhere

## Reproducibility

Agent must create:
- `scripts/run_minimal.sh`
- `scripts/run_full_cpu.sh`
- `scripts/reproduce_main_figures.sh`
- config files for every figure
- raw logs
- plot scripts
- manifest with git/hash/configs


---

# Prior Work Distinction Memo

## Dangerous prior-work buckets

### Risk-aware MPPI / CVaR-MPPI

Existing work uses CVaR/tail-risk objectives for safer MPPI. Do not claim first risk-aware MPPI.

Distinction:
CCR-MPC measures planner instability/regret across plausible learned dynamics models and calibrates that to observed closed-loop failure risk. Risk is decision-space, not just cost-tail or collision risk.

### Dynamic risk-aware / chance-constrained MPPI

Existing work handles predicted collision risk, dynamic obstacles, and chance constraints.

Distinction:
CCR-MPC targets learned-dynamics-induced control failure: tracking failure, saturation, instability, constraint violation, OOD dynamics, task failure.

### Conformal prediction for planning

Existing work uses conformal prediction sets/regions to support safe planning.

Distinction:
CCR-MPC does not merely calibrate future states. It calibrates a planner-level counterfactual regret/violation score induced by learned dynamics particles.

### Conformal Risk Control / Conformal Decision Theory

Existing work gives general risk-control/decision-calibration tools.

Distinction:
Use these as tools/baselines. Novelty is the control-specific CCR score and its use inside receding-horizon learned-dynamics MPC.

### Uncertainty-aware MPC / GP-MPC / safe MPC

Existing work penalizes uncertainty or propagates confidence sets.

Distinction:
Raw uncertainty may be unrelated to closed-loop decision risk. CCR focuses on whether plausible dynamics models would make the planner choose different/high-regret actions.

### SODA-like OOD fallback

Existing work detects unreliable dynamics and triggers fallback.

Distinction:
CCR-MPC shapes decisions before fallback; it measures counterfactual planner regret, not just OOD detection.

## Must-cite/must-compare categories

The agent must verify exact citations before final writing:
- risk-aware MPPI / CVaR MPPI
- chance-constrained/risk-calibrated MPPI
- conformal prediction for safe planning
- conformal risk control
- conformal decision theory
- safe learning-based MPC
- uncertainty-aware MPC
- model-based RL with MPC
- learned dynamics ensemble uncertainty
- control-aware representations/MPC at ICLR
- Dreamer/BMPC/BS-MPC only as broad ICLR precedent, not direct baselines unless run fairly

## Related-work wording

Use:
"These works calibrate prediction sets, cost tails, collision probabilities, or OOD monitors. We calibrate counterfactual planner regret/violation induced by learned dynamics uncertainty, and use it directly to select MPC actions."

Do not use:
"We are the first safe/risk-aware/conformal MPC method."


---

# Reviewer Attack Closure Matrix

| Attack | Severity | Closure artifact |
|---|---:|---|
| Just risk-aware MPPI | Fatal | Direct RA-MPPI/CVaR baseline; explain CCR is planner-instability risk |
| Just conformal risk control applied to MPC | Fatal | CCR score novelty; non-CCR conformal baselines; theory emphasizes control-specific score |
| Just ensemble uncertainty penalty | Fatal | Raw uncertainty baselines fail; CCR uses counterfactual regret/calibrated outcomes |
| No GPU => weak experiments | High | Theory-led paper; 5 CPU domains; many seeds; hard baselines |
| Too robotics for ICLR | High | ML framing: decision calibration with learned dynamics; theorem first |
| Safe but useless/conservative | Fatal | Pareto curves, freezing rate, nominal performance preserved |
| No prior-work comparison | Fatal | Must run/cite RA-MPPI, conformal, chance-constrained, OOD fallback, robust MPC |
| Prediction calibration already solved | High | separation theorem showing prediction calibration != control risk |
| Calibration assumptions unrealistic | Medium | state exchangeability limits; weighted/adaptive shift extension |
| Method MPPI-specific | Medium | secondary planner experiment with CEM-MPC/shooting MPC |
| Too many heuristics | High | formal CCR definition, calibration theorem, ablations |
| Not enough domains | High | synthetic + classic + car + quadrotor + pushing at minimum |
| Results depend on threshold alpha | Medium | sensitivity sweeps over alpha |
| Results depend on ensemble size | Medium | sensitivity sweeps over K |
| No real learned dynamics | Fatal | train dynamics models/ensembles per domain; log prediction metrics |
| No OOD shift | Fatal | friction/payload/latency/wind/contact shifts |
| No calibration metrics | Fatal | ECE/Brier/logloss/reliability diagrams |
| Fallback dominates | Medium | fallback ablation and fallback rate reporting |
| Runtime too slow | Medium | compute-time per MPC step and optimization |
| Theorem disconnected from experiments | Medium | D0 synthetic experiment exactly mirrors theorem |
| Overclaims foundation models | Fatal | remove "foundation" unless implemented |
| Insufficient reproducibility | High | scripts, configs, seeds, raw logs, artifact manifest |
| Reviewer says use better uncertainty | High | show raw/pred-calibrated uncertainty fails under decision boundary |


---

# Baselines and Ablations Checklist

## Hard baselines

- Vanilla MPPI/MPC
- Robust/conservative MPC
- Raw ensemble uncertainty penalty
- Prediction-calibrated uncertainty penalty
- CVaR / RA-MPPI-style
- Chance-constrained MPC-style
- Conformal prediction-set MPC
- Conformal risk control with non-CCR score
- Conformal decision/planning baseline
- SODA-like OOD detector + fallback
- Domain-randomized dynamics + MPC
- System ID / online adaptation + MPC
- Oracle dynamics + MPC

## Ablations

- CCR no calibration
- calibration no CCR
- planner disagreement only
- regret only
- violation-tail only
- no task conditioning
- no OOD features
- no online recalibration
- no fallback
- weighted calibration off
- open-loop calibration instead of closed-loop calibration
- MPPI only vs CEM-MPC secondary

Machine-readable method names:
- `ccr_no_calibration`
- `calibration_no_ccr`
- `disagreement_only`
- `regret_only`
- `violation_tail_only`

## Fairness rules

- Equal planning horizon where applicable.
- Equal action-sample budget.
- Equal dynamics training data.
- Equal calibration set size.
- Report compute overhead.
- Tune baselines reasonably and document sweep ranges.


---

# Completion Checklist

The CLI agent may only print the completion message if all are true:

## Theory
- [ ] separation theorem statement
- [ ] proof
- [ ] finite-sample CCR calibration theorem
- [ ] safe-cost optimality theorem
- [ ] shifted calibration theorem or explicitly skipped with reason

## Code
- [ ] CCR score implementation
- [ ] calibration implementation
- [ ] MPPI implementation
- [ ] secondary planner implementation
- [ ] all baselines
- [ ] all domains
- [ ] logging schema
- [ ] plotting scripts

## Experiments
- [ ] D0 synthetic separation
- [ ] classic control
- [ ] car
- [ ] quadrotor
- [ ] pushing/contact
- [ ] secondary planner
- [ ] OOD severity sweeps
- [ ] calibration sample-size sweeps
- [ ] all baselines
- [ ] ablations
- [ ] confidence intervals

## Paper
- [ ] abstract
- [ ] intro
- [ ] related work
- [ ] theory section
- [ ] method
- [ ] experiments
- [ ] limitations
- [ ] appendix outline

## Reports
- [ ] prior-work audit
- [ ] reviewer attack closure
- [ ] calibration report
- [ ] plot/table manifest
- [ ] final artifact manifest

Completion message:
ICLR CCR-MPC COMPLETE: bounded theory proofs, counterfactual-risk algorithms, calibration code, CPU experiment suite, baselines, ablations, plots, paper manuscript, related-work audit, and reviewer-defense reports are finished. All claims are backed by generated artifacts. Human review is required before submission.
