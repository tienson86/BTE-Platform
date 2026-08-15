"""Shen Sha relationship records — generic Relationship Framework types only."""

from __future__ import annotations

from engines.interpretation_engine.foundation.interpreters.shensha.facts import (
    ShenShaFacts,
)
from engines.interpretation_engine.foundation.relationship import (
    GenericRelationshipExplainer,
    RelationshipAssessment,
    RelationshipEvidence,
    RelationshipInput,
    RelationshipRecord,
)
from engines.interpretation_engine.foundation.relationship.types import (
    RELATIONSHIP_COMBINES,
    RELATIONSHIP_GENERATES,
    RELATIONSHIP_SUPPORTS,
)

_ALIAS_PAIRS: tuple[tuple[str, str], ...] = (
    ("Thiên Ất Quý Nhân", "Thiên Ất"),
    ("Hồng Loan", "Thiên Hỷ"),
    ("Thiên Đức", "Thiên Đức Quý Nhân"),
    ("Nguyệt Đức", "Nguyệt Đức Quý Nhân"),
)


def build_shensha_relationship_input(facts: ShenShaFacts) -> RelationshipInput:
    """Build upstream relationship records from ShenShaFacts. No new matching."""
    records: list[RelationshipRecord] = []
    evidence: list[RelationshipEvidence] = []
    seen: set[tuple[str, str, str]] = set()

    if facts.day_master:
        _add_evidence(evidence, "ev_day_master", "day_master", facts.day_master, "")

    for index, name in enumerate(facts.matched_shensha, start=1):
        target = f"shensha:{name}"
        evidence_id = f"ev_star_{index}"
        match = facts.matches[index - 1] if index <= len(facts.matches) else None
        rule_id = match.rule_id if match else ""
        _add_evidence(evidence, evidence_id, "matched_shensha", name, rule_id)
        if facts.day_master:
            _try_record(
                records,
                seen,
                RelationshipRecord(
                    source=f"day_master:{facts.day_master}",
                    target=target,
                    relationship_type=RELATIONSHIP_GENERATES,
                    confidence=1.0,
                    rule_ids=(rule_id,) if rule_id else (),
                    evidence_ids=("ev_day_master", evidence_id),
                    fact_refs=("day_master", "matched_shensha"),
                    source_kind="day_master",
                    target_kind="shensha",
                    source_label=facts.day_master,
                    target_label=name,
                    record_id=f"rel_dm_{index}",
                    source_origin="BaziContext.day_master",
                    target_origin="analysis.bazi.shensha",
                ),
            )

    for index, stem in enumerate(facts.related_stems, start=1):
        evidence_id = f"ev_stem_{index}"
        _add_evidence(evidence, evidence_id, "related_stems", stem, "")
        if facts.day_master:
            _try_record(
                records,
                seen,
                RelationshipRecord(
                    source=f"stem:{stem}",
                    target=f"day_master:{facts.day_master}",
                    relationship_type=RELATIONSHIP_SUPPORTS,
                    confidence=1.0,
                    evidence_ids=(evidence_id, "ev_day_master"),
                    fact_refs=("related_stems",),
                    source_kind="stem",
                    target_kind="day_master",
                    source_label=stem,
                    target_label=facts.day_master,
                    record_id=f"rel_stem_{index}",
                    source_origin="BaziContext.stems",
                    target_origin="BaziContext.day_master",
                ),
            )

    for index, branch in enumerate(facts.related_branches, start=1):
        evidence_id = f"ev_branch_{index}"
        _add_evidence(evidence, evidence_id, "related_branches", branch, "")
        if facts.day_master:
            _try_record(
                records,
                seen,
                RelationshipRecord(
                    source=f"branch:{branch}",
                    target=f"day_master:{facts.day_master}",
                    relationship_type=RELATIONSHIP_SUPPORTS,
                    confidence=1.0,
                    evidence_ids=(evidence_id, "ev_day_master"),
                    fact_refs=("related_branches",),
                    source_kind="branch",
                    target_kind="day_master",
                    source_label=branch,
                    target_label=facts.day_master,
                    record_id=f"rel_branch_{index}",
                    source_origin="BaziContext.branches",
                    target_origin="BaziContext.day_master",
                ),
            )

    for index, pillar in enumerate(facts.related_pillars, start=1):
        slot, _, value = pillar.partition(":")
        evidence_id = f"ev_pillar_{index}"
        _add_evidence(evidence, evidence_id, "related_pillars", pillar, "")
        if facts.day_master and slot:
            _try_record(
                records,
                seen,
                RelationshipRecord(
                    source=f"pillar:{slot}",
                    target=f"day_master:{facts.day_master}",
                    relationship_type=RELATIONSHIP_SUPPORTS,
                    confidence=1.0,
                    evidence_ids=(evidence_id, "ev_day_master"),
                    fact_refs=("related_pillars",),
                    source_kind="pillar",
                    target_kind="day_master",
                    source_label=value or slot,
                    target_label=facts.day_master,
                    record_id=f"rel_pillar_{index}",
                    source_origin="BaziContext.pillars",
                    target_origin="BaziContext.day_master",
                ),
            )

    present = set(facts.matched_shensha)
    for left, right in _ALIAS_PAIRS:
        if left in present and right in present:
            evidence_id = f"ev_alias_{left}"
            _add_evidence(
                evidence, evidence_id, "matched_shensha", f"{left}+{right}", ""
            )
            _try_record(
                records,
                seen,
                RelationshipRecord(
                    source=f"shensha:{left}",
                    target=f"shensha:{right}",
                    relationship_type=RELATIONSHIP_COMBINES,
                    confidence=1.0,
                    evidence_ids=(evidence_id,),
                    fact_refs=("matched_shensha",),
                    source_kind="shensha",
                    target_kind="shensha",
                    source_label=left,
                    target_label=right,
                    record_id=f"rel_alias_{left}",
                    source_origin="ShenShaService alias pair",
                    target_origin="ShenShaService alias pair",
                ),
            )

    return RelationshipInput(
        domain="ShenSha",
        records=tuple(records),
        evidence=tuple(evidence),
        confidence=1.0 if records else 0.0,
    )


def explain_shensha_relationships(facts: ShenShaFacts) -> RelationshipAssessment:
    """Run generic RelationshipExplainer on ShenShaFacts-derived records."""
    return GenericRelationshipExplainer().explain(build_shensha_relationship_input(facts))


def _try_record(
    records: list[RelationshipRecord],
    seen: set[tuple[str, str, str]],
    record: RelationshipRecord,
) -> None:
    """Skip duplicate source/target/type triples."""
    key = (record.source, record.target, record.relationship_type)
    if key in seen:
        return
    seen.add(key)
    records.append(record)


def _add_evidence(
    evidence: list[RelationshipEvidence],
    evidence_id: str,
    field: str,
    value: str,
    rule_id: str,
) -> None:
    """Copy one upstream field as evidence; skip duplicate ids."""
    if any(item.evidence_id == evidence_id for item in evidence):
        return
    evidence.append(
        RelationshipEvidence(
            evidence_id=evidence_id,
            source_engine="ShenShaService",
            source_field=field,
            rule_id=rule_id,
            fact=field,
            value=value,
            confidence=1.0,
        )
    )
