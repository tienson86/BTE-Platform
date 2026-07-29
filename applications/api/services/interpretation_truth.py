"""
Unified Interpretation truth — InterpretationResult → InterpretationView.
"""

from __future__ import annotations

from engines.interpretation_engine.legacy_builder import InterpretationResult

from applications.api.models.analysis_result import (
    InterpretationSectionView,
    InterpretationView,
)


def build_interpretation_view(result: InterpretationResult) -> InterpretationView:
    """Build authoritative InterpretationView from InterpretationEngine result."""
    portal = result.to_portal_dict()
    sections = [
        InterpretationSectionView(
            id=str(item.get("id") or ""),
            title=str(item.get("title") or ""),
            body=str(item.get("body") or ""),
        )
        for item in (portal.get("sections") or [])
        if isinstance(item, dict)
    ]
    # Internal engine fields stay on InterpretationResult only.
    # Production serialization is portal-compatible via to_dict().
    return InterpretationView(
        sections=sections,
        section_count=int(portal.get("section_count") or len(sections)),
        sentence_count=int(portal.get("sentence_count") or 0),
        confidence=float(portal.get("confidence") or 0.0),
    )


def interpretation_source_fingerprint() -> dict[str, str]:
    """Provenance block for API meta."""
    return {
        "engine": "engines.interpretation_engine.engine.InterpretationEngine",
        "method": "run",
        "contract": "interpretation_rule_context_v1",
        "view": (
            "applications.api.services.interpretation_truth.build_interpretation_view"
        ),
    }
