"""TV1-B05 narrative source-trace, catalog, and no-invention tests."""

from __future__ import annotations

import inspect

from consulting.marriage.exceptions import MarriageNarrativeError
from consulting.marriage.models.enums import DomainDecisionState
from consulting.marriage.narrative import composer as composer_module
from consulting.marriage.narrative.catalog import action_entry, domain_entry, overall_entry
from consulting.marriage.narrative.composer import CanonicalNarrativeComposer
from consulting.marriage.narrative.input import narrative_input_from_decision
from consulting.marriage.narrative.versions import LANGUAGE_VI, NARRATIVE_CATALOG_VERSION
from consulting.marriage.validation.narrative import MarriageNarrativeValidation
from tests.consulting.narrative_fixtures import compose_narrative, decision_with_recommendations


def test_narrative_reads_decision_and_recommendation_only() -> None:
    """Composer source must not reread Canonical snapshots or raw pillars."""
    source = inspect.getsource(composer_module)
    assert "canonical_a" not in source
    assert "useful_god" not in source
    assert "ten_gods" not in source
    assert "pillars" not in source
    assert "snapshot_a" not in source


def test_narrative_cannot_create_a_new_finding() -> None:
    """Narrative explains existing findings and does not append new ones."""
    decision = decision_with_recommendations()
    before = [item.finding_id for item in decision.findings]
    _, payload, narrative = compose_narrative(decision)
    assert [item.finding_id for item in decision.findings] == before
    used = {
        finding_id
        for section in narrative.sections
        for block in section.blocks
        for finding_id in block.source_finding_ids
    }
    assert used <= set(before)
    assert payload.findings
    assert [item.finding_id for item in payload.findings] == before


def test_narrative_cannot_create_a_new_recommendation() -> None:
    """Narrative communicates B04 actions and does not invent new ones."""
    decision = decision_with_recommendations()
    before = [item.recommendation_id for item in decision.recommendations]
    _, _, narrative = compose_narrative(decision)
    assert [item.recommendation_id for item in decision.recommendations] == before
    used = {
        rec_id
        for section in narrative.sections
        for block in section.blocks
        for rec_id in block.source_recommendation_ids
    }
    assert used <= set(before)


def test_no_score_grade_fabrication_in_narrative() -> None:
    """Narrative must not invent 82/100, Grade A-E, or percentages."""
    decision, _, narrative = compose_narrative()
    assert decision.overall.score is None
    assert decision.overall.grade is None
    blob = "\n".join(block.text for section in narrative.sections for block in section.blocks)
    lowered = blob.lower()
    assert "/100" not in lowered
    assert "grade a" not in lowered
    assert "%" not in blob
    MarriageNarrativeValidation().validate_narrative(decision, narrative)


def test_semantic_catalog_lookup() -> None:
    """Catalog keys are semantic, not raw birth facts."""
    supportive = overall_entry(DomainDecisionState.SUPPORTIVE.value)
    mixed = overall_entry(DomainDecisionState.MIXED.value)
    pressured = overall_entry(DomainDecisionState.PRESSURED.value)
    assert supportive.key == "marriage.overall.supportive"
    assert mixed.key == "marriage.overall.mixed"
    assert pressured.key == "marriage.overall.pressured"
    from consulting.marriage.models.enums import MarriageDomain

    five = domain_entry(MarriageDomain.FIVE_ELEMENTS, "supportive")
    assert five is not None
    assert five.key == "marriage.domain.five_elements.supportive"
    _, _, narrative = compose_narrative()
    keys = {block.catalog_key for section in narrative.sections for block in section.blocks}
    assert any(key.startswith("marriage.overall.") for key in keys)
    assert NARRATIVE_CATALOG_VERSION.startswith("marriage.narrative.catalog")


