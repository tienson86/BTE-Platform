"""Customer-safe compact summary for Evidence Priority. No IDs or traces."""

from __future__ import annotations

from typing import Any

from engines.detailed_interpretation_engine.evidence import (
    EvidencePriorityFinding,
    EvidencePriorityResult,
)

TITLE = "Trọng tâm lá số"


def present_evidence_priority_customer(result: EvidencePriorityResult) -> dict[str, Any]:
    """Compact customer labels only. Does not narrate domains."""
    lookup = {item.finding_id: item for item in result.findings}
    return {
        "title": TITLE,
        "driver": _label(lookup, result.driver_ids),
        "bottleneck": _label(lookup, result.bottleneck_ids),
        "risk": _label(lookup, result.risk_evidence),
        "opportunity": _label(lookup, result.opportunity_evidence),
        "condition": _label(lookup, result.conditions),
    }


def _label(lookup: dict[str, EvidencePriorityFinding], ids: tuple[str, ...]) -> str:
    for finding_id in ids:
        item = lookup.get(finding_id)
        if item is None:
            continue
        text = item.customer_label.strip()
        if text and "TR-P7" not in text and not text.startswith("E-DI-"):
            return text
    return ""
