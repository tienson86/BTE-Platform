"""Customer relevance filter — select current-chart knowledge for narrative.

This is composition policy. It does not calculate, decide, or add architecture.
"""

from __future__ import annotations

import re

from engines.interpretation_engine.foundation.narrative.constants import (
    COMMERCIAL_SHENSHA_LIMIT,
    GOVERNING_APPLICATION_DOMAINS,
    KIND_APPLICATION,
    SHENSHA_CANONICAL_OVER_ALIAS,
    SLOT_IMPACT,
    SLOT_OBSERVATION,
)
from engines.interpretation_engine.foundation.narrative.input import (
    ChartFocus,
    CopiedStatement,
    DecisionBundle,
    KnowledgeBundle,
    NarrativeComposerInput,
    RelationshipBundle,
    StateBundle,
)
from engines.interpretation_engine.foundation.narrative.text import (
    is_broken_fragment,
    normalize_text,
)

_HYPOTHETICAL_ROLE = re.compile(
    r"Khi\s+([^,.;:]{1,24}?)\s+là\s+(Dụng thần|Hỷ thần|Hỷ|Kỵ thần|Kỵ)\b"
)
_SCORE_DUMP = re.compile(
    r"(?:/\s*0\.\d+)|(?:\b0\.\d{2}\b)|(?:\bstrong\s*/)|(?:\bweak\s*/)",
    re.IGNORECASE,
)
_DISCLAIMER_ONLY = re.compile(
    r"^(không chẩn đoán.*|không hứa hiệu quả tài chính\.?)$",
    re.IGNORECASE,
)
_ALIAS_PEDAGOGY = (
    "tên gọi khác",
    "cả hai key",
    "bước nhận diện",
    "giữ hai key",
    "không cộng dồn",
    "production phải",
    "stems rỗng",
)
_TOURNAMENT_MARKERS = (
    ":rejected:",
    ":path:",
    "explain_rejected",
    "nhóm ưu tiên thấp hơn",
    "nhóm thân vượng nhược",
    "thứ tự xét duyệt",
)
_SKIP_OBSERVATION_LABELS = (
    "điều hậu:",
    "phân bố ngũ hành:",
    "thân: strong",
    "thân: weak",
)


def canonical_shensha_names(matched: tuple[str, ...]) -> tuple[str, ...]:
    """Keep canonical star names; drop aliases of the same mechanism."""
    chosen: list[str] = []
    seen: set[str] = set()
    for name in matched:
        canonical = SHENSHA_CANONICAL_OVER_ALIAS.get(name, name)
        if canonical in seen:
            continue
        seen.add(canonical)
        chosen.append(canonical)
        if len(chosen) >= COMMERCIAL_SHENSHA_LIMIT:
            break
    return tuple(chosen)


def apply_customer_relevance(source: NarrativeComposerInput) -> NarrativeComposerInput:
    """Drop unused, hypothetical, and broken statements before composition."""
    focus = source.chart_focus
    return NarrativeComposerInput(
        decision_bundles=tuple(
            _filter_decision(item, focus) for item in source.decision_bundles
        ),
        state_bundles=tuple(_filter_state(item, focus) for item in source.state_bundles),
        relationship_bundles=tuple(
            _filter_relationship(item, focus) for item in source.relationship_bundles
        ),
        knowledge_bundles=tuple(
            _filter_knowledge(item, focus) for item in source.knowledge_bundles
        ),
        chart_focus=focus,
    )


def statement_is_relevant(
    statement: CopiedStatement,
    focus: ChartFocus | None,
) -> bool:
    """True when a copied statement may enter customer narrative."""
    text = normalize_text(statement.text)
    if not text or is_broken_fragment(text):
        return False
    if _DISCLAIMER_ONLY.match(text.rstrip(".")):
        return False
    lowered = text.casefold()
    if any(marker in lowered for marker in _ALIAS_PEDAGOGY):
        return False
    ref = statement.engine_truth_ref.casefold()
    if any(marker in ref or marker in lowered for marker in _TOURNAMENT_MARKERS):
        return False
    if statement.slot == SLOT_OBSERVATION and _is_skip_observation(text):
        return False
    if focus is None:
        return not is_hypothetical_role_leak(text, ChartFocus())
    if is_hypothetical_role_leak(text, focus):
        return False
    if statement.kind == KIND_APPLICATION:
        if statement.slot == SLOT_IMPACT and not _application_domain_allowed(statement, focus):
            return False
    return True


def is_hypothetical_role_leak(text: str, focus: ChartFocus) -> bool:
    """True when prose discusses a Dụng/Hỷ/Kỵ role that is not on this chart."""
    blob = normalize_text(text)
    for match in _HYPOTHETICAL_ROLE.finditer(blob):
        name = match.group(1).strip()
        role = match.group(2)
        if not _name_fits_role(name, role, focus):
            return True
    return False


