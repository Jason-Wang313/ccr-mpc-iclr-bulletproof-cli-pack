"""
CCR-MPC experiment runner entrypoint.

This is a safe CLI scaffold. It validates the pack and enumerates the experiment
matrix without pretending that full experiments have run. A research agent should
replace `run_one_job` with domain implementations while preserving the logging
schema, matrix semantics, and completion gate.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "matrices" / "experiment_matrix_maxout.csv"
COMPLETION_MESSAGE = (
    "ICLR CCR-MPC COMPLETE: bounded theory proofs, counterfactual-risk algorithms, "
    "calibration code, CPU experiment suite, baselines, ablations, plots, paper "
    "manuscript, related-work audit, and reviewer-defense reports are finished. "
    "All claims are backed by generated artifacts. Human review is required "
    "before submission."
)


def read_matrix(path: Path = MATRIX_PATH) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def summarize_matrix(rows: Iterable[Dict[str, str]]) -> Dict[str, object]:
    rows = list(rows)
    return {
        "rows": len(rows),
        "domains": sorted({row["domain"] for row in rows}),
        "methods": sorted({row["method"] for row in rows}),
        "planners": sorted({row["planner"] for row in rows}),
        "priorities": dict(sorted(Counter(row["priority"] for row in rows).items())),
        "seeds": sorted({int(row["seed"]) for row in rows}),
    }


def run_pack_verifier() -> int:
    verifier = ROOT / "scripts" / "verify_pack.py"
    return subprocess.call([sys.executable, str(verifier), "--root", str(ROOT), "--smoke"])


def run_one_job(row: Dict[str, str]) -> None:
    raise RuntimeError(
        "Implement domain dynamics, planner, baseline, logging, and plotting for: "
        f"{row['domain']} / {row['method']} / {row['ood_shift']} / {row['level']} / seed {row['seed']}"
    )


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CCR-MPC CPU experiment scaffold")
    parser.add_argument("--matrix", type=Path, default=MATRIX_PATH)
    parser.add_argument("--verify-pack", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0, help="Maximum jobs to enumerate or run; 0 means all")
    parser.add_argument("--json", action="store_true", help="Print matrix summary as JSON")
    args = parser.parse_args(argv)

    if args.verify_pack:
        return run_pack_verifier()

    rows = read_matrix(args.matrix)
    if args.limit > 0:
        rows = rows[: args.limit]

    summary = summarize_matrix(rows)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print("CCR-MPC matrix loaded")
        print(f"rows: {summary['rows']}")
        print(f"domains: {', '.join(summary['domains'])}")
        print(f"methods: {', '.join(summary['methods'])}")
        print(f"planners: {', '.join(summary['planners'])}")
        print(f"priorities: {summary['priorities']}")

    if args.dry_run:
        print("dry-run only: no experiment results were generated")
        return 0

    for row in rows:
        run_one_job(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
