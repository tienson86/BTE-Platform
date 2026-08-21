"""G2-04 ten-case presentation parity. Copies stored analysis; no engine writes."""

from __future__ import annotations

from applications.api.services.customer_export import prepare_customer_report_input
from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.result_identity import stamp_customer_result_identity
from engines.report_engine.rendering.report_sections_v1 import build_presented_report

CASES: list[dict[str, object]] = [
    {"name": "Nguyễn Tiến Sơn", "year": 1987, "month": 1, "day": 21, "hour": 4, "minute": 30, "gender": "male", "timezone": "Asia/Bangkok"},
    {"name": "Lương Ngọc Huỳnh", "year": 1966, "month": 9, "day": 24, "hour": 4, "minute": 15, "gender": "male", "timezone": "Asia/Bangkok"},
    {"name": "Đặng Thị Dung", "year": 1982, "month": 5, "day": 22, "hour": 9, "minute": 30, "gender": "female", "timezone": "Asia/Bangkok"},
    {"name": "Đoàn Quang Hưng", "year": 1981, "month": 8, "day": 29, "hour": 4, "minute": 30, "gender": "male", "timezone": "Asia/Ho_Chi_Minh"},
    {"name": "Vũ Thị Thanh Tuyền", "year": 1984, "month": 7, "day": 13, "hour": 21, "minute": 1, "gender": "female", "timezone": "Asia/Bangkok"},
    {"name": "Cao Xuân Trường", "year": 1989, "month": 7, "day": 21, "hour": 15, "minute": 45, "gender": "male", "timezone": "Asia/Bangkok"},
    {"name": "Lưu Hoàng Sơn", "year": 1996, "month": 11, "day": 29, "hour": 17, "minute": 20, "gender": "male", "timezone": "Asia/Bangkok"},
    {"name": "Phạm Thị Huyền", "year": 1987, "month": 9, "day": 7, "hour": 2, "minute": 0, "gender": "female", "timezone": "Asia/Bangkok"},
    {"name": "Lương Văn Mạnh", "year": 1987, "month": 6, "day": 29, "hour": 6, "minute": 0, "gender": "male", "timezone": "Asia/Bangkok"},
    {"name": "Ngô Đắc Dũng", "year": 1985, "month": 9, "day": 18, "hour": 8, "minute": 0, "gender": "male", "timezone": "Asia/Bangkok"},
]


def _meta(report_input) -> dict[str, str]:
    useful = {label: value for label, value in _section(report_input, "useful-god")}
    strength = {label: value for label, value in _section(report_input, "strength")}
    pattern = {label: value for label, value in _section(report_input, "pattern")}
    return {
        "dung": useful.get("Dụng thần", ""),
        "reason": useful.get("Căn cứ chọn Dụng", ""),
        "hy": useful.get("Hỷ thần", ""),
        "ky": useful.get("Kỵ thần", ""),
        "dieu_hau": useful.get("Điều hậu ưu tiên", "") or useful.get("Ứng dụng Điều hậu", ""),
        "strength_score": strength.get("Điểm thân", ""),
        "pattern": pattern.get("Cách chính", ""),
    }


def _section(report_input, section_id: str) -> list[tuple[str, str]]:
    presented = build_presented_report(report_input)
    for section in presented.sections:
        if section.id == section_id:
            return list(section.meta_rows)
    return []


def test_ten_control_cases_presentation_matches_stored_payload() -> None:
    orch = OrchestratorService()
    diffs: list[str] = []
    for index, spec in enumerate(CASES):
        name = str(spec["name"])
        kwargs = {key: value for key, value in spec.items() if key != "name"}
        payload = stamp_customer_result_identity(orch.analyze(**kwargs), f"g2-04-{index}")
        report_input = prepare_customer_report_input(
            analysis_id=f"g2-04-{index}",
            source="current",
            data=payload,
            birth_input=spec,
        )
        presented = _meta(report_input)
        useful = payload["useful_god"]
        pattern = payload.get("pattern") or {}
        if presented["dung"] != str(useful.get("useful_display") or ""):
            diffs.append(f"{name} dung {presented['dung']!r}")
        if presented["hy"] != str(useful.get("favorable_display") or ""):
            diffs.append(f"{name} hy {presented['hy']!r}")
        if presented["ky"] != str(useful.get("unfavorable_display") or ""):
            diffs.append(f"{name} ky")
        live_reason = str(useful.get("short_reason") or "")
        if live_reason and presented["reason"] != live_reason:
            diffs.append(f"{name} reason")
        live_pattern = str(pattern.get("cach_cuc") or pattern.get("pattern") or "")
        if presented["pattern"] != live_pattern:
            diffs.append(f"{name} pattern {presented['pattern']!r}")
        assert report_input.metadata.case_id == f"g2-04-{index}"
        useful_rows = {label: value for label, value in _section(report_input, "useful-god")}
        assert "Dụng thần" in useful_rows
        assert "Điều hậu ưu tiên" in useful_rows or "Ứng dụng Điều hậu" in useful_rows
        assert useful_rows.get("Dụng thần") != useful_rows.get("Điều hậu ưu tiên")
        pillars = f"{report_input.pillars.year.stem} {report_input.pillars.year.branch}"
        assert pillars.strip()
        assert report_input.luck_cycles.cycles, f"{name} missing luck cycles"
    assert diffs == []
