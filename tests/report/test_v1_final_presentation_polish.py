"""V1.0 final presentation polish — customer Report V1 copy only."""

from __future__ import annotations

from engines.report_engine.contracts.report_input_v1 import (
    ReportInputV1,
    ReportMetadataV1,
    ReportPatternV1,
    ReportProfileV1,
    ReportShenShaItemV1,
    ReportStrengthV1,
    ReportTenGodsV1,
    ReportUsefulGodV1,
)
from engines.report_engine.rendering.customer_facing import (
    has_internal_rule_id,
    shensha_customer_line,
    strip_internal_rule_ids,
    temperature_customer_evidence,
    ten_gods_prominence,
)
from engines.report_engine.rendering.report_sections_v1 import build_presented_report


def _hidden(pillar: str, branch: str, stem: str, ten_god: str) -> dict[str, str]:
    return {
        "pillar": pillar,
        "branch": branch,
        "hidden_stem": stem,
        "stem": stem,
        "ten_god": ten_god,
    }


def test_strip_internal_rule_ids_leaves_canonical_facts() -> None:
    raw = "Nguyệt lệnh Tỵ · khí chính Bính · rule com_san_01"
    cleaned = strip_internal_rule_ids(raw)
    assert cleaned == "Nguyệt lệnh Tỵ · khí chính Bính"
    assert has_internal_rule_id(raw)
    assert not has_internal_rule_id(cleaned)


def test_temperature_customer_evidence_drops_climate_rule() -> None:
    evidence = temperature_customer_evidence(
        "Nguyệt lệnh Tỵ · mùa Hạ · khí hậu Nhiệt · Cần làm mát · rule cli_001"
    )
    assert "Sinh tháng Tỵ" in evidence
    assert "hạ" in evidence.lower()
    assert "nhiệt" in evidence.lower()
    assert "cli_" not in evidence
    assert "rule " not in evidence


def test_ten_gods_prominence_is_deterministic_and_skips_day_master() -> None:
    visible = [
        {"pillar": "year", "stem": "Nhâm", "ten_god": "Chính Ấn", "god_id": "zheng_yin"},
        {"pillar": "month", "stem": "Ất", "ten_god": "Tỷ Kiên", "god_id": "bi_jian"},
        {"pillar": "day", "stem": "Ất", "ten_god": "Nhật Chủ", "god_id": "day_master"},
        {"pillar": "hour", "stem": "Tân", "ten_god": "Thất Sát", "god_id": "qi_sha"},
    ]
    hidden = [
        _hidden("year", "Tuất", "Mậu", "Chính Tài"),
        _hidden("year", "Tuất", "Tân", "Thất Sát"),
        _hidden("year", "Tuất", "Đinh", "Thực Thần"),
        _hidden("month", "Tỵ", "Bính", "Thương Quan"),
        _hidden("month", "Tỵ", "Canh", "Chính Quan"),
        _hidden("month", "Tỵ", "Mậu", "Chính Tài"),
        _hidden("day", "Tỵ", "Bính", "Thương Quan"),
        _hidden("day", "Tỵ", "Canh", "Chính Quan"),
        _hidden("day", "Tỵ", "Mậu", "Chính Tài"),
        _hidden("hour", "Tỵ", "Bính", "Thương Quan"),
        _hidden("hour", "Tỵ", "Canh", "Chính Quan"),
        _hidden("hour", "Tỵ", "Mậu", "Chính Tài"),
    ]
    summary = ten_gods_prominence(visible, hidden, day_master_stem="Ất")
    by_name = {item["name"]: item for item in summary["all"]}
    assert by_name["Thất Sát"]["klass"] == "Lộ rõ"
    assert by_name["Tỷ Kiên"]["klass"] == "Lộ rõ"
    assert by_name["Tỷ Kiên"]["visible_count"] == 1
    assert by_name["Thương Quan"]["klass"] == "Ẩn nổi bật"
    assert by_name["Thương Quan"]["hidden_count"] == 3
    assert by_name["Chính Tài"]["klass"] == "Ẩn nổi bật"
    assert by_name["Chính Quan"]["klass"] == "Ẩn nổi bật"
    assert "Nhật Chủ" not in by_name
    names = [item["name"] for item in summary["all"]]
    assert names.index("Thương Quan") < names.index("Thực Thần")


