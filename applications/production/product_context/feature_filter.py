"""Feature visibility and safety filters for product context."""

from __future__ import annotations

from applications.production.product_context.models import (
    ActionProfile,
    LanguageProfile,
    LifeStage,
    PurchasePackage,
    ReaderRole,
    ReportType,
)

# Feature ids used in delivery.
FEATURE_IDENTITY = "identity_report"
FEATURE_CAREER = "career_report"
FEATURE_EXECUTIVE = "executive_consulting"
FEATURE_DEVELOPMENT = "development_guidance"
FEATURE_PARENT = "parent_guidance"
FEATURE_LEGACY = "legacy_reflection"
FEATURE_DOMAINS = "domain_interpretations"


def select_features(
    *,
    life_stage: LifeStage,
    reader_role: ReaderRole,
    purchase_package: PurchasePackage,
    report_type: ReportType,
) -> tuple[list[str], list[str], list[str]]:
    """Return (visible, hidden, blocked_sections)."""
    visible: list[str] = [FEATURE_DOMAINS]
    hidden: list[str] = []
    blocked: list[str] = []

    if life_stage == LifeStage.CHILD:
        visible.extend([FEATURE_IDENTITY, FEATURE_DEVELOPMENT, FEATURE_PARENT])
        # Soft executive for parents — not adult decision consulting.
        if reader_role in {ReaderRole.PARENT, ReaderRole.UNKNOWN, ReaderRole.SELF}:
            visible.append(FEATURE_EXECUTIVE)
        hidden.extend([FEATURE_CAREER, FEATURE_LEGACY])
        blocked.extend(
            [
                "career_decision",
                "business_advice",
                "marriage_timing",
                "income_projection",
                "job_title_recommendation",
            ]
        )
    elif life_stage == LifeStage.TEEN:
        visible.extend([FEATURE_IDENTITY, FEATURE_DEVELOPMENT, FEATURE_EXECUTIVE])
        hidden.append(FEATURE_CAREER)
        blocked.extend(["business_expansion", "marriage_timing", "income_projection"])
        if reader_role == ReaderRole.PARENT:
            visible.append(FEATURE_PARENT)
    elif life_stage == LifeStage.SENIOR:
        visible.extend(
            [FEATURE_IDENTITY, FEATURE_EXECUTIVE, FEATURE_LEGACY, FEATURE_CAREER]
        )
    else:
        # YOUNG_ADULT / ADULT / MID_CAREER
        visible.extend([FEATURE_IDENTITY, FEATURE_CAREER, FEATURE_EXECUTIVE])

    # Package gates (additive hide — never invent truth).
    if purchase_package == PurchasePackage.PACKAGE_A:
        if FEATURE_CAREER in visible:
            visible.remove(FEATURE_CAREER)
            hidden.append(FEATURE_CAREER)
        if FEATURE_EXECUTIVE in visible and life_stage != LifeStage.CHILD:
            # A = identity-first; keep executive only if not child soft summary needed
            visible.remove(FEATURE_EXECUTIVE)
            hidden.append(FEATURE_EXECUTIVE)
    elif purchase_package == PurchasePackage.PACKAGE_B:
        # Professional: identity + career + executive for adults
        pass
    elif purchase_package == PurchasePackage.PACKAGE_C:
        pass

    # Explicit report_type request cannot unblock safety.
    if report_type == ReportType.CAREER and FEATURE_CAREER in hidden:
        blocked.append("career_requested_but_blocked_by_life_stage")

    # Deduplicate preserve order.
    visible = list(dict.fromkeys(visible))
    hidden = list(dict.fromkeys([f for f in hidden if f not in visible]))
    blocked = list(dict.fromkeys(blocked))
    return visible, hidden, blocked


def select_language_profile(
    *,
    life_stage: LifeStage,
    reader_role: ReaderRole,
) -> LanguageProfile:
    """Select framing profile — does not rewrite claims."""
    if reader_role == ReaderRole.PARENT or life_stage == LifeStage.CHILD:
        return LanguageProfile.PARENT_SUPPORT
    if life_stage == LifeStage.TEEN:
        return LanguageProfile.GUIDANCE
    if life_stage == LifeStage.SENIOR:
        return LanguageProfile.SENIOR_REFLECTION
    if life_stage == LifeStage.YOUNG_ADULT:
        return LanguageProfile.COACHING
    if reader_role == ReaderRole.CONSULTANT:
        return LanguageProfile.CONSULTING
    return LanguageProfile.CONSULTING


def select_action_profile(
    *,
    life_stage: LifeStage,
    reader_role: ReaderRole,
) -> ActionProfile:
    """Select who actions address."""
    if life_stage == LifeStage.CHILD or reader_role == ReaderRole.PARENT:
        return ActionProfile.PARENT_ACTIONS
    if life_stage == LifeStage.TEEN:
        return ActionProfile.DEVELOPMENT_SUPPORT
    if life_stage == LifeStage.SENIOR:
        return ActionProfile.LEGACY_PLANNING
    return ActionProfile.SELF_DECISIONS


def select_tone(
    *,
    language_profile: LanguageProfile,
) -> str:
    """Tone label for delivery diagnostics."""
    mapping = {
        LanguageProfile.PARENT_SUPPORT: "parent_supportive",
        LanguageProfile.GUIDANCE: "developmental_guidance",
        LanguageProfile.COACHING: "coaching",
        LanguageProfile.CONSULTING: "consultant",
        LanguageProfile.SENIOR_REFLECTION: "reflective_senior",
    }
    return mapping[language_profile]


def safety_blocks_for(
    *,
    life_stage: LifeStage,
    visible: list[str],
) -> list[str]:
    """Impossible outputs prevented by context."""
    blocks: list[str] = []
    if life_stage in {LifeStage.CHILD, LifeStage.TEEN}:
        blocks.append("NO_ADULT_CAREER_DECISION")
        blocks.append("NO_BUSINESS_EXPANSION")
        blocks.append("NO_MARRIAGE_TIMING")
    if life_stage == LifeStage.CHILD and FEATURE_CAREER in visible:
        blocks.append("INVARIANT_VIOLATION_CAREER_VISIBLE_FOR_CHILD")
    return blocks
