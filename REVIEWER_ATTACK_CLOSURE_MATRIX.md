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
