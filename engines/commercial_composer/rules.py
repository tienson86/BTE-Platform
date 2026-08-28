"""INT-03B Commercial Composition Rules. Editorial specification only.

Does not run the Commercial Composer. Does not calculate analytical results.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Mapping
import re

RULES_CONTRACT_ID: Final[str] = "bte.commercial.composition_rules.v1"
RULES_VERSION: Final[str] = "1.0.0"

EDITORIAL_ROLE: Final[str] = "editor"

ALLOWED_EDITORIAL_OPERATIONS: Final[tuple[str, ...]] = (
    "reorder",
    "merge",
    "remove_repetition",
    "shorten",
    "clarify",
    "prioritize",
)

FORBIDDEN_EDITORIAL_OPERATIONS: Final[tuple[str, ...]] = (
    "invent",
    "expand",
    "reinterpret",
    "calculate",
    "predict",
    "infer",
    "hallucinate",
    "rewrite_analytical_meaning",
)

CUSTOMER_SECTION_ORDER: Final[tuple[str, ...]] = (
    "executive_summary",
    "current_situation",
    "strengths",
    "risks",
    "key_recommendation",
    "conclusion",
)

CUSTOMER_SECTION_TITLES_VI: Final[Mapping[str, str]] = {
    "executive_summary": "Tổng quan",
    "current_situation": "Hiện trạng",
    "strengths": "Điểm mạnh",
    "risks": "Điểm cần lưu ý",
    "key_recommendation": "Hướng điều chỉnh",
    "conclusion": "Kết luận",
}

CUSTOMER_ORDER_REASON: Final[str] = (
    "trust then understanding then action: "
    "published reading, current facts, constructive frame, caution, guidance, close"
)

EXECUTIVE_FINDING_PRIORITY: Final[tuple[str, ...]] = (
    "strength_level",
    "useful_god",
    "pattern",
    "luck_identity",
)

FACT_KEY_MARKERS: Final[Mapping[str, tuple[str, ...]]] = {
    "strength_level": ("Thân vượng", "Thân nhược", "Thân cân"),
    "useful_god": ("Dụng thần",),
    "pattern": ("Cách cục",),
    "luck_identity": ("Đại Vận", "Lưu Niên"),
}

RECOMMENDATION_MEANING_GROUPS: Final[tuple[str, ...]] = (
    "useful_god",
    "unfavorable",
    "climate",
)

TECHNICAL_ID_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"\b(?:str|pat|sea|tmp|ug)_[a-z0-9_]+\b",
    re.IGNORECASE,
)

MACHINE_ONLY_PREFIXES: Final[tuple[str, ...]] = ("{", "[")

FORBIDDEN_STYLE_MARKERS: Final[tuple[str, ...]] = (
    "chắc chắn",
    "nhất định",
    "sẽ giàu",
    "đại hung",
    "điềm gở",
    "vận hạn xấu",
)

RECOMMENDATION_OVERLAP_POLICY: Final[str] = "keep_strongest_published"

TRACE_ID_TEMPLATE: Final[str] = "integrated.{slot}[{index}]"

INT03A_RUNTIME_UNCHANGED: Final[bool] = True


@dataclass(slots=True, frozen=True)
class CommercialCompositionRule:
    """One canonical editorial rule."""

    rule_id: str
    name: str
    statement: str

    def to_dict(self) -> dict[str, str]:
        """Serialize the rule."""
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "statement": self.statement,
        }


COMPOSITION_RULES: Final[tuple[CommercialCompositionRule, ...]] = (
    CommercialCompositionRule(
        rule_id="C-001",
        name="executive_priority",
        statement=(
            "Executive Summary must contain the highest-priority published findings only."
        ),
    ),
    CommercialCompositionRule(
        rule_id="C-002",
        name="emit_once",
        statement="Repeated statements are emitted once.",
    ),
    CommercialCompositionRule(
        rule_id="C-003",
        name="group_recommendations",
        statement=(
            "Recommendations from multiple topics are grouped by meaning before presentation."
        ),
    ),
    CommercialCompositionRule(
        rule_id="C-004",
        name="hide_technical_ids",
        statement="Technical evidence ids are never customer-facing.",
    ),
    CommercialCompositionRule(
        rule_id="C-005",
        name="drop_machine_only",
        statement="Machine-only wording is removed.",
    ),
    CommercialCompositionRule(
        rule_id="C-006",
        name="preserve_analytical_truth",
        statement="Commercial wording must preserve analytical truth.",
    ),
    CommercialCompositionRule(
        rule_id="C-007",
        name="customer_section_order",
        statement="Customer-facing section order is frozen as six consulting sections.",
    ),
    CommercialCompositionRule(
        rule_id="C-008",
        name="traceability",
        statement=(
            "Every commercial sentence must reference Integrated Narrative sentence ids."
        ),
    ),
    CommercialCompositionRule(
        rule_id="C-009",
        name="strongest_recommendation",
        statement=(
            "Overlapping recommendations keep the strongest published version "
            "and preserve ownership."
        ),
    ),
    CommercialCompositionRule(
        rule_id="C-010",
        name="consulting_style",
        statement=(
            "Commercial Narrative is clear, professional, calm, and consulting-oriented."
        ),
    ),
)


def commercial_composition_rules() -> dict[str, Any]:
    """Return the frozen INT-03B editorial rule surface."""
    return {
        "contract_id": RULES_CONTRACT_ID,
        "rules_version": RULES_VERSION,
        "editorial_role": EDITORIAL_ROLE,
        "runtime": False,
        "recalculates": False,
        "llm": False,
        "int03a_runtime_unchanged": INT03A_RUNTIME_UNCHANGED,
        "allowed_operations": list(ALLOWED_EDITORIAL_OPERATIONS),
        "forbidden_operations": list(FORBIDDEN_EDITORIAL_OPERATIONS),
        "customer_section_order": list(CUSTOMER_SECTION_ORDER),
        "customer_section_titles_vi": dict(CUSTOMER_SECTION_TITLES_VI),
        "customer_order_reason": CUSTOMER_ORDER_REASON,
        "executive_finding_priority": list(EXECUTIVE_FINDING_PRIORITY),
        "recommendation_meaning_groups": list(RECOMMENDATION_MEANING_GROUPS),
        "recommendation_overlap_policy": RECOMMENDATION_OVERLAP_POLICY,
        "trace_id_template": TRACE_ID_TEMPLATE,
        "rules": [rule.to_dict() for rule in COMPOSITION_RULES],
    }


def integrated_sentence_id(slot: str, index: int) -> str:
    """Return the canonical Integrated sentence id for traceability."""
    return TRACE_ID_TEMPLATE.format(slot=slot, index=index)


def fact_key(text: str) -> str | None:
    """Return the published-fact key when the sentence restates a known finding."""
    for key, markers in FACT_KEY_MARKERS.items():
        if any(marker in text for marker in markers):
            return key
    return None


def is_repeated_meaning(first: str, second: str) -> bool:
    """True when two published sentences carry the same fact key."""
    left = fact_key(first)
    right = fact_key(second)
    return left is not None and left == right


def is_technical_language(text: str) -> bool:
    """True when customer prose would expose a technical evidence id."""
    return TECHNICAL_ID_PATTERN.search(text) is not None


def is_machine_only(text: str) -> bool:
    """True when the wording is a machine dump, not customer narrative."""
    stripped = text.strip()
    return bool(stripped) and stripped.startswith(MACHINE_ONLY_PREFIXES)


def is_forbidden_style(text: str) -> bool:
    """True when wording is alarmist, fortune-telling, or absolute."""
    lowered = text.casefold()
    return any(marker.casefold() in lowered for marker in FORBIDDEN_STYLE_MARKERS)


def keep_strongest_published(first: str, second: str) -> str:
    """Keep the containing published recommendation. Invent nothing."""
    left = first.strip()
    right = second.strip()
    left_core = left.rstrip(".")
    right_core = right.rstrip(".")
    if left_core in right or right_core.startswith(left_core):
        return right if len(right_core) >= len(left_core) else left
    if right_core in left or left_core.startswith(right_core):
        return left if len(left_core) >= len(right_core) else right
    return left


def is_eligible_executive_finding(text: str, source_path: str = "") -> bool:
    """True when a published sentence may enter Tổng quan."""
    if is_machine_only(text) or is_technical_language(text):
        return False
    if "compact" in source_path or "score" in source_path:
        return False
    return fact_key(text) in EXECUTIVE_FINDING_PRIORITY
