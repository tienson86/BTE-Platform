"""Ten Gods relationship records — generic Relationship Framework types only."""

from __future__ import annotations

from engines.interpretation_engine.foundation.interpreters.ten_gods.facts import (
    TenGodFacts,
    TenGodPosition,
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

_DAY_MASTER_LABEL = "Nhật Chủ"


def build_ten_god_relationship_input(facts: TenGodFacts) -> RelationshipInput:
    """Build upstream relationship records from TenGodFacts. No new astrology."""
    records: list[RelationshipRecord] = []
    evidence: list[RelationshipEvidence] = []
    seen_edges: set[tuple[str, str, str]] = set()

    if facts.day_master:
        _add_evidence(
            evidence,
            "ev_day_master",
            "day_master",
            facts.day_master,
            facts.rule_ids[0] if facts.rule_ids else "",
        )

    for index, item in enumerate(facts.positions, start=1):
        _add_position_records(records, evidence, facts, item, index, seen_edges)

    for index, edge in enumerate(facts.engine_relationships, start=1):
        source = f"ten_god:{edge['source']}"
        target = f"ten_god:{edge['target']}"
        rel_type = edge["type"]
        key = (source, target, rel_type)
        if key in seen_edges or source == target:
            continue
        evidence_id = f"ev_role_interaction_{index}"
        _add_evidence(
            evidence,
            evidence_id,
            "relationships",
            f"{edge['source']}:{rel_type}:{edge['target']}",
            facts.rule_ids[0] if facts.rule_ids else "",
        )
        records.append(
            RelationshipRecord(
                source=source,
                target=target,
                relationship_type=rel_type,
                confidence=1.0,
                rule_ids=facts.rule_ids,
                evidence_ids=(evidence_id,),
                fact_refs=("engine_relationships",),
                source_kind="ten_god",
                target_kind="ten_god",
                source_label=edge["source"],
                target_label=edge["target"],
                record_id=f"rel_role_{index}",
                source_origin="TenGodsResult.relationships",
                target_origin="TenGodsResult.relationships",
            )
        )
        seen_edges.add(key)

    return RelationshipInput(
        domain="TenGods",
        records=tuple(records),
        evidence=tuple(evidence),
        confidence=1.0 if records else 0.0,
    )


def explain_ten_god_relationships(facts: TenGodFacts) -> RelationshipAssessment:
    """Run generic RelationshipExplainer on TenGodFacts-derived records."""
    return GenericRelationshipExplainer().explain(build_ten_god_relationship_input(facts))


def _add_position_records(
    records: list[RelationshipRecord],
    evidence: list[RelationshipEvidence],
    facts: TenGodFacts,
    item: TenGodPosition,
    index: int,
    seen_edges: set[tuple[str, str, str]],
) -> None:
    """Copy Day Master → Ten God → pillar/stem/branch links for one occurrence."""
    if not item.name:
        return
    target = f"ten_god:{item.name}"
    prefix = f"{item.visibility or 'pos'}_{index}"
    if facts.day_master:
        rel_type = (
            RELATIONSHIP_COMBINES
            if item.name == _DAY_MASTER_LABEL
            else RELATIONSHIP_GENERATES
        )
        _try_record(
            records,
            seen_edges,
            RelationshipRecord(
                source=f"day_master:{facts.day_master}",
                target=target,
                relationship_type=rel_type,
                confidence=1.0,
                rule_ids=facts.rule_ids,
                evidence_ids=("ev_day_master",),
                fact_refs=("day_master", "positions"),
                source_kind="day_master",
                target_kind="ten_god",
                source_label=facts.day_master,
                target_label=item.name,
                record_id=f"rel_{prefix}_day_master",
                source_origin="TenGodInterpretationFacts.day_master",
                target_origin="TenGodPosition.name",
            ),
        )
    if item.pillar:
        evidence_id = f"ev_{prefix}_pillar"
        _add_evidence(
            evidence, evidence_id, "pillar", item.pillar, item.evidence
        )
        _try_record(
            records,
            seen_edges,
            RelationshipRecord(
                source=f"pillar:{item.pillar}",
                target=target,
                relationship_type=RELATIONSHIP_SUPPORTS,
                confidence=1.0,
                rule_ids=(item.evidence,) if item.evidence else facts.rule_ids,
                evidence_ids=(evidence_id,),
                fact_refs=("positions",),
                source_kind="pillar",
                target_kind="ten_god",
                source_label=item.pillar,
                target_label=item.name,
                record_id=f"rel_{prefix}_pillar",
                source_origin="TenGodPosition.pillar",
                target_origin="TenGodPosition.name",
            ),
        )
    if item.stem:
        evidence_id = f"ev_{prefix}_stem"
        _add_evidence(evidence, evidence_id, "stem", item.stem, item.evidence)
        _try_record(
            records,
            seen_edges,
            RelationshipRecord(
                source=f"stem:{item.pillar}:{item.stem}" if item.pillar else f"stem:{item.stem}",
                target=target,
                relationship_type=RELATIONSHIP_SUPPORTS,
                confidence=1.0,
                rule_ids=(item.evidence,) if item.evidence else facts.rule_ids,
                evidence_ids=(evidence_id,),
                fact_refs=("related_stems",),
                source_kind="stem",
                target_kind="ten_god",
                source_label=item.stem,
                target_label=item.name,
                record_id=f"rel_{prefix}_stem",
                source_origin="TenGodPosition.stem",
                target_origin="TenGodPosition.name",
            ),
        )
    if item.branch:
        evidence_id = f"ev_{prefix}_branch"
        _add_evidence(evidence, evidence_id, "branch", item.branch, item.evidence)
        _try_record(
            records,
            seen_edges,
            RelationshipRecord(
                source=(
                    f"branch:{item.pillar}:{item.branch}"
                    if item.pillar
                    else f"branch:{item.branch}"
                ),
                target=target,
                relationship_type=RELATIONSHIP_SUPPORTS,
                confidence=1.0,
                rule_ids=(item.evidence,) if item.evidence else facts.rule_ids,
                evidence_ids=(evidence_id,),
                fact_refs=("related_branches",),
                source_kind="branch",
                target_kind="ten_god",
                source_label=item.branch,
                target_label=item.name,
                record_id=f"rel_{prefix}_branch",
                source_origin="TenGodPosition.branch",
                target_origin="TenGodPosition.name",
            ),
        )


def _try_record(
    records: list[RelationshipRecord],
    seen_edges: set[tuple[str, str, str]],
    record: RelationshipRecord,
) -> None:
    """Skip duplicate source/target/type triples required by graph validation."""
    key = (record.source, record.target, record.relationship_type)
    if key in seen_edges:
        return
    seen_edges.add(key)
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
            source_engine="TenGodsEngine",
            source_field=field,
            rule_id=rule_id,
            fact=field,
            value=value,
            confidence=1.0,
        )
    )
