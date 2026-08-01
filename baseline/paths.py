"""Path resolution helpers for Pack 01 baseline."""

from __future__ import annotations

from pathlib import Path

from baseline.constants import (
    BASELINE_OUTPUT_REL_DIR,
    COMPILER_GENERATED_REL_DIR,
    COMPILER_REL_DIR,
    DEPENDENCY_REL_DIR,
    GOVERNANCE_GENERATED_REL_DIR,
    GOVERNANCE_REL_DIR,
    GRAPH_GENERATED_REL_DIR,
    GRAPH_REL_DIR,
    ONTOLOGY_REL_DIR,
    RECORDS_REL_DIR,
    REGISTRY_REL_DIR,
    VALIDATION_GENERATED_REL_DIR,
    VALIDATION_REL_DIR,
)


def resolve_project_root(explicit: Path | None = None) -> Path:
    """Resolve the BTE Platform project root."""
    if explicit is not None:
        return explicit.resolve()
    # baseline/ is at <root>/baseline
    return Path(__file__).resolve().parent.parent


class BaselinePaths:
    """Centralized path map for baseline generation."""

    def __init__(self, project_root: Path, version: str) -> None:
        """Initialize path map for a baseline version."""
        self.project_root = project_root.resolve()
        self.version = version
        self.knowledge = self.project_root / "knowledge"
        self.records_dir = self.project_root / RECORDS_REL_DIR
        self.ontology_dir = self.project_root / ONTOLOGY_REL_DIR
        self.registry_dir = self.project_root / REGISTRY_REL_DIR
        self.compiler_dir = self.project_root / COMPILER_REL_DIR
        self.validation_dir = self.project_root / VALIDATION_REL_DIR
        self.graph_dir = self.project_root / GRAPH_REL_DIR
        self.dependency_dir = self.project_root / DEPENDENCY_REL_DIR
        self.governance_dir = self.project_root / GOVERNANCE_REL_DIR
        self.baseline_root = self.project_root / BASELINE_OUTPUT_REL_DIR
        self.version_dir = self.baseline_root / f"v{version}"
        self.governance_generated = (
            self.project_root / GOVERNANCE_GENERATED_REL_DIR
        )
        self.compiler_generated = self.project_root / COMPILER_GENERATED_REL_DIR
        self.validation_generated = (
            self.project_root / VALIDATION_GENERATED_REL_DIR
        )
        self.graph_generated = self.project_root / GRAPH_GENERATED_REL_DIR

    def ensure_output_dirs(self) -> None:
        """Create all output directories used by the builder."""
        for path in (
            self.version_dir,
            self.governance_generated,
            self.compiler_generated,
            self.validation_generated,
            self.graph_generated,
            self.baseline_root / "diff",
        ):
            path.mkdir(parents=True, exist_ok=True)

    def artifact(self, filename: str) -> Path:
        """Return path to an artifact inside the version baseline folder."""
        return self.version_dir / filename
