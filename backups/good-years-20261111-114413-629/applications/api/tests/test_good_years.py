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
    assert expand_legacy_row({"id": "legacy", "result": legacy}) == {"id": "legacy", "result": selected}
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
        assert ("Năm thuận" if year["favorable"] else "Năm chưa đạt tiêu chí thuận") in section.title
        assert len([block for block in section.blocks if block.block_id.startswith("month-") and block.title.startswith("Tháng ")]) == len(year["months"])


def test_rejects_context_only_support_pressure_xung_and_uncertain_cycles():
    period = {
        "bazi": {"evidence": [{"type": "support", "text": "Dụng thần"},
                              {"type": "reference"}, {"type": "support", "text": "Đại vận"}],
                 "missing_context": []},
        "cung_phi": {"favorable": True, "note": "Cung Phi thuận", "relationship": "Thiên Y"},
    }
    assert assess(period)["favorable"]
    for entry in ({"type": "pressure"}, {"type": "interaction", "relation": "xung"}):
        period["bazi"]["evidence"].append(entry)
        assert not assess(period)["favorable"]
        period["bazi"]["evidence"].pop()
    period["bazi"]["missing_context"].append("Thiếu đại vận")
    assert not assess(period)["favorable"]
    period["bazi"]["missing_context"].clear()
    period["bazi"]["evidence"][0] = {"type": "reference"}
    assert not assess(period)["favorable"]
