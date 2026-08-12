"""Chart-specific theme derivation and selection — no CASE-0001 inheritance."""

from __future__ import annotations

from applications.production.interpretation.cross_domain.models import (
    ConfidenceState,
    CrossDomainRelation,
    DomainClaim,
    QuestionContext,
    ReasoningTheme,
    RelationType,
    ThemeStatus,
)

# Theme IDs are generic capability labels — activation requires supporting claims.
THEME_CAPACITY_STRONG = "CAPACITY_STRONG"
THEME_CAPACITY_BALANCED = "CAPACITY_BALANCED"
THEME_CAPACITY_WEAK = "CAPACITY_WEAK"
THEME_FOLLOW_STRUCTURE = "FOLLOW_STRUCTURE"
THEME_STANDARD_STRUCTURE = "STANDARD_STRUCTURE"
THEME_OPERATING_OUTPUT = "OPERATING_OUTPUT"
THEME_OPERATING_SELF_CARRY = "OPERATING_SELF_CARRY"
THEME_OPERATING_STANDARDS = "OPERATING_STANDARDS"
THEME_BALANCE_DIRECTION = "BALANCE_DIRECTION"
THEME_OVERLOAD_RISK = "OVERLOAD_RISK"


def derive_themes(
    claims: list[DomainClaim],
    relations: list[CrossDomainRelation],
    question_context: QuestionContext,
) -> list[ReasoningTheme]:
    """Derive themes only when claims support them."""
    by_id = {c.claim_id: c for c in claims}
    themes: list[ReasoningTheme] = []

    strength = by_id.get("str_body_level")
    if strength:
        if strength.value in {"strong", "very_strong"}:
            themes.append(
                _theme(
                    THEME_CAPACITY_STRONG,
                    "Năng lực chịu tải / nội lực vượng",
                    [strength.claim_id],
                    ["strength"],
                    salience=0.8,
                    customer_value=0.85,
                )
            )
            themes.append(
                _theme(
                    THEME_OVERLOAD_RISK,
                    "Rủi ro ôm quá tải khi nội lực mạnh",
                    [strength.claim_id],
                    ["strength"],
                    salience=0.55,
                    customer_value=0.7,
                )
            )
        elif strength.value == "balanced":
            themes.append(
                _theme(
                    THEME_CAPACITY_BALANCED,
                    "Nội lực trung hòa — cần nhịp cân bằng",
                    [strength.claim_id],
                    ["strength"],
                    salience=0.75,
                    customer_value=0.8,
                )
            )
        else:
            themes.append(
                _theme(
                    THEME_CAPACITY_WEAK,
                    "Nội lực thiên nhược — ưu tiên bảo toàn",
                    [strength.claim_id],
                    ["strength"],
                    salience=0.8,
                    customer_value=0.85,
                )
            )

    if "pat_follow_flag" in by_id:
        themes.append(
            _theme(
                THEME_FOLLOW_STRUCTURE,
                "Khung cấu trúc Tòng — định hướng theo cách đặc biệt",
                ["pat_follow_flag", "pat_structure"],
                ["pattern"],
                salience=0.95,
                customer_value=0.9,
            )
        )
    elif "pat_structure" in by_id:
        themes.append(
            _theme(
                THEME_STANDARD_STRUCTURE,
                "Khung cấu trúc dài hạn nhất quán",
                ["pat_structure"],
                ["pattern"],
                salience=0.7,
                customer_value=0.75,
            )
        )

    if "tg_output_family" in by_id or (
        "tg_primary" in by_id
        and any(
            token in by_id["tg_primary"].value
            for token in ("Thương Quan", "Thực Thần", "shang_guan", "shi_shen")
        )
    ):
        support = ["tg_output_family"] if "tg_output_family" in by_id else ["tg_primary"]
        themes.append(
            _theme(
                THEME_OPERATING_OUTPUT,
                "Vận hành theo đầu ra / biểu đạt",
                support,
                ["ten_gods"],
                salience=0.92,
                customer_value=0.95,
            )
        )

    if "tg_companion_family" in by_id:
        themes.append(
            _theme(
                THEME_OPERATING_SELF_CARRY,
                "Vận hành tự lực / đồng hành tự gánh",
                ["tg_companion_family", "tg_primary"],
                ["ten_gods"],
                salience=0.88,
                customer_value=0.9,
            )
        )

    if "tg_officer_family" in by_id:
        themes.append(
            _theme(
                THEME_OPERATING_STANDARDS,
                "Áp lực chuẩn mực / trách nhiệm",
                ["tg_officer_family"],
                ["ten_gods"],
                salience=0.65,
                customer_value=0.7,
            )
        )

    if "ug_strategy" in by_id:
        themes.append(
            _theme(
                THEME_BALANCE_DIRECTION,
                "Hướng điều tiết cân bằng đã công bố",
                ["ug_strategy"],
                ["useful_god"],
                salience=0.8,
                customer_value=0.85,
            )
        )

    # Boost for reinforcement relations.
    for relation in relations:
        if relation.relation_type == RelationType.REINFORCEMENT:
            for theme in themes:
                if (
                    relation.claim_a_id in theme.supporting_claims
                    or relation.claim_b_id in theme.supporting_claims
                ):
                    theme.salience = min(1.0, theme.salience + 0.08)

    # Question context salience (does not change facts).
    for theme in themes:
        theme.salience = _apply_context(theme, question_context)

    return select_and_rank_themes(themes, claims, relations)


