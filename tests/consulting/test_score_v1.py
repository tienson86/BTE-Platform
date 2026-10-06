"""TV-01 score model V1 acceptance tests."""

from __future__ import annotations

from consulting.marriage.decision.score import (
    DOMAIN_WEIGHTS,
    grade_for_score,
    project_marriage_score,
)
from consulting.marriage.models.enums import DomainGrade, MarriageDomain
from consulting.marriage.policy.versions import ACTIVE_SCORE_MODEL_VERSION
from tests.consulting.api_fixtures import api_client, valid_body
from tests.consulting.decision_fixtures import build_test_decision, golden_pair


def test_score_weights_follow_tv01_specification() -> None:
    assert sum(DOMAIN_WEIGHTS.values()) == 100.0
    assert DOMAIN_WEIGHTS == {
        MarriageDomain.FIVE_ELEMENTS: 20.0,
        MarriageDomain.STEM_BRANCH: 18.0,
        MarriageDomain.TEN_GODS: 18.0,
        MarriageDomain.INTERACTION: 15.0,
        MarriageDomain.FINANCE: 10.0,
        MarriageDomain.FAMILY: 8.0,
        MarriageDomain.CHILDREN: 4.0,
        MarriageDomain.LUCK: 7.0,
    }


def test_score_projection_is_deterministic_and_traceable() -> None:
    result_a = build_test_decision()
    result_b = build_test_decision()
    audit_a = project_marriage_score(result_a)
    audit_b = project_marriage_score(result_b)

    assert audit_a.overall_score == audit_b.overall_score
    assert audit_a.grade == audit_b.grade
    assert 0.0 <= audit_a.overall_score <= 100.0
    assert result_a.overall.score == audit_a.overall_score
    assert result_a.overall.grade == audit_a.grade
    assert result_a.overall.domain_scores
    assert all(
        item.score is None or 0.0 <= item.score <= 100.0
        for item in audit_a.domain_scores
    )
    assert any(item.evidence_ids for item in audit_a.domain_scores if item.score is not None)


def test_unavailable_domains_are_excluded_instead_of_defaulting_to_fifty() -> None:
    result = build_test_decision()
    audit = project_marriage_score(result)
    unavailable = [item for item in audit.domain_scores if item.score is None]
    assert unavailable
    assert all(item.effective_weight == 0.0 for item in unavailable)
    assert all(item.contribution == 0.0 for item in unavailable)


def test_cung_phi_and_house_group_are_bounded_secondary_adjustments() -> None:
    snapshot_a, snapshot_b = golden_pair()
    assert snapshot_a.feng_shui is not None
    assert snapshot_b.feng_shui is not None
    snapshot_a.feng_shui.cung_phi = "Khảm"
    snapshot_a.feng_shui.group = "Đông Tứ Trạch"
    snapshot_b.feng_shui.cung_phi = "Tốn"
    snapshot_b.feng_shui.group = "Đông Tứ Trạch"

    result = build_test_decision(snapshot_a, snapshot_b)
    audit = project_marriage_score(result)
    assert -3.0 <= audit.secondary_modifier <= 3.0
    keys = {item.key for item in audit.modifier_audit}
    assert "cung_phi_same_group" in keys
    assert any(key.startswith("cung_phi_") and key != "cung_phi_same_group" for key in keys)


def test_day_master_relation_is_a_bounded_stem_branch_adjustment() -> None:
    result = build_test_decision()
    audit = project_marriage_score(result)
    stem = next(item for item in audit.domain_scores if item.domain is MarriageDomain.STEM_BRANCH)
    day_master = next(item for item in stem.adjustments if item.key.startswith("day_master_"))
    assert -4.0 <= day_master.value <= 4.0


def test_grade_mapping_uses_frozen_bands() -> None:
    assert grade_for_score(81.0) is DomainGrade.A
    assert grade_for_score(61.0) is DomainGrade.B
    assert grade_for_score(41.0) is DomainGrade.C
    assert grade_for_score(21.0) is DomainGrade.D
    assert grade_for_score(20.0) is DomainGrade.E


def test_api_opt_in_returns_and_persists_explainable_score() -> None:
    client, _container = api_client()
    body = valid_body(gender_a="female", gender_b="male")
    body["options"] = {"include_score": True}

    response = client.post("/api/v1/consulting/marriage", json=body)

    assert response.status_code == 201
    payload = response.json()
    assert payload["status"] == "SUCCESS"
    data = payload["data"]
    assert 0.0 <= data["score"] <= 100.0
    assert data["grade"] in {"A", "B", "C", "D", "E"}
    assert data["domain_scores"]
    cung_phi = next(item for item in data["domain_scores"] if item["domain"] == "cung_phi")
    assert 0.0 <= cung_phi["score"] <= 100.0
    assert cung_phi["weight"] == 3.0
    assert "giới hạn ±3" in cung_phi["weight_label"]
    assert data["versions"]["score_model_version"] == ACTIVE_SCORE_MODEL_VERSION
    consultation_id = data["consultation_id"]
    history = client.get("/api/v1/consulting/marriage/history").json()["data"]["items"]
    row = next(item for item in history if item["consultation_id"] == consultation_id)
    assert row["score"] == data["score"]
    assert row["grade"] == data["grade"]

