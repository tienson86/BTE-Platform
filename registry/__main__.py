"""CLI for Registry Compiler: python -m registry compile."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from registry.compiler.registry_compiler import RegistryCompiler


def main(argv: list[str] | None = None) -> int:
    """Registry compiler CLI entrypoint."""
    parser = argparse.ArgumentParser(
        prog="registry",
        description="BTE Registry Compiler — generate indexes and reports only.",
    )
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    compile_p = sub.add_parser("compile", help="Compile registry indexes.")
    compile_p.add_argument("--timestamp", default=None)

    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    if args.command == "compile":
        compiler = RegistryCompiler(
            project_root=Path(args.project_root) if args.project_root else None,
            timestamp=args.timestamp,
        )
        summary = compiler.compile()
        json.dump(summary, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0 if summary.get("status") == "COMPILER_READY" else 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
