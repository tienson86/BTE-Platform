import unicodedata
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from consulting.naming.current_name import analyze_current_name, load_han_viet, load_name_words
from consulting.naming.models import CurrentNameRequest
from engines.calendar_engine.cung_phi import element_label_for_cung, personal_cung_phi_from_year_ganzhi
from engines.calendar_engine.tam_nguyen_dataset import jiazi_row_for_year
from engines.calendar_engine.lunar.converter import solar_to_lunar


def request(**overrides):
    return CurrentNameRequest(**{
        "full_name": "Nguyễn Tiến Sơn", "gender": "male", "lunar_birth_year": 1986,
        **overrides,
    })


def test_current_name_reads_words_without_inventing_a_full_chart():
    result = analyze_current_name(request())
    assert result["name_reading"]["given_part"] == "Tiến Sơn"
    assert result["name_reading"]["element"] == "Thổ"
    assert [part["word"] for part in result["name_reading"]["parts"]] == ["Tiến", "Sơn"]
    assert "vững chãi" in result["name_reading"]["meaning"]
    assert result["year_reference"]["can_chi"] == "Bính Dần"
    assert result["year_reference"]["nap_am"] == "Lư Trung Hỏa"
    assert result["comparisons"][0]["relation"] == "reference_generates_name"
    assert "chiều sinh ngược" not in result["comparisons"][0]["explanation"]
    assert result["basis"] == "lunar_birth_year_only"
    assert not {"pillars", "useful_god", "useful_elements", "rank_points", "score"} & result.keys()
    assert any("ngày và giờ sinh" in note for note in result["notes"])


@pytest.mark.parametrize("year", [1900, 1944, 1986, 2000, 2026])
@pytest.mark.parametrize("gender", ["male", "female"])
def test_year_signals_follow_existing_calendar_sources(year, gender):
    result = analyze_current_name(request(lunar_birth_year=year, gender=gender))
    source = jiazi_row_for_year(year)
    cung = personal_cung_phi_from_year_ganzhi(
        year_ganzhi=source.ganzhi, tam_nguyen=source.tam_nguyen,
        reference_year=year, gender=gender,
    )
    assert result["year_reference"]["can_chi"] == source.ganzhi
    assert result["year_reference"]["nap_am"] == source.nap_am
    assert result["year_reference"]["cung_phi"] == cung.cung_phi
    assert result["year_reference"]["cung_phi_element"] == element_label_for_cung(cung.cung_phi)


def test_known_name_reuses_curated_phrase_for_current_name_of_any_gender():
    result = analyze_current_name(request(full_name="Nguyễn Văn Ánh Dương"))
    assert result["name_reading"]["element"] == "Hỏa"
    assert result["name_reading"]["match_source"] == "catalog_name"
    assert result["name_reading"]["meaning"] == "Ánh mặt trời, gợi sự ấm áp và tươi sáng."


def test_nfc_and_casefold_are_used_without_removing_vietnamese_marks():
    value = unicodedata.normalize("NFD", "  NGUYỄN   TIẾN SƠN  ")
    result = analyze_current_name(request(full_name=value))
    assert result["full_name"] == "NGUYỄN TIẾN SƠN"
    assert result["name_reading"]["element"] == "Thổ"
    thuy = analyze_current_name(request(full_name="Nguyễn Thủy"))
    thuy_other_mark = analyze_current_name(request(full_name="Nguyễn Thúy"))
    assert thuy["name_reading"]["element"] == "Thủy"
    assert thuy_other_mark["name_reading"]["element"] is None


def test_unknown_names_are_not_forced_into_an_element():
    result = analyze_current_name(request(full_name="Nguyễn Minh Xyza"))
    assert result["name_reading"]["element"] is None
    assert result["name_reading"]["parts"][0]["element"] == "Hỏa"
    assert result["name_reading"]["parts"][1]["known"] is False
    assert all(item["relation"] == "unresolved" for item in result["comparisons"])
    assert any("Xyza" in note for note in result["notes"])


def test_family_names_do_not_determine_the_given_name_element():
    result = analyze_current_name(request(full_name="Kim Linh"))
    assert result["name_reading"]["element"] is None
    compound = analyze_current_name(request(full_name="Âu Dương An"))
    assert compound["name_reading"]["family_part"] == "Âu Dương"
    assert [part["word"] for part in compound["name_reading"]["parts"]] == ["An"]
    assert compound["name_reading"]["element"] is None


def test_single_word_name_does_not_crash():
    result = analyze_current_name(request(full_name="Sơn"))
    assert result["name_reading"]["family_part"] is None
    assert result["name_reading"]["element"] == "Thổ"


@pytest.mark.parametrize("overrides", [
    {"full_name": " "}, {"full_name": "---"}, {"full_name": "<script>"},
    {"full_name": "A" * 121}, {"gender": ""}, {"gender": "unknown"},
    {"lunar_birth_year": 1899}, {"lunar_birth_year": 2101}, {"lunar_birth_year": 2099},
    {"lunar_birth_year": True}, {"lunar_birth_year": "1986"}, {"lunar_birth_year": 1986.5},
    {"birth_date": "1986-01-01"},
])
def test_invalid_public_inputs_are_rejected(overrides):
    with pytest.raises(ValidationError):
        request(**overrides)


def test_meaning_words_have_unique_normalized_keys():
    words = load_name_words()
    assert len(words) >= 40
    assert all(entry["meaning"] for entry in words.values())


