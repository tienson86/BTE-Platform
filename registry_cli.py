#!/usr/bin/env python3
"""BTE Registry CLI — validate, query, export, import, and reindex."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.registry_exporter import RegistryExporter
from services.registry_importer import RegistryImporter
from services.registry_indexer import RegistryIndexer
from services.registry_loader import RegistryLoader
from services.registry_query import RegistryQuery
from services.registry_statistics import RegistryStatistics
from services.registry_sync import RegistrySync
from services.registry_validator import RegistryValidator

logger = logging.getLogger("registry_cli")


def _build_loader(args: argparse.Namespace) -> RegistryLoader:
    return RegistryLoader(
        registry_root=args.registry_root,
        project_root=args.project_root,
    )


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate registry JSON, schema, consistency, and duplicates."""
    loader = _build_loader(args)
    validator = RegistryValidator(loader)
    result = validator.validate_all(
        include_samples=args.include_samples,
        check_schema=not args.skip_schema,
        check_duplicates=not args.skip_duplicates,
        check_consistency=not args.skip_consistency,
    )
    payload = {
        "ok": result.ok,
        "catalogs_checked": result.catalogs_checked,
        "records_checked": result.records_checked,
        "error_count": len(result.errors),
        "warning_count": len(result.warnings),
        "issues": [
            {
                "severity": issue.severity,
                "code": issue.code,
                "message": issue.message,
                "path": issue.path,
                "registry_id": issue.registry_id,
            }
            for issue in result.issues
        ],
    }
    _print_json(payload)
    return 0 if result.ok else 1


def cmd_stats(args: argparse.Namespace) -> int:
    """Print aggregate registry statistics."""
    loader = _build_loader(args)
    stats = RegistryStatistics(loader)
    _print_json(stats.to_dict())
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """List registry records with optional filters."""
    loader = _build_loader(args)
    query = RegistryQuery(loader)
    hits = query.list_records(
        registry_name=args.registry,
        status=args.status,
        namespace=args.namespace,
        limit=args.limit,
    )
    _print_json(
        [
            {
                "registry_name": hit.registry_name,
                "registry_id": hit.registry_id,
                "object_id": hit.object_id,
                "canonical_name": hit.canonical_name,
                "status": hit.status,
            }
            for hit in hits
        ]
    )
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    """Search registry records."""
    loader = _build_loader(args)
    query = RegistryQuery(loader)
    hits = query.search(args.query, limit=args.limit)
    _print_json(
        [
            {
                "registry_name": hit.registry_name,
                "registry_id": hit.registry_id,
                "object_id": hit.object_id,
                "canonical_name": hit.canonical_name,
                "status": hit.status,
                "score": hit.score,
            }
            for hit in hits
        ]
    )
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    """Export catalogs or a bundle."""
    loader = _build_loader(args)
    exporter = RegistryExporter(loader)
    if args.bundle:
        path = exporter.export_bundle(
            args.output,
            include_indexes=args.include_indexes,
        )
    elif args.registry:
        path = exporter.export_catalog(args.registry, args.output)
    else:
        paths = exporter.export_all(
            args.output,
            include_indexes=args.include_indexes,
        )
        _print_json({"written": [str(item) for item in paths]})
        return 0
    _print_json({"written": str(path)})
    return 0


def cmd_import(args: argparse.Namespace) -> int:
    """Import a catalog file or bundle."""
    loader = _build_loader(args)
    importer = RegistryImporter(loader)
    if args.bundle:
        paths = importer.import_bundle(
            args.source,
            dry_run=args.dry_run,
            validate=not args.no_validate,
        )
        _print_json({"imported": [str(item) for item in paths], "dry_run": args.dry_run})
    else:
        path = importer.import_catalog_file(
            args.source,
            registry_name=args.registry,
            dry_run=args.dry_run,
            validate=not args.no_validate,
        )
        _print_json({"imported": str(path), "dry_run": args.dry_run})
    return 0


def cmd_reindex(args: argparse.Namespace) -> int:
    """Rebuild derived indexes and optionally refresh statistics."""
    loader = _build_loader(args)
    sync = RegistrySync(loader, indexer=RegistryIndexer(loader, max_workers=args.workers))
    payload = sync.sync_all(parallel=not args.no_parallel, write=args.write)
    summary = {
        "index_names": sorted(payload["indexes"].keys()),
        "total_records": payload["statistics"]["statistics"]["total_records"],
        "written": args.write,
    }
    _print_json(summary)
    return 0


def _print_json(payload: Any) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    """Build CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="registry_cli",
        description="BTE Registry infrastructure CLI",
    )
    parser.add_argument(
        "--project-root",
        default=str(ROOT),
        help="Repository root (default: current package root)",
    )
    parser.add_argument(
        "--registry-root",
        default=None,
        help="Override knowledge/registry path",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate registry catalogs")
    validate.add_argument("--include-samples", action="store_true")
    validate.add_argument("--skip-schema", action="store_true")
    validate.add_argument("--skip-duplicates", action="store_true")
    validate.add_argument("--skip-consistency", action="store_true")
    validate.set_defaults(func=cmd_validate)

    stats = sub.add_parser("stats", help="Show registry statistics")
    stats.set_defaults(func=cmd_stats)

    list_cmd = sub.add_parser("list", help="List registry records")
    list_cmd.add_argument("--registry", default=None)
    list_cmd.add_argument("--status", default=None)
    list_cmd.add_argument("--namespace", default=None)
    list_cmd.add_argument("--limit", type=int, default=None)
    list_cmd.set_defaults(func=cmd_list)

    search = sub.add_parser("search", help="Search registry records")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=50)
    search.set_defaults(func=cmd_search)

    export = sub.add_parser("export", help="Export registry catalogs")
    export.add_argument("--output", required=True)
    export.add_argument("--registry", default=None)
    export.add_argument("--bundle", action="store_true")
    export.add_argument("--include-indexes", action="store_true")
    export.set_defaults(func=cmd_export)

    import_cmd = sub.add_parser("import", help="Import registry catalogs")
    import_cmd.add_argument("--source", required=True)
    import_cmd.add_argument("--registry", default=None)
    import_cmd.add_argument("--bundle", action="store_true")
    import_cmd.add_argument("--dry-run", action="store_true")
    import_cmd.add_argument("--no-validate", action="store_true")
    import_cmd.set_defaults(func=cmd_import)

    reindex = sub.add_parser("reindex", help="Rebuild indexes and statistics")
    reindex.add_argument("--write", action="store_true")
    reindex.add_argument("--no-parallel", action="store_true")
    reindex.add_argument("--workers", type=int, default=4)
    reindex.set_defaults(func=cmd_reindex)

    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
