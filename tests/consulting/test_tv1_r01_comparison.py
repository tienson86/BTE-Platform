"""TV1-R01 comparative marriage decision tests."""

from __future__ import annotations

import json
from pathlib import Path

from consulting.marriage.models.enums import (
    ComparisonFactKind,
    MarriageDomain,
    RelationshipSubject,
)
from consulting.marriage.narrative.facts import render_fact
from consulting.marriage.report.access import customer_visible_text
from tests.consulting.golden.cases import GOLDEN_CASES, run_golden_case
from tests.consulting.narrative_fixtures import compose_report_bundle


_GENERIC_LABELS = (
    "Điểm hỗ trợ nền tảng",
    "Điểm bổ trợ vai trò",
    "Điểm cần lưu ý ở nền tảng",
    "Điểm ma sát Can Chi",
    "Điểm bổ trợ tài chính",
)


def test_comparison_is_attached_without_mutating_evidence() -> None:
    """Comparison is a parallel overlay. Evidence ids stay frozen."""
    decision, _, _, _ = compose_report_bundle()
    assert decision.comparison is not None
    before = [item.evidence_id for item in decision.evidence]
    assert [item.evidence_id for item in decision.evidence] == before
    assert decision.overall.score is None
    assert decision.overall.grade is None


def test_d1_exposes_directional_element_comparison() -> None:
    """D1 answers who supports whom on published useful-god elements."""
    decision, _, _, _ = compose_report_bundle()
    comparison = decision.comparison
    assert comparison is not None
    d1 = comparison.five_elements
    assert d1.available is True
    facts = [
        item
        for item in comparison.facts
        if item.domain is MarriageDomain.FIVE_ELEMENTS
        and item.template_key == "useful_god_support"
    ]
    assert facts
    directions = {item.subject for item in facts}
    assert directions <= {
        RelationshipSubject.A_TO_B,
        RelationshipSubject.B_TO_A,
        RelationshipSubject.MUTUAL,
        RelationshipSubject.SHARED,
    }
    assert d1.mutual_state
    assert "missing" not in d1.mutual_state


def test_d2_exposes_named_stem_branch_interactions() -> None:
    """D2 facts name relation type and pillars instead of a generic friction label."""
    signature = run_golden_case("CASE-M02")
    decision = signature["decision"]
    comparison = decision.comparison
    assert comparison is not None
    clash = [
        item
        for item in comparison.facts
        if item.template_key == "branch_clash"
    ]
    assert clash
    assert clash[0].slots.get("relation_type") == "branch_clash"
    assert clash[0].slots.get("slot_a") or clash[0].slots.get("slot_b")


def test_d3_names_the_role_being_complemented_or_pressured() -> None:
    """Role facts include the published role name, not a generic label."""
    decision, _, _, _ = compose_report_bundle()
    comparison = decision.comparison
    assert comparison is not None
    roles = [
        item
        for item in comparison.facts
        if item.domain is MarriageDomain.TEN_GODS
        and item.kind in {ComparisonFactKind.SUPPORT, ComparisonFactKind.CONFLICT}
    ]
    if not roles:
        return
    assert all(item.slots.get("role") for item in roles)
    assert all(item.slots.get("theme") for item in roles)


def test_d4_is_derived_from_d1_d2_d3_only() -> None:
    """D4 comparison facts trace to earlier-domain evidence. No new psychology."""
    decision, _, _, _ = compose_report_bundle()
    comparison = decision.comparison
    assert comparison is not None
    source_ids = {
        eid
        for item in comparison.facts
        if item.domain in {MarriageDomain.FIVE_ELEMENTS, MarriageDomain.STEM_BRANCH, MarriageDomain.TEN_GODS}
        for eid in item.evidence_ids
    }
    derived = [item for item in comparison.facts if item.domain is MarriageDomain.INTERACTION]
    for item in derived:
        assert item.evidence_ids
        assert set(item.evidence_ids) <= source_ids


def test_d7_children_stays_unavailable() -> None:
    """Children comparison is not fabricated."""
    decision, _, _, _ = compose_report_bundle()
    comparison = decision.comparison
    assert comparison is not None
    assert comparison.children.available is False
    assert not [
        item
        for item in comparison.facts
        if item.domain is MarriageDomain.CHILDREN
    ]


def test_overall_questions_are_structured_before_narrative() -> None:
    """Q1–Q7 exist on the decision comparison object."""
    decision, payload, _, _ = compose_report_bundle()
    comparison = decision.comparison
    assert comparison is not None
    overall = comparison.overall
    assert overall.q1_compatibility == decision.overall.state.value
    assert overall.q2_mutual_support
    assert overall.q3_asymmetry
    assert overall.q4_conflict
    assert overall.q5_rescue
    assert overall.q6_long_term
    assert overall.q7_condition
    assert payload.overall_comparison is not None
    assert payload.overall_comparison.q1_text


def test_customer_report_has_no_generic_placeholder_labels() -> None:
    """Standalone generic labels must not appear without a specific comparison fact."""
    _, _, _, report = compose_report_bundle()
    blob = customer_visible_text(report)
    for phrase in _GENERIC_LABELS:
        assert phrase not in blob
    assert "/100" not in blob
    assert "Grade" not in blob


def test_comparison_facts_render_without_internal_ids() -> None:
    """Customer fact sentences never expose EV-/F-/CF- identities."""
    decision, payload, _, _ = compose_report_bundle()
    comparison = decision.comparison
    assert comparison is not None
    for fact in comparison.facts:
        text = render_fact(fact, "An", "Binh")
        assert "EV-" not in text
        assert "F-" not in text
        assert "CF-" not in text
    for item in payload.comparison_facts:
        assert "EV-" not in item.text
        assert item.fact_id.startswith("CF-")


def test_golden_overall_state_remains_mixed() -> None:
    """R01 must not force Golden overall states off MIXED."""
    for case in GOLDEN_CASES:
        signature = run_golden_case(case.case_id)["signature"]
        assert signature["overall_state"] == "mixed"
        assert signature["score"] is None
        assert signature["grade"] is None


def test_golden_evidence_truth_unchanged_for_m01_m02() -> None:
    """B08 evidence identities stay frozen while comparison is added."""
    m01 = run_golden_case("CASE-M01")["signature"]
    m02 = run_golden_case("CASE-M02")["signature"]
    types_m01 = {item["type"] for item in m01["evidence"]}
    types_m02 = {item["type"] for item in m02["evidence"]}
    assert "useful_god_support" in types_m01
    assert "branch_clash" not in types_m01
    assert "useful_god_support" in types_m02
    assert "branch_clash" in types_m02


def test_golden_comparison_signature_frozen() -> None:
    """New R01 comparison Golden files freeze directional semantics, not prose."""
    expected_dir = Path(__file__).resolve().parent / "golden" / "comparison"
    for case in GOLDEN_CASES:
        expected_path = expected_dir / f"{case.case_id}.json"
        assert expected_path.is_file(), f"missing comparison golden {expected_path}"
        actual = run_golden_case(case.case_id)["signature"]["comparison"]
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        assert actual == expected
        assert actual["q1"] == "mixed"
        assert actual["d7_available"] is False
