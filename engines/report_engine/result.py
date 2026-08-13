"""Report Engine terminal result — portal report + narrative slices."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ReportResult:
    """
    Authoritative Report Engine output for the production pipeline.

    ``report`` and ``narrative`` are portal-compatible dicts only — no internal
    template metadata on the wire. Customer prose source is ``canonical_narrative``.
    """

    report: dict[str, Any] = field(default_factory=dict)
    narrative: dict[str, Any] | None = None
    canonical_narrative: dict[str, Any] | None = None
    source: str = ""
    diagnostics: dict[str, Any] = field(default_factory=dict)

    def to_portal_report_dict(self) -> dict[str, Any]:
        """Serialize ``AnalysisResult.report`` / API ``data.report``."""
        return dict(self.report)

    def to_portal_narrative_dict(self) -> dict[str, Any]:
        """Serialize ``AnalysisResult.narrative`` / API ``data.narrative``."""
        if self.narrative is None:
            return {}
        return dict(self.narrative)
