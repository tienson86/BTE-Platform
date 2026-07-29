"""
Unified Report truth — ReportResult → ReportView / NarrativeView.
"""

from __future__ import annotations

from engines.report_engine.result import ReportResult

from applications.api.models.analysis_result import NarrativeView, ReportView


def build_report_view(result: ReportResult) -> ReportView:
    """Build authoritative ReportView from ReportEngine result."""
    portal = result.to_portal_report_dict()
    return ReportView(
        title=str(portal.get("title") or ""),
        markdown=str(portal.get("markdown") or ""),
        html=str(portal.get("html") or ""),
        section_count=int(portal.get("section_count") or 0),
    )


def build_narrative_view(result: ReportResult) -> NarrativeView:
    """Build authoritative NarrativeView from ReportEngine result."""
    portal = result.to_portal_narrative_dict()
    tone = portal.get("tone")
    metrics = portal.get("metrics")
    return NarrativeView(
        title=str(portal.get("title") or ""),
        markdown=str(portal.get("markdown") or ""),
        html=str(portal.get("html") or ""),
        section_count=int(portal.get("section_count") or 0),
        tone=str(tone) if tone else None,
        metrics=dict(metrics) if isinstance(metrics, dict) else None,
    )


def report_source_fingerprint() -> dict[str, str]:
    """Provenance block for API meta."""
    return {
        "engine": "engines.report_engine.engine.ReportEngine",
        "method": "render_from_analysis",
        "contract": "report_analysis_result_v1",
        "view": (
            "applications.api.services.report_truth.build_report_view"
        ),
    }