@pytest.mark.parametrize("day, expected_year", [(1, 1986), (28, 1986), (29, 1987), (31, 1987)])
def test_january_1987_uses_the_actual_tet_boundary(day, expected_year):
    lunar = solar_to_lunar(day, 1, 1987)
    assert lunar.year == expected_year
    result = analyze_current_name(request(lunar_birth_year=lunar.year))
    assert result["lunar_birth_year"] == expected_year
    assert result["year_reference"]["calendar"] == "vietnamese_lunar_year"
    assert result["year_reference"]["can_chi"] == ("Bính Dần" if expected_year == 1986 else "Đinh Mão")
    assert "birth_year" not in result


def test_legacy_gregorian_field_is_rejected_instead_of_silently_reinterpreted():
    with pytest.raises(ValidationError, match="năm sinh âm lịch"):
        CurrentNameRequest(full_name="Nguyễn Tiến Sơn", gender="male", birth_year=1987)


def test_future_year_validation_observes_lunar_new_year(monkeypatch):
    class BeforeTet(datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(1987, 1, 28, tzinfo=tz)

    monkeypatch.setattr("consulting.naming.models.datetime", BeforeTet)
    assert request(lunar_birth_year=1986).lunar_birth_year == 1986
    with pytest.raises(ValidationError, match="âm lịch.*tương lai"):
        request(lunar_birth_year=1987)


def test_tien_son_has_grounded_han_viet_and_composed_reading():
    reading = analyze_current_name(request())["name_reading"]
    assert reading["parts"][0]["han_characters"] == [{"character": "進", "meaning": "tiến lên, đi về phía trước"}]
    assert reading["parts"][1]["han_characters"] == [{"character": "山", "meaning": "núi"}]
    assert all(len(part["interpretation"]) > 100 for part in reading["parts"])
    combined = reading["han_viet"]
    assert combined["source"] == "curated_phrase"
    assert combined["phrase"] == "Tiến Sơn"
    assert len(combined["paragraphs"]) == 2
    assert "tiến bộ bền bỉ" in combined["paragraphs"][0]
    assert "nhiều chữ Hán" in combined["note"]


def test_homophones_have_alternatives_without_forcing_an_element():
    reading = analyze_current_name(request(full_name="Nguyễn Thanh Dương"))["name_reading"]
    assert [item["character"] for item in reading["parts"][0]["han_characters"]] == ["清", "青"]
    assert [item["character"] for item in reading["parts"][1]["han_characters"]] == ["陽", "洋"]
    assert reading["element"] is None
    thuy = analyze_current_name(request(full_name="Nguyễn Thúy"))["name_reading"]
    assert thuy["parts"][0]["han_characters"][0]["character"] == "翠"
    assert thuy["element"] is None


def test_unknown_and_vietnamese_only_words_are_not_given_fabricated_characters():
    reading = analyze_current_name(request(full_name="Nguyễn Minh Xyza"))["name_reading"]
    assert reading["parts"][-1]["han_characters"] == []
    assert reading["parts"][-1]["interpretation"] is None
    assert reading["han_viet"]["source"] == "partial"
    assert reading["han_viet"]["phrase"] is None
    anh = analyze_current_name(request(full_name="Nguyễn Ánh Dương"))["name_reading"]
    assert anh["parts"][0]["han_characters"] == []
    assert anh["han_viet"]["source"] == "curated_phrase"


def test_han_viet_data_covers_existing_words_and_known_phrase_suffixes():
    data = load_han_viet()
    assert set(data["words"]) == set(load_name_words())
    result = analyze_current_name(request(full_name="NGUYỄN VĂN TIẾN SƠN"))
    assert result["name_reading"]["han_viet"]["phrase"] == "Tiến Sơn"
    assert result["name_reading"]["element"] == "Thổ"


def test_public_api_works_without_auth_but_private_routes_stay_protected(monkeypatch, tmp_path):
    monkeypatch.setenv("BTE_MARRIAGE_DATA_PATH", str(tmp_path / "marriage.json"))
    monkeypatch.setenv("BTE_CHILDBIRTH_DATA_DIR", str(tmp_path / "childbirth"))
    from consulting.marriage.api.http import create_marriage_api_app

    client = TestClient(create_marriage_api_app())
    response = client.post("/api/v1/public/naming/analyze-current", json=request().model_dump())
    assert response.status_code == 200
    assert response.json()["data"]["full_name"] == "Nguyễn Tiến Sơn"
    assert client.post("/api/v1/public/naming/analyze-current", json={}).status_code == 422
    old_payload = {"full_name": "Nguyễn Tiến Sơn", "gender": "male", "birth_year": 1987}
    old_response = client.post("/api/v1/public/naming/analyze-current", json=old_payload)
    assert old_response.status_code == 422
    assert "năm sinh âm lịch" in old_response.text
    for path in ("naming/analyze", "marriage", "childbirth/analyze"):
        assert client.post("/api/v1/consulting/" + path, json={}).status_code == 401
    assert client.get("/api/v1/public/naming/history").status_code == 404
    assert not list(tmp_path.rglob("*.json"))


def test_public_errors_do_not_expose_internal_diagnostics(monkeypatch, tmp_path):
    monkeypatch.setenv("BTE_MARRIAGE_DATA_PATH", str(tmp_path / "marriage.json"))
    monkeypatch.setenv("BTE_CHILDBIRTH_DATA_DIR", str(tmp_path / "childbirth"))
    from consulting.marriage.api.http import create_marriage_api_app

    def unavailable(body):
        raise RuntimeError("private-diagnostic-path")

    monkeypatch.setattr("consulting.naming.api.analyze_current_name", unavailable)
    response = TestClient(create_marriage_api_app()).post(
        "/api/v1/public/naming/analyze-current", json=request().model_dump(),
    )
    assert response.status_code == 503
    assert response.json()["status"] == "FAILED"
    assert "private-diagnostic-path" not in response.text