def select_and_rank_themes(
    themes: list[ReasoningTheme],
    claims: list[DomainClaim],
    relations: list[CrossDomainRelation],
) -> list[ReasoningTheme]:
    """Assign PRIMARY/SECONDARY/SUPPORTING/SUPPRESSED deterministically."""
    if not themes:
        return []

    # Suppress overload/self-carry themes when not supported by strong capacity
    # or companion claims (anti-overfit against CASE-0001-shaped narratives).
    claim_ids = {c.claim_id for c in claims}
    strength = next((c for c in claims if c.claim_id == "str_body_level"), None)
    for theme in themes:
        if theme.theme_id == THEME_OVERLOAD_RISK:
            if not strength or strength.value not in {"strong", "very_strong"}:
                theme.status = ThemeStatus.SUPPRESSED
                theme.salience = 0.0
        if theme.theme_id == THEME_OPERATING_SELF_CARRY:
            if "tg_companion_family" not in claim_ids:
                theme.status = ThemeStatus.SUPPRESSED
                theme.salience = 0.0
        if theme.theme_id == THEME_CAPACITY_STRONG:
            if strength and strength.value not in {"strong", "very_strong"}:
                theme.status = ThemeStatus.SUPPRESSED
                theme.salience = 0.0

    active = [t for t in themes if t.status != ThemeStatus.SUPPRESSED]
    active.sort(
        key=lambda t: (
            -t.salience,
            -t.customer_value,
            -len(t.supporting_claims),
            t.theme_id,
        )
    )
    if not active:
        return themes

    active[0].status = ThemeStatus.PRIMARY
    if len(active) > 1:
        active[1].status = ThemeStatus.SECONDARY
    for theme in active[2:]:
        theme.status = ThemeStatus.SUPPORTING

    # Merge suppressed back for trace.
    suppressed = [t for t in themes if t.status == ThemeStatus.SUPPRESSED]
    return active + suppressed


def _theme(
    theme_id: str,
    label: str,
    supporting: list[str],
    domains: list[str],
    *,
    salience: float,
    customer_value: float,
) -> ReasoningTheme:
    return ReasoningTheme(
        theme_id=theme_id,
        label=label,
        supporting_claims=[s for s in supporting if s],
        domains=domains,
        salience=salience,
        confidence_state=ConfidenceState.MEDIUM,
        customer_value=customer_value,
        status=ThemeStatus.SUPPORTING,
    )


def _apply_context(theme: ReasoningTheme, ctx: QuestionContext) -> float:
    score = theme.salience
    if ctx == QuestionContext.CAREER:
        if theme.theme_id in {
            THEME_OPERATING_OUTPUT,
            THEME_OPERATING_SELF_CARRY,
            THEME_OPERATING_STANDARDS,
            THEME_BALANCE_DIRECTION,
        }:
            score += 0.1
    if ctx == QuestionContext.IDENTITY:
        if theme.theme_id in {
            THEME_FOLLOW_STRUCTURE,
            THEME_CAPACITY_BALANCED,
            THEME_CAPACITY_STRONG,
            THEME_OPERATING_OUTPUT,
            THEME_OPERATING_SELF_CARRY,
        }:
            score += 0.08
    return min(1.0, score)
