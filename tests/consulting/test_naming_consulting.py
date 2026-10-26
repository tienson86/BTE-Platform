from dataclasses import replace
from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError

from consulting.marriage.models.enums import CanonicalGender, FiveElement, YinYang
from consulting.marriage.models.person import BirthDataQuality, CanonicalVersionReference, MarriagePersonReference
from consulting.marriage.models.snapshot import (
    DayMasterSnapshot, ElementOrStemReference, FengShuiSnapshot, FiveElementSnapshot,
    MarriageCanonicalSnapshot, PillarSnapshot, PillarValue, StrengthSnapshot,
    TenGodSnapshot, UsefulGodSnapshot,
)
from consulting.naming.api import build_naming_router
from consulting.naming.models import NamingRequest
from consulting.naming.service import load_catalog, recommend_names


def request(**overrides):
    return NamingRequest(**{
        "family_name": "Nguyễn", "gender": "male", "birth_date": "2020-05-10",
        "birth_time": "08:30", **overrides,
    })


def snapshot():
    pillar = PillarValue(stem="Canh", branch="Tý", can_chi="Canh Tý", na_yin="Bích Thượng Thổ")
    return MarriageCanonicalSnapshot(
        person=MarriagePersonReference(
            analysis_id="TEST", gender=CanonicalGender.MALE,
            birth_data_quality=BirthDataQuality(True, True, True, True, 1.0),
            canonical_version=CanonicalVersionReference(),
        ),
        pillars=PillarSnapshot(year=pillar, month=pillar, day=pillar, hour=pillar),
        day_master=DayMasterSnapshot(stem="Quý", element=FiveElement.WATER, yin_yang=YinYang.YIN),
        five_elements=FiveElementSnapshot(distribution={}),
        strength=StrengthSnapshot(classification="Thân nhược"), pattern=None,
        useful_god=UsefulGodSnapshot(
            useful=[ElementOrStemReference(element=FiveElement.FIRE)],
            favorable=[ElementOrStemReference(element=FiveElement.WOOD)],
            unfavorable=[ElementOrStemReference(element=FiveElement.EARTH)],
        ),
        ten_gods=TenGodSnapshot(), source_analysis_id="TEST",
        feng_shui=FengShuiSnapshot(cung_phi="Khôn", element=FiveElement.EARTH),
    )


@pytest.mark.parametrize("gender", ["male", "female"])
@pytest.mark.parametrize("count", [5, 8, 10])
def test_names_have_requested_count_gender_and_no_duplicates(gender, count):
    result = recommend_names(request(gender=gender, count=count), snapshot())
    names = result["recommendations"]
    eligible = {entry["id"] for entry in load_catalog()["names"] if gender in entry["genders"]}
    assert len(names) == len({entry["full_name"] for entry in names}) == count
    assert all(entry["id"] in eligible and entry["full_name"].startswith("Nguyễn ") for entry in names)
    assert all(entry["meaning"] and entry["element_basis"] and len(entry["reasons"]) == 3 for entry in names)


def test_useful_god_outranks_secondary_references_and_unfavorable_loses():
    result = recommend_names(request(count=10), snapshot())
    names = result["recommendations"]
    assert all(entry["element"] == "Hỏa" for entry in names[:3])
    assert all(entry["element"] == "Mộc" for entry in names[3:6])
    assert not any(entry["element"] == "Thổ" for entry in names)


def test_unfavorable_wins_over_conflicting_useful_signal():
    signals = snapshot()
    signals.useful_god.unfavorable = [ElementOrStemReference(element=FiveElement.FIRE)]
    names = recommend_names(request(count=10), signals)["recommendations"]
    assert all(entry["element"] != "Hỏa" for entry in names)


