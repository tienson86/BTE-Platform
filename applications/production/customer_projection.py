"""Project pipeline outputs to Customer Mode — hide internal runtime."""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine_v2.strength.contracts.models import InterpretationResult


def project_strength_interpretation(result: InterpretationResult) -> dict[str, Any]:
    """Return customer-mode strength interpretation only."""
    sections = []
    for section in result.customer_mode:
        body = "\n\n".join(section.paragraphs)
        sections.append(
            {
                "section_id": section.section_id,
                "title": section.title,
                "body": body,
            }
        )
    return {
        "case_id": result.meta.case_id,
        "sections": sections,
    }


def assert_no_internal_keys(payload: dict[str, Any]) -> None:
    """Raise if customer payload contains forbidden internal keys."""
    forbidden = {
        "validation_mode",
        "narrative_plan",
        "diagnostics",
        "evidence",
        "trace",
        "reason_codes",
        "matched_rules",
        "rule_context",
        "internal",
    }
    found = forbidden.intersection(payload.keys())
    if found:
        raise ValueError(f"Customer payload contains internal keys: {sorted(found)}")
