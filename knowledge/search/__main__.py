"""CLI: python -m knowledge.search build|search."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from knowledge.search.search_engine import SearchEngine


def main(argv: list[str] | None = None) -> int:
    """Knowledge search CLI entrypoint."""
    parser = argparse.ArgumentParser(
        prog="knowledge.search",
        description="BTE Knowledge Search Engine",
    )
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    build_p = sub.add_parser("build", help="Build search index artifacts.")
    build_p.add_argument("--timestamp", default=None)

    search_p = sub.add_parser("search", help="Run a search query.")
    search_p.add_argument("query")
    search_p.add_argument("--mode", default="exact")
    search_p.add_argument("--kind", default=None)
    search_p.add_argument("--limit", type=int, default=50)

    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    root = Path(args.project_root) if args.project_root else None
    engine = SearchEngine(project_root=root)

    if args.command == "build":
        if args.timestamp:
            engine.timestamp = args.timestamp
        summary = engine.build_index()
        json.dump(summary, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0 if summary.get("status") == "SEARCH_READY" else 1

    if args.command == "search":
        engine.load_index()
        result = engine.search(
            args.query,
            mode=args.mode,
            kind=args.kind,
            limit=args.limit,
        )
        json.dump(result.to_dict(), sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
