"""Adapt Narrative Composer V2 into the live report/portal NarrativeResult shape.

Does not import Pack 05 engine code. Consumer keys stay stable so Portal,
report, and PDF do not need a redesign.
"""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.foundation.narrative.constants import (
    NARRATIVE_RESULT_V2_GENERATOR,
    NARRATIVE_SECTIONS,
    PACK05_CONTRACT,
    PACK05_SECTION_MAP,
    PACK05_SECTION_TONES,
    SECTION_EXECUTIVE_SUMMARY,
    SECTION_RECOMMENDATION,
    SECTION_WARNING,
)
from engines.interpretation_engine.foundation.narrative.models import (
    NarrativeComposerResult,
    NarrativeSection,
    RecommendationItem,
)


def narrative_result_v2_to_dict(
    result: NarrativeComposerResult,
    *,
    run_id: str = "",
) -> dict[str, Any]:
    """Serialize V2 composition as the canonical production NarrativeResult."""
    sections = [_section_payload(section) for section in result.sections]
    summary = _summary_payload(result)
    recommendations = [
        _recommendation_payload(item, index)
        for index, item in enumerate(result.recommendations)
    ]
    status = "complete" if not result.diagnostics else "partial_insufficient"
    overall = _overall_confidence(result)
    return {
        "contract": PACK05_CONTRACT,
        "generator": NARRATIVE_RESULT_V2_GENERATOR,
        "summary": summary,
        "sections": sections,
        "recommendations": recommendations,
        "confidence": overall,
        "status": status,
        "run_id": run_id,
        "source_fingerprint": {
            "engine": (
                "engines.interpretation_engine.foundation.narrative"
                ".NarrativeComposerV2"
            ),
            "method": "compose",
            "contract": PACK05_CONTRACT,
            "generator": NARRATIVE_RESULT_V2_GENERATOR,
        },
        "metadata": {
            "composer": NARRATIVE_RESULT_V2_GENERATOR,
            "metrics": result.metrics.to_dict(),
            "section_names": list(NARRATIVE_SECTIONS),
        },
        "validation_issues": list(result.diagnostics),
        "evidence": result.evidence.to_dict(),
        "traceability": [item.to_dict() for item in result.traceability],
    }


def _section_payload(section: NarrativeSection) -> dict[str, Any]:
    """Map one V2 section onto Pack 05 section ids/intents/titles."""
    section_id, intent, title = PACK05_SECTION_MAP[section.name]
    paragraphs = []
    for index, sentence in enumerate(section.sentences):
        role = "summary" if section.name == SECTION_EXECUTIVE_SUMMARY else "explanation"
        if section.name == SECTION_RECOMMENDATION:
            role = "suggestion"
        elif section.name == SECTION_WARNING:
            role = "impact"
        paragraphs.append(
            {
                "id": sentence.sentence_id or f"p-{section_id}-{index}",
                "role": role,
                "text": sentence.text,
                "evidence_refs": list(sentence.evidence_ids),
                "interpretation_refs": list(sentence.bundle_ids),
                "rule_refs": list(sentence.engine_truth_refs),
                "knowledge_refs": [],
                "confidence": 0.0,
                "insufficient_data": False,
            }
        )
    recs = []
    if section.name == SECTION_RECOMMENDATION:
        for index, sentence in enumerate(section.sentences):
            recs.append(
                {
                    "id": f"rec-{index}",
                    "priority": "high" if index == 0 else "medium",
                    "action": sentence.text,
                    "reason": "",
                    "benefit": "",
                    "evidence_refs": list(sentence.evidence_ids),
                    "interpretation_refs": list(sentence.bundle_ids),
                    "rule_refs": list(sentence.engine_truth_refs),
                    "knowledge_refs": [],
                    "insufficient_data": False,
                }
            )
    return {
        "id": section_id,
        "intent": intent,
        "title": title,
        "paragraphs": paragraphs,
        "recommendations": recs,
        "evidence_refs": list(section.evidence_ids),
        "interpretation_refs": [],
        "confidence": 0.0,
        "insufficient_data": not section.sentences,
        "tone": PACK05_SECTION_TONES.get(section.name, "neutral_factual"),
    }


def _summary_payload(result: NarrativeComposerResult) -> dict[str, Any]:
    """Build the five commercial summary answers from copied V2 sentences."""
    exec_section = result.section(SECTION_EXECUTIVE_SUMMARY)
    rec_section = result.section(SECTION_RECOMMENDATION)
    warn_section = result.section(SECTION_WARNING)
    identity = " ".join(sentence.text for sentence in (exec_section.sentences if exec_section else ()))
    recs = [sentence.text for sentence in (rec_section.sentences if rec_section else ())]
    warns = [sentence.text for sentence in (warn_section.sentences if warn_section else ())]
    strengths = tuple(item.statement for item in result.applications[:3])
    return {
        "identity": identity,
        "strengths": list(strengths),
        "weaknesses": warns[:3],
        "priority_recommendation": recs[0] if recs else "",
        "next_action": recs[0] if recs else "",
        "overall_confidence": _overall_confidence(result),
        "insufficient_flags": list(result.diagnostics),
    }


def _recommendation_payload(item: RecommendationItem, index: int) -> dict[str, Any]:
    """Serialize one structured recommendation for the top-level list."""
    return {
        "id": item.recommendation_id or f"rec-{index}",
        "priority": "high" if index == 0 else "medium",
        "action": item.action,
        "reason": item.rationale,
        "benefit": "",
        "evidence_refs": list(item.evidence_ids),
        "interpretation_refs": [item.bundle_id],
        "rule_refs": [],
        "knowledge_refs": [],
        "insufficient_data": False,
    }


def _overall_confidence(result: NarrativeComposerResult) -> float:
    """Copy the highest bundle confidence already present on evidence."""
    if not result.evidence.nodes:
        return 0.0
    return max(node.confidence for node in result.evidence.nodes)
