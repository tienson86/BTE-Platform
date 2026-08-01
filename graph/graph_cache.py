"""Memory and persistent cache for Graph Builder V2."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from graph.constants import BUILDER_VERSION, DEFAULT_TIMESTAMP, SCHEMA_VERSION
from graph.io_utils import read_json, write_json
from graph.models import KnowledgeGraph

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class GraphCache:
    """In-memory + persistent graph cache."""

    memory: dict[str, KnowledgeGraph] = field(default_factory=dict)
    persistent_path: Path | None = None

    def get(self, graph_type: str) -> KnowledgeGraph | None:
        """Return a cached graph by type."""
        return self.memory.get(graph_type)

    def set(self, graph_type: str, graph: KnowledgeGraph) -> None:
        """Store a graph in memory."""
        self.memory[graph_type] = graph

    def clear(self) -> None:
        """Clear memory cache."""
        self.memory.clear()

    def save_persistent(self, path: Path | None = None) -> Path:
        """Persist all cached graphs as JSON."""
        target = path or self.persistent_path
        if target is None:
            raise ValueError("persistent cache path is not configured")
        payload = {
            "artifact": "graph_cache",
            "schema_version": SCHEMA_VERSION,
            "builder_version": BUILDER_VERSION,
            "timestamp": DEFAULT_TIMESTAMP,
            "graphs": {
                key: graph.to_dict() for key, graph in sorted(self.memory.items())
            },
        }
        write_json(target, payload)
        self.persistent_path = target
        logger.info("Persisted graph cache (%s graphs) to %s", len(self.memory), target)
        return target

    def load_persistent(self, path: Path | None = None) -> int:
        """Load persistent cache into memory."""
        target = path or self.persistent_path
        if target is None or not target.is_file():
            return 0
        payload = read_json(target)
        graphs = payload.get("graphs", {})
        if not isinstance(graphs, dict):
            return 0
        loaded = 0
        for key, value in graphs.items():
            if isinstance(value, dict):
                self.memory[key] = KnowledgeGraph.from_dict(value)
                loaded += 1
        self.persistent_path = target
        return loaded