def test_customer_wording_supportive_state() -> None:
    """Supportive overall wording stays professional and non-fatalistic."""
    entry = overall_entry(DomainDecisionState.SUPPORTIVE.value)
    assert entry.headline == "Tương hợp tốt về cấu trúc"
    assert "chắc chắn" not in entry.observation.lower()
    payload_state = DomainDecisionState.SUPPORTIVE
    decision, payload, narrative = compose_narrative()
    payload.overall_state = payload_state
    rewritten = CanonicalNarrativeComposer().compose(payload)
    overall = next(section for section in rewritten.sections if section.section_id == "overall")
    assert any("Tương hợp tốt về cấu trúc" in block.text for block in overall.blocks)
    assert decision.overall.state is not None


def test_customer_wording_mixed_and_pressured_state() -> None:
    """Mixed and pressured wording uses caution without fortune claims."""
    mixed = overall_entry(DomainDecisionState.MIXED.value)
    pressured = overall_entry(DomainDecisionState.PRESSURED.value)
    assert mixed.headline == "Có một số điểm cần điều chỉnh"
    assert pressured.headline == "Cần lưu ý các điểm áp lực"
    assert "không nên cưới" not in mixed.observation.lower()
    assert "ngoại tình" not in pressured.observation.lower()
    _, payload, _ = compose_narrative()
    payload.overall_state = DomainDecisionState.MIXED
    mixed_narrative = CanonicalNarrativeComposer().compose(payload)
    overall = next(section for section in mixed_narrative.sections if section.section_id == "overall")
    assert any("Có một số điểm cần điều chỉnh" in block.text for block in overall.blocks)
    payload.overall_state = DomainDecisionState.PRESSURED
    pressured_narrative = CanonicalNarrativeComposer().compose(payload)
    overall = next(section for section in pressured_narrative.sections if section.section_id == "overall")
    assert any("Cần lưu ý" in block.text for block in overall.blocks)


def test_rescued_conditions_preserved_in_wording() -> None:
    """Rescued findings keep the condition-preservation sentence."""
    decision = decision_with_recommendations()
    rescued = [item for item in decision.findings if "rescued" in item.conditions]
    if not rescued:
        return
    _, _, narrative = compose_narrative(decision)
    blob = "\n".join(block.text for section in narrative.sections for block in section.blocks)
    assert "có thể được giảm nếu" in blob.lower()


def test_recommendation_intent_preserved() -> None:
    """Action catalog keys follow B04 action types. No new action types."""
    decision, _, narrative = compose_narrative()
    action_section = next(section for section in narrative.sections if section.section_id == "actions")
    rec_types = {item.action_type.value for item in decision.recommendations}
    catalog_types = {
        block.catalog_key.removeprefix("marriage.action.")
        for block in action_section.blocks
        if block.catalog_key.startswith("marriage.action.") and block.catalog_key != "marriage.action.none"
    }
    assert catalog_types <= rec_types
    for rec in decision.recommendations:
        entry = action_entry(rec.action_type)
        assert entry is not None
        assert rec.narrative_key is None


def test_narrative_language_is_vietnamese() -> None:
    """TV-01 V1 customer narrative is Vietnamese."""
    _, payload, narrative = compose_narrative()
    assert payload.language == LANGUAGE_VI
    assert narrative.language == LANGUAGE_VI
    blob = "\n".join(block.text for section in narrative.sections for block in section.blocks)
    assert " và " in blob


def test_narrative_validation_rejects_unresolved_finding() -> None:
    """Validation fails closed when a narrative block cites a missing finding."""
    decision, _, narrative = compose_narrative()
    narrative.sections[0].blocks[0].source_finding_ids = ["F-9999"]
    try:
        MarriageNarrativeValidation().validate_narrative(decision, narrative)
        raise AssertionError("unresolved finding must fail")
    except MarriageNarrativeError as exc:
        assert "narrative_finding_unresolved" in str(exc)


def test_input_boundary_excludes_raw_canonical() -> None:
    """NarrativeInput has identity labels and decision facts, not snapshots."""
    decision = decision_with_recommendations()
    payload = narrative_input_from_decision(decision, language=LANGUAGE_VI, audience="customer")
    assert not hasattr(payload, "canonical_a")
    assert not hasattr(payload, "evidence")
    assert payload.consultation_id == decision.consultation_id
    assert payload.person_a_correlation_id == decision.person_a.analysis_id
