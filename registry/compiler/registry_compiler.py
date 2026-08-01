"""Registry Compiler orchestrator."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

from registry.compiler.constants import (
    COMPILER_VERSION,
    DEFAULT_TIMESTAMP,
    GENERATED_ROOT_REL,
    OUTPUT_FILES,
    SCHEMA_VERSION,
)
from registry.compiler.io_utils import relative_posix, write_json, write_text
from registry.compiler.registry_cache import RegistryCache
from registry.compiler.registry_indexer import RegistryIndexer
from registry.compiler.registry_loader import RegistryLoader
from registry.compiler.registry_manifest import build_compiler_manifest

logger = logging.getLogger(__name__)


class RegistryCompiler:
    """Compile read-only registry sources into generated indexes and reports."""

    def __init__(
        self,
        project_root: Path | None = None,
        *,
        timestamp: str | None = None,
    ) -> None:
        """Initialize compiler with project root and deterministic timestamp."""
        self.project_root = (
            project_root.resolve()
            if project_root is not None
            else Path(__file__).resolve().parents[2]
        )
        self.timestamp = (
            timestamp
            or os.environ.get("SOURCE_DATE_EPOCH_ISO")
            or DEFAULT_TIMESTAMP
        )
        self.generated_root = self.project_root / GENERATED_ROOT_REL
        self.loader = RegistryLoader(self.project_root)
        self.indexer = RegistryIndexer()
        self.cache = RegistryCache(
            persistent_path=self.generated_root / "cache" / "registry_cache.json"
        )

    def compile(self) -> dict[str, Any]:
        """Run the full registry compile pipeline and write artifacts."""
        logger.info("Starting registry compile at %s", self.timestamp)
        self.generated_root.mkdir(parents=True, exist_ok=True)
        (self.generated_root / "indexes").mkdir(parents=True, exist_ok=True)
        (self.generated_root / "reports").mkdir(parents=True, exist_ok=True)
        (self.generated_root / "cache").mkdir(parents=True, exist_ok=True)

        loaded = self.loader.load_all()
        indexed = self.indexer.build_all(
            loaded["domains"],
            loaded["auxiliary"],
            loaded["sidecars"],
            loaded["ontology"],
        )

        statistics = self._build_statistics(loaded, indexed)
        registry_index = {
            "artifact": "registry_index",
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
            "timestamp": self.timestamp,
            "domains": [
                {
                    "name": item.name,
                    "path": item.path,
                    "version": item.version,
                    "checksum": item.checksum,
                    "record_count": len(item.records),
                }
                for item in loaded["domains"]
            ],
            "indexes": {
                "id": "indexes/id_index.json",
                "name": "indexes/name_index.json",
                "category": "indexes/category_index.json",
                "ontology": "indexes/ontology_index.json",
                "dependency": "indexes/dependency_index.json",
                "relationship": "indexes/relationship_index.json",
            },
            "object_count": len(indexed["objects"]),
            "objects": indexed["objects"],
            "statistics": statistics,
        }
        lookup = {
            "artifact": "registry_lookup",
            "schema_version": SCHEMA_VERSION,
            "timestamp": self.timestamp,
            "count": len(indexed["lookup"]),
            "lookup": indexed["lookup"],
        }
        reverse_lookup = {
            "artifact": "registry_reverse_lookup",
            "schema_version": SCHEMA_VERSION,
            "timestamp": self.timestamp,
            "count": len(indexed["reverse_lookup"]),
            "reverse_lookup": indexed["reverse_lookup"],
        }
        statistics_doc = {
            "artifact": "registry_statistics",
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
            "timestamp": self.timestamp,
            **statistics,
        }

        written: dict[str, str] = {}
        written["registry_index.json"] = self._write(
            "registry_index.json", registry_index
        )
        written["registry_lookup.json"] = self._write(
            "registry_lookup.json", lookup
        )
        written["registry_reverse_lookup.json"] = self._write(
            "registry_reverse_lookup.json", reverse_lookup
        )
        written["registry_statistics.json"] = self._write(
            "registry_statistics.json", statistics_doc
        )

        index_payloads = {
            "indexes/id_index.json": {
                "artifact": "id_index",
                "count": len(indexed["indexes"]["id_index"]),
                "entries": indexed["indexes"]["id_index"],
            },
            "indexes/name_index.json": {
                "artifact": "name_index",
                "count": len(indexed["indexes"]["name_index"]),
                "entries": indexed["indexes"]["name_index"],
            },
            "indexes/category_index.json": {
                "artifact": "category_index",
                "count": len(indexed["indexes"]["category_index"]),
                "entries": indexed["indexes"]["category_index"],
            },
            "indexes/ontology_index.json": {
                "artifact": "ontology_index",
                **indexed["indexes"]["ontology_index"],
            },
            "indexes/dependency_index.json": {
                "artifact": "dependency_index",
                **indexed["indexes"]["dependency_index"],
            },
            "indexes/relationship_index.json": {
                "artifact": "relationship_index",
                **indexed["indexes"]["relationship_index"],
            },
        }
        for rel, payload in index_payloads.items():
            written[rel] = self._write(rel, payload)

        # Cache layers.
        self.cache.set("registry_index", registry_index, checksum=written["registry_index.json"])
        self.cache.set("lookup", lookup, checksum=written["registry_lookup.json"])
        self.cache.set(
            "reverse_lookup",
            reverse_lookup,
            checksum=written["registry_reverse_lookup.json"],
        )
        self.cache.set("statistics", statistics_doc, checksum=written["registry_statistics.json"])
        self.cache.set("version_snapshot", self.cache.version_snapshot())
        cache_path = self.cache.save_persistent()
        written["cache/registry_cache.json"] = relative_posix(
            cache_path, self.project_root
        )

        reports = {
            "reports/registry_build_report.md": self._build_report(
                written, statistics
            ),
            "reports/registry_statistics.md": self._statistics_report(statistics),
            "reports/registry_inventory.md": self._inventory_report(loaded, indexed),
        }
        for rel, text in reports.items():
            path = self.generated_root / rel
            write_text(path, text)
            written[rel] = relative_posix(path, self.project_root)

        # Also mirror top-level report names requested by the sprint.
        for name in (
            "registry_build_report.md",
            "registry_statistics.md",
            "registry_inventory.md",
        ):
            source = self.generated_root / "reports" / name
            target = self.generated_root / name
            write_text(target, source.read_text(encoding="utf-8"))
            written[name] = relative_posix(target, self.project_root)

        manifest = build_compiler_manifest(
            timestamp=self.timestamp,
            domains=loaded["domains"],
            auxiliary=loaded["auxiliary"],
            sidecars=loaded["sidecars"],
            output_files=written,
            statistics=statistics,
        )
        written["registry_compiler_manifest.json"] = self._write(
            "registry_compiler_manifest.json", manifest
        )

        summary = {
            "status": "COMPILER_READY",
            "compiler_version": COMPILER_VERSION,
            "timestamp": self.timestamp,
            "output_dir": relative_posix(self.generated_root, self.project_root),
            "artifact_count": len(written),
            "artifacts": sorted(written.keys()),
            "statistics": statistics,
            "expected_outputs": list(OUTPUT_FILES),
        }
        write_json(self.generated_root / "compile_summary.json", summary)
        logger.info(
            "Registry compile complete: %s artifacts", len(written)
        )
        return summary

    def _write(self, relative: str, payload: dict[str, Any]) -> str:
        path = self.generated_root / relative
        write_json(path, payload)
        return relative_posix(path, self.project_root)

    def _build_statistics(
        self,
        loaded: dict[str, Any],
        indexed: dict[str, Any],
    ) -> dict[str, Any]:
        domains = loaded["domains"]
        return {
            "domain_count": len(domains),
            "auxiliary_catalog_count": len(loaded["auxiliary"]),
            "sidecar_index_count": len(loaded["sidecars"]),
            "total_domain_records": sum(len(item.records) for item in domains),
            "indexed_object_count": len(indexed["objects"]),
            "id_index_count": len(indexed["indexes"]["id_index"]),
            "name_index_count": len(indexed["indexes"]["name_index"]),
            "category_index_count": len(indexed["indexes"]["category_index"]),
            "ontology_class_count": indexed["indexes"]["ontology_index"]["statistics"][
                "class_count"
            ],
            "dependency_edge_count": indexed["indexes"]["dependency_index"][
                "edge_count"
            ],
            "relationship_count": indexed["indexes"]["relationship_index"][
                "relationship_count"
            ],
            "lookup_count": len(indexed["lookup"]),
            "reverse_lookup_count": len(indexed["reverse_lookup"]),
            "by_domain": {
                item.name: len(item.records) for item in domains
            },
        }

    def _build_report(
        self,
        written: dict[str, str],
        statistics: dict[str, Any],
    ) -> str:
        lines = [
            "# Registry Build Report",
            "",
            f"- Compiler version: `{COMPILER_VERSION}`",
            f"- Timestamp: `{self.timestamp}`",
            f"- Status: `COMPILER_READY`",
            "",
            "## Artifacts",
            "",
        ]
        for name in sorted(written):
            lines.append(f"- `{name}`")
        lines.extend(
            [
                "",
                "## Statistics",
                "",
                f"- Domains: `{statistics['domain_count']}`",
                f"- Indexed objects: `{statistics['indexed_object_count']}`",
                f"- ID index: `{statistics['id_index_count']}`",
                f"- Name index: `{statistics['name_index_count']}`",
                f"- Category index: `{statistics['category_index_count']}`",
                f"- Ontology classes: `{statistics['ontology_class_count']}`",
                f"- Dependency edges: `{statistics['dependency_edge_count']}`",
                f"- Relationships: `{statistics['relationship_count']}`",
                "",
                "## Policy",
                "",
                "- Knowledge Records were not modified.",
                "- Registry source contents were not modified.",
                "- Only generated indexes and compiler artifacts were written.",
                "",
            ]
        )
        return "\n".join(lines)

    def _statistics_report(self, statistics: dict[str, Any]) -> str:
        lines = [
            "# Registry Statistics",
            "",
            f"- Timestamp: `{self.timestamp}`",
            "",
            "| Metric | Value |",
            "|---|---:|",
        ]
        for key in sorted(statistics):
            value = statistics[key]
            if isinstance(value, dict):
                continue
            lines.append(f"| {key} | {value} |")
        lines.extend(["", "## Records by Domain", "", "| Domain | Records |", "|---|---:|"])
        for domain, count in sorted(statistics.get("by_domain", {}).items()):
            lines.append(f"| {domain} | {count} |")
        lines.append("")
        return "\n".join(lines)

    def _inventory_report(
        self,
        loaded: dict[str, Any],
        indexed: dict[str, Any],
    ) -> str:
        lines = [
            "# Registry Inventory",
            "",
            f"- Timestamp: `{self.timestamp}`",
            "",
            "## Domain Catalogs",
            "",
            "| Registry | Path | Version | Records | Checksum |",
            "|---|---|---|---:|---|",
        ]
        for item in loaded["domains"]:
            lines.append(
                f"| {item.name} | `{item.path}` | {item.version} | "
                f"{len(item.records)} | `{item.checksum[:12]}…` |"
            )
        lines.extend(
            [
                "",
                "## Indexed Object Kinds",
                "",
            ]
        )
        kind_counts: dict[str, int] = {}
        for obj in indexed["objects"]:
            kind = str(obj.get("kind") or "unknown")
            kind_counts[kind] = kind_counts.get(kind, 0) + 1
        lines.extend(["| Kind | Count |", "|---|---:|"])
        for kind, count in sorted(kind_counts.items()):
            lines.append(f"| {kind} | {count} |")
        lines.append("")
        return "\n".join(lines)


def compile_registry(
    project_root: Path | None = None,
    *,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Convenience API to compile registry artifacts."""
    return RegistryCompiler(
        project_root=project_root,
        timestamp=timestamp,
    ).compile()