def _name_fits_role(name: str, role: str, focus: ChartFocus) -> bool:
    """Check a named hypothetical against current selected/Hỷ/Kỵ."""
    if role.startswith("Dụng"):
        return bool(name) and name == focus.selected
    if role.startswith("Hỷ"):
        return name in focus.favorable or name == focus.selected
    if role.startswith("Kỵ"):
        return name in focus.unfavorable
    return False


def _is_skip_observation(text: str) -> bool:
    """Drop score dumps and climate internals from Observation."""
    lowered = text.casefold()
    if _SCORE_DUMP.search(text):
        return True
    return any(label in lowered for label in _SKIP_OBSERVATION_LABELS)


def _application_domain_allowed(statement: CopiedStatement, focus: ChartFocus) -> bool:
    """Applications come from governing domains, not the full catalogue."""
    ref = statement.engine_truth_ref
    for domain in GOVERNING_APPLICATION_DOMAINS:
        if f":{domain}:" in f":{ref}:" or statement.engine_truth_ref.startswith(
            f"knowledge:{domain}:"
        ):
            return True
        if f"knowledge:{domain.lower()}" in ref.casefold():
            return True
    bundle_hint = ref.split(":")
    if len(bundle_hint) >= 2 and bundle_hint[1] in GOVERNING_APPLICATION_DOMAINS:
        return True
    if "usefulgod" in ref.casefold() or "useful_god" in ref.casefold():
        return True
    if "pattern" in ref.casefold() or "strength" in ref.casefold():
        return True
    return not focus.active_names()


def _filter_decision(bundle: DecisionBundle, focus: ChartFocus | None) -> DecisionBundle:
    """Keep selected-decision statements that pass the customer filter."""
    return DecisionBundle(
        bundle_id=bundle.bundle_id,
        domain=bundle.domain,
        selected=bundle.selected,
        reason=bundle.reason,
        confidence=bundle.confidence,
        importance=bundle.importance,
        statements=_filter_statements(bundle.statements, focus),
        engine_truth_refs=bundle.engine_truth_refs,
    )


def _filter_state(bundle: StateBundle, focus: ChartFocus | None) -> StateBundle:
    """Keep state statements that pass the customer filter."""
    return StateBundle(
        bundle_id=bundle.bundle_id,
        domain=bundle.domain,
        state=bundle.state,
        label=bundle.label,
        confidence=bundle.confidence,
        importance=bundle.importance,
        statements=_filter_statements(bundle.statements, focus),
        engine_truth_refs=bundle.engine_truth_refs,
    )


def _filter_relationship(
    bundle: RelationshipBundle,
    focus: ChartFocus | None,
) -> RelationshipBundle:
    """Keep relationship statements that pass the customer filter."""
    return RelationshipBundle(
        bundle_id=bundle.bundle_id,
        domain=bundle.domain,
        confidence=bundle.confidence,
        importance=bundle.importance,
        statements=_filter_statements(bundle.statements, focus),
        engine_truth_refs=bundle.engine_truth_refs,
    )


def _filter_knowledge(
    bundle: KnowledgeBundle,
    focus: ChartFocus | None,
) -> KnowledgeBundle:
    """Keep knowledge statements that pass the customer filter."""
    return KnowledgeBundle(
        bundle_id=bundle.bundle_id,
        domain=bundle.domain,
        entity_keys=bundle.entity_keys,
        confidence=bundle.confidence,
        importance=bundle.importance,
        statements=_filter_statements(bundle.statements, focus),
        engine_truth_refs=bundle.engine_truth_refs,
    )


def _filter_statements(
    statements: tuple[CopiedStatement, ...],
    focus: ChartFocus | None,
) -> tuple[CopiedStatement, ...]:
    """Apply the customer filter to one bundle's copied statements."""
    return tuple(item for item in statements if statement_is_relevant(item, focus))


def entity_is_relevant(domain: str, key: str, focus: ChartFocus | None) -> bool:
    """True when a knowledge entity belongs on the current customer report."""
    if focus is None or not key:
        return True
    if domain == "UsefulGod":
        return key == focus.selected or key in focus.favorable or key in focus.unfavorable
    if domain == "TenGods":
        return key in focus.present_ten_gods
    if domain == "ShenSha":
        return key in focus.canonical_shensha
    return True


def recommendation_role_allowed(role: str, entity_role: str) -> bool:
    """Keep a knowledge recommendation only when its role matches this chart."""
    if not role:
        return True
    return role == entity_role
