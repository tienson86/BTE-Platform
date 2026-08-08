"""Build CompositionSource from analysis/interpretation + NarrativeTree."""

from __future__ import annotations

from typing import Any

from engines.narrative_engine.runtime.input_adapter import (
    _is_technical,
    build_runtime_input,
)
from engines.narrative_engine.runtime.models import EvidenceKind, NarrativeTree

from .source_bundle import CompositionSource, SourceFact


def build_composition_source(
    tree: NarrativeTree,
    *,
    analysis: Any = None,
    interpretation: Any = None,
) -> CompositionSource:
    """
    Build factual source bundle for D2 composer.

    Extracts labels/values/texts from sources; does not invent conclusions.
    """
    runtime_input = build_runtime_input(analysis=analysis, interpretation=interpretation)
    facts: dict[str, SourceFact] = {}

    # Seed from runtime evidence ids, then enrich with payload values.
    for unit in runtime_input.evidence:
        facts[unit.id] = SourceFact(
            id=unit.id,
            kind=unit.kind.value,
            label=unit.kind.value,
            value="",
            raw_text="",
            source_path=unit.source_path,
            confidence=unit.confidence,
            commercial_ok=unit.commercial_ok,
        )
    _enrich_from_analysis_dict(facts, analysis if isinstance(analysis, dict) else {})

    interpretation_facts: dict[str, SourceFact] = {}
    for ref in runtime_input.interpretation_refs:
        body = _section_body(interpretation, ref.section_id)
        interpretation_facts[ref.id] = SourceFact(
            id=ref.id,
            kind="interpretation",
            label=ref.title or ref.section_id,
            value="",
            raw_text=body if ref.commercial_ok else "",
            source_path=f"interpretation.sections.{ref.section_id}",
            rule_refs=_rule_refs_from_analysis(analysis),
            knowledge_refs=("knowledge:interpretation_section",),
            confidence=0.7 if ref.commercial_ok else 0.0,
            commercial_ok=ref.commercial_ok and bool(body.strip()),
        )

    return CompositionSource(
        tree=tree,
        facts=facts,
        interpretation_facts=interpretation_facts,
        analysis=analysis,
        interpretation=interpretation,
    )