def test_shensha_multiple_occurrences_are_highlighted() -> None:
    hong_loan = ReportShenShaItemV1(
        id="hong_luan",
        name="Hồng Loan",
        present=True,
        presence_label="Có · trụ Tháng · trụ Ngày · trụ Giờ",
        occurrences=[
            {"pillar": "month", "location": "branch", "target_value": "Tỵ"},
            {"pillar": "day", "location": "branch", "target_value": "Tỵ"},
            {"pillar": "hour", "location": "branch", "target_value": "Tỵ"},
        ],
    )
    thien_duc = ReportShenShaItemV1(
        id="tian_de",
        name="Thiên Đức Quý Nhân",
        present=True,
        presence_label="Có · trụ Giờ",
        occurrences=[{"pillar": "hour", "location": "stem", "target_value": "Tân"}],
    )
    name, presence, evidence = shensha_customer_line(hong_loan)
    assert name == "Hồng Loan"
    assert presence == "Nổi bật"
    assert evidence == "Có tại trụ Tháng · Ngày · Giờ"
    _, single_presence, single_evidence = shensha_customer_line(thien_duc)
    assert single_presence == "Có"
    assert single_evidence == "Có tại trụ Giờ"


def test_presented_report_has_no_customer_rule_ids() -> None:
    report_input = ReportInputV1(
        metadata=ReportMetadataV1(case_id="dung-presentation"),
        profile=ReportProfileV1(full_name="Đặng Thị Dung"),
        strength=ReportStrengthV1(day_master="Ất", score=0.24, level="weak"),
        pattern=ReportPatternV1(primary_pattern="Sát Ấn tương sinh"),
        useful_god=ReportUsefulGodV1(
            climate_evidence="Nguyệt lệnh Tỵ · mùa Hạ · khí hậu Nhiệt · Cần làm mát · rule cli_001",
            balancing_need="cooling",
            temperature_adjustment="hot",
            winning_rule_id="sea_002",
        ),
        ten_gods=ReportTenGodsV1(
            visible=["Chính Ấn", "Tỷ Kiên", "Nhật Chủ", "Thất Sát"],
            visible_entries=[
                {"pillar": "year", "stem": "Nhâm", "ten_god": "Chính Ấn"},
                {"pillar": "month", "stem": "Ất", "ten_god": "Tỷ Kiên"},
                {"pillar": "day", "stem": "Ất", "ten_god": "Nhật Chủ", "god_id": "day_master"},
                {"pillar": "hour", "stem": "Tân", "ten_god": "Thất Sát"},
            ],
            hidden_entries=[
                _hidden("month", "Tỵ", "Bính", "Thương Quan"),
                _hidden("day", "Tỵ", "Bính", "Thương Quan"),
                _hidden("hour", "Tỵ", "Bính", "Thương Quan"),
            ],
        ),
        shensha=[
            ReportShenShaItemV1(
                id="hong_luan",
                name="Hồng Loan",
                present=True,
                occurrences=[
                    {"pillar": "month"},
                    {"pillar": "day"},
                    {"pillar": "hour"},
                ],
            )
        ],
    )
    presented = build_presented_report(report_input)
    blob = " ".join(
        f"{label} {value}"
        for section in presented.sections
        for label, value in section.meta_rows
    )
    blob += " ".join(
        " ".join(row)
        for section in presented.sections
        if section.table
        for row in section.table.rows
    )
    assert "rule " not in blob
    assert "cli_" not in blob
    assert "com_san_" not in blob
    assert "Căn cứ khí hậu" not in blob
    useful = next(item for item in presented.sections if item.id == "useful-god")
    meta = dict(useful.meta_rows)
    assert "Điều hậu" in meta
    assert "cli_" not in meta["Điều hậu"]
    shensha = next(item for item in presented.sections if item.id == "shensha")
    assert shensha.table is not None
    assert shensha.table.headers == ["Tên", "Hiện diện", "Vị trí"]
    assert any("Hồng Loan" in row[0] and "Nổi bật" in row[1] for row in shensha.table.rows)
    ten_gods = next(item for item in presented.sections if item.id == "ten-gods")
    ten_meta = dict(ten_gods.meta_rows)
    assert any("Thất Sát" in label for label in ten_meta)
    assert any(label == "Lộ can" for label in ten_meta)
