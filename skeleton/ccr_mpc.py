"""
Reference CCR-MPC utilities.

This module is intentionally small and dependency-light. It gives the CLI agent a
tested interface for computing counterfactual-control-risk features, fitting a
split-calibration threshold, and selecting a risk-acceptable candidate. Domain
dynamics, MPPI/CEM sampling, training loops, and plotting still belong in the
full implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, Mapping, Optional, Tuple

import numpy as np


Array = np.ndarray


@dataclass(frozen=True)
class CCRConfig:
    alpha: float = 0.10
    risk_mode: str = "cvar_regret"
    cvar_quantile: float = 0.90
    use_violation_tail: bool = True
    use_rank_instability: bool = True
    use_action_disagreement: bool = True
    regret_weight: float = 1.0
    violation_weight: float = 1.0
    margin_weight: float = 0.25
    rank_weight: float = 0.25
    action_weight: float = 0.25
    eps: float = 1e-8

    def __post_init__(self) -> None:
        if not 0.0 < self.alpha < 1.0:
            raise ValueError("alpha must be in (0, 1)")
        if not 0.0 < self.cvar_quantile < 1.0:
            raise ValueError("cvar_quantile must be in (0, 1)")


def _normalize(values: Array, eps: float = 1e-8) -> Array:
    values = np.asarray(values, dtype=float)
    lo = np.nanmin(values)
    hi = np.nanmax(values)
    if not np.isfinite(lo) or not np.isfinite(hi) or hi - lo <= eps:
        return np.zeros_like(values, dtype=float)
    return (values - lo) / (hi - lo + eps)


def _as_action_sequences(action_sequences: Array) -> Array:
    actions = np.asarray(action_sequences, dtype=float)
    if actions.ndim < 2:
        raise ValueError("action_sequences must have shape [N, H, action_dim] or [N, H]")
    if actions.ndim == 2:
        actions = actions[:, :, None]
    return actions


def evaluate_candidates_under_models(
    models: Iterable[Callable[[Array, Array], Array]],
    state: Array,
    action_sequences: Array,
    cost_fn: Callable[[Array, Array], float],
    constraint_fn: Callable[[Array, Array], Tuple[float, float]],
) -> Tuple[Array, Array, Array]:
    """Roll out each candidate sequence under each dynamics particle.

    Args:
        models: Callables `next_state = model(state, action)`.
        state: Initial state.
        action_sequences: Candidate controls with shape `[N, H, action_dim]`.
        cost_fn: Callable returning scalar rollout cost from `(trajectory, actions)`.
        constraint_fn: Callable returning `(violation_indicator, min_margin)`.

    Returns:
        `(costs, violations, margins)` with shape `[K, N]`.
    """

    model_list = list(models)
    actions = _as_action_sequences(action_sequences)
    if not model_list:
        raise ValueError("at least one dynamics model is required")

    num_models = len(model_list)
    num_candidates = actions.shape[0]
    costs = np.zeros((num_models, num_candidates), dtype=float)
    violations = np.zeros((num_models, num_candidates), dtype=float)
    margins = np.zeros((num_models, num_candidates), dtype=float)

    for model_idx, model in enumerate(model_list):
        for cand_idx, sequence in enumerate(actions):
            x = np.asarray(state, dtype=float).copy()
            trajectory = [x.copy()]
            for action in sequence:
                x = np.asarray(model(x, action), dtype=float)
                trajectory.append(x.copy())
            trajectory_arr = np.stack(trajectory, axis=0)
            costs[model_idx, cand_idx] = float(cost_fn(trajectory_arr, sequence))
            violation, margin = constraint_fn(trajectory_arr, sequence)
            violations[model_idx, cand_idx] = float(violation)
            margins[model_idx, cand_idx] = float(margin)

    return costs, violations, margins


def compute_counterfactual_regret(costs: Array) -> Array:
    """Return per-model regret against that model's best sampled candidate."""

    costs = np.asarray(costs, dtype=float)
    if costs.ndim != 2:
        raise ValueError("costs must have shape [K, N]")
    best_per_model = costs.min(axis=1, keepdims=True)
    return costs - best_per_model


