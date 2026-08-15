"""Pattern relationship records — generic Relationship Framework types only."""

from __future__ import annotations

from engines.interpretation_engine.foundation.interpreters.pattern.facts import (
    PatternFacts,
)
from engines.interpretation_engine.foundation.relationship import (
    GenericRelationshipExplainer,
    RelationshipAssessment,
    RelationshipEvidence,
    RelationshipInput,
    RelationshipRecord,
)
from engines.interpretation_engine.foundation.relationship.types import (
    RELATIONSHIP_GENERATES,
    RELATIONSHIP_SUPPORTS,
)


def build_pattern_relationship_input(facts: PatternFacts) -> RelationshipInput:
    """Build upstream relationship records from PatternFacts. No new astrology."""
    records: list[RelationshipRecord] = []
    evidence: list[RelationshipEvidence] = []
    rule_id = facts.rule_ids[0] if facts.rule_ids else ""
    if facts.month_command and facts.selected:
        records.append(
            RelationshipRecord(
                source=f"month_command:{facts.month_command}",
                target=f"pattern:{facts.selected}",
                relationship_type=RELATIONSHIP_GENERATES,
                confidence=facts.confidence,
                rule_ids=facts.rule_ids,
                evidence_ids=("ev_month_command",),
                fact_refs=("month_command", "selected"),
                source_kind="month_command",
                target_kind="pattern",
                source_label=facts.month_command,
                target_label=facts.label or facts.selected,
                record_id="rel_month_command_pattern",
                source_origin="PatternContext.month_branch_ten_god",
                target_origin="PatternResult.pattern",
            )
        )
        evidence.append(
            _evidence(
                "ev_month_command",
                "month_branch_ten_god",
                facts.month_command,
                rule_id,
                facts.confidence,
            )
        )
    if facts.day_master and facts.selected:
        records.append(
            RelationshipRecord(
                source=f"day_master:{facts.day_master}",
                target=f"pattern:{facts.selected}",
                relationship_type=RELATIONSHIP_SUPPORTS,
                confidence=facts.confidence,
                rule_ids=facts.rule_ids,
                evidence_ids=("ev_day_master",),
                fact_refs=("day_master", "selected"),
                source_kind="day_master",
                target_kind="pattern",
                source_label=facts.day_master,
                target_label=facts.label or facts.selected,
                record_id="rel_day_master_pattern",
                source_origin="PatternContext.day_master",
                target_origin="PatternResult.pattern",
            )
        )
        evidence.append(
            _evidence(
                "ev_day_master",
                "day_master",
                facts.day_master,
                rule_id,
                facts.confidence,
            )
        )
    for index, god in enumerate(facts.ten_gods, start=1):
        if god == facts.month_command:
            continue
        evidence_id = f"ev_ten_god_{index}"
        records.append(
            RelationshipRecord(
                source=f"ten_god:{god}",
                target=f"pattern:{facts.selected}",
                relationship_type=RELATIONSHIP_SUPPORTS,
                confidence=facts.confidence,
                rule_ids=facts.rule_ids,
                evidence_ids=(evidence_id,),
                fact_refs=("ten_gods",),
                source_kind="ten_god",
                target_kind="pattern",
                source_label=god,
                target_label=facts.label or facts.selected,
                record_id=f"rel_ten_god_{index}",
                source_origin="PatternContext.ten_gods_list",
                target_origin="PatternResult.pattern",
            )
        )
        evidence.append(
            _evidence(evidence_id, "ten_gods_list", god, rule_id, facts.confidence)
        )
    return RelationshipInput(
        domain="Pattern",
        records=tuple(records),
        evidence=tuple(evidence),
        confidence=facts.confidence,
    )


def explain_pattern_relationships(facts: PatternFacts) -> RelationshipAssessment:
    """Run generic RelationshipExplainer on PatternFacts-derived records."""
    return GenericRelationshipExplainer().explain(build_pattern_relationship_input(facts))


def _evidence(
    evidence_id: str,
    field: str,
    value: str,
    rule_id: str,
    confidence: float,
) -> RelationshipEvidence:
    """Copy one upstream field as evidence."""
    return RelationshipEvidence(
        evidence_id=evidence_id,
        source_engine="PatternEngine",
        source_field=field,
        rule_id=rule_id,
        fact=field,
        value=value,
        confidence=confidence,
    )
