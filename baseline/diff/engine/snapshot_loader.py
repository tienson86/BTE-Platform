"""Snapshot loader for baseline diff operations."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from baseline.io_utils import read_json

logger = logging.getLogger(__name__)

CORE_SNAPSHOTS = (
    "baseline_manifest.json",
    "ontology_snapshot.json",
    "registry_snapshot.json",
    "dependency_snapshot.json",
    "compiler_snapshot.json",
    "validation_snapshot.json",
    "knowledge_graph.json",
    "statistics.json",
    "checksums.json",
    "governance_metadata.json",
)


def resolve_baseline_dir(path: Path) -> Path:
    """Resolve a baseline version directory from a path or version label."""
    if path.is_dir() and (path / "baseline_manifest.json").is_file():
        return path.resolve()
    if path.is_dir() and path.name.startswith("v"):
        return path.resolve()
    text = str(path)
    if text.startswith("v"):
        candidate = path
        if candidate.is_dir():
            return candidate.resolve()
    raise FileNotFoundError(f"Baseline directory not found: {path}")


class SnapshotLoader:
    """Load snapshot JSON documents from a baseline version directory."""

    def __init__(self, baseline_dir: Path) -> None:
        """Initialize loader for one baseline directory."""
        self.baseline_dir = resolve_baseline_dir(baseline_dir)

    def load(self, filename: str) -> Any:
        """Load a single snapshot file."""
        path = self.baseline_dir / filename
        if not path.is_file():
            raise FileNotFoundError(path)
        return read_json(path)

    def load_all(self) -> dict[str, Any]:
        """Load all known core snapshots that exist."""
        loaded: dict[str, Any] = {}
        for filename in CORE_SNAPSHOTS:
            path = self.baseline_dir / filename
            if path.is_file():
                loaded[filename] = read_json(path)
            else:
                logger.debug("Snapshot missing: %s", path)
        return loaded

    def available(self) -> list[str]:
        """List available snapshot filenames."""
        return sorted(
            path.name
            for path in self.baseline_dir.glob("*")
            if path.is_file()
        )
