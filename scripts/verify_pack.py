#!/usr/bin/env python3
"""
Verify the CCR-MPC ICLR bulletproof CLI pack.

This script is intentionally standard-library only. It validates the pack as a
research-execution contract, not as a completed paper implementation.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
from collections.abc import Mapping
from collections import Counter
from pathlib import Path
from typing import Iterable, List, Sequence, Set


COMPLETION_MESSAGE = (
    "ICLR CCR-MPC COMPLETE: bounded theory proofs, counterfactual-risk algorithms, "
    "calibration code, CPU experiment suite, baselines, ablations, plots, paper "
    "manuscript, related-work audit, and reviewer-defense reports are finished. "
    "All claims are backed by generated artifacts. Human review is required "
    "before submission."
)

REQUIRED_FILES = [
    "README_FIRST.md",
    "CLI_AGENT_MASTER_PROMPT.md",
    "COUNTERFACTUAL_CONTROL_RISK_MASTER_PLAN.md",
    "THEORY_MOAT_PLAN.md",
    "EXPERIMENT_MAXOUT_PLAN.md",
    "PRIOR_WORK_DISTINCTION_MEMO.md",
    "REVIEWER_ATTACK_CLOSURE_MATRIX.md",
    "BASELINES_ABLATIONS_CHECKLIST.md",
    "tasks.yaml",
    "matrices/experiment_matrix_maxout.csv",
    "schemas/result_schema.json",
    "schemas/artifact_manifest_schema.json",
    "schemas/claim_ledger_schema.json",
    "skeleton/ccr_mpc.py",
    "skeleton/run_experiments.py",
    "scripts/verify_pack.py",
    "scripts/run_pack_checks.ps1",
    "scripts/run_pack_checks.sh",
    "scripts/execute_paper_cpu_study.py",
    "paper/CCR_MPC_paper.tex",
    "paper/CCR_MPC_paper.pdf",
    "paper/references.bib",
    "paper/CCR_MPC_paper_draft.md",
    "reports/citation_verification.md",
    "reports/completion_audit_report.md",
    "templates/claim_ledger.csv",
    "templates/readiness_gate_report.md",
]

REQUIRED_DOMAINS = {
    "synthetic_separation",
    "classic_control",
    "dynamic_bicycle_car",
    "planar_quadrotor",
    "quasistatic_pushing",
    "secondary_planner",
}

REQUIRED_METHODS = {
    "vanilla_mppi",
    "robust_mpc",
    "ensemble_uncertainty_penalty",
    "prediction_calibrated_penalty",
    "cvar_ra_mppi",
    "chance_constrained_mpc",
    "conformal_prediction_mpc",
    "conformal_risk_non_ccr",
    "conformal_decision_baseline",
    "soda_like_fallback",
    "domain_randomized_mpc",
    "sysid_mpc",
    "oracle_mpc",
    "ccr_no_calibration",
    "calibration_no_ccr",
    "disagreement_only",
    "regret_only",
    "violation_tail_only",
    "ccr_mpc",
}

MAIN_TABLE_METHODS = [
    "vanilla_mppi",
    "robust_mpc",
    "cvar_ra_mppi",
    "conformal_prediction_mpc",
    "conformal_risk_non_ccr",
    "ccr_no_calibration",
    "ccr_mpc",
    "oracle_mpc",
]

MAIN_TABLE_DISPLAY = {
    "vanilla_mppi": "Vanilla MPPI",
    "robust_mpc": "Robust MPC",
    "cvar_ra_mppi": "CVaR/RA-MPPI",
    "conformal_prediction_mpc": "Conf. prediction MPC",
    "conformal_risk_non_ccr": "Conf. risk, non-CCR",
    "ccr_no_calibration": "CCR no calibration",
    "ccr_mpc": "CCR-MPC",
    "oracle_mpc": "Oracle MPC",
}

REQUIRED_METRICS = {
    "reward",
    "cost",
    "violation_rate",
    "observed_risk",
    "target_risk",
    "ece",
    "brier",
    "log_loss",
    "freezing_rate",
    "compute_ms",
    "oracle_regret",
    "fallback_rate",
    "decision_disagreement",
    "empirical_coverage",
}

REQUIRED_REPORTS = {
    "theory_moat_report.md",
    "prior_work_distinctions.md",
    "experiment_results_summary.md",
    "calibration_report.md",
    "reviewer_attack_closure_report.md",
    "claim_ledger.csv",
    "readiness_gate_report.md",
    "completion_audit_report.md",
    "final_artifact_manifest.json",
}

MANIFEST_GROUPS = ["theory", "code", "experiments", "plots", "paper", "reports"]
REQUIRED_MANIFEST_ARTIFACTS = {
    "BASELINES_ABLATIONS_CHECKLIST.md",
    "CLI_AGENT_MASTER_PROMPT.md",
    "COUNTERFACTUAL_CONTROL_RISK_MASTER_PLAN.md",
    "EXPERIMENT_MAXOUT_PLAN.md",
    "PRIOR_WORK_DISTINCTION_MEMO.md",
    "README_FIRST.md",
    "REVIEWER_ATTACK_CLOSURE_MATRIX.md",
    "THEORY_MOAT_PLAN.md",
    "configs/execution_config.json",
    "logs/calibration_samples.csv",
    "logs/results.jsonl",
    "logs/results_flat.csv",
    "logs/step_predictions.csv",
    "matrices/experiment_matrix_maxout.csv",
    "paper/CCR_MPC_paper.pdf",
    "paper/CCR_MPC_paper.tex",
    "paper/references.bib",
    "reports/claim_ledger.csv",
    "reports/citation_verification.md",
    "reports/completion_audit_report.md",
    "schemas/artifact_manifest_schema.json",
    "schemas/claim_ledger_schema.json",
    "schemas/result_schema.json",
    "scripts/execute_paper_cpu_study.py",
    "scripts/run_pack_checks.ps1",
    "scripts/run_pack_checks.sh",
    "scripts/verify_pack.py",
    "skeleton/ccr_mpc.py",
    "skeleton/run_experiments.py",
    "tables/main_results_table_rows.tex",
    "tables/summary_by_domain_method.csv",
    "tables/summary_by_method.csv",
    "tables/summary_by_method_level.csv",
    "tasks.yaml",
    "templates/claim_ledger.csv",
    "templates/readiness_gate_report.md",
}
ALLOWED_LOG_FILES = {
    "calibration_samples.csv",
    "dynamics_prediction_metrics.csv",
    "results.jsonl",
    "results_flat.csv",
    "risk_model_validation.csv",
    "step_predictions.csv",
    "trained_dynamics_stage_a_calibration_samples.csv",
    "trained_dynamics_stage_a_results.jsonl",
    "trained_dynamics_stage_a_results_flat.csv",
    "trained_dynamics_stage_a_step_predictions.csv",
}
LATEX_SCRATCH_SUFFIXES = (
    ".aux",
    ".bbl",
    ".blg",
    ".log",
    ".out",
    ".toc",
    ".fls",
    ".fdb_latexmk",
    ".synctex.gz",
)
FINAL_LEVELS = {"L0", "L1", "L2"}
FINAL_SEEDS = {0, 1, 2}


class Reporter:
    def __init__(self) -> None:
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.notes: List[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.error(message)

    def print(self) -> None:
        for note in self.notes:
            print(f"[OK] {note}")
        for warning in self.warnings:
            print(f"[WARN] {warning}")
        for error in self.errors:
            print(f"[ERROR] {error}")


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_declared_path(root: Path, declared: str, reporter: Reporter, context: str) -> Path | None:
    if not isinstance(declared, str) or not declared.strip():
        reporter.error(f"{context} has empty artifact path")
        return None
    relative = Path(declared)
    if relative.is_absolute() or ".." in relative.parts:
        reporter.error(f"{context} has unsafe artifact path: {declared}")
        return None
    resolved = (root / relative).resolve()
    if not is_within(resolved, root):
        reporter.error(f"{context} escapes pack root: {declared}")
        return None
    return resolved


def require_files(root: Path, reporter: Reporter) -> None:
    for item in REQUIRED_FILES:
        path = root / item
        reporter.require(path.exists(), f"missing required file: {item}")
    reporter.note(f"required file check completed ({len(REQUIRED_FILES)} paths)")


def check_json(root: Path, reporter: Reporter) -> None:
    for path in sorted((root / "schemas").glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
            reporter.note(f"valid JSON: {rel(root, path)}")
        except json.JSONDecodeError as exc:
            reporter.error(f"invalid JSON in {rel(root, path)}: {exc}")


def check_completion_message(root: Path, reporter: Reporter) -> None:
    targets = [
        root / "README_FIRST.md",
        root / "CLI_AGENT_MASTER_PROMPT.md",
        root / "tasks.yaml",
    ]
    for path in targets:
        text = path.read_text(encoding="utf-8")
        reporter.require(COMPLETION_MESSAGE in " ".join(text.split()), f"completion message drift in {rel(root, path)}")
    reporter.note("completion message is consistent across README, prompt, and tasks")


def parse_matrix(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def check_set(name: str, actual: Set[str], expected: Set[str], reporter: Reporter) -> None:
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    reporter.require(not missing, f"matrix missing {name}: {', '.join(missing)}")
    if extra:
        reporter.warn(f"matrix has extra {name}: {', '.join(extra)}")


def check_matrix(root: Path, reporter: Reporter) -> None:
    path = root / "matrices" / "experiment_matrix_maxout.csv"
    rows = parse_matrix(path)
    reporter.require(len(rows) >= 57000, f"experiment matrix has too few rows: {len(rows)}")

    headers = set(rows[0].keys()) if rows else set()
    expected_headers = {"domain", "method", "ood_shift", "level", "seed", "planner", "required_metrics", "priority"}
    reporter.require(headers == expected_headers, f"matrix header mismatch: {sorted(headers)}")

    domains = {row["domain"] for row in rows}
    methods = {row["method"] for row in rows}
    planners = {row["planner"] for row in rows}
    priorities = Counter(row["priority"] for row in rows)
    check_set("domains", domains, REQUIRED_DOMAINS, reporter)
    check_set("methods", methods, REQUIRED_METHODS, reporter)
    reporter.require({"MPPI", "CEM-MPC"}.issubset(planners), "matrix must include MPPI and CEM-MPC planners")
    reporter.require({"P0", "P1"}.issubset(set(priorities)), "matrix must include P0 and P1 priorities")

    bad_metric_rows = []
    for index, row in enumerate(rows, start=2):
        metrics = {item.strip() for item in row["required_metrics"].split(",") if item.strip()}
        if not REQUIRED_METRICS.issubset(metrics):
            bad_metric_rows.append(index)
            if len(bad_metric_rows) >= 5:
                break
    reporter.require(not bad_metric_rows, f"matrix rows missing required metrics near CSV lines: {bad_metric_rows}")

    method_counts = Counter(row["method"] for row in rows)
    low_coverage = [name for name in REQUIRED_METHODS if method_counts[name] < 3000]
    reporter.require(not low_coverage, f"methods with low matrix coverage: {', '.join(sorted(low_coverage))}")
    reporter.note(
        f"matrix coverage ok: {len(rows)} rows, {len(domains)} domains, "
        f"{len(methods)} methods, planners={sorted(planners)}"
    )


def check_tasks_yaml_text(root: Path, reporter: Reporter) -> None:
    text = (root / "tasks.yaml").read_text(encoding="utf-8")
    for method in sorted(REQUIRED_METHODS):
        reporter.require(method in text, f"tasks.yaml missing method/baseline: {method}")
    for report in sorted(REQUIRED_REPORTS):
        reporter.require(report in text, f"tasks.yaml missing required report: {report}")
    reporter.note("tasks.yaml text includes required methods and reports")


def check_templates(root: Path, reporter: Reporter) -> None:
    ledger = root / "templates" / "claim_ledger.csv"
    with ledger.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, [])
    expected = [
        "claim_id",
        "paper_location",
        "claim_text",
        "claim_type",
        "evidence_artifacts",
        "tested_scope",
        "comparison_class",
        "compute_budget",
        "limitations",
        "strongest_alternative_explanation",
        "status",
    ]
    reporter.require(header == expected, "claim ledger template header does not match schema contract")
    reporter.note("claim ledger template header matches schema contract")


def check_no_unsafe_completion(root: Path, reporter: Reporter) -> None:
    reports = root / "reports"
    complete = reports / "ICLR_CCR_MPC_COMPLETE.md"
    if not complete.exists():
        reporter.warn("completion report absent, as expected for a plan pack that has not run experiments yet")
        return

    missing = [name for name in REQUIRED_REPORTS if not (reports / name).exists()]
    reporter.require(not missing, f"completion report exists but required reports are missing: {', '.join(sorted(missing))}")
    manifest = reports / "final_artifact_manifest.json"
    if manifest.exists():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            reporter.require(data.get("completion_message") == COMPLETION_MESSAGE, "manifest completion message mismatch")
        except json.JSONDecodeError as exc:
            reporter.error(f"final manifest is not valid JSON: {exc}")


def load_manifest(root: Path, reporter: Reporter) -> dict | None:
    manifest_path = root / "reports" / "final_artifact_manifest.json"
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        reporter.error("final artifact manifest is missing")
    except json.JSONDecodeError as exc:
        reporter.error(f"final manifest is not valid JSON: {exc}")
    return None


def collect_manifest_paths(root: Path, reporter: Reporter) -> Set[str] | None:
    manifest = load_manifest(root, reporter)
    if manifest is None:
        return None

    paths: Set[str] = set()
    for group in MANIFEST_GROUPS:
        entries = manifest.get(group, [])
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if isinstance(entry, Mapping) and isinstance(entry.get("path"), str):
                paths.add(entry["path"])
    return paths


def check_manifest_integrity(root: Path, reporter: Reporter) -> None:
    manifest = load_manifest(root, reporter)
    if manifest is None:
        return

    for key in [
        "paper_title",
        "created_utc",
        "git_commit",
        "completion_message",
        "claim_ledger",
        "known_limitations",
    ]:
        reporter.require(key in manifest, f"manifest missing top-level key: {key}")
    reporter.require(manifest.get("completion_message") == COMPLETION_MESSAGE, "manifest completion message mismatch")

    seen_paths: Counter[str] = Counter()
    checked = 0
    for group in MANIFEST_GROUPS:
        entries = manifest.get(group)
        reporter.require(isinstance(entries, list) and bool(entries), f"manifest group missing or empty: {group}")
        if not isinstance(entries, list):
            continue
        for index, entry in enumerate(entries):
            context = f"manifest {group}[{index}]"
            if not isinstance(entry, Mapping):
                reporter.error(f"{context} is not an object")
                continue
            declared_path = entry.get("path")
            declared_hash = entry.get("sha256")
            description = entry.get("description")
            reporter.require(isinstance(description, str) and bool(description.strip()), f"{context} missing description")
            artifact = resolve_declared_path(root, str(declared_path or ""), reporter, context)
            if artifact is None:
                continue
            seen_paths[artifact.relative_to(root).as_posix()] += 1
            reporter.require(artifact.exists(), f"{context} path missing: {declared_path}")
            if artifact.exists():
                actual_hash = sha256_file(artifact)
                reporter.require(
                    isinstance(declared_hash, str) and actual_hash == declared_hash.lower(),
                    f"{context} sha256 mismatch for {declared_path}",
                )
                checked += 1

    ledger_path = resolve_declared_path(root, str(manifest.get("claim_ledger", "")), reporter, "manifest claim_ledger")
    if ledger_path is not None:
        reporter.require(ledger_path.exists(), f"manifest claim_ledger path missing: {manifest.get('claim_ledger')}")

    allowed_duplicates = {"reports/theory_moat_report.md"}
    duplicate_paths = sorted(path for path, count in seen_paths.items() if count > 1 and path not in allowed_duplicates)
    reporter.require(not duplicate_paths, f"manifest repeats artifact paths unexpectedly: {', '.join(duplicate_paths)}")
    missing_required = sorted(REQUIRED_MANIFEST_ARTIFACTS - set(seen_paths))
    reporter.require(not missing_required, f"manifest missing required reproducibility artifacts: {', '.join(missing_required)}")
    reporter.note(f"manifest artifact hashes verified ({checked} entries)")


def check_claim_ledger(root: Path, reporter: Reporter) -> None:
    path = root / "reports" / "claim_ledger.csv"
    expected_header = [
        "claim_id",
        "paper_location",
        "claim_text",
        "claim_type",
        "evidence_artifacts",
        "tested_scope",
        "comparison_class",
        "compute_budget",
        "limitations",
        "strongest_alternative_explanation",
        "status",
    ]
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except FileNotFoundError:
        reporter.error("claim ledger is missing")
        return
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        actual_header = next(reader, [])
    reporter.require(actual_header == expected_header, "claim ledger header mismatch")
    reporter.require(bool(rows), "claim ledger has no claim rows")

    manifest_paths = collect_manifest_paths(root, reporter)
    seen_claims: Set[str] = set()
    for row in rows:
        claim_id = row.get("claim_id", "")
        reporter.require(claim_id not in seen_claims, f"duplicate claim id in ledger: {claim_id}")
        seen_claims.add(claim_id)
        reporter.require(row.get("status") == "supported", f"claim {claim_id} is not fully supported: {row.get('status')}")
        artifacts = [item.strip() for item in row.get("evidence_artifacts", "").split(";") if item.strip()]
        reporter.require(bool(artifacts), f"claim {claim_id} has no evidence artifacts")
        for artifact_text in artifacts:
            artifact_path = artifact_text.split("::", 1)[0]
            resolved = resolve_declared_path(root, artifact_path, reporter, f"claim {claim_id}")
            if resolved is not None:
                reporter.require(resolved.exists(), f"claim {claim_id} evidence path missing: {artifact_path}")
                if manifest_paths is not None and resolved.exists() and resolved.is_file():
                    rel_path = resolved.relative_to(root).as_posix()
                    reporter.require(rel_path in manifest_paths, f"claim {claim_id} evidence is not manifest-hashed: {rel_path}")
    if manifest_paths is None:
        reporter.note(f"claim ledger evidence paths verified ({len(rows)} claims)")
    else:
        reporter.note(f"claim ledger evidence paths verified and manifest-hashed ({len(rows)} claims)")


def check_result_logs(root: Path, reporter: Reporter) -> None:
    path = root / "logs" / "results.jsonl"
    if not path.exists():
        reporter.error("results log is missing: logs/results.jsonl")
        return

    domains: Set[str] = set()
    methods: Set[str] = set()
    levels: Set[str] = set()
    seeds: Set[int] = set()
    run_ids: Set[str] = set()
    rows = 0
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            rows += 1
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                reporter.error(f"invalid JSONL in results log line {line_number}: {exc}")
                continue
            run_id = row.get("run_id")
            if isinstance(run_id, str):
                reporter.require(run_id not in run_ids, f"duplicate run_id in results log: {run_id}")
                run_ids.add(run_id)
            domains.add(str(row.get("domain")))
            methods.add(str(row.get("method")))
            ood_shift = row.get("ood_shift", {})
            if isinstance(ood_shift, Mapping):
                levels.add(str(ood_shift.get("level")))
            if isinstance(row.get("seed"), int):
                seeds.add(row["seed"])
            metrics = row.get("metrics", {})
            if isinstance(metrics, Mapping):
                missing_metrics = REQUIRED_METRICS - set(metrics)
                reporter.require(not missing_metrics, f"results log line {line_number} missing metrics: {', '.join(sorted(missing_metrics))}")
            else:
                reporter.error(f"results log line {line_number} metrics field is not an object")

    check_set("result-log domains", domains, REQUIRED_DOMAINS, reporter)
    check_set("result-log methods", methods, REQUIRED_METHODS, reporter)
    reporter.require(FINAL_LEVELS.issubset(levels), f"results log missing OOD levels: {', '.join(sorted(FINAL_LEVELS - levels))}")
    reporter.require(FINAL_SEEDS.issubset(seeds), f"results log missing seeds: {', '.join(str(seed) for seed in sorted(FINAL_SEEDS - seeds))}")
    expected_min_rows = len(REQUIRED_DOMAINS) * len(REQUIRED_METHODS) * len(FINAL_LEVELS) * len(FINAL_SEEDS)
    reporter.require(rows >= expected_min_rows, f"results log has too few rows: {rows} < {expected_min_rows}")
    reporter.note(f"results log coverage verified ({rows} rows)")


def main_table_cell(row: Mapping[str, str], mean_col: str, sem_col: str, scale: float = 1.0) -> str:
    return f"{scale * float(row[mean_col]):.2f} ({scale * float(row[sem_col]):.2f})"


def check_main_table_consistency(root: Path, reporter: Reporter) -> None:
    summary_path = root / "tables" / "summary_by_method.csv"
    rows_path = root / "tables" / "main_results_table_rows.tex"
    try:
        with summary_path.open("r", encoding="utf-8", newline="") as handle:
            summary_rows = list(csv.DictReader(handle))
    except FileNotFoundError:
        reporter.error("summary table is missing: tables/summary_by_method.csv")
        return

    required_columns = {
        "method",
        "cost_mean",
        "cost_sem",
        "violation_rate_mean",
        "violation_rate_sem",
        "observed_risk_mean",
        "observed_risk_sem",
        "freezing_rate_mean",
        "freezing_rate_sem",
        "compute_ms_mean",
        "compute_ms_sem",
    }
    if summary_rows:
        missing_columns = required_columns - set(summary_rows[0])
        reporter.require(not missing_columns, f"summary_by_method.csv missing columns: {', '.join(sorted(missing_columns))}")
    else:
        reporter.error("summary_by_method.csv has no data rows")
        return

    indexed = {row["method"]: row for row in summary_rows}
    missing_methods = [method for method in MAIN_TABLE_METHODS if method not in indexed]
    reporter.require(not missing_methods, f"summary_by_method.csv missing main-table methods: {', '.join(missing_methods)}")
    if missing_methods:
        return

    expected_lines: List[str] = []
    for method in MAIN_TABLE_METHODS:
        row = indexed[method]
        expected_lines.append(
            f"{MAIN_TABLE_DISPLAY[method]} & "
            f"{main_table_cell(row, 'cost_mean', 'cost_sem')} & "
            f"{main_table_cell(row, 'violation_rate_mean', 'violation_rate_sem', 100.0)} & "
            f"{main_table_cell(row, 'observed_risk_mean', 'observed_risk_sem', 100.0)} & "
            f"{main_table_cell(row, 'freezing_rate_mean', 'freezing_rate_sem', 100.0)} & "
            f"{main_table_cell(row, 'compute_ms_mean', 'compute_ms_sem')} \\\\"
        )
    expected_lines.append(r"\bottomrule")

    try:
        actual_lines = rows_path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        reporter.error("generated LaTeX table rows are missing: tables/main_results_table_rows.tex")
        return
    reporter.require(
        actual_lines == expected_lines,
        "main_results_table_rows.tex is not synchronized with summary_by_method.csv",
    )
    reporter.note("main paper table rows match summary_by_method.csv means and SEMs")


def collect_result_code_hashes(root: Path, reporter: Reporter) -> Set[str]:
    path = root / "logs" / "results.jsonl"
    hashes: Set[str] = set()
    if not path.exists():
        reporter.error("cannot collect result code hashes because logs/results.jsonl is missing")
        return hashes
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            artifacts = row.get("artifacts", {})
            if isinstance(artifacts, Mapping):
                code_hash = artifacts.get("code_hash")
                if isinstance(code_hash, str) and code_hash:
                    hashes.add(code_hash)
                else:
                    reporter.error(f"results log line {line_number} missing artifact code_hash")
            else:
                reporter.error(f"results log line {line_number} artifacts field is not an object")
    return hashes


def check_execution_config(root: Path, reporter: Reporter) -> None:
    path = root / "configs" / "execution_config.json"
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        reporter.error("execution config is missing")
        return
    except json.JSONDecodeError as exc:
        reporter.error(f"execution config is not valid JSON: {exc}")
        return

    reporter.require(
        config.get("execution_record_type") == "focused_cpu_run_with_regeneration_metadata",
        "execution config missing focused-run record type",
    )
    args = config.get("args", {})
    run_settings = config.get("run_settings", {})
    regeneration = config.get("regeneration", {})
    reporter.require(isinstance(args, Mapping), "execution config args must be an object")
    reporter.require(isinstance(run_settings, Mapping), "execution config run_settings must be an object")
    reporter.require(isinstance(regeneration, Mapping), "execution config regeneration must be an object")
    if isinstance(args, Mapping):
        reporter.require(args.get("plots_only") is False, "execution config actual run args must not be plots-only")
    if isinstance(run_settings, Mapping):
        reporter.require(
            run_settings.get("plots_only_regeneration") is not True,
            "execution config run_settings must describe the actual run, not plots-only regeneration",
        )
        reporter.require(set(run_settings.get("domains", [])) == REQUIRED_DOMAINS, "execution config domain set mismatch")
        reporter.require(set(run_settings.get("methods", [])) == REQUIRED_METHODS, "execution config method set mismatch")
        reporter.require(set(run_settings.get("levels", [])) == FINAL_LEVELS, "execution config OOD level set mismatch")
        reporter.require(set(run_settings.get("seeds", [])) == FINAL_SEEDS, "execution config seed set mismatch")
        reporter.require(run_settings.get("num_candidates") == 32, "execution config focused run candidate budget mismatch")
        reporter.require(run_settings.get("calibration_contexts") == 36, "execution config focused run calibration-context budget mismatch")
    if isinstance(regeneration, Mapping):
        reporter.require("generated_by_plots_only" in regeneration, "execution config missing regeneration mode")
        if regeneration.get("generated_by_plots_only"):
            source_logs = set(regeneration.get("source_logs", []))
            for required in {
                "logs/results.jsonl",
                "logs/results_flat.csv",
                "logs/step_predictions.csv",
                "logs/calibration_samples.csv",
            }:
                reporter.require(required in source_logs, f"execution config regeneration metadata missing source log: {required}")

    result_hashes = collect_result_code_hashes(root, reporter)
    config_hashes = set(config.get("result_log_code_hashes", []))
    reporter.require(bool(config_hashes), "execution config missing result_log_code_hashes")
    reporter.require(config_hashes == result_hashes, "execution config result_log_code_hashes do not match results.jsonl")
    reporter.require(isinstance(config.get("current_package_code_hash"), str), "execution config missing current_package_code_hash")
    reporter.note("execution config separates focused-run settings from regeneration metadata")


def run_smoke(root: Path, reporter: Reporter) -> None:
    script = root / "skeleton" / "ccr_mpc.py"
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(root),
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        reporter.error(f"CCR smoke test failed:\n{result.stdout}")
    else:
        reporter.note("CCR smoke test passed")

    runner = subprocess.run(
        [sys.executable, str(root / "skeleton" / "run_experiments.py"), "--dry-run", "--limit", "5", "--json"],
        cwd=str(root),
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if runner.returncode != 0:
        reporter.error(f"runner dry-run failed:\n{runner.stdout}")
    else:
        reporter.note("runner dry-run passed")


def check_primary_text(root: Path, reporter: Reporter) -> None:
    plan_text = (root / "COUNTERFACTUAL_CONTROL_RISK_MASTER_PLAN.md").read_text(encoding="utf-8")
    reviewer_text = (root / "REVIEWER_ATTACK_CLOSURE_MATRIX.md").read_text(encoding="utf-8")
    for phrase in [
        "Prediction calibration / low one-step error does not imply low control risk",
        "finite-sample CCR risk guarantee",
        "safe-cost optimality",
    ]:
        reporter.require(phrase in plan_text, f"master plan missing theory phrase: {phrase}")
    for phrase in [
        "Just risk-aware MPPI",
        "Just conformal risk control applied to MPC",
        "Safe but useless/conservative",
        "No real learned dynamics",
    ]:
        reporter.require(phrase in reviewer_text, f"reviewer matrix missing attack: {phrase}")
    reporter.note("primary plan and reviewer matrix include fatal-risk coverage")


def check_completion_audit(root: Path, reporter: Reporter) -> None:
    path = root / "reports" / "completion_audit_report.md"
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        reporter.error("completion audit report is missing")
        return

    for phase in [f"P{index}" for index in range(13)]:
        reporter.require(phase in text, f"completion audit missing phase: {phase}")
    for report in sorted(REQUIRED_REPORTS):
        reporter.require(report in text, f"completion audit missing required-report row: {report}")
    for phrase in [
        "bounded package claim",
        "not as external ICLR submission readiness",
        "full 57,000-row max-out run",
        "Human review remains required",
        "Pack is clean for distribution",
        "Claim evidence files are manifest-hashed",
    ]:
        reporter.require(phrase in text, f"completion audit missing scope/gate phrase: {phrase}")
    reporter.note("completion audit maps phases, required reports, quality gates, and scope caveats")


def check_paper_artifacts(root: Path, reporter: Reporter) -> None:
    tex = root / "paper" / "CCR_MPC_paper.tex"
    pdf = root / "paper" / "CCR_MPC_paper.pdf"
    bib = root / "paper" / "references.bib"
    citation_report = root / "reports" / "citation_verification.md"

    reporter.require(pdf.exists() and pdf.stat().st_size > 100_000, "compiled paper PDF is missing or too small")
    tex_text = tex.read_text(encoding="utf-8")
    bib_text = bib.read_text(encoding="utf-8")
    citation_text = citation_report.read_text(encoding="utf-8")
    for phrase in [
        "CCR-MPC tied the lowest aggregate violation rate",
        "does not dominate CVaR/RA-MPPI",
        "The experiments do not establish hardware safety",
    ]:
        reporter.require(phrase in tex_text, f"paper missing bounded-claim phrase: {phrase}")
    for key in [
        "angelopoulos2024conformalrisk",
        "lekeufack2023conformaldecision",
        "yin2023ramppi",
        "williams2017mppi",
        "chua2018pets",
    ]:
        reporter.require(key in bib_text, f"references.bib missing key: {key}")
        reporter.require(key in citation_text, f"citation verification missing key: {key}")

    manifest_path = root / "reports" / "final_artifact_manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            paper_paths = {entry.get("path") for entry in manifest.get("paper", [])}
            for required in {
                "paper/CCR_MPC_paper.tex",
                "paper/CCR_MPC_paper.pdf",
                "paper/references.bib",
            }:
                reporter.require(required in paper_paths, f"manifest missing paper artifact: {required}")
        except json.JSONDecodeError as exc:
            reporter.error(f"final manifest is not valid JSON during paper check: {exc}")
    reporter.note("paper PDF, TeX, BibTeX, and citation verification are present")


def check_clean_artifacts(root: Path, reporter: Reporter) -> None:
    tmp_dir = root / "tmp"
    reporter.require(not tmp_dir.exists(), "temporary render directory should not be packaged: tmp/")

    pycache_dirs = sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("__pycache__")
        if path.is_dir()
    )
    reporter.require(
        not pycache_dirs,
        "Python bytecode cache directories should not be packaged: " + ", ".join(pycache_dirs),
    )

    paper_dir = root / "paper"
    latex_scratch = sorted(
        path.relative_to(root).as_posix()
        for path in paper_dir.rglob("*")
        if path.is_file() and any(path.name.endswith(suffix) for suffix in LATEX_SCRATCH_SUFFIXES)
    )
    reporter.require(
        not latex_scratch,
        "LaTeX scratch files should not be packaged: " + ", ".join(latex_scratch),
    )

    logs_dir = root / "logs"
    if logs_dir.exists():
        log_entries = sorted(path for path in logs_dir.iterdir())
        unexpected_dirs = [path.name for path in log_entries if path.is_dir()]
        unexpected_files = [
            path.name for path in log_entries if path.is_file() and path.name not in ALLOWED_LOG_FILES
        ]
        reporter.require(not unexpected_dirs, "logs/ contains unexpected directories: " + ", ".join(unexpected_dirs))
        reporter.require(not unexpected_files, "logs/ contains unmanifested files: " + ", ".join(unexpected_files))
    reporter.note("packaged tree is free of scratch artifacts and unmanifested logs")


def verify(root: Path, smoke: bool) -> Reporter:
    reporter = Reporter()
    require_files(root, reporter)
    check_json(root, reporter)
    check_completion_message(root, reporter)
    check_matrix(root, reporter)
    check_tasks_yaml_text(root, reporter)
    check_templates(root, reporter)
    check_no_unsafe_completion(root, reporter)
    check_manifest_integrity(root, reporter)
    check_claim_ledger(root, reporter)
    check_result_logs(root, reporter)
    check_main_table_consistency(root, reporter)
    check_execution_config(root, reporter)
    check_primary_text(root, reporter)
    check_completion_audit(root, reporter)
    check_paper_artifacts(root, reporter)
    if smoke:
        run_smoke(root, reporter)
    check_clean_artifacts(root, reporter)
    return reporter


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify CCR-MPC ICLR CLI pack")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--smoke", action="store_true", help="Run Python smoke tests")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    reporter = verify(root, smoke=args.smoke)
    reporter.print()
    if reporter.errors:
        print(f"PACK VERIFY FAILED: {len(reporter.errors)} error(s), {len(reporter.warnings)} warning(s)")
        return 1
    print(f"PACK VERIFY PASSED: {len(reporter.warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
