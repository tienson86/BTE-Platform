"""CLI for Pack 01 baseline infrastructure."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

from baseline.baseline_builder import BaselineBuilder
from baseline.constants import BASELINE_VERSION, DEFAULT_BUILD_TIMESTAMP
from baseline.diff.engine.baseline_diff import BaselineDiffEngine
from baseline.io_utils import read_json
from baseline.paths import resolve_project_root

logger = logging.getLogger("baseline")


def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def _print_json(payload: Any) -> None:
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")


def cmd_build(args: argparse.Namespace) -> int:
    """Build the full baseline artifact set."""
    builder = BaselineBuilder(
        project_root=Path(args.project_root) if args.project_root else None,
        version=args.version,
        timestamp=args.timestamp,
    )
    summary = builder.build()
    _print_json(summary)
    return 0 if summary.get("overall_status") == "READY_FOR_FREEZE" else 1


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate Pack 01 baseline inputs/outputs."""
    builder = BaselineBuilder(
        project_root=Path(args.project_root) if args.project_root else None,
        version=args.version,
        timestamp=args.timestamp,
    )
    result = builder.validate_only()
    _print_json(result)
    return 0 if result.get("status") == "PASS" else 1


def cmd_diff(args: argparse.Namespace) -> int:
    """Diff two baseline versions."""
    engine = BaselineDiffEngine(
        project_root=Path(args.project_root) if args.project_root else None
    )
    result = engine.compare(
        args.old,
        args.new,
        output_dir=Path(args.output_dir) if args.output_dir else None,
    )
    _print_json(result)
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    """Print existing baseline reports."""
    root = resolve_project_root(
        Path(args.project_root) if args.project_root else None
    )
    version_dir = root / "knowledge" / "baseline" / f"v{args.version}"
    path = version_dir / args.name
    if not path.is_file():
        logger.error("Report not found: %s", path)
        return 1
    text = path.read_text(encoding="utf-8")
    sys.stdout.write(text)
    if not text.endswith("\n"):
        sys.stdout.write("\n")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    """Print baseline statistics."""
    root = resolve_project_root(
        Path(args.project_root) if args.project_root else None
    )
    path = root / "knowledge" / "baseline" / f"v{args.version}" / "statistics.json"
    if not path.is_file():
        logger.error("Statistics not found: %s", path)
        return 1
    _print_json(read_json(path))
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Create the baseline CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="baseline",
        description="BTE Pack 01 Baseline & Freeze Infrastructure CLI",
    )
    parser.add_argument(
        "--project-root",
        default=None,
        help="Optional project root path (defaults to repository root).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    build_p = sub.add_parser("build", help="Generate the full baseline.")
    build_p.add_argument("--version", default=BASELINE_VERSION)
    build_p.add_argument("--timestamp", default=DEFAULT_BUILD_TIMESTAMP)
    build_p.set_defaults(func=cmd_build)

    validate_p = sub.add_parser("validate", help="Run baseline validations.")
    validate_p.add_argument("--version", default=BASELINE_VERSION)
    validate_p.add_argument("--timestamp", default=DEFAULT_BUILD_TIMESTAMP)
    validate_p.set_defaults(func=cmd_validate)

    diff_p = sub.add_parser("diff", help="Compare two baseline versions.")
    diff_p.add_argument("old", help="Old version (e.g. 1.0.0 or path)")
    diff_p.add_argument("new", help="New version (e.g. 1.0.0 or path)")
    diff_p.add_argument("--output-dir", default=None)
    diff_p.set_defaults(func=cmd_diff)

    report_p = sub.add_parser("report", help="Print a baseline report file.")
    report_p.add_argument("--version", default=BASELINE_VERSION)
    report_p.add_argument(
        "--name",
        default="validation_report.md",
        help="Report filename inside knowledge/baseline/vX.Y.Z/",
    )
    report_p.set_defaults(func=cmd_report)

    stats_p = sub.add_parser("stats", help="Print baseline statistics JSON.")
    stats_p.add_argument("--version", default=BASELINE_VERSION)
    stats_p.set_defaults(func=cmd_stats)

    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args(argv)
    _configure_logging(args.verbose)
    return int(args.func(args))
