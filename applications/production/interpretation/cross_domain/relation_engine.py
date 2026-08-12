"""Scope-aware cross-domain relation detection."""

from __future__ import annotations

from applications.production.interpretation.cross_domain.models import (
    ClaimScope,
    CrossDomainRelation,
    DomainClaim,
    RelationType,
)

# Published policy refs (existing docs — not new doctrine).
POLICY_FOLLOW_VS_STRENGTH = (
    "knowledge/pilot/replay/root_cause/strength_taxonomy_v2/"
    "STRENGTH_BOUNDARY_MODEL.md#Pattern-follow-contradicts-strength"
)
POLICY_FOLLOW_PHILOSOPHY = (
    "knowledge/packages/follow_pattern/core/documentation/philosophy.md"
)


def _by_id(claims: list[DomainClaim]) -> dict[str, DomainClaim]:
    return {c.claim_id: c for c in claims}


def detect_relations(claims: list[DomainClaim]) -> list[CrossDomainRelation]:
    """Detect cross-domain relations with frozen relation types."""
    relations: list[CrossDomainRelation] = []
    index = _by_id(claims)
    strength = index.get("str_body_level")
    pattern = index.get("pat_structure")
    follow = index.get("pat_follow_flag")
    tg_primary = index.get("tg_primary")
    tg_output = index.get("tg_output_family")
    tg_companion = index.get("tg_companion_family")
    ug = index.get("ug_strategy")

    if strength and pattern:
        relations.extend(_strength_pattern(strength, pattern, follow))

    if tg_output and follow:
        relations.append(
            CrossDomainRelation(
                relation_id="tg_output_reinforces_follow",
                relation_type=RelationType.REINFORCEMENT,
                claim_a_id=tg_output.claim_id,
                claim_b_id=follow.claim_id,
                rationale=(
                    "Output-family operating style aligns with follow-output structure."
                ),
                customer_safe_state=(
                    "Hai lớp phân tích đang cùng chỉ về hướng vận hành theo đầu ra / biểu đạt."
                ),
            )
        )

    if tg_companion and strength and strength.value in {"strong", "very_strong"}:
        relations.append(
            CrossDomainRelation(
                relation_id="tg_companion_reinforces_strong",
                relation_type=RelationType.REINFORCEMENT,
                claim_a_id=tg_companion.claim_id,
                claim_b_id=strength.claim_id,
                rationale="Companion-led style reinforces strong body capacity themes.",
            )
        )

    if ug and strength:
        if strength.value in {"weak", "very_weak"} and "tiết" in (ug.raw_text or "").lower():
            relations.append(
                CrossDomainRelation(
                    relation_id="ug_drain_vs_weak",
                    relation_type=RelationType.TRUE_CONFLICT,
                    claim_a_id=strength.claim_id,
                    claim_b_id=ug.claim_id,
                    rationale="Weak body strength vs drain/output balance strategy.",
                    customer_safe_state=(
                        "Dữ liệu hiện tại chưa đủ để khẳng định một hướng cân bằng duy nhất "
                        "khi tín hiệu nội lực và chiến lược điều tiết đang căng nhau."
                    ),
                    unresolved_blocker="TRUE_CONFLICT_NEEDS_ARBITRATION",
                )
            )
        elif strength.value in {"strong", "very_strong"}:
            relations.append(
                CrossDomainRelation(
                    relation_id="ug_balance_with_strong",
                    relation_type=RelationType.CONDITIONAL_NUANCE,
                    claim_a_id=strength.claim_id,
                    claim_b_id=ug.claim_id,
                    rationale="Strong capacity with balance strategy — conditional nuance.",
                    customer_safe_state=(
                        "Kết luận này cần được hiểu có điều kiện: nội lực đủ mạnh "
                        "nhưng vẫn cần hướng điều tiết đã công bố."
                    ),
                )
            )

    if tg_primary and pattern:
        relations.append(
            CrossDomainRelation(
                relation_id="tg_vs_pattern_scope",
                relation_type=RelationType.DIFFERENT_SCOPE,
                claim_a_id=tg_primary.claim_id,
                claim_b_id=pattern.claim_id,
                rationale="Operating style vs destiny structure — different scopes.",
                customer_safe_state=(
                    "Hai lớp phân tích đang phản ánh hai khía cạnh khác nhau: "
                    "cách vận hành hàng ngày và khung cấu trúc dài hạn."
                ),
            )
        )

    if not relations and len(claims) >= 2:
        relations.append(
            CrossDomainRelation(
                relation_id="default_not_comparable_pair",
                relation_type=RelationType.NOT_COMPARABLE,
                claim_a_id=claims[0].claim_id,
                claim_b_id=claims[1].claim_id,
                rationale="No overlapping comparable scope pair detected.",
            )
        )

    return relations


