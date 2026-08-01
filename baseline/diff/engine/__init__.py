"""Diff engine package.

Public exports for Pack 01 baseline lifecycle comparisons.
"""

from __future__ import annotations

from baseline.diff.engine.baseline_compare import (
    compare_compiler_snapshots,
    compare_dependency_snapshots,
    compare_ontology_snapshots,
    compare_registry_snapshots,
    compare_validation_snapshots,
)
from baseline.diff.engine.baseline_diff import BaselineDiffEngine, diff_baselines
from baseline.diff.engine.report_generator import (
    generate_diff_html,
    generate_diff_json,
    generate_diff_markdown,
)
from baseline.diff.engine.snapshot_loader import SnapshotLoader

__all__ = [
    "BaselineDiffEngine",
    "SnapshotLoader",
    "compare_compiler_snapshots",
    "compare_dependency_snapshots",
    "compare_ontology_snapshots",
    "compare_registry_snapshots",
    "compare_validation_snapshots",
    "diff_baselines",
    "generate_diff_html",
    "generate_diff_json",
    "generate_diff_markdown",
]
