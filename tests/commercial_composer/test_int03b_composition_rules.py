"""INT-03B Commercial Composition Rules. Specification only. No composer runtime."""

from __future__ import annotations

from pathlib import Path

from engines.commercial_composer.rules import (
    ALLOWED_EDITORIAL_OPERATIONS,
    COMPOSITION_RULES,
    CUSTOMER_ORDER_REASON,
    CUSTOMER_SECTION_ORDER,
    CUSTOMER_SECTION_TITLES_VI,
    EDITORIAL_ROLE,
    EXECUTIVE_FINDING_PRIORITY,
    FORBIDDEN_EDITORIAL_OPERATIONS,
    INT03A_RUNTIME_UNCHANGED,
    RECOMMENDATION_MEANING_GROUPS,
    RECOMMENDATION_OVERLAP_POLICY,
    RULES_CONTRACT_ID,
    commercial_composition_rules,
    fact_key,
    integrated_sentence_id,
    is_eligible_executive_finding,
    is_forbidden_style,
    is_machine_only,
    is_repeated_meaning,
    is_technical_language,
    keep_strongest_published,
)

ROOT = Path(__file__).resolve().parents[2]
COMPOSER_DIR = ROOT / "engines" / "commercial_composer"


def test_rule_order_is_frozen() -> None:
    """Canonical rules are published in C-001 … C-010 order."""
    assert [rule.rule_id for rule in COMPOSITION_RULES] == [
        "C-001",
        "C-002",
        "C-003",
        "C-004",
        "C-005",
        "C-006",
        "C-007",
        "C-008",
        "C-009",
        "C-010",
    ]
    payload = commercial_composition_rules()
    assert payload["contract_id"] == RULES_CONTRACT_ID
    assert payload["editorial_role"] == EDITORIAL_ROLE
    assert payload["runtime"] is False
    assert payload["int03a_runtime_unchanged"] is True
    assert INT03A_RUNTIME_UNCHANGED is True
    assert payload["rules"][0]["name"] == "executive_priority"
    assert payload["rules"][6]["name"] == "customer_section_order"


def test_customer_section_order() -> None:
    """Customer-facing order is six consulting sections, not topic-summary concat."""
    assert CUSTOMER_SECTION_ORDER == (
        "executive_summary",
        "current_situation",
        "strengths",
        "risks",
        "key_recommendation",
        "conclusion",
    )
    assert CUSTOMER_SECTION_TITLES_VI["executive_summary"] == "Tổng quan"
    assert CUSTOMER_SECTION_TITLES_VI["current_situation"] == "Hiện trạng"
    assert CUSTOMER_SECTION_TITLES_VI["strengths"] == "Điểm mạnh"
    assert CUSTOMER_SECTION_TITLES_VI["risks"] == "Điểm cần lưu ý"
    assert CUSTOMER_SECTION_TITLES_VI["key_recommendation"] == "Hướng điều chỉnh"
    assert CUSTOMER_SECTION_TITLES_VI["conclusion"] == "Kết luận"
    assert "overall_reading" not in CUSTOMER_SECTION_ORDER
    assert "trust" in CUSTOMER_ORDER_REASON
    assert "action" in CUSTOMER_ORDER_REASON


def test_editorial_role_forbids_authorship() -> None:
    """Composer may edit published prose and must not author new meaning."""
    assert ALLOWED_EDITORIAL_OPERATIONS == (
        "reorder",
        "merge",
        "remove_repetition",
        "shorten",
        "clarify",
        "prioritize",
    )
    assert "invent" in FORBIDDEN_EDITORIAL_OPERATIONS
    assert "expand" in FORBIDDEN_EDITORIAL_OPERATIONS
    assert "reinterpret" in FORBIDDEN_EDITORIAL_OPERATIONS
    assert "calculate" in FORBIDDEN_EDITORIAL_OPERATIONS
    assert "predict" in FORBIDDEN_EDITORIAL_OPERATIONS
    assert "infer" in FORBIDDEN_EDITORIAL_OPERATIONS
    assert "hallucinate" in FORBIDDEN_EDITORIAL_OPERATIONS
    assert "rewrite_analytical_meaning" in FORBIDDEN_EDITORIAL_OPERATIONS


