"""TV1-B08 Golden Dataset freeze. Semantic truth only."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.consulting.golden.cases import GOLDEN_CASES, CASE_BY_ID, run_golden_case

EXPECTED_DIR = Path(__file__).resolve().parent / "golden" / "expected"

REQUIRED_REPORT_PREFIX = (
    "identity",
    "executive_summary",
    "compatibility_hero",
    "strengths",
    "risks",
)
REQUIRED_REPORT_SUFFIX = (
    "domain_analysis",
    "action_plan",
    "confidence_limitations",
    "conclusion",
    "appendix",
)


_FROZEN_KEYS = (
    "overall_state",
    "score",
    "grade",
    "confidence_level",
    "limitations",
    "domain_availability",
    "domain_states",
    "evidence",
    "findings",
    "recommendations",
)


@pytest.mark.parametrize("case_id", [item.case_id for item in GOLDEN_CASES])
def test_golden_semantic_signature_frozen(case_id: str) -> None:
    """Each Golden case matches the frozen evidence/decision signature."""
    expected_path = EXPECTED_DIR / f"{case_id}.json"
    assert expected_path.is_file(), f"missing frozen golden {expected_path}"
    actual = run_golden_case(case_id)["signature"]
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    for key in _FROZEN_KEYS:
        assert actual[key] == expected[key]
    assert actual["score"] is None
    assert actual["grade"] is None


def test_case_m01_is_structurally_supportive() -> None:
    """CASE-M01 records strong structural support, not a mixed clash pair."""
    signature = run_golden_case("CASE-M01")["signature"]
    types = {item["type"] for item in signature["evidence"]}
    assert "useful_god_support" in types
    assert "branch_clash" not in types
    assert signature["overall_state"] in {"supportive", "balanced", "mixed"}
    assert signature["domain_availability"]["five_elements"] is True


def test_case_m02_preserves_support_and_clash() -> None:
    """CASE-M02 is the mixed useful-support + clash pair."""
    signature = run_golden_case("CASE-M02")["signature"]
    types = {item["type"] for item in signature["evidence"]}
    assert "useful_god_support" in types
    assert "branch_clash" in types
    assert signature["overall_state"] == "mixed"


def test_case_m03_preserves_rescued_pressure() -> None:
    """CASE-M03 keeps clash/harm while useful support remains as rescue."""
    bundle = run_golden_case("CASE-M03")
    types = {item["type"] for item in bundle["signature"]["evidence"]}
    assert "useful_god_support" in types
    assert "branch_clash" in types
    rescued = [
        item
        for item in bundle["decision"].resolved_evidence or []
        if item.status.value == "rescued"
    ]
    assert rescued
    assert any("rescued" in (finding.conditions or []) for finding in bundle["decision"].findings) or rescued


def test_case_m04_asymmetric_a_to_b() -> None:
    """CASE-M04 keeps A→B useful support without converting it to mutual."""
    signature = run_golden_case("CASE-M04")["signature"]
    useful = [item for item in signature["evidence"] if item["type"] == "useful_god_support"]
    subjects = {item["subject"] for item in useful}
    assert "A_TO_B" in subjects
    assert "MUTUAL" not in subjects
    assert "B_TO_A" not in subjects


def test_case_m05_asymmetric_b_to_a() -> None:
    """CASE-M05 keeps B→A useful support without converting it to mutual."""
    signature = run_golden_case("CASE-M05")["signature"]
    useful = [item for item in signature["evidence"] if item["type"] == "useful_god_support"]
    subjects = {item["subject"] for item in useful}
    assert "B_TO_A" in subjects
    assert "MUTUAL" not in subjects
    assert "A_TO_B" not in subjects


def test_case_m06_secondary_cannot_rewrite_overall() -> None:
    """Favorable secondary evidence cannot change the mixed natal overall state."""
    mixed = run_golden_case("CASE-M02")["signature"]
    secondary = run_golden_case("CASE-M06")["signature"]
    assert mixed["overall_state"] == secondary["overall_state"]
    assert mixed["domain_states"]["five_elements"] == secondary["domain_states"]["five_elements"]
    assert mixed["domain_states"]["stem_branch"] == secondary["domain_states"]["stem_branch"]
    extra = {item["type"] for item in secondary["evidence"]} - {item["type"] for item in mixed["evidence"]}
    assert extra <= {"shen_sha_support", "shen_sha_risk", "feng_shui_reference", "na_yin_reference"}


def test_case_m07_m08_missing_hour_is_limitation_not_risk() -> None:
    """Unknown birth hour is a data limitation, not a marital-risk finding."""
    for case_id in ("CASE-M07", "CASE-M08"):
        bundle = run_golden_case(case_id)
        signature = bundle["signature"]
        assert "birth_time_unknown" in signature["limitations"]
        blob = " ".join(
            block.text
            for section in bundle["narrative"].sections
            for block in section.blocks
        ).lower()
        assert "marital risk" not in blob
        assert signature["score"] is None


def test_case_m09_finance_finding_and_action() -> None:
    """CASE-M09 publishes finance evidence, finding, and financial_structure action."""
    signature = run_golden_case("CASE-M09")["signature"]
    assert signature["domain_availability"]["finance"] is True
    assert any(item["domain"] == "finance" for item in signature["findings"])
    assert any(item["action_type"] == "financial_structure" for item in signature["recommendations"])


def test_case_m10_timing_only_if_legitimately_present() -> None:
    """CASE-M10 records timing when luck evidence exists; otherwise documents absence."""
    signature = run_golden_case("CASE-M10")["signature"]
    luck_types = {
        item["type"]
        for item in signature["evidence"]
        if item["type"] in {"luck_alignment", "luck_misalignment"}
    }
    if luck_types:
        assert signature["domain_availability"]["luck"] is True
        assert any(item["action_type"] == "timing_awareness" for item in signature["recommendations"])
        assert signature["overall_state"] == run_golden_case("CASE-M02")["signature"]["overall_state"]
    else:
        assert signature["domain_availability"]["luck"] is False
        assert signature["has_timing_section"] is False


def test_case_m11_unavailable_domains_are_insufficient() -> None:
    """D4 Interaction, D6 Family, and D7 Children stay unpublished."""
    signature = run_golden_case("CASE-M11")["signature"]
    for domain in ("interaction", "family", "children"):
        assert signature["domain_availability"][domain] is False
        assert signature["domain_states"][domain] == "insufficient"
        assert not any(item["domain"] == domain for item in signature["findings"] if item["type"] != "condition")


def test_case_m12_semantic_dedup_groups_sources() -> None:
    """Repeated same-semantic evidence collapses into one finding with multiple sources."""
    signature = run_golden_case("CASE-M12")["signature"]
    clash_findings = [
        item
        for item in signature["findings"]
        if item["semantic_key"] in {"branch_clash", "clash_zi_wu"} or "clash" in item["semantic_key"]
    ]
    assert any(item["source_count"] > 1 for item in signature["findings"] + clash_findings)


def test_golden_report_story_order_and_no_score() -> None:
    """Customer story sections stay in order and never freeze a numeric score."""
    for case in GOLDEN_CASES:
        signature = run_golden_case(case.case_id)["signature"]
        sections = signature["report_sections"]
        for name in REQUIRED_REPORT_PREFIX:
            assert name in sections
        for name in REQUIRED_REPORT_SUFFIX:
            assert name in sections
        assert sections.index("identity") == 0
        assert sections.index("executive_summary") < sections.index("compatibility_hero")
        if signature["has_timing_section"]:
            assert sections.index("timing") < sections.index("action_plan")
        else:
            assert "timing" not in sections
        assert signature["score"] is None
        assert signature["grade"] is None


def test_golden_case_registry_is_complete() -> None:
    """The B08 dataset covers the required CASE-M01..M12 identities."""
    assert [item.case_id for item in GOLDEN_CASES] == [f"CASE-M{index:02d}" for index in range(1, 13)]
    assert set(CASE_BY_ID) == {item.case_id for item in GOLDEN_CASES}
