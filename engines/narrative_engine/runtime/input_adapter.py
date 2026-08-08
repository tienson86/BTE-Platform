"""
Adapt analysis / interpretation payloads into RuntimeInput.

Extracts ids, kinds, confidence, and commercial_ok flags only.
Does not copy prose into NarrativeTree.
"""

from __future__ import annotations

import re
from typing import Any

from .models import (
    EvidenceKind,
    RuntimeEvidenceUnit,
    RuntimeInput,
    RuntimeInterpretationRef,
)

_TECHNICAL_MARKERS: tuple[re.Pattern[str], ...] = (
    re.compile(r"kích hoạt khi", re.IGNORECASE),
    re.compile(r"áp dụng bảng", re.IGNORECASE),
    re.compile(r"ưu tiên xác định", re.IGNORECASE),
    re.compile(r"matched[_ ]?rules?", re.IGNORECASE),
    re.compile(r"\bpack[_\s]?\d+", re.IGNORECASE),
    re.compile(r"\(mock\)", re.IGNORECASE),
    re.compile(r"placeholder", re.IGNORECASE),
)


def build_runtime_input(
    *,
    analysis: Any = None,
    interpretation: Any = None,
    run_id: str = "",
    analysis_valid: bool | None = None,
    interpretation_valid: bool | None = None,
) -> RuntimeInput:
    """Build RuntimeInput from AnalysisResult-like and Interpretation-like objects/dicts."""
    evidence = _extract_evidence(analysis)
    interp_refs = _extract_interpretation_refs(interpretation)
    resolved_analysis_valid = (
        True if analysis_valid is None else bool(analysis_valid)
    )
    if analysis_valid is None and analysis is None:
        # Allow interpretation-only structural runs when caller did not supply analysis.
        resolved_analysis_valid = True
    resolved_interpretation_valid = (
        True if interpretation_valid is None else bool(interpretation_valid)
    )
    if interpretation is None and interpretation_valid is None:
        resolved_interpretation_valid = True
    return RuntimeInput(
        evidence=evidence,
        interpretation_refs=interp_refs,
        analysis_valid=resolved_analysis_valid,
        interpretation_valid=resolved_interpretation_valid,
        run_id=run_id,
    )


def _extract_evidence(analysis: Any) -> tuple[RuntimeEvidenceUnit, ...]:
    """Extract structural evidence units from analysis object/dict."""
    if analysis is None:
        return ()
    units: list[RuntimeEvidenceUnit] = []

    if isinstance(analysis, dict):
        units.extend(_evidence_from_analysis_dict(analysis))
        return tuple(units)

    # Object-style AnalysisResult (Pack 03-like).
    strength = getattr(analysis, "strength", None)
    if strength is not None:
        units.append(
            RuntimeEvidenceUnit(
                id="ev-strength",
                kind=EvidenceKind.STRENGTH,
                confidence=_as_confidence(getattr(strength, "confidence", 0.0)),
                source_path="analysis.strength",
            )
        )
        if getattr(strength, "value", None) or getattr(strength, "score", None) is not None:
            units.append(
                RuntimeEvidenceUnit(
                    id="ev-identity-strength",
                    kind=EvidenceKind.IDENTITY,
                    confidence=_as_confidence(getattr(strength, "confidence", 0.5)),
                    source_path="analysis.strength.value",
                )
            )
    pattern = getattr(analysis, "pattern", None)
    if pattern is not None:
        units.append(
            RuntimeEvidenceUnit(
                id="ev-pattern",
                kind=EvidenceKind.IDENTITY,
                confidence=_as_confidence(getattr(pattern, "confidence", 0.6)),
                source_path="analysis.pattern",
            )
        )
    useful = getattr(analysis, "useful_god", None)
    if useful is not None:
        units.append(
            RuntimeEvidenceUnit(
                id="ev-useful-god",
                kind=EvidenceKind.ACTION,
                confidence=_as_confidence(getattr(useful, "confidence", 0.6)),
                source_path="analysis.useful_god",
            )
        )
    overall = getattr(analysis, "overall", None)
    if overall is not None:
        units.append(
            RuntimeEvidenceUnit(
                id="ev-grade",
                kind=EvidenceKind.GRADE,
                confidence=_as_confidence(getattr(overall, "confidence", 0.5)),
                source_path="analysis.overall",
            )
        )
    return tuple(units)


