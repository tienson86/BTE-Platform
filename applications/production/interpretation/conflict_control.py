"""Cross-domain conflict detection — classify, do not silently pick."""

from __future__ import annotations

from applications.production.interpretation.contracts import (
    ConflictClass,
    CrossDomainConflict,
    DomainInterpretationResult,
)


def detect_conflicts(
    domains: dict[str, DomainInterpretationResult],
) -> list[CrossDomainConflict]:
    """Detect contradictions between domain conclusions."""
    conflicts: list[CrossDomainConflict] = []
    strength = domains.get("strength")
    pattern = domains.get("pattern")
    useful = domains.get("useful_god")
    ten_gods = domains.get("ten_gods")

    if strength and pattern:
        str_level = str(strength.diagnostics.get("class_id") or "")
        pattern_body = " ".join(
            paragraph
            for section in pattern.sections
            for paragraph in section.paragraphs
        )
        if str_level in {"strong", "very_strong"} and "Nhược" in pattern_body:
            conflicts.append(
                CrossDomainConflict(
                    conflict_id="str_vs_pattern_body",
                    classification=ConflictClass.DIFFERENT_SCOPE,
                    domain_a="strength",
                    domain_b="pattern",
                    claim_a=strength.conclusion,
                    claim_b="Pattern thân khí qualifier Nhược",
                    resolution=(
                        "Customer: qualify as different scopes — "
                        "engine strength vs pattern-frame thân khí."
                    ),
                )
            )

    if useful and ten_gods:
        ug = str(useful.diagnostics.get("useful_god") or "")
        tg_primary = ten_gods.diagnostics.get("primary") or []
        if ug and ug in {"Thực Thần", "Thương Quan"}:
            if ug not in tg_primary and "Thực Thần" not in (
                ten_gods.diagnostics.get("secondary") or []
            ):
                # Useful god may prescribe output while Ten Gods shows output dormant.
                secondary = ten_gods.diagnostics.get("secondary") or []
                if ug not in secondary:
                    conflicts.append(
                        CrossDomainConflict(
                            conflict_id="ug_output_vs_tg_dormant",
                            classification=ConflictClass.CONDITIONAL_NUANCE,
                            domain_a="useful_god",
                            domain_b="ten_gods",
                            claim_a=f"Useful God directs {ug}",
                            claim_b="Output role may not be currently dominant in Ten Gods",
                            resolution=(
                                "Customer: present Useful God as balance strategy, "
                                "Ten Gods as current operating emphasis — not contradiction."
                            ),
                        )
                    )

    if strength and useful:
        str_level = str(strength.diagnostics.get("class_id") or "")
        reasoning = useful.conclusion
        if str_level in {"weak", "very_weak"} and "tiết khí" in reasoning.lower():
            conflicts.append(
                CrossDomainConflict(
                    conflict_id="weak_vs_drain_strategy",
                    classification=ConflictClass.TRUE_CONFLICT,
                    domain_a="strength",
                    domain_b="useful_god",
                    claim_a=strength.conclusion,
                    claim_b=useful.conclusion,
                    resolution=(
                        "Validation retains both; customer omits unresolved drain claim "
                        "or qualifies until arbitration exists."
                    ),
                )
            )

    return conflicts


def customer_safe_claims(
    domains: dict[str, DomainInterpretationResult],
    conflicts: list[CrossDomainConflict],
) -> dict[str, str]:
    """Return domain → customer conclusion with true conflicts omitted/qualified."""
    true_conflict_domains: set[str] = set()
    for conflict in conflicts:
        if conflict.classification == ConflictClass.TRUE_CONFLICT:
            true_conflict_domains.add(conflict.domain_b)

    safe: dict[str, str] = {}
    for domain, result in domains.items():
        if domain in true_conflict_domains:
            safe[domain] = (
                f"{result.conclusion} "
                "(Cần đối chiếu thêm với tín hiệu nội lực trước khi áp dụng.)"
            )
        else:
            safe[domain] = result.conclusion
    return safe
