from types import SimpleNamespace

from applications.api.services.good_years import assess, expand_legacy_row, select_good_periods
from applications.api.services.van_han_core import build
from applications.api.services.van_han_export import document
from applications.api.services.van_han_service import get_result, list_results, save_result


def test_selects_months_independently_and_uses_same_export_content(tmp_path, monkeypatch):
    monkeypatch.setenv("BTE_ANALYSIS_ARCHIVE_PATH", str(tmp_path / "archive.sqlite3"))
    profile = {
        "name": "Khách thử nghiệm",
        "gender": "male",
        "lunar_birth_year": 1990,
        "pillars": {"year": "Canh Ngọ", "month": "Mậu Dần", "day": "Giáp Tý", "hour": "Giáp Tý"},
        "useful": {"element": "Thổ", "stem": "Mậu", "favorable": ["Kim"], "unfavorable": []},
        "cycles": [{"year_start": 2023, "year_end": 2050, "gan_zhi": "Mậu Thìn"}],
    }
    result = build(profile, 2024, 2044)
    result.update(profile=profile, source_analysis_id="chart-1")
    selected = select_good_periods(result)
    assert any(year["favorable"] for year in selected["years"])
    assert any(not year["favorable"] and any(month["favorable"] for month in year["months"]) for year in selected["years"])
    assert any(month["leap"] for year in selected["years"] for month in year["months"])
    assert any(not month["favorable"] for year in selected["years"] for month in year["months"])
    for raw, enhanced in zip(result["years"], selected["years"], strict=True):
        assert enhanced["narrative"] == raw["narrative"]
        assert len(enhanced["months"]) == len(raw["months"])
    legacy = {**selected, "version": "GOOD-YEARS-01", "years": [
        {**year, "months": [month for month in year["months"] if month["favorable"]]}
        for year in selected["years"]
    ]}
    for old_result in (legacy, {**selected, "version": "GOOD-YEARS-02"}, {**selected, "version": "GOOD-YEARS-03"}):
        assert expand_legacy_row({"id": "legacy", "result": old_result}) == {"id": "legacy", "result": selected}
    assert all("favorable" not in year for year in result["years"])

    user = SimpleNamespace(user_id="one", username="one", display_name="Thành viên")
    row = save_result(user, selected, good_years=True)
    assert list_results("user:one") == []
    assert list_results("user:two", good_years=True) == []
    assert get_result("user:two", row["id"], good_years=True) is None
    assert get_result("user:one", row["id"], good_years=True) == row

    report = document(row)
    assert report.heading == "TÍNH CÁC NĂM TỐT"
    for year, section in zip(selected["years"], report.sections, strict=True):
        assert year["assessment_label"] in section.title
        assert len([block for block in section.blocks if block.block_id.startswith("month-") and block.title.startswith("Tháng ")]) == len(year["months"])


def test_distinguishes_direct_evidence_and_context():
    period = {
        "ganzhi": "Ất Mão",
        "bazi": {"evidence": [{"type": "support", "text": "Dụng thần"},
                              {"type": "reference"}, {"type": "support", "text": "Đại vận"}],
                 "missing_context": [], "day_master": "Canh", "exact_useful_stem": False, "ten_god": "Chính Tài"},
        "cung_phi": {"favorable": True, "note": "Cung Phi thuận", "relationship": "Thiên Y"},
    }
    assert assess(period)["favorable"]
    for entry in ({"type": "pressure", "text": "Kỵ thần đại vận"}, {"type": "interaction", "relation": "xung", "text": "Lục xung"}):
        period["bazi"]["evidence"].append(entry)
        assert assess(period)["bazi_assessment_label"] == "Thuận có lưu ý"
        period["bazi"]["evidence"].pop()
    period["bazi"]["missing_context"].append("Thiếu đại vận")
    assert not assess(period)["bazi_favorable"]
    assert assess(period)["favorable"]
    period["bazi"]["missing_context"].clear()
    period["bazi"]["evidence"][0] = {"type": "reference"}
    assert not assess(period)["bazi_favorable"]
    assert assess(period)["favorable"]


def test_giap_ngo_can_be_favorable_despite_giap_thin_cycle_and_du_nien():
    profile = {
        "gender": "male", "lunar_birth_year": 1986,
        "pillars": {"year": "Bính Dần", "month": "Tân Sửu", "day": "Canh Ngọ", "hour": "Mậu Dần"},
        "useful": {"element": "Hỏa", "stem": "Đinh", "favorable": ["Hỏa", "Mộc"], "unfavorable": ["Kim", "Thổ"]},
        "cycles": [{"year_start": 2012, "year_end": 2021, "gan_zhi": "Giáp Thìn"}],
    }
    forecast = select_good_periods(build(profile, 2026, 2035))["years"]
    assert [y["cung_phi"]["relationship_id"] for y in forecast[:6]] == [
        "tuyet_menh", "luc_sat", "sinh_khi", "thien_y", "dien_nien", "phuc_vi",
    ]
    assert sum(y["cung_phi"]["favorable"] for y in forecast) == 5
    for year in forecast:
        for month in year["months"]:
            assert month["cung_phi"]["favorable"] == (month["cung_phi"]["period"] in {"Cấn", "Đoài", "Càn", "Khôn"})
            if month["cung_phi"]["favorable"]:
                assert month["favorable"]
    raw = build(profile, 2014, 2020)
    years = select_good_periods(raw)["years"]
    year = years[0]
    assert year["ganzhi"] == "Giáp Ngọ"
    assert year["bazi_assessment_label"] == "Thuận có lưu ý"
    assert "Chi đại vận Giáp Thìn" in year["assessment"]
    assert any(month["favorable"] for item in years for month in item["months"])
    assert any(month["bazi_assessment_label"] == "Thuận nghịch đan xen" for item in years for month in item["months"])
