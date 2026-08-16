"""Build frozen composer input from production engine output. No recalculation."""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.foundation.assessment.strength import (
    build_strength_assessment,
)
from engines.interpretation_engine.foundation.interpreters.pattern import (
    build_pattern_facts,
    build_pattern_interpretation_bundle,
)
from engines.interpretation_engine.foundation.interpreters.shensha import (
    build_shensha_facts,
    build_shensha_interpretation_bundle,
)
from engines.interpretation_engine.foundation.interpreters.ten_gods import (
    build_ten_god_facts,
    build_ten_god_interpretation_bundle,
)
from engines.interpretation_engine.foundation.knowledge.entity_types import (
    TEN_GOD_PILLAR_KEYS,
)
from engines.interpretation_engine.foundation.knowledge.retrieval import (
    build_useful_god_knowledge_bundle,
)
from engines.interpretation_engine.foundation.knowledge.strength_retrieval import (
    build_strength_knowledge_bundle,
)
from engines.interpretation_engine.foundation.narrative.adapters import (
    composer_input_from_domains,
)
from engines.interpretation_engine.foundation.narrative.input import (
    NarrativeComposerInput,
)


def build_composer_input_from_production(output: Any) -> NarrativeComposerInput:
    """Copy Decision, State, Relationship, and Knowledge bundles from production.

    Does not calculate astrology, select a useful god, or generate knowledge.
    """
    foundation = output.interpretation_foundation
    if foundation is None:
        return NarrativeComposerInput()
    useful_god_knowledge = None
    if foundation.useful_god_explanation is not None:
        useful_god_knowledge = build_useful_god_knowledge_bundle(
            foundation.useful_god_explanation
        )
    strength_assessment = build_strength_assessment(
        foundation.facts.strength,
        strength_result=output.strength_result,
    )
    strength_knowledge = build_strength_knowledge_bundle(strength_assessment)
    pattern_bundle = build_pattern_interpretation_bundle(
        build_pattern_facts(
            foundation.facts.pattern,
            pattern_context=output.pattern_context,
            pattern_result=output.pattern_result,
        )
    )
    ten_god_bundle = build_ten_god_interpretation_bundle(
        _ten_god_facts(output)
    )
    shensha_bundle = build_shensha_interpretation_bundle(
        _shensha_facts(output)
    )
    return composer_input_from_domains(
        useful_god_explanation=foundation.useful_god_explanation,
        useful_god_interpretation=foundation.useful_god_interpretation,
        useful_god_knowledge=useful_god_knowledge,
        strength_assessment=strength_assessment,
        strength_knowledge=strength_knowledge,
        pattern_bundle=pattern_bundle,
        ten_god_bundle=ten_god_bundle,
        shensha_bundle=shensha_bundle,
        current_dayun=_current_dayun(output),
        five_elements=_five_elements(output),
        dominant_element=_dominant_element(output),
    )


def _ten_god_facts(output: Any):
    """Copy Ten God facts from production without rerunning the engine."""
    foundation = output.interpretation_foundation
    bazi = foundation.context.bazi
    branches: dict[str, str] = {}
    for pillar in TEN_GOD_PILLAR_KEYS:
        text = str(getattr(bazi, pillar) or "")
        parts = text.split()
        if len(parts) >= 2:
            branches[pillar] = parts[-1]
    return build_ten_god_facts(
        foundation.facts.ten_gods,
        ten_gods_result=output.ten_gods,
        strength_level=foundation.facts.strength.level,
        pattern_label=foundation.facts.pattern.label,
        useful_god_selected=foundation.facts.useful_god.selected,
        pillar_branches=branches,
    )


def _shensha_facts(output: Any):
    """Copy Shen Sha facts from production names without rematching."""
    foundation = output.interpretation_foundation
    bazi = foundation.context.bazi
    pillars = {slot: str(getattr(bazi, slot) or "") for slot in TEN_GOD_PILLAR_KEYS}
    stems: list[str] = []
    branches: list[str] = []
    for text in pillars.values():
        parts = str(text).split()
        if parts:
            stems.append(parts[0])
        if len(parts) >= 2:
            branches.append(parts[-1])
    matched = tuple(output.analysis.bazi.shensha or ())
    ten_god_roles = tuple(dict.fromkeys(item.ten_god for item in output.ten_gods.visible))
    return build_shensha_facts(
        foundation.facts.shensha,
        matched_names=matched,
        day_master=bazi.day_master,
        stems=stems,
        branches=branches,
        pillars=pillars,
        pattern_label=foundation.facts.pattern.label,
        ten_god_roles=ten_god_roles,
        strength_level=foundation.facts.strength.level,
    )


def _current_dayun(output: Any) -> str:
    """Copy the confirmed current luck cycle label. Do not interpret luck."""
    luck = getattr(output, "luck", None) or {}
    if not isinstance(luck, dict):
        return ""
    current = luck.get("current_cycle") or luck.get("current_dayun") or {}
    if not isinstance(current, dict):
        return str(current or "")
    gan = str(current.get("gan_zhi") or current.get("ganzhi") or "").strip()
    years = ""
    start = current.get("year_start")
    end = current.get("year_end")
    if start and end:
        years = f"{start}–{end}"
    return " ".join(part for part in (gan, years) if part)


_ELEMENT_LABELS: tuple[tuple[str, str], ...] = (
    ("wood", "Mộc"),
    ("fire", "Hỏa"),
    ("earth", "Thổ"),
    ("metal", "Kim"),
    ("water", "Thủy"),
)


def _five_elements(output: Any) -> tuple[tuple[str, int], ...]:
    """Copy five-element counts. Does not recalculate wuxing."""
    foundation = getattr(output, "interpretation_foundation", None)
    if foundation is None:
        return ()
    facts = getattr(getattr(foundation, "facts", None), "five_elements", None)
    if facts is None:
        facts = getattr(getattr(foundation, "context", None), "five_elements", None)
    if facts is None:
        return ()
    items: list[tuple[str, int]] = []
    for field, label in _ELEMENT_LABELS:
        value = getattr(facts, field, None)
        if value is None:
            continue
        items.append((label, int(value)))
    return tuple(items)


def _dominant_element(output: Any) -> str:
    """Copy the thickest element name when counts exist."""
    counts = _five_elements(output)
    if not counts:
        return ""
    return max(counts, key=lambda item: item[1])[0]
