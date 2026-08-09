"""Admit Luck Foundation package metadata for Luck Analysis. Read-only."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from engines.luck_engine.analysis_constants import (
    ANALYSIS_VERSION,
    REQUIRED_ANALYSIS_PIPELINE_VERSION,
    REQUIRED_DECISION_PIPELINE_VERSION,
    REQUIRED_TIMELINE_VERSION,
)
from engines.luck_engine.timeline.package_loader import LoadedLuckPackage, LuckPackageLoader


@dataclass(frozen=True, slots=True)
class LoadedLuckAnalysisSupport:
    """Version bundle Luck Analysis may consume."""

    timeline_package: LoadedLuckPackage
    analysis_version: str
    required_timeline_version: str
    required_analysis_pipeline_version: str
    required_decision_pipeline_version: str


class LuckAnalysisPackageLoader:
    """Load bz_09 identity for version compatibility. Does not evaluate rules."""

    def __init__(self, package_root: Path | None = None) -> None:
        """Optional override of the Luck Foundation root."""
        self._loader = LuckPackageLoader(package_root=package_root)

    def load(self) -> LoadedLuckAnalysisSupport:
        """Admit the released timeline foundation package."""
        package = self._loader.load()
        return LoadedLuckAnalysisSupport(
            timeline_package=package,
            analysis_version=ANALYSIS_VERSION,
            required_timeline_version=REQUIRED_TIMELINE_VERSION,
            required_analysis_pipeline_version=REQUIRED_ANALYSIS_PIPELINE_VERSION,
            required_decision_pipeline_version=REQUIRED_DECISION_PIPELINE_VERSION,
        )