def test_executive_selection_prioritizes_published_findings() -> None:
    """Tổng quan selects high-priority published findings. It does not concat summaries."""
    assert EXECUTIVE_FINDING_PRIORITY == (
        "strength_level",
        "useful_god",
        "pattern",
        "luck_identity",
    )
    assert is_eligible_executive_finding("Nhật chủ được đọc là Thân vượng.")
    assert is_eligible_executive_finding("Dụng thần đã công bố là Hỏa · Đinh · Chính Quan.")
    assert is_eligible_executive_finding("Cách cục đã công bố là Chính Ấn.")
    assert is_eligible_executive_finding("Đại Vận hiện tại đã công bố là Ất Tỵ.")
    assert not is_eligible_executive_finding(
        "Tướng địa theo tháng +25 · rule str_003",
        source_path="strength.evidence_compact",
    )
    assert not is_eligible_executive_finding('{"kind": "five_layer_luck_runtime_summary"}')


def test_duplicate_removal_emits_fact_once() -> None:
    """Thân vượng and Dụng thần meaning appear once."""
    assert fact_key("Nhật chủ được đọc là Thân vượng.") == "strength_level"
    assert fact_key("Phân loại lực đã công bố vẫn là Thân vượng.") == "strength_level"
    assert is_repeated_meaning(
        "Nhật chủ được đọc là Thân vượng.",
        "Phân loại lực đã công bố vẫn là Thân vượng.",
    )
    assert fact_key("Dụng thần đã công bố là Hỏa · Đinh · Chính Quan.") == "useful_god"
    assert is_repeated_meaning(
        "Dụng thần đã công bố là Hỏa · Đinh · Chính Quan.",
        "Dụng thần đã công bố vẫn là Hỏa · Đinh · Chính Quan.",
    )
    assert not is_repeated_meaning(
        "Nhật chủ được đọc là Thân vượng.",
        "Dụng thần đã công bố là Hỏa · Đinh · Chính Quan.",
    )


def test_recommendation_merge_keeps_strongest_published() -> None:
    """Overlapping recommendations keep the containing published line. No invented advice."""
    assert RECOMMENDATION_MEANING_GROUPS == (
        "useful_god",
        "unfavorable",
        "climate",
    )
    assert RECOMMENDATION_OVERLAP_POLICY == "keep_strongest_published"
    short = "Ưu tiên hướng Dụng thần đã công bố: Hỏa."
    full = "Ưu tiên hướng Dụng thần đã công bố: Hỏa · Đinh · Chính Quan."
    assert keep_strongest_published(short, full) == full
    assert keep_strongest_published(full, short) == full
    distinct = "Hạn chế Kỵ thần đã công bố: Kim."
    assert keep_strongest_published(full, distinct) == full


def test_no_rule_ids_or_json_leakage() -> None:
    """Technical ids and machine dumps are ineligible for customers."""
    assert is_technical_language("Yếu tố hỗ trợ Dụng thần: Hỷ thần, str_003, sea_001.")
    assert is_technical_language("Hỗ trợ cách cục đã công bố: pat_ca_01.")
    assert not is_technical_language("Cách cục đã công bố là Chính Ấn.")
    assert is_machine_only('{"kind": "five_layer_luck_runtime_summary"}')
    assert not is_machine_only("Đại Vận hiện tại đã công bố là Ất Tỵ.")


def test_style_forbids_alarm_and_fortune_telling() -> None:
    """Consulting voice stays calm. Absolute certainty is not commercial style."""
    assert is_forbidden_style("Bạn nhất định sẽ giàu.")
    assert is_forbidden_style("Đây là đại hung.")
    assert not is_forbidden_style("Ưu tiên hướng Dụng thần đã công bố: Hỏa.")


def test_traceability_uses_integrated_sentence_ids() -> None:
    """No orphan commercial sentence: every line cites integrated.{slot}[index]."""
    assert integrated_sentence_id("observation", 0) == "integrated.observation[0]"
    assert integrated_sentence_id("recommendation", 2) == "integrated.recommendation[2]"
    payload = commercial_composition_rules()
    assert payload["trace_id_template"] == "integrated.{slot}[{index}]"


def test_no_analytical_changes_in_rules_package() -> None:
    """Rules package does not calculate. Editorial runtime lives in compose/editor."""
    rules_source = (COMPOSER_DIR / "rules.py").read_text(encoding="utf-8")
    assert "from engines.calendar" not in rules_source
    assert "from engines.strength" not in rules_source
    assert "from engines.identity" not in rules_source
    assert "def calculate(" not in rules_source
    assert "compose_commercial_narrative" not in rules_source
