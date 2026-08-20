"""G2-01 audit probe: Frozen Truth vs live orchestrator. Read-only. No engine writes."""

from __future__ import annotations

import json
from pathlib import Path

from applications.api.services.orchestrator import OrchestratorService
from applications.api.services.useful_god_truth import useful_god_source_fingerprint

ROOT = Path(__file__).resolve().parent
FROZEN = ROOT.parent / "gate_01" / "G1_PREFINAL_CONTROL_CASES.json"

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

COMPARE_KEYS = (
    "four_pillars",
    "strength_score",
    "strength_level",
    "pattern",
    "detected_special_pattern",
    "ug_override_eligible",
    "dieu_hau",
    "overall_dung",
    "reason_archetype",
    "customer_hy",
    "ky",
    "current_luck",
    "contract",
)


def _pillar(payload: dict, key: str) -> str:
    item = (payload.get("bazi") or {}).get(key) or {}
    return f"{item.get('stem') or ''} {item.get('branch') or ''}".strip()


def _luck(payload: dict) -> str:
    cycle = (payload.get("luck") or {}).get("current_cycle") or {}
    stem = str(cycle.get("heavenly_stem") or cycle.get("stem") or "")
    branch = str(cycle.get("earthly_branch") or cycle.get("branch") or "")
    label = f"{stem} {branch}".strip()
    gan = str(cycle.get("gan_zhi") or "")
    if gan and not label:
        label = gan
    age = cycle.get("age_start")
    age_end = cycle.get("age_end")
    if age is not None:
        label = f"{label} ages {age}–{age_end}".strip()
    return label


def fingerprint(name: str, payload: dict) -> dict[str, object]:
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
    customer_hy = str(useful.get("favorable_display") or "")
    internal_hy = str(useful.get("canonical_favorable_display") or "")
    gods = useful.get("favorable_gods") or []
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
        "dieu_hau": useful.get("climate_display"),
        "climate_preference_label": useful.get("climate_preference_label"),
        "overall_dung": useful.get("useful_display"),
        "reason_archetype": useful.get("reason_archetype"),
        "short_reason": useful.get("short_reason"),
        "customer_hy": customer_hy,
        "canonical_hy": internal_hy,
        "hy_role_status": useful.get("hy_role_status"),
        "ky": useful.get("unfavorable_display"),
        "contract": (payload.get("useful_god_source") or {}).get("contract"),
        "current_luck": _luck(payload),
        "analysis_id_in_payload": payload.get("analysis_id"),
        "customer_hy_equals_internal": customer_hy == internal_hy and bool(customer_hy),
        "customer_hy_equals_dung": customer_hy == str(useful.get("useful_display") or ""),
        "internal_gods_include_dung": str(useful.get("useful_god") or "") in [str(x) for x in gods],
        "pattern_hy_than": pattern.get("hy_than"),
        "pattern_dung_than": pattern.get("dung_than"),
        "has_short_reason": bool(str(useful.get("short_reason") or "").strip()),
        "has_str_rule_in_short_reason": "str_" in str(useful.get("short_reason") or ""),
    }


def presentation_copy(fp: dict[str, object]) -> dict[str, object]:
    """Simulate Canonical Desktop / Full Report copy rules (no engine)."""
    dung = str(fp.get("overall_dung") or "")
    hy = str(fp.get("customer_hy") or "") or str(fp.get("pattern_hy_than") or "") or "—"
    return {
        "result_dung": dung,
        "result_hy": hy,
        "report_dung": dung,
        "report_hy": str(fp.get("customer_hy") or ""),
        "result_hy_uses_pattern_fallback": not bool(fp.get("customer_hy")) and bool(fp.get("pattern_hy_than")),
    }


def main() -> None:
    frozen_rows = json.loads(FROZEN.read_text(encoding="utf-8"))
    frozen_by = {row["case"]: row for row in frozen_rows}
    orch = OrchestratorService()
    contract = useful_god_source_fingerprint()
    mismatches: list[dict[str, object]] = []
    rows: list[dict[str, object]] = []
    for spec in CASES:
        name = str(spec["name"])
        kwargs = {k: v for k, v in spec.items() if k != "name"}
        payload = orch.analyze(**kwargs)
        live = fingerprint(name, payload)
        frozen = frozen_by[name]
        diffs = {}
        for key in COMPARE_KEYS:
            a = frozen.get(key)
            b = live.get(key)
            if a != b:
                diffs[key] = {"frozen": a, "live": b}
        copy = presentation_copy(live)
        rows.append(
            {
                "case": name,
                "frozen_vs_api": "MATCH" if not diffs else "DIFF",
                "diffs": diffs,
                "live": live,
                "presentation": copy,
            }
        )
        if diffs:
            mismatches.append({"case": name, "diffs": diffs})

    dung = next(r for r in rows if r["case"] == "Ngô Đắc Dũng")
    tuyen = next(r for r in rows if r["case"] == "Vũ Thị Thanh Tuyền")
    out = {
        "contract_fingerprint": contract,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "rows": rows,
        "dung_probe": dung,
        "tuyen_probe": tuyen,
    }
    dest = ROOT / "G2_01_BINDING_PROBE.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"mismatch_count": len(mismatches), "contract": contract, "mismatches": mismatches}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
