"""Production Knowledge Graph Builder V2 orchestrator."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

from graph.constants import (
    BUILDER_VERSION,
    DEFAULT_TIMESTAMP,
    EXPORT_FORMATS,
    GRAPH_TYPES,
    OUTPUT_REL,
    SCHEMA_VERSION,
)
from graph.edge_builder import EdgeBuilder
from graph.graph_cache import GraphCache
from graph.graph_exporter import GraphExporter
from graph.graph_optimizer import GraphOptimizer
from graph.io_utils import relative_posix, sha256_file, write_json, write_text
from graph.models import KnowledgeGraph
from graph.node_builder import NodeBuilder
from graph.validator import GraphValidator

logger = logging.getLogger(__name__)


class GraphBuilder:
    """Build, optimize, validate, cache, and export all Pack 01 graph types."""

    def __init__(
        self,
        project_root: Path | None = None,
        *,
        timestamp: str | None = None,
    ) -> None:
        """Initialize builder with deterministic timestamp."""
        self.project_root = (
            project_root.resolve()
            if project_root is not None
            else Path(__file__).resolve().parent.parent
        )
        self.timestamp = (
            timestamp
            or os.environ.get("SOURCE_DATE_EPOCH_ISO")
            or DEFAULT_TIMESTAMP
        )
        self.output_dir = self.project_root / OUTPUT_REL
        self.node_builder = NodeBuilder(self.project_root)
        self.edge_builder = EdgeBuilder(self.project_root)
        self.optimizer = GraphOptimizer()
        self.exporter = GraphExporter()
        self.validator = GraphValidator()
        self.cache = GraphCache(
            persistent_path=self.output_dir / "cache" / "graph_cache.json"
        )

    def build_all(self) -> dict[str, Any]:
        """Build all five graphs and write all export formats + metadata."""
        logger.info("Building Graph V2 artifacts at %s", self.timestamp)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "cache").mkdir(parents=True, exist_ok=True)

        graphs = {
            "academic_graph": self.build_academic_graph(),
            "ontology_graph": self.build_ontology_graph(),
            "dependency_graph": self.build_dependency_graph(),
            "registry_graph": self.build_registry_graph(),
            "runtime_graph": self.build_runtime_graph(),
        }

        written: dict[str, str] = {}
        validations: dict[str, Any] = {}
        for graph_type, graph in graphs.items():
            optimized = self.optimizer.optimize(graph)
            validation = self.validator.validate(optimized, check_cycles=False)
            validations[graph_type] = validation.to_dict()
            self.cache.set(graph_type, optimized)
            exports = self.exporter.export_all(optimized)
            for fmt, text in exports.items():
                filename = f"{graph_type}.{fmt if fmt != 'mmd' else 'mmd'}"
                # normalize extension names
                ext = {
                    "json": "json",
                    "graphml": "graphml",
                    "dot": "dot",
                    "mmd": "mmd",
                    "jsonld": "jsonld",
                }[fmt]
                path = self.output_dir / f"{graph_type}.{ext}"
                write_text(path, text)
                written[f"{graph_type}.{ext}"] = relative_posix(
                    path, self.project_root
                )

        self.cache.save_persistent()
        written["cache/graph_cache.json"] = relative_posix(
            self.cache.persistent_path, self.project_root  # type: ignore[arg-type]
        )

        statistics = self._build_statistics(graphs, validations)
        inventory = self._build_inventory(written, graphs)
        manifest = self._build_manifest(written, statistics, validations)

        written["graph_statistics.json"] = relative_posix(
            self._write_json("graph_statistics.json", statistics),
            self.project_root,
        )
        written["graph_inventory.json"] = relative_posix(
            self._write_json("graph_inventory.json", inventory),
            self.project_root,
        )
        written["graph_manifest.json"] = relative_posix(
            self._write_json("graph_manifest.json", manifest),
            self.project_root,
        )
        written["graph_validation.json"] = relative_posix(
            self._write_json("graph_validation.json", validations),
            self.project_root,
        )

        summary = {
            "status": "GRAPH_BUILDER_READY",
            "builder_version": BUILDER_VERSION,
            "timestamp": self.timestamp,
            "output_dir": relative_posix(self.output_dir, self.project_root),
            "graph_types": list(GRAPH_TYPES),
            "export_formats": list(EXPORT_FORMATS),
            "artifact_count": len(written),
            "artifacts": sorted(written.keys()),
            "statistics": statistics,
            "validation_ok": all(item.get("ok") for item in validations.values()),
        }
        write_json(self.output_dir / "build_summary.json", summary)
        logger.info(
            "Graph V2 build complete: %s artifacts, validation_ok=%s",
            len(written),
            summary["validation_ok"],
        )
        return summary

    def build_academic_graph(self) -> KnowledgeGraph:
        """Build academic knowledge graph."""
        return KnowledgeGraph(
            graph_id="GRAPH-ACAD-000001",
            graph_type="academic_graph",
            title="Pack 01 Academic Graph",
            nodes=self.node_builder.academic_nodes(),
            edges=self.edge_builder.academic_edges(),
            timestamp=self.timestamp,
            metadata={"pack_id": "PACK_01"},
        )

    def build_ontology_graph(self) -> KnowledgeGraph:
        """Build ontology hierarchy graph."""
        return KnowledgeGraph(
            graph_id="GRAPH-ONT-000001",
            graph_type="ontology_graph",
            title="Pack 01 Ontology Graph",
            nodes=self.node_builder.ontology_nodes(),
            edges=self.edge_builder.ontology_edges(),
            timestamp=self.timestamp,
        )

    def build_dependency_graph(self) -> KnowledgeGraph:
        """Build dependency graph."""
        return KnowledgeGraph(
            graph_id="GRAPH-DEP-000001",
            graph_type="dependency_graph",
            title="Pack 01 Dependency Graph",
            nodes=self.node_builder.dependency_nodes(),
            edges=self.edge_builder.dependency_edges(),
            timestamp=self.timestamp,
        )

    def build_registry_graph(self) -> KnowledgeGraph:
        """Build registry graph."""
        return KnowledgeGraph(
            graph_id="GRAPH-REG-000001",
            graph_type="registry_graph",
            title="Pack 01 Registry Graph",
            nodes=self.node_builder.registry_nodes(),
            edges=self.edge_builder.registry_edges(),
            timestamp=self.timestamp,
        )

    def build_runtime_graph(self) -> KnowledgeGraph:
        """Build runtime/compiler graph."""
        return KnowledgeGraph(
            graph_id="GRAPH-RT-000001",
            graph_type="runtime_graph",
            title="Pack 01 Runtime Graph",
            nodes=self.node_builder.runtime_nodes(),
            edges=self.edge_builder.runtime_edges(),
            timestamp=self.timestamp,
        )

    def _write_json(self, filename: str, payload: dict[str, Any]) -> Path:
        path = self.output_dir / filename
        write_json(path, payload)
        return path

    def _build_statistics(
        self,
        graphs: dict[str, KnowledgeGraph],
        validations: dict[str, Any],
    ) -> dict[str, Any]:
        by_type = {
            name: {
                "node_count": len(graph.nodes),
                "edge_count": len(graph.edges),
                "validation_ok": validations.get(name, {}).get("ok", False),
            }
            for name, graph in sorted(graphs.items())
        }
        return {
            "artifact": "graph_statistics",
            "schema_version": SCHEMA_VERSION,
            "builder_version": BUILDER_VERSION,
            "timestamp": self.timestamp,
            "graph_count": len(graphs),
            "total_nodes": sum(len(g.nodes) for g in graphs.values()),
            "total_edges": sum(len(g.edges) for g in graphs.values()),
            "by_type": by_type,
            "export_formats": list(EXPORT_FORMATS),
        }

    def _build_inventory(
        self,
        written: dict[str, str],
        graphs: dict[str, KnowledgeGraph],
    ) -> dict[str, Any]:
        files = []
        for name, rel in sorted(written.items()):
            path = self.project_root / rel
            files.append(
                {
                    "name": name,
                    "path": rel,
                    "exists": path.is_file(),
                    "sha256": sha256_file(path) if path.is_file() else "",
                    "size_bytes": path.stat().st_size if path.is_file() else 0,
                }
            )
        return {
            "artifact": "graph_inventory",
            "schema_version": SCHEMA_VERSION,
            "timestamp": self.timestamp,
            "graph_types": {
                name: {
                    "graph_id": graph.graph_id,
                    "node_count": len(graph.nodes),
                    "edge_count": len(graph.edges),
                }
                for name, graph in sorted(graphs.items())
            },
            "files": files,
        }

    def _build_manifest(
        self,
        written: dict[str, str],
        statistics: dict[str, Any],
        validations: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "artifact": "graph_manifest",
            "schema_version": SCHEMA_VERSION,
            "builder_version": BUILDER_VERSION,
            "timestamp": self.timestamp,
            "graph_types": list(GRAPH_TYPES),
            "export_formats": list(EXPORT_FORMATS),
            "outputs": written,
            "statistics": statistics,
            "validation": {
                name: {"ok": payload.get("ok"), "finding_count": len(payload.get("findings", []))}
                for name, payload in sorted(validations.items())
            },
            "compiler_ready": all(payload.get("ok") for payload in validations.values()),
        }


def build_all_graphs(
    project_root: Path | None = None,
    *,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Convenience API to build all Graph V2 artifacts."""
    return GraphBuilder(project_root=project_root, timestamp=timestamp).build_all()
