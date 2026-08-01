"""CLI: python -m graph build."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from graph.builder import GraphBuilder


def main(argv: list[str] | None = None) -> int:
    """Graph Builder V2 CLI entrypoint."""
    parser = argparse.ArgumentParser(
        prog="graph",
        description="BTE Knowledge Graph Builder V2",
    )
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)
    build_p = sub.add_parser("build", help="Build all graph artifacts.")
    build_p.add_argument("--timestamp", default=None)
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    if args.command == "build":
        builder = GraphBuilder(
            project_root=Path(args.project_root) if args.project_root else None,
            timestamp=args.timestamp,
        )
        summary = builder.build_all()
        json.dump(summary, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0 if summary.get("validation_ok") else 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
