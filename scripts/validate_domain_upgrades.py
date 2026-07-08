#!/usr/bin/env python3
"""Validate higher-dimensional CPU domain prototypes."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from domains.high_dimensional import domains  # noqa: E402


LEVELS = {"L0": 0.0, "L1": 0.55, "L2": 1.0, "L3": 1.35}


def policy(domain_name: str, state: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    if domain_name == "cartpole_safety":
        x, x_dot, theta, theta_dot = state
        return np.array([-8.0 * theta - 1.2 * theta_dot - 0.4 * x - 0.2 * x_dot]) + rng.normal(0, 0.4, size=1)
    if domain_name == "dynamic_bicycle_4d":
        _, py, yaw, v = state
        return np.array([0.6 * (1.6 - v), -0.9 * py - 0.7 * yaw]) + rng.normal(0, [0.08, 0.03])
    if domain_name == "planar_quadrotor_6d":
        _, z, _, vz, theta, omega = state
        thrust = 9.81 + 4.0 * (1.2 - z) - 1.3 * vz
        torque = -1.8 * theta - 0.35 * omega
        return np.array([thrust, torque]) + rng.normal(0, [0.2, 0.03])
    if domain_name == "pushing_contact_4d":
        ox, oy, theta, _ = state
        angle = np.arctan2(-oy, 1.0 - ox)
        return np.array([0.75, angle - 0.2 * theta]) + rng.normal(0, [0.04, 0.08])
    raise ValueError(domain_name)


def rollout(name: str, level: str, seed: int) -> Dict[str, object]:
    domain = domains()[name]
    severity = LEVELS[level]
    rng = np.random.default_rng(seed)
    state = np.asarray(domain.initial_state, dtype=float) + rng.normal(0.0, 0.02, size=domain.state_dim)
    states = [state.copy()]
    margins = [domain.constraint_margin(state)]
    action_norms: List[float] = []
    for _ in range(domain.horizon):
        action = policy(name, state, rng)
        action_norms.append(float(np.linalg.norm(action)))
        state = domain.step(state, action, severity)
        states.append(state.copy())
        margins.append(domain.constraint_margin(state))
    arr = np.stack(states, axis=0)
    return {
        "domain": name,
        "label": domain.label,
        "level": level,
        "seed": seed,
        "state_dim": domain.state_dim,
        "action_dim": domain.action_dim,
        "horizon": domain.horizon,
        "min_margin": float(np.min(margins)),
        "violation": float(np.min(margins) < 0.0),
        "mean_action_norm": float(np.mean(action_norms)),
        "final_state_norm": float(np.linalg.norm(arr[-1])),
    }


def plot_schematic() -> List[Path]:
    fig_dir = ROOT / "figures"
    fig_dir.mkdir(exist_ok=True)
    paths: List[Path] = []
    for name, domain in domains().items():
        rng = np.random.default_rng(123)
        state = np.asarray(domain.initial_state, dtype=float)
        traj = [state.copy()]
        for _ in range(domain.horizon):
            state = domain.step(state, policy(name, state, rng), 0.55)
            traj.append(state.copy())
        arr = np.stack(traj, axis=0)
        fig, ax = plt.subplots(figsize=(5.8, 3.8))
        if domain.state_dim >= 2:
            ax.plot(arr[:, 0], arr[:, 1], lw=2)
            ax.scatter(arr[0, 0], arr[0, 1], label="start", s=36)
            ax.scatter(arr[-1, 0], arr[-1, 1], label="end", s=36)
            ax.set_xlabel("state[0]")
            ax.set_ylabel("state[1]")
        else:
            ax.plot(arr[:, 0], lw=2)
            ax.set_xlabel("step")
            ax.set_ylabel("state[0]")
        ax.set_title(domain.label)
        ax.grid(alpha=0.25)
        ax.legend(fontsize=8)
        fig.tight_layout()
        path = fig_dir / f"domain_schematic_{name}.png"
        fig.savefig(path, dpi=160)
        plt.close(fig)
        paths.append(path)
    return paths


def main() -> int:
    rows: List[Dict[str, object]] = []
    for name in domains():
        for level in LEVELS:
            for seed in range(5):
                rows.append(rollout(name, level, seed))
    out = pd.DataFrame(rows)
    out_path = ROOT / "logs" / "domain_validation_metrics.csv"
    out.to_csv(out_path, index=False)
    paths = plot_schematic()
    summary = out.groupby(["domain", "level"], as_index=False).agg(
        violation_rate=("violation", "mean"),
        min_margin_mean=("min_margin", "mean"),
        final_state_norm_mean=("final_state_norm", "mean"),
    )
    lines = [
        "# Domain Validation Report",
        "",
        "## Status",
        "",
        "Higher-dimensional CPU domain prototypes were added and smoke-validated. They are not yet integrated into the main MPC experiment runner.",
        "",
        "## Domains",
        "",
    ]
    for domain in domains().values():
        lines.append(f"- `{domain.name}`: {domain.label}; state_dim={domain.state_dim}; action_dim={domain.action_dim}; shifts={', '.join(domain.shift_names)}")
    lines.extend(
        [
            "",
            "## Aggregate Validation",
            "",
            summary.to_markdown(index=False, floatfmt=".4f"),
            "",
            "## Artifacts",
            "",
            "- `src/domains/high_dimensional.py`",
            "- `logs/domain_validation_metrics.csv`",
        ]
    )
    for path in paths:
        lines.append(f"- `{path.relative_to(ROOT).as_posix()}`")
    lines.extend(
        [
            "",
            "## Limitation",
            "",
            "These domains are CPU prototypes for the next experiment stage. The current paper results still use the original simplified domains and trained Stage-A runner.",
        ]
    )
    (ROOT / "reports" / "domain_validation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out_path.relative_to(ROOT).as_posix()} and {len(paths)} schematics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
