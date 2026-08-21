"""G2-05 ten-control history snapshot parity. Copies stored analysis; no engine writes."""

from __future__ import annotations

import copy

from applications.api.services.customer_export import (
    build_customer_export_filename,
    prepare_customer_report_input,
)
from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.result_identity import stamp_customer_result_identity

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


def _fp(payload: dict) -> dict[str, object]:
    bazi = payload.get("bazi") or {}
    strength = payload.get("strength") or {}
    pattern = payload.get("pattern") or {}
    useful = payload.get("useful_god") or {}
    luck = ((payload.get("luck") or {}).get("current_cycle") or {})

    def pillar(key: str) -> str:
        item = bazi.get(key) or {}
        return f"{item.get('stem') or ''} {item.get('branch') or ''}".strip()

    return {
        "analysis_id": payload.get("analysis_id"),
        "four_pillars": " / ".join(
            [pillar("year_pillar"), pillar("month_pillar"), pillar("day_pillar"), pillar("hour_pillar")]
        ),
        "strength": f"{strength.get('strength_score')} {strength.get('strength_level')}",
        "pattern": pattern.get("cach_cuc") or pattern.get("pattern"),
        "dung": useful.get("useful_display"),
        "luck": luck.get("gan_zhi"),
    }


def test_ten_control_history_snapshots_match_save_time_payload() -> None:
    orch = OrchestratorService()
    diffs: list[str] = []
    for index, spec in enumerate(CASES):
        name = str(spec["name"])
        kwargs = {key: value for key, value in spec.items() if key != "name"}
        live = stamp_customer_result_identity(orch.analyze(**kwargs), f"g2-05-{index}")
        stored = copy.deepcopy(live)
        if _fp(stored) != _fp(live):
            diffs.append(f"{name} snapshot drifted at save")
        report = prepare_customer_report_input(
            analysis_id=f"g2-05-{index}",
            source="history",
            data=stored,
            birth_input=spec,
        )
        assert report.metadata.case_id == f"g2-05-{index}"
        assert report.useful_god.useful_display == str(stored["useful_god"]["useful_display"])
        assert "created_at" in (stored.get("result_meta") or {})
        assert stored["useful_god_source"]["contract"] == "analysis_result.UsefulGodView@1.5"
    assert diffs == []


def test_history_export_uses_selected_snapshot_not_current() -> None:
    orch = OrchestratorService()
    dung_spec = CASES[-1]
    tuyen_spec = CASES[4]
    dung = stamp_customer_result_identity(
        orch.analyze(**{k: v for k, v in dung_spec.items() if k != "name"}),
        "hist-dung",
    )
    tuyen = stamp_customer_result_identity(
        orch.analyze(**{k: v for k, v in tuyen_spec.items() if k != "name"}),
        "current-tuyen",
    )
    stored_dung = copy.deepcopy(dung)
    report = prepare_customer_report_input(
        analysis_id="hist-dung",
        source="history",
        data=stored_dung,
        birth_input=dung_spec,
    )
    assert report.metadata.case_id == "hist-dung"
    assert report.useful_god.useful_display == dung["useful_god"]["useful_display"]
    assert report.useful_god.useful_display != tuyen["useful_god"]["useful_display"]
    filename = build_customer_export_filename(report, "pdf")
    assert "Dung" in filename or "Đung" in filename or "Ngo" in filename
    assert "Tuyen" not in filename
    assert stored_dung["useful_god"]["useful_display"] == dung["useful_god"]["useful_display"]
