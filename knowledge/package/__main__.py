"""CLI: python -m knowledge.package build|validate|import."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from knowledge.package.package_builder import PackageBuilder
from knowledge.package.package_validator import PackageValidator


def main(argv: list[str] | None = None) -> int:
    """Knowledge package CLI entrypoint."""
    parser = argparse.ArgumentParser(
        prog="knowledge.package",
        description="BTE Knowledge Package Builder",
    )
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    build_p = sub.add_parser("build", help="Build a distributable pack.")
    build_p.add_argument("--pack-id", default="PACK_01")
    build_p.add_argument("--version", default=None)
    build_p.add_argument("--timestamp", default=None)

    validate_p = sub.add_parser("validate", help="Validate a package dir or archive.")
    validate_p.add_argument("path")

    import_p = sub.add_parser("import", help="Import/extract a package archive.")
    import_p.add_argument("archive")
    import_p.add_argument("--dest", default=None)

    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    root = Path(args.project_root) if args.project_root else None
    builder = PackageBuilder(project_root=root)

    if args.command == "build":
        if args.timestamp:
            builder.timestamp = args.timestamp
        summary = builder.build(args.pack_id, version=args.version)
        json.dump(summary, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0 if summary.get("status") == "PACKAGE_READY" else 1

    if args.command == "validate":
        path = Path(args.path)
        validator = PackageValidator()
        result = (
            validator.validate_directory(path)
            if path.is_dir()
            else validator.validate_archive(path)
        )
        json.dump(result.to_dict(), sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0 if result.ok else 1

    if args.command == "import":
        dest = Path(args.dest) if args.dest else None
        result = builder.import_package(Path(args.archive), dest)
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0 if result["validation"]["ok"] else 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
