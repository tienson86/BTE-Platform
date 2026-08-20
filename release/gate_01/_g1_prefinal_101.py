"""G1-PREFINAL: dump 101 Golden inputs through live production (read-only)."""

from __future__ import annotations

import json
from pathlib import Path

from applications.api.services.orchestrator import OrchestratorService

ROOT = Path(__file__).resolve().parents[2]
INPUT_DIR = ROOT / "tests" / "golden_dataset" / "inputs"
OUT = Path(__file__).with_name("G1_PREFINAL_101_TRUTH.json")


def _pillar(bazi: dict, key: str) -> str:
    item = bazi.get(key) or {}
    return f"{item.get('stem', '')} {item.get('branch', '')}".strip()


def _luck(payload: dict) -> str:
    cycle = (payload.get("luck") or {}).get("current_cycle") or {}
    stem = str(cycle.get("heavenly_stem") or cycle.get("stem") or "")
    branch = str(cycle.get("earthly_branch") or cycle.get("branch") or "")
    years = str(cycle.get("year_range") or "")
    label = f"{stem} {branch}".strip()
    if years:
        label = f"{label} ({years})"
    return label


def main() -> None:
    orch = OrchestratorService()
    rows = []
    files = sorted(INPUT_DIR.glob("case_*.json"))
    for path in files:
        raw = json.loads(path.read_text(encoding="utf-8"))
        birth = raw.get("birth") or raw
        solar = str(birth.get("solar_datetime") or raw.get("solar_datetime") or "")
        gender = str(birth.get("gender") or raw.get("gender") or "male")
        timezone = str(birth.get("timezone") or "Asia/Ho_Chi_Minh")
        from datetime import datetime

        dt = datetime.fromisoformat(solar.replace("Z", "+00:00"))
        payload = orch.analyze(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            gender=gender,
            timezone=timezone,
        )
        bazi = payload.get("bazi") or {}
        strength = payload.get("strength") or {}
        pattern = payload.get("pattern") or {}
        useful = payload.get("useful_god") or {}
        rows.append(
            {
                "case_id": path.stem,
                "solar": solar,
                "gender": gender,
                "four_pillars": " / ".join(
                    [
                        _pillar(bazi, "year_pillar"),
                        _pillar(bazi, "month_pillar"),
                        _pillar(bazi, "day_pillar"),
                        _pillar(bazi, "hour_pillar"),
                    ]
                ),
                "strength_level": strength.get("strength_level"),
                "strength_score": strength.get("strength_score"),
                "pattern": pattern.get("cach_cuc") or pattern.get("pattern"),
                "detected_special_pattern": pattern.get("detected_special_pattern"),
                "qualification_level": pattern.get("qualification_level"),
                "ug_override_eligible": pattern.get("ug_override_eligible"),
                "fallback_used": pattern.get("fallback_used"),
                "overall_dung": useful.get("useful_display"),
                "winning_rule_id": useful.get("winning_rule_id"),
                "reason_archetype": useful.get("reason_archetype"),
                "customer_hy": useful.get("favorable_display"),
                "hy_role_status": useful.get("hy_role_status"),
                "ky": useful.get("unfavorable_display"),
                "dieu_hau": useful.get("climate_display"),
                "current_luck": _luck(payload),
                "contract": (payload.get("useful_god_source") or {}).get("contract"),
            }
        )
        print(path.stem, rows[-1]["four_pillars"], rows[-1]["overall_dung"])
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", OUT, "n=", len(rows))


if __name__ == "__main__":
    main()
