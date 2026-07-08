#!/usr/bin/env python3
"""Validate simple risk-score models on available CCR calibration samples."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score


ROOT = Path(__file__).resolve().parents[1]
FEATURES = ["combined", "uncertainty", "violation_rate", "rank_instability", "regret_cvar", "violation_tail"]


def stable_fold(*parts: object) -> float:
    text = "::".join(str(part) for part in parts)
    value = int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:12], 16)
    return value / float(16**12 - 1)


def normalize(values: Sequence[float]) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    lo = np.nanmin(arr)
    hi = np.nanmax(arr)
    if not np.isfinite(lo) or not np.isfinite(hi) or hi - lo <= 1e-12:
        return np.zeros_like(arr)
    return (arr - lo) / (hi - lo)


def ece(pred: np.ndarray, obs: np.ndarray, bins: int = 10) -> float:
    pred = np.clip(np.asarray(pred, dtype=float), 1e-6, 1.0 - 1e-6)
    obs = np.asarray(obs, dtype=float)
    out = 0.0
    edges = np.linspace(0.0, 1.0, bins + 1)
    for lo, hi in zip(edges[:-1], edges[1:]):
        mask = (pred >= lo) & (pred < hi if hi < 1.0 else pred <= hi)
        if np.any(mask):
            out += float(np.mean(mask)) * abs(float(np.mean(pred[mask]) - np.mean(obs[mask])))
    return float(out)


def metric_row(source: str, model: str, y: np.ndarray, pred: np.ndarray, n_train: int, n_test: int) -> Dict[str, object]:
    pred = np.clip(np.asarray(pred, dtype=float), 1e-6, 1.0 - 1e-6)
    both_classes = len(set(float(v) for v in y)) == 2
    return {
        "source": source,
        "risk_model": model,
        "n_train": n_train,
        "n_test": n_test,
        "positive_rate_test": float(np.mean(y)) if y.size else 0.0,
        "roc_auc": float(roc_auc_score(y, pred)) if both_classes else float("nan"),
        "brier": float(brier_score_loss(y, pred)) if y.size else float("nan"),
        "log_loss": float(log_loss(y, pred, labels=[0, 1])) if y.size else float("nan"),
        "ece": ece(pred, y) if y.size else float("nan"),
    }


def load_sources() -> List[pd.DataFrame]:
    specs = [
        ("focused_surrogate", ROOT / "logs" / "calibration_samples.csv"),
        ("trained_stage_a", ROOT / "logs" / "trained_dynamics_stage_a_calibration_samples.csv"),
    ]
    frames: List[pd.DataFrame] = []
    for source, path in specs:
        if not path.exists():
            continue
        df = pd.read_csv(path)
        if "true_failure" not in df.columns:
            continue
        present = [feature for feature in FEATURES if feature in df.columns]
        if not present:
            continue
        df = df.copy()
        df["source"] = source
        for feature in FEATURES:
            if feature not in df.columns:
                df[feature] = 0.0
        frames.append(df)
    return frames


def validate_source(df: pd.DataFrame) -> List[Dict[str, object]]:
    source = str(df["source"].iloc[0])
    folds = np.array(
        [
            stable_fold(source, row.get("domain", ""), row.get("level", ""), row.get("context", ""), row.get("candidate", ""))
            for _, row in df.iterrows()
        ]
    )
    train_mask = folds < 0.70
    test_mask = ~train_mask
    train = df.loc[train_mask].reset_index(drop=True)
    test = df.loc[test_mask].reset_index(drop=True)
    if train.empty or test.empty:
        return []
    y_train = train["true_failure"].astype(float).to_numpy()
    y_test = test["true_failure"].astype(float).to_numpy()
    rows: List[Dict[str, object]] = []

    for feature in FEATURES:
        pred = normalize(test[feature].to_numpy())
        rows.append(metric_row(source, f"single_{feature}", y_test, pred, len(train), len(test)))

    x_train = train[FEATURES].astype(float).to_numpy()
    x_test = test[FEATURES].astype(float).to_numpy()
    if len(set(float(v) for v in y_train)) == 2:
        logistic = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=0)
        logistic.fit(x_train, y_train)
        rows.append(metric_row(source, "logistic_all_features", y_test, logistic.predict_proba(x_test)[:, 1], len(train), len(test)))

        forest = RandomForestClassifier(n_estimators=100, min_samples_leaf=5, random_state=0, class_weight="balanced_subsample")
        forest.fit(x_train, y_train)
        rows.append(metric_row(source, "random_forest_all_features", y_test, forest.predict_proba(x_test)[:, 1], len(train), len(test)))

        iso = IsotonicRegression(out_of_bounds="clip")
        iso.fit(normalize(train["combined"].to_numpy()), y_train)
        rows.append(metric_row(source, "isotonic_combined", y_test, iso.predict(normalize(test["combined"].to_numpy())), len(train), len(test)))
    return rows


def write_report(result: pd.DataFrame) -> None:
    report_path = ROOT / "reports" / "risk_model_validation_report.md"
    best = result.sort_values(["source", "brier", "ece"], ascending=[True, True, True]).groupby("source").head(3)
    payload = {
        "sources": sorted(result["source"].unique().tolist()),
        "rows": int(len(result)),
        "best_by_brier": best[["source", "risk_model", "brier", "roc_auc", "ece"]].to_dict(orient="records"),
    }
    lines = [
        "# Risk Model Validation Report",
        "",
        "## Status",
        "",
        "Preliminary validation on available calibration-sample logs. These results are for model-selection diagnostics only and are not held-out Stage-B test claims.",
        "",
        "## Summary",
        "",
        "```json",
        json.dumps(payload, indent=2),
        "```",
        "",
        "## Artifacts",
        "",
        "- `logs/risk_model_validation.csv`",
        "- `scripts/validate_risk_models.py`",
        "",
        "## Limitation",
        "",
        "The current validation samples are calibration diagnostics, not a locked held-out benchmark. Final claims require validation-selected risk models evaluated on fresh held-out Stage-B/Stage-C runs.",
    ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    rows: List[Dict[str, object]] = []
    for frame in load_sources():
        rows.extend(validate_source(frame))
    if not rows:
        raise RuntimeError("no risk-model validation rows were generated")
    result = pd.DataFrame(rows)
    out = ROOT / "logs" / "risk_model_validation.csv"
    result.to_csv(out, index=False)
    write_report(result)
    print(f"wrote {out.relative_to(ROOT).as_posix()} with {len(result)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
