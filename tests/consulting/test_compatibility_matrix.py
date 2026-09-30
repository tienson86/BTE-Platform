"""Acceptance tests for the customer-safe marriage comparison matrix."""

from __future__ import annotations

from consulting.marriage.decision.score import project_marriage_score
from consulting.marriage.dto.request import CanonicalBirthInput
from tests.consulting.api_fixtures import api_client, valid_body
from tests.consulting.decision_fixtures import build_test_decision, golden_pair, make_snapshot
from consulting.marriage.models.enums import CanonicalGender, FiveElement, PersonSide
from consulting.marriage.runtime.snapshot_builder import build_marriage_snapshot
from tests.consulting.runtime_fixtures import canonical_payload


def test_matrix_explains_four_pillar_cung_phi_and_element_support() -> None:
    snapshot_a, snapshot_b = golden_pair()
    values = {
        "year": ("Khôn", "Khôn", "Phục Vị"),
        "month": ("Càn", "Đoài", "Sinh Khí"),
        "day": ("Khảm", "Chấn", "Thiên Y"),
        "hour": ("Khôn", "Khôn", "Phục Vị"),
    }
    for slot, (cung_a, cung_b, _relation) in values.items():
        getattr(snapshot_a.pillars, slot).cung_phi = cung_a
        getattr(snapshot_b.pillars, slot).cung_phi = cung_b

    result = build_test_decision(snapshot_a, snapshot_b)
    project_marriage_score(result)

    assert result.compatibility_matrix is not None
    sections = {item.key: item for item in result.compatibility_matrix.sections}
    assert set(sections) == {"useful_god", "cung_phi", "structure", "married_life"}
    cung_rows = {item.key: item for item in sections["cung_phi"].rows}
    for slot, (cung_a, cung_b, relation) in values.items():
        assert cung_rows[slot].value_a == cung_a
        assert cung_rows[slot].value_b == cung_b
        assert relation in cung_rows[slot].relationship
        assert cung_rows[slot].status == "supportive"
    assert len(sections["useful_god"].rows) == 2
    assert all(row.basis for row in sections["useful_god"].rows)
    assert any(row.key == "day_master" for row in sections["structure"].rows)
    assert any(row.key == "pattern" and row.status == "reference" for row in sections["structure"].rows)
    assert any(row.key == "shen_sha" and row.status == "reference" for row in sections["structure"].rows)
    life_rows = {item.key: item for item in sections["married_life"].rows}
    assert set(life_rows) == {"interaction", "family", "finance", "children", "luck"}
    assert life_rows["children"].status == "unavailable"
    assert "không tạo điểm phạt" in life_rows["children"].relationship


def test_unknown_hour_is_marked_unavailable_and_not_invented() -> None:
    snapshot_a = make_snapshot(
        analysis_id="MC-NO-HOUR-A",
        side=PersonSide.A,
        gender=CanonicalGender.FEMALE,
        day_stem="Ất",
        day_branch="Mão",
        day_element=FiveElement.WOOD,
        useful=FiveElement.FIRE,
        hour_known=False,
    )
    snapshot_b = make_snapshot(
        analysis_id="MC-NO-HOUR-B",
        side=PersonSide.B,
        gender=CanonicalGender.MALE,
        day_stem="Bính",
        day_branch="Ngọ",
        day_element=FiveElement.FIRE,
        useful=FiveElement.WOOD,
        hour_known=False,
    )
    result = build_test_decision(snapshot_a, snapshot_b)
    project_marriage_score(result)

    assert result.compatibility_matrix is not None
    cung = next(item for item in result.compatibility_matrix.sections if item.key == "cung_phi")
    hour = next(item for item in cung.rows if item.key == "hour")
    assert hour.available is False
    assert hour.status == "unavailable"
    assert hour.score_effect is None


def test_public_api_returns_matrix_without_internal_evidence_ids() -> None:
    client, _container = api_client()
    body = valid_body(gender_a="female", gender_b="male")
    body["options"] = {"include_score": True}

    response = client.post("/api/v1/consulting/marriage", json=body)

    assert response.status_code == 201
    matrix = response.json()["data"]["compatibility_matrix"]
    assert matrix["version"].startswith("marriage.compatibility_matrix.v1")
    assert [item["key"] for item in matrix["sections"]] == [
        "useful_god",
        "cung_phi",
        "structure",
        "married_life",
    ]
    assert "evidence_id" not in str(matrix)
    assert all(row["basis"] for section in matrix["sections"] for row in section["rows"])


def test_snapshot_builder_copies_cung_phi_for_all_four_pillars() -> None:
    payload = canonical_payload()
    payload["calendar"] = {
        "ganzhi_routing": {
            "year": {"cung_phi": "Khôn"},
            "month": {"cung_phi": "Càn"},
            "day": {"cung_phi": "Khảm"},
            "hour": {"cung_phi": "Đoài"},
        }
    }
    person = CanonicalBirthInput(
        gender=CanonicalGender.FEMALE,
        birth_date="1987-09-25",
        birth_time="04:30",
        timezone="Asia/Ho_Chi_Minh",
    )

    snapshot = build_marriage_snapshot(
        analysis={"canonical": payload, "hour_known": True},
        person=person,
        analysis_id="MC-ROUTING",
        side=PersonSide.A,
    )

    assert snapshot.pillars.year.cung_phi == "Khôn"
    assert snapshot.pillars.month.cung_phi == "Càn"
    assert snapshot.pillars.day.cung_phi == "Khảm"
    assert snapshot.pillars.hour is not None
    assert snapshot.pillars.hour.cung_phi == "Đoài"
