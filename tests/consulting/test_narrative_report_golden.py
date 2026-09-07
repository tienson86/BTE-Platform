"""Golden narrative/report semantics. Structure and keys, not full prose snapshots."""

from __future__ import annotations

from consulting.marriage.narrative.versions import NARRATIVE_CATALOG_VERSION, NARRATIVE_VERSION
from consulting.marriage.report.versions import REPORT_MODEL_VERSION, report_profile_token
from consulting.marriage.validation.narrative import MarriageReportValidation
from tests.consulting.narrative_fixtures import compose_report_bundle


def test_golden_narrative_report_semantics() -> None:
    """Golden pair produces stable section ids, catalog keys, and source refs."""
    decision, payload, narrative, report = compose_report_bundle()
    assert decision.overall.score is None
    assert decision.overall.grade is None
    assert decision.overall.state is not None
    assert narrative.version == NARRATIVE_VERSION
    assert narrative.catalog_version == NARRATIVE_CATALOG_VERSION
    overall = next(section for section in narrative.sections if section.section_id == "overall")
    assert overall.blocks[0].catalog_key.startswith("marriage.overall.")
    assert overall.blocks[0].catalog_key.endswith(decision.overall.state.value)

    ids = [item.section_id for item in report.sections]
    assert ids[0] == "identity"
    assert ids[1] == "executive_summary"
    assert ids[2] == "compatibility_hero"
    assert "action_plan" in ids
    assert "appendix" in ids
    assert report.metadata.consultation_id == decision.consultation_id
    assert report.metadata.narrative_version == NARRATIVE_VERSION
    assert report.metadata.report_profile_version == report_profile_token()
    assert report.metadata.report_model_version == REPORT_MODEL_VERSION
    assert report.metadata.person_a_correlation_id.endswith("-A") or report.metadata.person_a_correlation_id == decision.person_a.analysis_id
    assert report.metadata.language == "vi"

    family_published = any(
        block.domain and block.domain.value == "family" and block.kind == "domain_summary"
        for section in report.sections
        if section.section_id == "domain_analysis"
        for block in section.blocks
        if block.visibility != "expert"
    )
    assert family_published is False
    children_published = any(
        block.domain and block.domain.value == "children" and block.kind == "domain_summary"
        for section in report.sections
        if section.section_id == "domain_analysis"
        for block in section.blocks
        if block.visibility != "expert"
    )
    assert children_published is False

    rec_ids = {item.recommendation_id for item in decision.recommendations}
    action = next(item for item in report.sections if item.section_id == "action_plan")
    reported_actions = {
        rec_id
        for block in action.blocks
        for rec_id in block.source_recommendation_ids
    }
    assert reported_actions <= rec_ids
    MarriageReportValidation().validate_report(decision, narrative, report)
    assert payload.score_model_version == "unavailable"
