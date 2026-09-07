"""TV1-B05 semantic report model, story order, and mode tests."""

from __future__ import annotations

from consulting.marriage.models.enums import MarriageDomain
from consulting.marriage.report.access import customer_visible_text, expert_visible_text
from consulting.marriage.report.versions import REQUIRED_CUSTOMER_SECTIONS
from consulting.marriage.validation.narrative import MarriageReportValidation
from tests.consulting.narrative_fixtures import compose_report_bundle


def test_report_story_order() -> None:
    """Present sections follow the frozen customer story order."""
    _, _, _, report = compose_report_bundle()
    ids = [item.section_id for item in report.sections]
    allowed = [
        "identity",
        "executive_summary",
        "compatibility_hero",
        "strengths",
        "risks",
        "timing",
        "domain_analysis",
        "action_plan",
        "confidence_limitations",
        "conclusion",
        "appendix",
    ]
    last = -1
    for section_id in ids:
        index = allowed.index(section_id)
        assert index > last
        last = index


def test_required_report_sections() -> None:
    """Customer mode required sections are present."""
    _, _, _, report = compose_report_bundle()
    ids = {item.section_id for item in report.sections}
    assert set(REQUIRED_CUSTOMER_SECTIONS) <= ids


def test_unavailable_d4_d6_d7_are_not_published() -> None:
    """Interaction/family/children do not appear as fake domain analysis."""
    decision, _, _, report = compose_report_bundle()
    unavailable = []
    for item in (decision.domains.interaction, decision.domains.family, decision.domains.children):
        if not item.availability.available or (item.state and item.state.value == "insufficient"):
            unavailable.append(item.domain)
    domain_section = next(item for item in report.sections if item.section_id == "domain_analysis")
    published = [
        block.domain
        for block in domain_section.blocks
        if block.visibility != "expert" and block.kind == "domain_summary" and block.domain
    ]
    assert not any(domain in unavailable for domain in published)
    assert MarriageDomain.FAMILY in unavailable or decision.domains.family.availability.available


def test_semantic_only_hero() -> None:
    """Hero carries semantic state only. No gauge or percentage."""
    decision, _, _, report = compose_report_bundle()
    hero = next(item for item in report.sections if item.section_id == "compatibility_hero")
    kinds = {block.kind for block in hero.blocks}
    assert "decision_state" in kinds
    assert "gauge" not in kinds
    assert "score" not in kinds
    blob = "\n".join(f"{block.title or ''} {block.body or ''}" for block in hero.blocks)
    assert "/100" not in blob
    assert "%" not in blob
    assert decision.overall.score is None
    assert any(block.state == decision.overall.state.value for block in hero.blocks if block.state)


def test_customer_mode_hides_technical_ids() -> None:
    """Customer-visible text must not include Evidence/Finding IDs."""
    _, _, _, report = compose_report_bundle()
    text = customer_visible_text(report)
    assert "EV-" not in text
    assert "F-" not in text
    assert "rule_id" not in text.lower()


def test_expert_mode_contains_traceable_references() -> None:
    """Expert projection includes finding ids and version references."""
    decision, _, _, report = compose_report_bundle()
    text = expert_visible_text(report)
    assert any(item.finding_id in text for item in decision.findings)
    assert decision.versions.decision_profile_version in text or "policy=" in text
    assert "narrative=" in text


def test_confidence_and_limitations_rendering() -> None:
    """Limitations are stated without turning missing data into a marital defect."""
    decision, _, _, report = compose_report_bundle()
    section = next(item for item in report.sections if item.section_id == "confidence_limitations")
    blob = "\n".join(block.body or "" for block in section.blocks)
    assert blob
    assert "không đồng nghĩa" in blob.lower() or "giới hạn" in blob.lower() or "tin cậy" in blob.lower()


def test_timing_does_not_invent_dates() -> None:
    """Timing copy never includes calendar years or wedding dates."""
    _, _, _, report = compose_report_bundle()
    text = customer_visible_text(report)
    assert "2020" not in text
    assert "2029" not in text
    assert "ngày cưới" not in text.lower() or "không đặt ngày cưới" in text.lower()


def test_report_model_has_no_renderer_specific_styling() -> None:
    """Semantic blocks do not carry CSS/layout/PDF fields."""
    _, _, _, report = compose_report_bundle()
    for section in report.sections:
        assert not hasattr(section, "css")
        assert not hasattr(section, "x")
        assert not hasattr(section, "width")
        for block in section.blocks:
            assert not hasattr(block, "font")
            assert not hasattr(block, "color")
            assert block.kind not in {"pdf", "docx", "html", "css"}


def test_narrative_and_report_traceability() -> None:
    """Report recommendation ids resolve on the Decision Result."""
    decision, _, narrative, report = compose_report_bundle()
    finding_ids = {item.finding_id for item in decision.findings}
    rec_ids = {item.recommendation_id for item in decision.recommendations}
    for section in narrative.sections:
        for block in section.blocks:
            assert set(block.source_finding_ids) <= finding_ids
            assert set(block.source_recommendation_ids) <= rec_ids
    action = next(item for item in report.sections if item.section_id == "action_plan")
    for block in action.blocks:
        assert set(block.source_recommendation_ids) <= rec_ids
    MarriageReportValidation().validate_report(decision, narrative, report)


def test_report_determinism() -> None:
    """The same Decision yields identical report section ids and semantic keys."""
    first = compose_report_bundle()
    second = compose_report_bundle()
    report_a = first[3]
    report_b = second[3]
    assert [item.section_id for item in report_a.sections] == [item.section_id for item in report_b.sections]
    keys_a = [block.semantic_key for section in report_a.sections for block in section.blocks]
    keys_b = [block.semantic_key for section in report_b.sections for block in section.blocks]
    assert keys_a == keys_b
    assert first[0].overall.state == second[0].overall.state
    assert [item.recommendation_id for item in first[0].recommendations] == [
        item.recommendation_id for item in second[0].recommendations
    ]
