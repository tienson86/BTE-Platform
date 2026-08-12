"""Build ExecutiveClaimPlan from reasoning result — no prose sentences."""

from __future__ import annotations

from applications.production.interpretation.cross_domain.models import (
    CrossDomainRelation,
    DomainClaim,
    ExecutiveClaimPlan,
    ReasoningTheme,
    RelationType,
    ThemeStatus,
)
from applications.production.interpretation.cross_domain import theme_engine as te


def build_executive_claim_plan(
    claims: list[DomainClaim],
    themes: list[ReasoningTheme],
    relations: list[CrossDomainRelation],
) -> ExecutiveClaimPlan:
    """Fill executive slots with claim values / theme labels — not sentences."""
    by_id = {c.claim_id: c for c in claims}
    primary = next((t for t in themes if t.status == ThemeStatus.PRIMARY), None)
    secondary = next((t for t in themes if t.status == ThemeStatus.SECONDARY), None)

    strength = by_id.get("str_body_level")
    pattern = by_id.get("pat_structure")
    tg = by_id.get("tg_primary")
    ug = by_id.get("ug_strategy")

    identity_bits = []
    if primary:
        identity_bits.append(primary.label)
    if strength:
        identity_bits.append(f"body:{strength.value}")
    if pattern:
        identity_bits.append(f"structure:{pattern.value}")

    operating = tg.value if tg else (secondary.label if secondary else "")
    support = ""
    if ug:
        support = f"balance:{ug.value}"
    elif strength and strength.value in {"strong", "very_strong"}:
        support = f"capacity:{strength.value}"

    constraint = ""
    for theme in themes:
        if theme.theme_id == te.THEME_OVERLOAD_RISK and theme.status != ThemeStatus.SUPPRESSED:
            constraint = theme.theme_id
            break
    if not constraint:
        for relation in relations:
            if relation.relation_type in {
                RelationType.CONDITIONAL_NUANCE,
                RelationType.DEPENDENCY_OVERRIDE,
                RelationType.TRUE_CONFLICT,
            }:
                constraint = relation.relation_id
                break

    balance = ug.value if ug else ""
    insight = primary.label if primary else ""
    # Prefer balance+structure insight when follow/output, not overload.
    theme_ids = {t.theme_id: t for t in themes if t.status != ThemeStatus.SUPPRESSED}
    if te.THEME_FOLLOW_STRUCTURE in theme_ids and te.THEME_OPERATING_OUTPUT in theme_ids:
        insight = (
            f"{theme_ids[te.THEME_FOLLOW_STRUCTURE].label} + "
            f"{theme_ids[te.THEME_OPERATING_OUTPUT].label}"
        )
    elif te.THEME_CAPACITY_STRONG in theme_ids and te.THEME_OVERLOAD_RISK in theme_ids:
        insight = theme_ids[te.THEME_OVERLOAD_RISK].label
    elif te.THEME_BALANCE_DIRECTION in theme_ids:
        insight = theme_ids[te.THEME_BALANCE_DIRECTION].label

    priorities: list[str] = []
    if tg:
        priorities.append(f"align_operating_role:{tg.value}")
    if ug:
        priorities.append(f"apply_balance:{ug.value}")
    if strength and strength.value == "balanced":
        priorities.append("keep_load_recovery_rhythm")
    if strength and strength.value in {"strong", "very_strong"}:
        priorities.append("convert_load_to_defined_output")
    if pattern:
        priorities.append(f"keep_structure_consistency:{pattern.value}")
    priorities = priorities[:3]

    avoidances: list[str] = []
    if te.THEME_OVERLOAD_RISK in theme_ids:
        avoidances.append("avoid_reflex_extra_load")
    if te.THEME_FOLLOW_STRUCTURE in theme_ids:
        avoidances.append("avoid_forcing_ordinary_daymaster_frame")
    if te.THEME_OPERATING_OUTPUT in theme_ids:
        avoidances.append("avoid_suppressing_expression_channel")
    if te.THEME_CAPACITY_BALANCED in theme_ids:
        avoidances.append("avoid_overexertion_cycles")
    while len(avoidances) < 3:
        avoidances.append("avoid_claims_beyond_published_data")
    avoidances = avoidances[:3]

    unresolved = []
    for relation in relations:
        if relation.relation_type in {RelationType.TRUE_CONFLICT, RelationType.UNRESOLVED}:
            unresolved.append(relation.unresolved_blocker or relation.relation_id)
        if relation.relation_type == RelationType.DEPENDENCY_OVERRIDE:
            unresolved.append(f"qualified:{relation.relation_id}")

    return ExecutiveClaimPlan(
        identity_core=" | ".join(identity_bits),
        operating_style=operating,
        main_support=support,
        main_constraint=constraint,
        balance_direction=balance,
        primary_insight=insight,
        priorities=priorities,
        avoidances=avoidances,
        unresolved=unresolved,
    )