def cvar(values: Array, q: float, axis: int = 0) -> Array:
    """Upper-tail CVaR for candidate risk features."""

    values = np.asarray(values, dtype=float)
    if not 0.0 < q < 1.0:
        raise ValueError("q must be in (0, 1)")
    threshold = np.quantile(values, q, axis=axis, keepdims=True)
    masked = np.where(values >= threshold, values, np.nan)
    return np.nanmean(masked, axis=axis)


def rank_instability(costs: Array) -> Array:
    """Normalized standard deviation of candidate ranks across model particles."""

    costs = np.asarray(costs, dtype=float)
    order = np.argsort(costs, axis=1)
    ranks = np.empty_like(order, dtype=float)
    row_ids = np.arange(costs.shape[0])[:, None]
    ranks[row_ids, order] = np.arange(costs.shape[1], dtype=float)
    denom = max(costs.shape[1] - 1, 1)
    return ranks.std(axis=0) / denom


def first_action_disagreement(action_sequences: Optional[Array]) -> Array:
    """Distance of each candidate's first action from the sampled action centroid."""

    if action_sequences is None:
        return np.array([], dtype=float)
    actions = _as_action_sequences(action_sequences)
    first_actions = actions[:, 0, :]
    centroid = first_actions.mean(axis=0, keepdims=True)
    return np.linalg.norm(first_actions - centroid, axis=1)


def ccr_score(
    costs: Array,
    violations: Array,
    margins: Array,
    cfg: CCRConfig,
    action_sequences: Optional[Array] = None,
) -> Dict[str, Array]:
    """Compute candidate-level CCR features and a normalized combined score."""

    costs = np.asarray(costs, dtype=float)
    violations = np.asarray(violations, dtype=float)
    margins = np.asarray(margins, dtype=float)
    if costs.shape != violations.shape or costs.shape != margins.shape:
        raise ValueError("costs, violations, and margins must share shape [K, N]")

    regrets = compute_counterfactual_regret(costs)
    features: Dict[str, Array] = {
        "regret_cvar": cvar(regrets, cfg.cvar_quantile, axis=0),
        "regret_mean": regrets.mean(axis=0),
        "violation_rate": violations.mean(axis=0),
        "violation_tail": cvar(violations, cfg.cvar_quantile, axis=0),
        "min_margin": margins.min(axis=0),
        "negative_margin_tail": cvar(np.maximum(0.0, -margins), cfg.cvar_quantile, axis=0),
        "rank_instability": rank_instability(costs),
    }

    disagreement = first_action_disagreement(action_sequences)
    if disagreement.size:
        features["first_action_disagreement"] = disagreement
    else:
        features["first_action_disagreement"] = np.zeros(costs.shape[1], dtype=float)

    combined = cfg.regret_weight * _normalize(features["regret_cvar"], cfg.eps)
    if cfg.use_violation_tail:
        combined += cfg.violation_weight * _normalize(features["violation_tail"], cfg.eps)
        combined += cfg.margin_weight * _normalize(features["negative_margin_tail"], cfg.eps)
    if cfg.use_rank_instability:
        combined += cfg.rank_weight * _normalize(features["rank_instability"], cfg.eps)
    if cfg.use_action_disagreement:
        combined += cfg.action_weight * _normalize(features["first_action_disagreement"], cfg.eps)

    features["combined"] = combined
    return features


