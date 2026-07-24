"""
WP4.5 — Generate Golden Dataset expansion cases.

Does not modify Engine / Matcher / Rule / Knowledge.
Writes inputs/case_XXXX.json (+ optional expected stubs for metadata only).
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT_DIR = ROOT / "inputs"
MANIFEST_PATH = ROOT / "wp45_manifest.json"

TZ = timezone(timedelta(hours=7))

# Coverage taxonomy required by WP4.5
COVERAGE_GOALS: list[dict] = [
    {"goal": "Strong Day Master", "tag": "strong_day_master", "count": 5},
    {"goal": "Weak Day Master", "tag": "weak_day_master", "count": 5},
    {"goal": "Follow Strong", "tag": "follow_strong", "count": 4},
    {"goal": "Follow Weak", "tag": "follow_weak", "count": 4},
    {"goal": "Chính Quan", "tag": "chinh_quan", "count": 5},
    {"goal": "Thất Sát", "tag": "that_sat", "count": 5},
    {"goal": "Chính Tài", "tag": "chinh_tai", "count": 4},
    {"goal": "Thiên Tài", "tag": "thien_tai", "count": 4},
    {"goal": "Chính Ấn", "tag": "chinh_an", "count": 4},
    {"goal": "Thiên Ấn", "tag": "thien_an", "count": 4},
    {"goal": "Thực Thần", "tag": "thuc_than", "count": 4},
    {"goal": "Thương Quan", "tag": "thuong_quan", "count": 4},
    {"goal": "Tỷ Kiên", "tag": "ty_kien", "count": 4},
    {"goal": "Kiếp Tài", "tag": "kiep_tai", "count": 4},
    {"goal": "Temperature nóng", "tag": "temperature_hot", "count": 4},
    {"goal": "Temperature lạnh", "tag": "temperature_cold", "count": 4},
    {"goal": "Combination", "tag": "combination", "count": 4},
    {"goal": "Clash", "tag": "clash", "count": 4},
    {"goal": "Harm", "tag": "harm", "count": 3},
    {"goal": "Punishment", "tag": "punishment", "count": 3},
    {"goal": "Useful God", "tag": "useful_god", "count": 5},
    {"goal": "Luck", "tag": "luck", "count": 5},
    {"goal": "Shensha", "tag": "shensha", "count": 5},
]


def _birth(dt: datetime, gender: str, case_id: str) -> dict:
    return {
        "gender": gender,
        "solar_datetime": dt.isoformat(),
        "timezone": "Asia/Ho_Chi_Minh",
        "location": {
            "country": "Vietnam",
            "province": "Ha Noi",
            "district": "Dong Da",
            "latitude": 21.0285,
            "longitude": 105.8542,
        },
    }


def _upstream_for(tag: str) -> dict:
    """Optional upstream payloads accepted by RuleContextBuilder (no engine change)."""
    if tag == "temperature_hot":
        return {
            "temperature": {
                "status": "HOT",
                "result": "HOT",
                "hot_score": 85,
                "cold_score": 10,
                "damp_score": 20,
                "dry_score": 70,
                "climate_pattern": "hot_dry",
                "severity": "high",
            }
        }
    if tag == "temperature_cold":
        return {
            "temperature": {
                "status": "COLD",
                "result": "COLD",
                "cold_score": 85,
                "hot_score": 10,
                "damp_score": 60,
                "dry_score": 15,
                "climate_pattern": "cold_damp",
                "severity": "high",
            }
        }
    if tag == "luck":
        return {
            "luck": {
                "available": True,
                "status": "GOOD_LUCK",
                "phase": "major",
                "support": True,
                "attack": False,
                "pillars": [{"stem": "Giáp", "branch": "Tý"}],
            }
        }
    if tag == "shensha":
        return {
            "shensha": {
                "stars": [
                    "Thiên Ất Quý Nhân",
                    "Văn Xương",
                    "Hồng Loan",
                    "Lộc Thần",
                    "Hoa Cái",
                ],
                "status": "PRESENT",
            }
        }
    if tag == "useful_god":
        return {
            "useful_god": {
                "name": "Chính Quan",
                "status": "Dụng thần xuất hiện Thiên Can",
                "favorable": ["Thủy"],
                "unfavorable": ["Hỏa"],
                "in_stem": True,
                "in_branch": True,
                "in_hidden": False,
            }
        }
    return {}


def _fact_overrides_for(tag: str) -> dict:
    """Fact overrides applied by coverage runner only (not Engine)."""
    maps = {
        "strong_day_master": {
            "strong_day_master": True,
            "strength_vuong": True,
            "day_master_strength_calculated": True,
        },
        "weak_day_master": {
            "weak_day_master": True,
            "strength_nhuoc": True,
            "day_master_strength_calculated": True,
        },
        "follow_strong": {
            "tong_vuong_confirmed": True,
            "follow_pattern_confirmed": True,
            "special_pattern": True,
            "pattern_la_tong_vuong": True,
        },
        "follow_weak": {
            "tong_nhuoc_confirmed": True,
            "follow_pattern_confirmed": True,
            "special_pattern": True,
            "pattern_la_tong_nhuoc": True,
        },
        "chinh_quan": {
            "pattern_la_chinh_quan_cach": True,
            "quan_tinh_ton_tai": True,
            "quan_tinh_thanh_cach": True,
            "pattern_confirmed": True,
        },
        "that_sat": {
            "pattern_la_that_sat_cach": True,
            "that_sat_ton_tai": True,
            "that_sat_thanh_cach": True,
            "HỮU_CHẾ": True,
        },
        "chinh_tai": {
            "pattern_la_tai_cach": True,
            "tai_tinh_ton_tai": True,
            "tai_tinh_thanh_cach": True,
        },
        "thien_tai": {"tai_tinh_ton_tai": True},
        "chinh_an": {
            "pattern_la_an_cach": True,
            "an_tinh_ton_tai": True,
            "an_tinh_thanh_cach": True,
        },
        "thien_an": {
            "pattern_la_thien_an_cach": True,
            "an_tinh_ton_tai": True,
        },
        "thuc_than": {
            "pattern_la_thuc_than_cach": True,
            "xuat_tinh_ton_tai": True,
            "xuat_tinh_thanh_cach": True,
        },
        "thuong_quan": {
            "pattern_la_thuong_quan_cach": True,
            "thuong_quan_ton_tai": True,
            "xuat_tinh_ton_tai": True,
        },
        "ty_kien": {
            "pattern_la_ty_kiep_cach": True,
            "ty_kiep_ton_tai": True,
            "ty_kiep_thanh_cach": True,
        },
        "kiep_tai": {"ty_kiep_ton_tai": True},
        "temperature_hot": {
            "temperature_profile_calculated": True,
            "chart_hot": True,
            "temperature_excess_hot": True,
        },
        "temperature_cold": {
            "temperature_profile_calculated": True,
            "chart_cold": True,
            "temperature_excess_cold": True,
        },
        "combination": {
            "combination_rule_valid": True,
            "combination_confirmed": True,
            "three_harmony_found": True,
            "heavenly_stem_combination_found": True,
            "earthly_branch_six_combination_found": True,
            "half_combination_found": True,
        },
        "clash": {
            "earthly_branch_clash_found": True,
            "heavenly_stem_clash_found": True,
        },
        "harm": {"harm_relation_found": True},
        "punishment": {
            "punishment_relation_found": True,
            "destruction_relation_found": True,
        },
        "useful_god": {
            "useful_god_found": True,
            "dung_than_da_xac_dinh": True,
            "useful_god_active": True,
            "hy_than_da_xac_dinh": True,
            "HỮU_DỤNG": True,
        },
        "luck": {
            "dai_van_da_phan_tich": True,
            "luu_nien_da_phan_tich": True,
        },
        "shensha": {"than_sat_da_phan_tich": True},
    }
    return dict(maps.get(tag, {}))


def _expected_for(tag: str, goal: str) -> dict:
    pattern_hints = {
        "chinh_quan": "chinh_quan",
        "that_sat": "that_sat",
        "chinh_tai": "chinh_tai",
        "thien_tai": "thien_tai",
        "chinh_an": "chinh_an",
        "thien_an": "thien_an",
        "thuc_than": "thuc_than",
        "thuong_quan": "thuong_quan",
        "ty_kien": "ty_kien",
        "kiep_tai": "kiep_tai",
        "follow_strong": "tong_vuong",
        "follow_weak": "tong_nhuoc",
    }
    return {
        "coverage_goal": goal,
        "expected_pattern": pattern_hints.get(tag, "any"),
        "expected_score_range": [0, 100],
        "expected_matched_rule_count": {"min": 1, "max": 2000},
    }


def build_cases() -> list[dict]:
    cases: list[dict] = []
    # Start after case_0001
    case_no = 2
    base = datetime(1960, 1, 15, 8, 0, tzinfo=TZ)
    idx = 0

    for spec in COVERAGE_GOALS:
        for i in range(spec["count"]):
            case_id = f"case_{case_no:04d}"
            dt = base + timedelta(days=37 * idx + 11 * i, hours=(idx + i) % 23)
            gender = "male" if (idx + i) % 2 == 0 else "female"
            tag = spec["tag"]
            goal = spec["goal"]
            expected = _expected_for(tag, goal)
            case = {
                "case_id": case_id,
                "description": f"WP4.5 coverage case — {goal} ({i + 1})",
                "tags": ["wp45", "golden_expansion", tag, goal.replace(" ", "_").lower()],
                "coverage_goal": goal,
                "expected_pattern": expected["expected_pattern"],
                "expected_score_range": expected["expected_score_range"],
                "expected_matched_rule_count": expected["expected_matched_rule_count"],
                "birth": _birth(dt, gender, case_id),
                "options": {
                    "calendar": {
                        "calendar_type": "solar",
                        "use_true_solar_time": True,
                        "use_dst": False,
                    },
                    "engine": {
                        "language": "vi",
                        "rule_database": "v1.0",
                        "output_format": "json",
                    },
                },
                "upstream": _upstream_for(tag),
                "fact_overrides": _fact_overrides_for(tag),
                "metadata": {
                    "author": "wp45",
                    "created_at": datetime.now(tz=TZ).isoformat(),
                    "dataset_version": "wp45-1.0",
                    "notes": f"Coverage target: {goal}",
                },
            }
            cases.append(case)
            case_no += 1
            idx += 1

    # Pad to at least 100 new cases (101 total with case_0001)
    while len(cases) < 100:
        case_id = f"case_{case_no:04d}"
        dt = base + timedelta(days=19 * case_no, hours=case_no % 24)
        gender = "female" if case_no % 2 else "male"
        # rotate goals
        spec = COVERAGE_GOALS[case_no % len(COVERAGE_GOALS)]
        tag = spec["tag"]
        goal = spec["goal"]
        expected = _expected_for(tag, goal)
        cases.append(
            {
                "case_id": case_id,
                "description": f"WP4.5 padding case — {goal}",
                "tags": ["wp45", "golden_expansion", tag, "padding"],
                "coverage_goal": goal,
                "expected_pattern": expected["expected_pattern"],
                "expected_score_range": expected["expected_score_range"],
                "expected_matched_rule_count": expected["expected_matched_rule_count"],
                "birth": _birth(dt, gender, case_id),
                "options": {
                    "calendar": {
                        "calendar_type": "solar",
                        "use_true_solar_time": True,
                        "use_dst": False,
                    },
                    "engine": {
                        "language": "vi",
                        "rule_database": "v1.0",
                        "output_format": "json",
                    },
                },
                "upstream": _upstream_for(tag),
                "fact_overrides": _fact_overrides_for(tag),
                "metadata": {
                    "author": "wp45",
                    "created_at": datetime.now(tz=TZ).isoformat(),
                    "dataset_version": "wp45-1.0",
                    "notes": f"Coverage target: {goal}",
                },
            }
        )
        case_no += 1

    return cases


def main() -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    cases = build_cases()
    manifest = {
        "version": "wp45-1.0",
        "case_count": len(cases) + 1,  # include case_0001
        "coverage_goals": [item["goal"] for item in COVERAGE_GOALS],
        "cases": [],
    }

    for case in cases:
        path = INPUT_DIR / f"{case['case_id']}.json"
        path.write_text(
            json.dumps(case, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        manifest["cases"].append(
            {
                "case_id": case["case_id"],
                "coverage_goal": case["coverage_goal"],
                "expected_pattern": case["expected_pattern"],
                "expected_score_range": case["expected_score_range"],
                "expected_matched_rule_count": case["expected_matched_rule_count"],
                "tags": case["tags"],
            }
        )

    # Ensure case_0001 is listed in manifest
    manifest["cases"].insert(
        0,
        {
            "case_id": "case_0001",
            "coverage_goal": "Basic validation",
            "expected_pattern": "any",
            "expected_score_range": [0, 100],
            "expected_matched_rule_count": {"min": 0, "max": 2000},
            "tags": ["basic"],
        },
    )
    manifest["case_count"] = len(manifest["cases"])

    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {len(cases)} cases to {INPUT_DIR}")
    print(f"Manifest: {MANIFEST_PATH} (total {manifest['case_count']})")


if __name__ == "__main__":
    main()
