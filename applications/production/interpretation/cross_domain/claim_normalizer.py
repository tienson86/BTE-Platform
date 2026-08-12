"""Normalize engine + domain outputs into DomainClaim objects."""

from __future__ import annotations

from applications.production.interpretation.cross_domain.models import (
    ClaimScope,
    ClaimType,
    ConfidenceState,
    CrossDomainReasoningInput,
    DomainClaim,
    QuestionContext,
)


def _is_follow_pattern(pattern_key: str, pattern_label: str, tong_cach: str) -> bool:
    blob = f"{pattern_key} {pattern_label} {tong_cach}".lower()
    return "tong_" in pattern_key.lower() or "tòng" in blob or "tong " in blob


def normalize_claims(
    data: CrossDomainReasoningInput,
) -> list[DomainClaim]:
    """Build normalized claims from canonical input."""
    claims: list[DomainClaim] = []
    ctx = data.question_context

    if data.strength_level:
        claims.append(
            DomainClaim(
                claim_id="str_body_level",
                domain="strength",
                claim_type=ClaimType.CLASSIFICATION,
                subject="body_strength",
                value=data.strength_level,
                scope=ClaimScope.BODY_STRENGTH,
                strength=max(0.1, float(data.strength_score) or 0.5),
                evidence_refs=["strength_result.strength_level"],
                confidence_state=ConfidenceState.HIGH,
                customer_relevance=0.9 if ctx == QuestionContext.IDENTITY else 0.7,
                question_relevance=0.9 if ctx != QuestionContext.CAREER else 0.6,
                raw_text=data.domain_conclusions.get("strength", ""),
            )
        )

    if data.pattern_label or data.pattern_key:
        follow = _is_follow_pattern(
            data.pattern_key, data.pattern_label, data.tong_cach
        )
        claims.append(
            DomainClaim(
                claim_id="pat_structure",
                domain="pattern",
                claim_type=ClaimType.STRUCTURE,
                subject="destiny_structure",
                value=data.pattern_label or data.pattern_key,
                scope=ClaimScope.STRUCTURAL_PATTERN,
                strength=0.9 if follow else 0.75,
                dependencies=["follow_pattern"] if follow else [],
                evidence_refs=["pattern.cach_cuc", "pattern.pattern"],
                confidence_state=ConfidenceState.HIGH,
                customer_relevance=0.85,
                question_relevance=0.8 if ctx == QuestionContext.IDENTITY else 0.7,
                raw_text=data.domain_conclusions.get("pattern", ""),
            )
        )
        if follow:
            claims.append(
                DomainClaim(
                    claim_id="pat_follow_flag",
                    domain="pattern",
                    claim_type=ClaimType.CLASSIFICATION,
                    subject="follow_pattern",
                    value="FOLLOW",
                    scope=ClaimScope.STRUCTURAL_PATTERN,
                    strength=1.0,
                    evidence_refs=["pattern.tong_cach", "pattern.pattern"],
                    confidence_state=ConfidenceState.HIGH,
                    customer_relevance=0.9,
                    question_relevance=0.85,
                    raw_text=data.tong_cach or data.pattern_label,
                )
            )

    if data.ten_gods_primary:
        primary = ", ".join(data.ten_gods_primary)
        claims.append(
            DomainClaim(
                claim_id="tg_primary",
                domain="ten_gods",
                claim_type=ClaimType.OPERATING_ROLE,
                subject="dominant_operating_role",
                value=primary,
                scope=ClaimScope.OPERATING_STYLE,
                strength=0.95,
                evidence_refs=["ten_gods.dominant.primary_god_ids"],
                confidence_state=ConfidenceState.HIGH,
                customer_relevance=0.95,
                question_relevance=1.0 if ctx == QuestionContext.CAREER else 0.85,
                raw_text=data.domain_conclusions.get("ten_gods", ""),
            )
        )
        families = set(data.ten_gods_families)
        if "output" in families:
            claims.append(
                DomainClaim(
                    claim_id="tg_output_family",
                    domain="ten_gods",
                    claim_type=ClaimType.OPERATING_ROLE,
                    subject="output_operating_family",
                    value="output",
                    scope=ClaimScope.OPERATING_STYLE,
                    strength=0.9,
                    evidence_refs=["ten_gods.hierarchy"],
                    confidence_state=ConfidenceState.HIGH,
                    customer_relevance=0.9,
                    question_relevance=0.95 if ctx == QuestionContext.CAREER else 0.8,
                )
            )
        if "officer" in families:
            claims.append(
                DomainClaim(
                    claim_id="tg_officer_family",
                    domain="ten_gods",
                    claim_type=ClaimType.CONSTRAINT,
                    subject="standards_pressure",
                    value="officer",
                    scope=ClaimScope.OPERATING_STYLE,
                    strength=0.7,
                    evidence_refs=["ten_gods.hierarchy"],
                    confidence_state=ConfidenceState.MEDIUM,
                    customer_relevance=0.7,
                    question_relevance=0.75,
                )
            )
        if "companion" in families and "output" not in families:
            claims.append(
                DomainClaim(
                    claim_id="tg_companion_family",
                    domain="ten_gods",
                    claim_type=ClaimType.OPERATING_ROLE,
                    subject="self_carry_operating",
                    value="companion",
                    scope=ClaimScope.OPERATING_STYLE,
                    strength=0.85,
                    evidence_refs=["ten_gods.hierarchy"],
                    confidence_state=ConfidenceState.HIGH,
                    customer_relevance=0.85,
                    question_relevance=0.8,
                )
            )

    if data.useful_god:
        claims.append(
            DomainClaim(
                claim_id="ug_strategy",
                domain="useful_god",
                claim_type=ClaimType.BALANCE,
                subject="balance_direction",
                value=data.useful_god,
                scope=ClaimScope.BALANCE_STRATEGY,
                strength=0.85,
                evidence_refs=["useful_god.useful_god"],
                confidence_state=ConfidenceState.HIGH,
                customer_relevance=0.8,
                question_relevance=0.85,
                raw_text=data.useful_reasoning or data.domain_conclusions.get("useful_god", ""),
            )
        )

    return claims