class RiskCalibrator:
    """Split-calibration threshold for monotone risk scores.

    High score means high expected failure risk. The threshold is the largest
    score whose one-sided Hoeffding upper bound on accepted calibration failures
    is at most `alpha`.
    """

    def __init__(self, confidence_delta: float = 0.05) -> None:
        if not 0.0 < confidence_delta < 1.0:
            raise ValueError("confidence_delta must be in (0, 1)")
        self.confidence_delta = confidence_delta
        self._scores: Optional[Array] = None
        self._failures: Optional[Array] = None
        self._thresholds: Dict[float, float] = {}

    def fit(self, scores: Array, observed_failures: Array) -> "RiskCalibrator":
        scores = np.asarray(scores, dtype=float).reshape(-1)
        failures = np.asarray(observed_failures, dtype=float).reshape(-1)
        if scores.shape != failures.shape:
            raise ValueError("scores and observed_failures must have the same length")
        if scores.size == 0:
            raise ValueError("calibration data cannot be empty")
        if np.any((failures < 0.0) | (failures > 1.0)):
            raise ValueError("observed_failures must be binary or probabilities in [0, 1]")

        order = np.argsort(scores)
        self._scores = scores[order]
        self._failures = failures[order]
        self._thresholds.clear()
        return self

    def _check_fit(self) -> Tuple[Array, Array]:
        if self._scores is None or self._failures is None:
            raise RuntimeError("RiskCalibrator.fit must be called before use")
        return self._scores, self._failures

    def predict_risk(self, scores: Array) -> Array:
        cal_scores, cal_failures = self._check_fit()
        query = np.asarray(scores, dtype=float)
        flat = query.reshape(-1)
        out = np.zeros_like(flat, dtype=float)
        cumulative_failures = np.cumsum(cal_failures)
        counts = np.arange(1, cal_scores.size + 1, dtype=float)

        for idx, score in enumerate(flat):
            pos = np.searchsorted(cal_scores, score, side="right") - 1
            if pos < 0:
                out[idx] = 0.0
            else:
                empirical = cumulative_failures[pos] / counts[pos]
                radius = np.sqrt(np.log(1.0 / self.confidence_delta) / (2.0 * counts[pos]))
                out[idx] = min(1.0, empirical + radius)
        return out.reshape(query.shape)

    def threshold(self, alpha: float) -> float:
        if not 0.0 < alpha < 1.0:
            raise ValueError("alpha must be in (0, 1)")
        if alpha in self._thresholds:
            return self._thresholds[alpha]

        cal_scores, cal_failures = self._check_fit()
        cumulative_failures = np.cumsum(cal_failures)
        counts = np.arange(1, cal_scores.size + 1, dtype=float)
        empirical = cumulative_failures / counts
        radius = np.sqrt(np.log(1.0 / self.confidence_delta) / (2.0 * counts))
        upper = empirical + radius
        ok = np.flatnonzero(upper <= alpha)
        tau = float(cal_scores[ok[-1]]) if ok.size else float(np.min(cal_scores) - 1e-12)
        self._thresholds[alpha] = tau
        return tau


def score_array(scores: Mapping[str, Array], key: str = "combined") -> Array:
    if key not in scores:
        raise KeyError(f"missing CCR score key: {key}")
    return np.asarray(scores[key], dtype=float)


def select_action(
    costs: Array,
    scores: Mapping[str, Array],
    calibrator: RiskCalibrator,
    alpha: float,
    score_key: str = "combined",
) -> Tuple[int, Array]:
    """Select the lowest mean-cost candidate passing the calibrated risk gate."""

    costs = np.asarray(costs, dtype=float)
    candidate_scores = score_array(scores, score_key)
    risk = calibrator.predict_risk(candidate_scores)
    acceptable = candidate_scores <= calibrator.threshold(alpha)

    if acceptable.any():
        masked_cost = np.where(acceptable, costs.mean(axis=0), np.inf)
        return int(np.argmin(masked_cost)), risk
    return int(np.argmin(risk)), risk


def _smoke_test() -> None:
    costs = np.array([[1.0, 2.0, 5.0], [1.2, 1.8, 6.0], [0.9, 2.5, 4.8]])
    violations = np.array([[0, 0, 1], [0, 0, 1], [0, 1, 1]], dtype=float)
    margins = np.array([[1.0, 0.4, -0.5], [0.9, 0.2, -0.7], [1.1, -0.1, -0.4]])
    actions = np.array([[[0.0], [0.1]], [[0.2], [0.1]], [[2.0], [2.0]]])
    cfg = CCRConfig(alpha=0.2)
    features = ccr_score(costs, violations, margins, cfg, actions)
    cal = RiskCalibrator(confidence_delta=0.2).fit(
        np.array([0.0, 0.1, 0.2, 0.8, 1.0]),
        np.array([0, 0, 0, 1, 1]),
    )
    idx, risk = select_action(costs, features, cal, alpha=0.5)
    assert idx in {0, 1}
    assert risk.shape == (3,)


if __name__ == "__main__":
    _smoke_test()
    print("ccr_mpc.py smoke test passed")