def _enrich_from_analysis_dict(facts: dict[str, SourceFact], data: dict[str, Any]) -> None:
    """Attach concrete values from orchestrator-style analysis dict."""
    bazi = data.get("bazi") if isinstance(data.get("bazi"), dict) else {}
    pattern = data.get("pattern") if isinstance(data.get("pattern"), dict) else {}
    useful = data.get("useful_god") if isinstance(data.get("useful_god"), dict) else {}
    strength = data.get("strength") if isinstance(data.get("strength"), dict) else {}
    score = data.get("score") if isinstance(data.get("score"), dict) else {}

    def upsert(
        fact_id: str,
        *,
        kind: str,
        label: str,
        value: str,
        raw_text: str = "",
        source_path: str,
        confidence: float,
        rule_refs: tuple[str, ...] = (),
        knowledge_refs: tuple[str, ...] = (),
    ) -> None:
        commercial_ok = not _is_technical(raw_text or value or label)
        existing = facts.get(fact_id)
        facts[fact_id] = SourceFact(
            id=fact_id,
            kind=kind,
            label=label,
            value=value,
            raw_text=raw_text if commercial_ok else "",
            source_path=source_path,
            rule_refs=rule_refs or (existing.rule_refs if existing else ()),
            knowledge_refs=knowledge_refs
            or (existing.knowledge_refs if existing else ("knowledge:analysis",)),
            confidence=confidence,
            commercial_ok=commercial_ok,
        )

    if bazi.get("day_master"):
        upsert(
            "ev-day-master",
            kind=EvidenceKind.IDENTITY.value,
            label="Nhật chủ",
            value=str(bazi.get("day_master")),
            source_path="bazi.day_master",
            confidence=0.9,
            knowledge_refs=("knowledge:bazi.day_master",),
        )
    if pattern.get("cach_cuc") or pattern.get("pattern"):
        upsert(
            "ev-pattern",
            kind=EvidenceKind.IDENTITY.value,
            label="Cách cục",
            value=str(pattern.get("cach_cuc") or pattern.get("pattern")),
            source_path="pattern.cach_cuc",
            confidence=0.8,
            knowledge_refs=("knowledge:pattern",),
        )
    if strength or score.get("strength_score") is not None:
        level = str(strength.get("strength_level") or "")
        score_v = strength.get("strength_score", score.get("strength_score", ""))
        reasoning = str(strength.get("reasoning") or "")
        upsert(
            "ev-strength",
            kind=EvidenceKind.STRENGTH.value,
            label="Thân",
            value=" ".join(part for part in (level, str(score_v)) if part).strip(),
            raw_text=reasoning,
            source_path="strength",
            confidence=0.75,
            knowledge_refs=("knowledge:strength",),
        )
        if reasoning:
            upsert(
                "ev-explanation",
                kind=EvidenceKind.EXPLANATION.value,
                label="Lý giải thân",
                value="",
                raw_text=reasoning,
                source_path="strength.reasoning",
                confidence=0.55,
                knowledge_refs=("knowledge:strength.reasoning",),
            )
            upsert(
                "ev-implication",
                kind=EvidenceKind.IMPLICATION.value,
                label="Ý nghĩa thân",
                value="",
                raw_text=reasoning,
                source_path="strength.reasoning",
                confidence=0.5,
                knowledge_refs=("knowledge:strength.reasoning",),
            )
    commercial_action = str(useful.get("commercial_recommendation") or "").strip()
    action_value = str(
        useful.get("useful_god")
        or pattern.get("dung_than")
        or score.get("analytical_recommendation")
        or ("" if commercial_action else score.get("recommendation"))
        or ""
    )
    if action_value or commercial_action:
        matched = useful.get("matched_rules") if isinstance(useful.get("matched_rules"), list) else []
        knowledge_unit = str(score.get("commercial_knowledge_unit_id") or "")
        upsert(
            "ev-action",
            kind=EvidenceKind.ACTION.value,
            label="Dụng thần / khuyến nghị",
            value=action_value or commercial_action,
            raw_text=commercial_action,
            source_path="useful_god|score.recommendation|commercial",
            confidence=0.77,
            rule_refs=tuple(str(item) for item in matched),
            knowledge_refs=(
                (f"knowledge:{knowledge_unit}",)
                if knowledge_unit
                else ("knowledge:useful_god",)
            ),
        )
    risk_value = ""
    if isinstance(useful.get("unfavorable_gods"), list) and useful.get("unfavorable_gods"):
        risk_value = ", ".join(str(item) for item in useful["unfavorable_gods"])
    elif pattern.get("ky_than"):
        risk_value = str(pattern.get("ky_than"))
    commercial_weakness = str(
        useful.get("commercial_weakness_text")
        or score.get("commercial_weakness")
        or strength.get("commercial_weakness_text")
        or ""
    ).strip()
    if risk_value or commercial_weakness:
        upsert(
            "ev-risk",
            kind=EvidenceKind.RISK.value,
            label="Kỵ / bất lợi",
            value=risk_value or commercial_weakness,
            raw_text=commercial_weakness,
            source_path="useful_god.unfavorable|pattern.ky_than|commercial",
            confidence=0.65,
            knowledge_refs=("knowledge:risk",),
        )
        upsert(
            "ev-weakness",
            kind=EvidenceKind.WEAKNESS.value,
            label="Điểm hạn chế",
            value=risk_value or commercial_weakness,
            raw_text=commercial_weakness,
            source_path="useful_god.unfavorable|pattern.ky_than|commercial",
            confidence=0.65,
            knowledge_refs=("knowledge:weakness",),
        )
    if score.get("grade") is not None:
        upsert(
            "ev-grade",
            kind=EvidenceKind.GRADE.value,
            label="Hạng",
            value=str(score.get("grade")),
            source_path="score.grade",
            confidence=0.7,
            knowledge_refs=("knowledge:score",),
        )


def _section_body(interpretation: Any, section_id: str) -> str:
    """Read interpretation section body by id without mutating sources."""
    if interpretation is None:
        return ""
    sections: list[Any]
    if isinstance(interpretation, dict):
        raw = interpretation.get("sections") or []
        sections = raw if isinstance(raw, list) else []
    else:
        raw = getattr(interpretation, "sections", None)
        sections = raw if isinstance(raw, list) else []
    for section in sections:
        if isinstance(section, dict):
            if str(section.get("id") or "") == section_id:
                return str(section.get("body") or section.get("content") or "")
            continue
        if str(getattr(section, "id", "")) == section_id:
            return str(getattr(section, "body", "") or "")
    return ""


def _rule_refs_from_analysis(analysis: Any) -> tuple[str, ...]:
    """Collect matched rule ids when present on useful_god."""
    if not isinstance(analysis, dict):
        return ()
    useful = analysis.get("useful_god")
    if not isinstance(useful, dict):
        return ()
    matched = useful.get("matched_rules")
    if not isinstance(matched, list):
        return ()
    return tuple(str(item) for item in matched if item)
