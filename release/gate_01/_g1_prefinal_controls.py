"""G1-PREFINAL: recompute 10 control cases from live production (read-only)."""

from __future__ import annotations

import json
from pathlib import Path

from applications.api.services.orchestrator import OrchestratorService

CASES: list[dict[str, object]] = [
    {
        "name": "Nguyễn Tiến Sơn",
        "year": 1987, "month": 1, "day": 21, "hour": 4, "minute": 30,
        "gender": "male", "timezone": "Asia/Bangkok",
    },
    {
        "name": "Lương Ngọc Huỳnh",
        "year": 1966, "month": 9, "day": 24, "hour": 4, "minute": 15,
        "gender": "male", "timezone": "Asia/Bangkok",
    },
    {
        "name": "Đặng Thị Dung",
        "year": 1982, "month": 5, "day": 22, "hour": 9, "minute": 30,
        "gender": "female", "timezone": "Asia/Bangkok",
    },
    {
        "name": "Đoàn Quang Hưng",
        "year": 1981, "month": 8, "day": 29, "hour": 4, "minute": 30,
        "gender": "male", "timezone": "Asia/Ho_Chi_Minh",
    },
    {
        "name": "Vũ Thị Thanh Tuyền",
        "year": 1984, "month": 7, "day": 13, "hour": 21, "minute": 1,
        "gender": "female", "timezone": "Asia/Bangkok",
    },
    {
        "name": "Cao Xuân Trường",
        "year": 1989, "month": 7, "day": 21, "hour": 15, "minute": 45,
        "gender": "male", "timezone": "Asia/Bangkok",
    },
    {
        "name": "Lưu Hoàng Sơn",
        "year": 1996, "month": 11, "day": 29, "hour": 17, "minute": 20,
        "gender": "male", "timezone": "Asia/Bangkok",
    },
    {
        "name": "Phạm Thị Huyền",
        "year": 1987, "month": 9, "day": 7, "hour": 2, "minute": 0,
        "gender": "female", "timezone": "Asia/Bangkok",
    },
    {
        "name": "Lương Văn Mạnh",
        "year": 1987, "month": 6, "day": 29, "hour": 6, "minute": 0,
        "gender": "male", "timezone": "Asia/Bangkok",
    },
    {
        "name": "Ngô Đắc Dũng",
        "year": 1985, "month": 9, "day": 18, "hour": 8, "minute": 0,
        "gender": "male", "timezone": "Asia/Bangkok",
    },
]


def _pillar(payload: dict, key: str) -> str:
    item = (payload.get("bazi") or {}).get(key) or {}
    stem = str(item.get("stem") or "")
    branch = str(item.get("branch") or "")
    return f"{stem} {branch}".strip()


def _luck(payload: dict) -> str:
    luck = payload.get("luck") or {}
    cycle = luck.get("current_cycle") or {}
    stem = str(cycle.get("heavenly_stem") or cycle.get("stem") or "")
    branch = str(cycle.get("earthly_branch") or cycle.get("branch") or "")
    years = str(cycle.get("year_range") or cycle.get("years") or "")
    age = cycle.get("age_start")
    age_end = cycle.get("age_end")
    label = f"{stem} {branch}".strip()
    if years:
        label = f"{label} ({years})".strip()
    if age is not None:
        label = f"{label} ages {age}–{age_end}".strip()
    return label or str(cycle)[:180]


def row_from(name: str, payload: dict) -> dict[str, object]:
    bazi = payload.get("bazi") or {}
    strength = payload.get("strength") or {}
    pattern = payload.get("pattern") or {}
    useful = payload.get("useful_god") or {}
    pillars = " / ".join(
        [
            _pillar(payload, "year_pillar"),
            _pillar(payload, "month_pillar"),
            _pillar(payload, "day_pillar"),
            _pillar(payload, "hour_pillar"),
        ]
    )
    return {
        "case": name,
        "four_pillars": pillars,
        "day_master": bazi.get("day_master"),
        "strength_level": strength.get("strength_level"),
        "strength_score": strength.get("strength_score"),
        "pattern": pattern.get("cach_cuc") or pattern.get("pattern"),
        "detected_special_pattern": pattern.get("detected_special_pattern"),
        "qualification_level": pattern.get("qualification_level"),
        "ug_override_eligible": pattern.get("ug_override_eligible"),
        "fallback_used": pattern.get("fallback_used"),
        "dieu_hau": useful.get("climate_display"),
        "climate_preference_label": useful.get("climate_preference_label"),
        "overall_dung": useful.get("useful_display"),
        "winning_rule_id": useful.get("winning_rule_id"),
        "winning_rule_group": useful.get("winning_rule_group"),
        "reason_archetype": useful.get("reason_archetype"),
        "short_reason": useful.get("short_reason"),
        "customer_hy": useful.get("favorable_display"),
        "canonical_hy": useful.get("canonical_favorable_display"),
        "hy_role_status": useful.get("hy_role_status"),
        "ky": useful.get("unfavorable_display"),
        "contract": (payload.get("useful_god_source") or {}).get("contract"),
        "current_luck": _luck(payload),
        "analysis_id": payload.get("analysis_id"),
    }


def main() -> None:
    orch = OrchestratorService()
    rows = []
    for spec in CASES:
        kwargs = {k: v for k, v in spec.items() if k != "name"}
        payload = orch.analyze(**kwargs)
        rows.append(row_from(str(spec["name"]), payload))
    out = Path(__file__).with_name("G1_PREFINAL_CONTROL_CASES.json")
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
