#!/usr/bin/env python3
"""BTE Knowledge CLI — validate, list, search, stats, graph, export."""

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

from services.knowledge.dependency_index import DependencyIndex
from services.knowledge.knowledge_index import KnowledgeIndex
from services.knowledge.knowledge_loader import KnowledgeLoader
from services.knowledge.knowledge_validator import KnowledgeValidator
from services.knowledge.relationship_index import RelationshipIndex
from services.knowledge.search_index import SearchIndex

logger = logging.getLogger("knowledge_cli")


def _loader(args: argparse.Namespace) -> KnowledgeLoader:
    return KnowledgeLoader(
        project_root=args.project_root,
        canon_root=args.canon_root,
        schema_root=args.schema_root,
    )


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate foundation schemas and knowledge records."""
    loader = _loader(args)
    result = KnowledgeValidator(loader).validate_all(
        check_foundation_schemas=not args.skip_foundation,
        check_schema=not args.skip_schema,
        check_relationships=not args.skip_relationships,
        check_references=not args.skip_references,
        check_integrity=not args.skip_integrity,
    )
    _print(
        {
            "ok": result.ok,
            "schemas_checked": result.schemas_checked,
            "records_checked": result.records_checked,
            "error_count": len(result.errors),
            "warning_count": len(result.warnings),
            "issues": [
                {
                    "severity": issue.severity,
                    "code": issue.code,
                    "message": issue.message,
                    "path": issue.path,
                    "knowledge_id": issue.knowledge_id,
                }
                for issue in result.issues
            ],
        }
    )
    return 0 if result.ok else 1


def cmd_list(args: argparse.Namespace) -> int:
    """List knowledge records."""
    loader = _loader(args)
    records = loader.load_records(args.domain)
    index = KnowledgeIndex().build(records)
    ids = index.list_ids(domain_dir=args.domain, status=args.status)
    if args.limit is not None:
        ids = ids[: args.limit]
    rows = []
    for knowledge_id in ids:
        record = index.get(knowledge_id)
        if record is None:
            continue
        identity = record.data.get("identity", {})
        metadata = record.data.get("metadata", {})
        rows.append(
            {
                "knowledge_id": knowledge_id,
                "domain_dir": record.domain_dir,
                "canonical_name": (
                    str(identity.get("canonical_name", ""))
                    if isinstance(identity, dict)
                    else ""
                ),
                "status": (
                    str(metadata.get("status", ""))
                    if isinstance(metadata, dict)
                    else ""
                ),
                "path": record.path,
            }
        )
    _print(rows)
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    """Search knowledge records."""
    loader = _loader(args)
    hits = SearchIndex().build(loader.load_records()).search(
        args.query,
        limit=args.limit,
    )
    _print(
        [
            {
                "knowledge_id": hit.knowledge_id,
                "domain": hit.domain,
                "canonical_name": hit.canonical_name,
                "status": hit.status,
                "score": hit.score,
                "path": hit.path,
            }
            for hit in hits
        ]
    )
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    """Print knowledge statistics."""
    loader = _loader(args)
    stats = loader.stats()
    _print(
        {
            "total_records": stats.total_records,
            "schema_count": stats.schema_count,
            "by_domain": stats.by_domain,
            "by_status": stats.by_status,
            "generated_at": stats.generated_at,
        }
    )
    return 0


def cmd_graph(args: argparse.Namespace) -> int:
    """Print dependency / relationship graphs."""
    loader = _loader(args)
    records = loader.load_records()
    dep = DependencyIndex().build(records)
    rel = RelationshipIndex().build(records)
    payload: dict[str, Any] = {
        "dependencies": dep.graph(),
    }
    if args.include_relationships:
        payload["relationships"] = {
            key: value for key, value in rel.by_type.items()
        }
    if args.knowledge_id:
        payload["node"] = {
            "knowledge_id": args.knowledge_id,
            "dependencies": dep.dependencies_of(args.knowledge_id),
            "dependents": dep.dependents_of(args.knowledge_id),
            "edges": rel.edges_for(args.knowledge_id),
        }
    _print(payload)
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    """Export knowledge bundle to a JSON file."""
    loader = _loader(args)
    bundle = loader.export_bundle()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(bundle, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    _print({"written": str(out), "records": len(bundle["records"])})
    return 0


def _print(payload: Any) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser."""
    parser = argparse.ArgumentParser(
        prog="knowledge_cli",
        description="BTE Knowledge infrastructure CLI",
    )
    parser.add_argument("--project-root", default=str(ROOT))
    parser.add_argument("--canon-root", default=None)
    parser.add_argument("--schema-root", default=None)
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate schemas and records")
    validate.add_argument("--skip-foundation", action="store_true")
    validate.add_argument("--skip-schema", action="store_true")
    validate.add_argument("--skip-relationships", action="store_true")
    validate.add_argument("--skip-references", action="store_true")
    validate.add_argument("--skip-integrity", action="store_true")
    validate.set_defaults(func=cmd_validate)

    list_cmd = sub.add_parser("list", help="List knowledge records")
    list_cmd.add_argument("--domain", default=None)
    list_cmd.add_argument("--status", default=None)
    list_cmd.add_argument("--limit", type=int, default=None)
    list_cmd.set_defaults(func=cmd_list)

    search = sub.add_parser("search", help="Search knowledge records")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=50)
    search.set_defaults(func=cmd_search)

    stats = sub.add_parser("stats", help="Show knowledge statistics")
    stats.set_defaults(func=cmd_stats)

    graph = sub.add_parser("graph", help="Show dependency/relationship graph")
    graph.add_argument("--knowledge-id", default=None)
    graph.add_argument("--include-relationships", action="store_true")
    graph.set_defaults(func=cmd_graph)

    export = sub.add_parser("export", help="Export knowledge bundle JSON")
    export.add_argument("--output", required=True)
    export.set_defaults(func=cmd_export)
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
