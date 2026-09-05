"""Consume and normalize Pattern Engine identity. Do not reclassify."""

from __future__ import annotations

from engines.mingju.constants import (
    PATTERN_CODE_ALIASES,
    PATTERN_FAMILY_BY_ID,
    PATTERN_LABEL_ALIASES,
    PATTERN_LABEL_BY_ID,
)
from engines.mingju.enums import AnalysisState
from engines.mingju.evidence import RecordBook
from engines.mingju.models import MingJuContext, PatternDecision
from engines.mingju.versions import PATTERN_SOURCE


def normalize_pattern_id(code: str, label: str) -> str:
    """Map Pattern Engine codes and Vietnamese labels onto MC-01 IDs."""
    token = code.strip().lower().replace("-", "_").replace(" ", "_")
    if token in PATTERN_FAMILY_BY_ID:
        return token
    if token in PATTERN_CODE_ALIASES:
        return PATTERN_CODE_ALIASES[token]
    text = label.strip()
    if text in PATTERN_LABEL_ALIASES:
        return PATTERN_LABEL_ALIASES[text]
    cleaned = text.replace(" cách", "").replace(" Cách", "").strip()
    if cleaned in PATTERN_LABEL_ALIASES:
        return PATTERN_LABEL_ALIASES[cleaned]
    lowered = cleaned.lower()
    for name, pattern_id in PATTERN_LABEL_ALIASES.items():
        if name.lower() == lowered:
            return pattern_id
    return ""


def resolve_pattern(context: MingJuContext, book: RecordBook) -> PatternDecision:
    """Publish Pattern reference from upstream Pattern Engine only."""
    if not context.pattern_success and not context.pattern_label and not context.pattern_code:
        book.add_warning("pattern_unresolved", "mc01.pattern.unresolved")
        return PatternDecision(state=AnalysisState.UNRESOLVED.value, confidence=0.0)
    pattern_id = normalize_pattern_id(context.pattern_code, context.pattern_label)
    if not pattern_id:
        book.add_warning("pattern_unmapped", "mc01.pattern.unmapped")
        return PatternDecision(
            state=AnalysisState.UNRESOLVED.value,
            label=context.pattern_label,
            source_code=context.pattern_code,
            source=PATTERN_SOURCE,
            confidence=0.0,
        )
    evidence_id = book.add_evidence(
        "pattern_identity",
        "mc01.pattern.upstream",
        source=PATTERN_SOURCE,
        pattern_id=pattern_id,
        label=context.pattern_label,
        source_code=context.pattern_code,
    )
    book.add_trace("pattern", "MC-PAT-001", "mc01.pattern.consumed", (evidence_id,))
    secondary: list[str] = []
    for item in context.secondary_labels:
        mapped = normalize_pattern_id("", item)
        if mapped and mapped != pattern_id and mapped not in secondary:
            secondary.append(mapped)
    family = PATTERN_FAMILY_BY_ID.get(pattern_id, "special")
    return PatternDecision(
        state=AnalysisState.RESOLVED.value,
        pattern_id=pattern_id,
        label=context.pattern_label or PATTERN_LABEL_BY_ID.get(pattern_id, pattern_id),
        family=family,
        source=PATTERN_SOURCE,
        source_code=context.pattern_code,
        secondary_ids=tuple(secondary),
        month_branch=context.month_branch,
        month_main_qi=context.month_main_qi,
        month_main_qi_ten_god=context.month_main_qi_ten_god,
        day_master=context.day_master,
        evidence_ids=(evidence_id,),
        confidence=0.92 if context.hour_present else 0.78,
    )