def test_unknown_time_never_uses_assumed_hour_useful_gods():
    signals = snapshot()
    first = recommend_names(request(birth_time=None), signals)
    signals.useful_god = UsefulGodSnapshot(useful=[ElementOrStemReference(element=FiveElement.METAL)])
    second = recommend_names(request(birth_time=None), signals)
    assert first["recommendations"] == second["recommendations"]
    assert first["signals"]["useful_elements"] == first["signals"]["favorable_elements"] == []
    assert first["signals"]["unfavorable_elements"] == []
    assert first["signals"]["pillars"]["hour"] is None
    assert first["quality"] == "preliminary"
    assert any("giờ giả định" in warning for warning in first["warnings"])


def test_missing_canonical_signals_are_not_invented():
    signals = snapshot()
    signals.pillars.year = replace(signals.pillars.year, na_yin=None)
    signals.feng_shui = None
    signals.useful_god = UsefulGodSnapshot()
    result = recommend_names(request(), signals)
    assert result["signals"]["nap_am_element"] is None
    assert result["signals"]["cung_phi_element"] is None
    assert result["quality"] == "preliminary"
    assert all(entry["rank_points"] == 0 for entry in result["recommendations"])
    assert len(result["warnings"]) == 3


def test_rename_excludes_current_name_with_unicode_and_case_normalization():
    current = "  NGUYỄN   MINH NHẬT "
    result = recommend_names(request(mode="rename", current_name=current, count=10), snapshot())
    assert "Minh Nhật" not in {entry["given_name"] for entry in result["recommendations"]}
    assert len(result["recommendations"]) == 10


@pytest.mark.parametrize("overrides", [
    {"family_name": "   "}, {"family_name": "<script>"}, {"gender": "other"},
    {"birth_date": "2020-02-30"}, {"birth_date": "01/01/2020"},
    {"birth_date": "1899-12-31"}, {"birth_date": "2099-01-01"},
    {"birth_time": "24:00"}, {"birth_time": "12:60"}, {"birth_time": "8:30"},
    {"timezone": "Invalid/Zone"}, {"mode": "rename", "current_name": ""},
    {"count": 4}, {"count": 11}, {"count": True},
])
def test_invalid_inputs_are_rejected(overrides):
    with pytest.raises(ValidationError):
        request(**overrides)


def test_catalog_covers_every_element_for_each_gender():
    catalog = load_catalog()
    assert len(catalog["names"]) == 25
    for gender in ("male", "female"):
        assert {entry["element"].lower() for entry in catalog["names"] if gender in entry["genders"]} == {entry.value for entry in FiveElement}


def test_api_validates_and_returns_results_without_writing_profiles(monkeypatch):
    app = FastAPI()
    app.include_router(build_naming_router(), prefix="/api/v1")
    analyze = Mock(return_value=recommend_names(request(), snapshot()))
    monkeypatch.setattr("consulting.naming.api.analyze_naming", analyze)
    client = TestClient(app)
    response = client.post("/api/v1/consulting/naming/analyze", json=request().model_dump())
    assert response.status_code == 200
    assert len(response.json()["data"]["recommendations"]) == 8
    assert client.post("/api/v1/consulting/naming/analyze", json={}).status_code == 422
    assert analyze.call_count == 1
    analyze.side_effect = RuntimeError("sensitive diagnostic")
    failed = client.post("/api/v1/consulting/naming/analyze", json=request().model_dump())
    assert failed.status_code == 503
    assert "sensitive diagnostic" not in failed.text


def test_naming_endpoint_is_mounted_and_keeps_existing_authentication(monkeypatch, tmp_path):
    monkeypatch.setenv("BTE_MARRIAGE_DATA_PATH", str(tmp_path / "marriage.json"))
    monkeypatch.setenv("BTE_CHILDBIRTH_DATA_DIR", str(tmp_path / "childbirth"))
    from consulting.marriage.api.http import create_marriage_api_app

    app = create_marriage_api_app()
    assert "/api/v1/consulting/naming/analyze" in app.openapi()["paths"]
    response = TestClient(app).post("/api/v1/consulting/naming/analyze", json=request().model_dump())
    assert response.status_code == 401