def _evidence_from_analysis_dict(data: dict[str, Any]) -> list[RuntimeEvidenceUnit]:
    """Map orchestrator-style analysis dict into evidence units."""
    units: list[RuntimeEvidenceUnit] = []
    strength = data.get("strength") if isinstance(data.get("strength"), dict) else {}
    pattern = data.get("pattern") if isinstance(data.get("pattern"), dict) else {}
    useful = data.get("useful_god") if isinstance(data.get("useful_god"), dict) else {}
    score = data.get("score") if isinstance(data.get("score"), dict) else {}
    bazi = data.get("bazi") if isinstance(data.get("bazi"), dict) else {}

    if bazi.get("day_master"):
        units.append(
            RuntimeEvidenceUnit(
                id="ev-day-master",
                kind=EvidenceKind.IDENTITY,
                confidence=0.9,
                source_path="bazi.day_master",
            )
        )
    if strength or score.get("strength_score") is not None:
        units.append(
            RuntimeEvidenceUnit(
                id="ev-strength",
                kind=EvidenceKind.STRENGTH,
                confidence=_as_confidence(
                    strength.get("confidence", score.get("confidence", 0.6))
                ),
                source_path="strength|score.strength_score",
            )
        )
    if pattern.get("cach_cuc") or pattern.get("pattern"):
        units.append(
            RuntimeEvidenceUnit(
                id="ev-pattern",
                kind=EvidenceKind.IDENTITY,
                confidence=0.8,
                source_path="pattern.cach_cuc",
            )
        )
    if useful.get("useful_god") or pattern.get("dung_than") or score.get("recommendation"):
        units.append(
            RuntimeEvidenceUnit(
                id="ev-action",
                kind=EvidenceKind.ACTION,
                confidence=_as_confidence(useful.get("confidence", 0.7)),
                source_path="useful_god|pattern.dung_than|score.recommendation",
            )
        )
    if useful.get("unfavorable_gods") or pattern.get("ky_than"):
        units.append(
            RuntimeEvidenceUnit(
                id="ev-risk",
                kind=EvidenceKind.RISK,
                confidence=0.65,
                source_path="useful_god.unfavorable|pattern.ky_than",
            )
        )
        units.append(
            RuntimeEvidenceUnit(
                id="ev-weakness",
                kind=EvidenceKind.WEAKNESS,
                confidence=0.65,
                source_path="useful_god.unfavorable|pattern.ky_than",
            )
        )
    if score.get("grade") is not None or score.get("total_score") is not None:
        units.append(
            RuntimeEvidenceUnit(
                id="ev-grade",
                kind=EvidenceKind.GRADE,
                confidence=0.7,
                source_path="score.grade",
            )
        )
    # Explanation / implication structural markers when reasoning fields exist.
    if strength.get("reasoning"):
        units.append(
            RuntimeEvidenceUnit(
                id="ev-explanation",
                kind=EvidenceKind.EXPLANATION,
                confidence=0.55,
                source_path="strength.reasoning",
                commercial_ok=not _is_technical(str(strength.get("reasoning"))),
            )
        )
        units.append(
            RuntimeEvidenceUnit(
                id="ev-implication",
                kind=EvidenceKind.IMPLICATION,
                confidence=0.5,
                source_path="strength.reasoning",
                commercial_ok=not _is_technical(str(strength.get("reasoning"))),
            )
        )
    return units


def _extract_interpretation_refs(interpretation: Any) -> tuple[RuntimeInterpretationRef, ...]:
    """Extract interpretation section references without storing prose on the tree."""
    if interpretation is None:
        return ()
    sections: list[Any] = []
    if isinstance(interpretation, dict):
        raw = interpretation.get("sections") or []
        if isinstance(raw, list):
            sections = raw
    else:
        raw = getattr(interpretation, "sections", None)
        if isinstance(raw, list):
            sections = raw

    refs: list[RuntimeInterpretationRef] = []
    for index, section in enumerate(sections):
        if isinstance(section, dict):
            section_id = str(section.get("id") or f"section-{index + 1}")
            title = str(section.get("title") or "")
            body = str(section.get("body") or section.get("content") or "")
            ref_id = f"interp:{section_id}"
            commercial_ok = not _is_technical(body) and not _is_technical(title)
            refs.append(
                RuntimeInterpretationRef(
                    id=ref_id,
                    section_id=section_id,
                    title=title,
                    commercial_ok=commercial_ok,
                    intent_hints=_hint_from_title(title),
                )
            )
            continue
        section_id = str(getattr(section, "id", "") or f"section-{index + 1}")
        title = str(getattr(section, "title", "") or "")
        body = str(getattr(section, "body", "") or "")
        refs.append(
            RuntimeInterpretationRef(
                id=f"interp:{section_id}",
                section_id=section_id,
                title=title,
                commercial_ok=not _is_technical(body) and not _is_technical(title),
                intent_hints=_hint_from_title(title),
            )
        )
    return tuple(refs)


def _hint_from_title(title: str) -> tuple[str, ...]:
    """Derive coarse intent hints from section title only."""
    text = title.strip().lower()
    if not text:
        return ()
    return (text,)


def _is_technical(text: str) -> bool:
    """Detect technical/rule prose for commercial_ok gating."""
    value = (text or "").strip()
    if not value:
        return True
    return any(pattern.search(value) for pattern in _TECHNICAL_MARKERS)


def _as_confidence(value: Any) -> float:
    """Normalize confidence-like values into [0, 1]."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    if number > 1.0 and number <= 100.0:
        number = number / 100.0
    if number < 0.0:
        return 0.0
    if number > 1.0:
        return 1.0
    return number