def _strength_pattern(
    strength: DomainClaim,
    pattern: DomainClaim,
    follow: DomainClaim | None,
) -> list[CrossDomainRelation]:
    """Handle Strength ↔ Pattern including CASE-0002-class tension generically."""
    out: list[CrossDomainRelation] = []
    pattern_weak_language = any(
        token in (pattern.value or "").lower()
        for token in ("nhược", "cực nhược", "weak")
    )
    body = strength.value

    # Different scopes always when comparing body strength vs structural pattern.
    out.append(
        CrossDomainRelation(
            relation_id="str_pattern_scope",
            relation_type=RelationType.DIFFERENT_SCOPE,
            claim_a_id=strength.claim_id,
            claim_b_id=pattern.claim_id,
            rationale=(
                "Body strength classification and destiny-structure label "
                "evaluate different scopes."
            ),
            customer_safe_state=(
                "Hai lớp phân tích đang phản ánh hai khía cạnh khác nhau: "
                "nội lực thân và khung cấu trúc vận mệnh."
            ),
        )
    )

    if follow is not None:
        # Published boundary policy: publish both; lower confidence.
        out.append(
            CrossDomainRelation(
                relation_id="follow_qualifies_strength",
                relation_type=RelationType.DEPENDENCY_OVERRIDE,
                claim_a_id=follow.claim_id,
                claim_b_id=strength.claim_id,
                rationale=(
                    "Follow/special pattern classification recontextualizes how "
                    "ordinary body-strength is read for structure — does not delete "
                    "the strength publish."
                ),
                policy_ref=POLICY_FOLLOW_VS_STRENGTH,
                customer_safe_state=(
                    "Kết luận này cần được hiểu có điều kiện: khung Tòng/cấu trúc đặc biệt "
                    "định hình cách đọc nội lực thường — hai tín hiệu đều được giữ, "
                    "không chọn một cái thay cho cái kia."
                ),
            )
        )
        out.append(
            CrossDomainRelation(
                relation_id="follow_strength_nuance",
                relation_type=RelationType.CONDITIONAL_NUANCE,
                claim_a_id=strength.claim_id,
                claim_b_id=follow.claim_id,
                rationale="Follow pattern + body strength form conditional nuance.",
                policy_ref=POLICY_FOLLOW_PHILOSOPHY,
                customer_safe_state=(
                    "Nội lực công bố và khung Tòng cùng đúng trong phạm vi của chúng; "
                    "khách hàng cần đọc cả hai lớp."
                ),
            )
        )
        return out

    if pattern_weak_language and body in {"strong", "very_strong", "balanced"}:
        out.append(
            CrossDomainRelation(
                relation_id="str_pattern_intensity_tension",
                relation_type=RelationType.CONDITIONAL_NUANCE,
                claim_a_id=strength.claim_id,
                claim_b_id=pattern.claim_id,
                rationale=(
                    "Intensity wording differs across scopes without follow flag — nuance."
                ),
                customer_safe_state=(
                    "Hai lớp phân tích đang phản ánh hai khía cạnh khác nhau về cường độ; "
                    "không gộp thành một nhãn duy nhất."
                ),
            )
        )

    if pattern_weak_language and body in {"strong", "very_strong"} and follow is None:
        # Apparent contradiction without published override policy for non-follow.
        if strength.scope == pattern.scope:
            out.append(
                CrossDomainRelation(
                    relation_id="str_pattern_true_conflict",
                    relation_type=RelationType.TRUE_CONFLICT,
                    claim_a_id=strength.claim_id,
                    claim_b_id=pattern.claim_id,
                    rationale="Same-scope intensity contradiction.",
                    unresolved_blocker="SAME_SCOPE_INTENSITY_CONFLICT",
                    customer_safe_state=(
                        "Dữ liệu hiện tại chưa đủ để khẳng định một mức cường độ duy nhất."
                    ),
                )
            )

    return out


def scopes_overlap(a: ClaimScope, b: ClaimScope) -> bool:
    """Return True when scopes are comparable for conflict."""
    if a == b:
        return True
    if a == ClaimScope.GENERAL or b == ClaimScope.GENERAL:
        return True
    return False
