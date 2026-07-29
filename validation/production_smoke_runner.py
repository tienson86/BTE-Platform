"""
Production smoke runner — Architecture V1.0 stabilization.

Runs 100+ real-world BaZi validation cases through the production orchestrator
and API without modifying engines or contracts.

Output: validation/production_smoke_raw.json
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@dataclass(slots=True)
class SmokeCase:
    """One production validation case."""

    id: str
    category: str
    year: int
    month: int
    day: int
    hour: int = 0
    minute: int = 0
    gender: str | None = "male"
    timezone: str = "Asia/Ho_Chi_Minh"
    notes: str = ""
    expect_http: int = 200
    expect_pipeline: bool = True


REQUIRED_PIPELINE = [
    "calendar",
    "bazi",
    "pattern",
    "score",
    "interpretation",
    "report",
    "narrative",
]

PORTAL_REQUIRED = {
    "calendar": ["solar_date", "lunar"],
    "bazi": ["year_pillar", "month_pillar", "day_pillar", "hour_pillar", "day_master"],
    "pattern": ["pattern", "cach_cuc", "success"],
    "score": ["total_score", "success"],
    "interpretation": ["sections", "section_count"],
    "report": ["title", "markdown", "html", "section_count"],
    "narrative": ["title", "markdown", "html", "section_count"],
}


def _build_case_library() -> list[SmokeCase]:
    """Growing validation library — 100+ cases covering production edge categories."""
    cases: list[SmokeCase] = []

    def add(
        id_: str,
        category: str,
        y: int,
        m: int,
        d: int,
        h: int = 12,
        mi: int = 0,
        gender: str | None = "male",
        notes: str = "",
        expect_http: int = 200,
        expect_pipeline: bool = True,
    ) -> None:
        cases.append(
            SmokeCase(
                id=id_,
                category=category,
                year=y,
                month=m,
                day=d,
                hour=h,
                minute=mi,
                gender=gender,
                notes=notes,
                expect_http=expect_http,
                expect_pipeline=expect_pipeline,
            )
        )

    # --- Critical reference (production audit blocker) ---
    add("ref_1987_0121", "critical_reference", 1987, 1, 21, 3, 30, "male", "Critical 1987-01-21")
    add("ref_1987_0121_0430", "critical_reference", 1987, 1, 21, 4, 30, "male", "Same Zi-hour bucket 03-05")
    add("ref_production_readiness", "critical_reference", 1987, 1, 21, 3, 30, "male", "test_production_readiness SAMPLE")

    # --- Li Chun before / after ---
    for year in (1987, 2000, 2024, 1988, 1996):
        add(f"lichun_before_{year}", "before_li_chun", year, 2, 3, 12, 0, "male", f"Day before Li Chun {year}")
        add(f"lichun_after_{year}", "after_li_chun", year, 2, 4, 12, 0, "male", f"Li Chun day {year}")
        add(f"lichun_on_{year}", "on_li_chun", year, 2, 4, 0, 0, "male", f"Li Chun midnight {year}")

    # --- Leap year solar ---
    for year in (2000, 2004, 2020, 2024, 2028):
        add(f"leap_feb29_{year}", "leap_year", year, 2, 29, 12, 0, "female", f"Leap year Feb 29 {year}")

    # --- Leap month lunar (known calendar regression dates) ---
    add("leap_lunar_2020_04", "leap_month", 2020, 4, 23, 12, 0, "male", "2020 leap month case")
    add("leap_lunar_2023_03", "leap_month", 2023, 3, 22, 12, 0, "female", "Near leap boundary")

    # --- Solar-term / month boundary ---
    add("solar_term_1987_0121", "solar_term", 1987, 1, 21, 3, 30, "male", "Đại Hàn")
    add("solar_term_1987_0205", "solar_term", 1987, 2, 5, 12, 0, "male", "Post Li Chun month change")
    add("solar_term_2000_0204", "solar_term", 2000, 2, 4, 12, 0, "male", "2000 Li Chun")
    add("solar_term_2024_0210", "solar_term", 2024, 2, 10, 12, 0, "male", "2024 post Li Chun")

    # --- Zi hour / midnight / hour boundary ---
    for hour in (0, 1, 2, 23):
        add(f"zi_hour_{hour:02d}", "zi_hour", 1987, 1, 21, hour, 30, "male", f"Zi-hour band hour={hour}")
    add("midnight_0000", "midnight", 1990, 5, 15, 0, 0, "male", "Exact midnight")
    add("midnight_2359", "midnight", 1990, 5, 15, 23, 59, "male", "End of day")
    add("hour_boundary_0300", "hour_boundary", 1987, 1, 21, 3, 0, "male")
    add("hour_boundary_0500", "hour_boundary", 1987, 1, 21, 5, 0, "male")

    # --- Missing / optional gender ---
    add("gender_none", "missing_gender", 1990, 5, 15, 10, 30, None, "gender=null")
    add("gender_female", "gender_female", 1990, 5, 15, 10, 30, "female")

    # --- RC1 real_cases (20) ---
    rc1 = [
        ("rc1_01", 1990, 5, 15, 10, 30, "male"),
        ("rc1_02", 1988, 1, 8, 6, 0, "female"),
        ("rc1_03", 1975, 12, 31, 23, 45, "male"),
        ("rc1_04", 2000, 2, 29, 12, 0, "female"),
        ("rc1_05", 1960, 7, 4, 4, 20, "male"),
        ("rc1_06", 1995, 9, 9, 9, 9, "female"),
        ("rc1_07", 1982, 3, 21, 15, 15, "male"),
        ("rc1_08", 1999, 11, 11, 11, 11, "female"),
        ("rc1_09", 1970, 6, 1, 0, 0, "male"),
        ("rc1_10", 2010, 8, 20, 18, 30, "female"),
        ("rc1_11", 1985, 4, 12, 7, 45, "male"),
        ("rc1_12", 1992, 10, 3, 21, 10, "female"),
        ("rc1_13", 1968, 2, 14, 8, 0, "male"),
        ("rc1_14", 2005, 5, 5, 5, 5, "female"),
        ("rc1_15", 1978, 8, 18, 14, 0, "male"),
        ("rc1_16", 1993, 1, 1, 1, 1, "female"),
        ("rc1_17", 1980, 12, 25, 19, 30, "male"),
        ("rc1_18", 1997, 7, 7, 17, 0, "female"),
        ("rc1_19", 1965, 9, 30, 3, 15, "male"),
        ("rc1_20", 2001, 3, 8, 13, 45, "female"),
    ]
    for id_, y, m, d, h, mi, g in rc1:
        add(id_, "rc1_real_case", y, m, d, h, mi, g)

    # --- Bazi regression CASES from test_bazi_calendar_regression ---
    bazi_cases = [
        ("bazi_reg_19861230", 1986, 12, 30, 12, 0),
        ("bazi_reg_19870205", 1987, 2, 5, 12, 0),
        ("bazi_reg_19880217", 1988, 2, 17, 12, 0),
        ("bazi_reg_20000204", 2000, 2, 4, 12, 0),
        ("bazi_reg_20240210", 2024, 2, 10, 12, 0),
    ]
    for id_, y, m, d, h, mi in bazi_cases:
        add(id_, "bazi_regression", y, m, d, h, mi, "male")

    # --- Hour sweep (sample every 2 hours on reference date) ---
    for hour in range(0, 24, 2):
        add(f"hour_sweep_{hour:02d}", "hour_sweep", 1990, 5, 15, hour, 0, "male")

    # --- Decade grid (fill to 100+) ---
    grid_years = list(range(1960, 2025, 5))
    for i, y in enumerate(grid_years):
        add(f"grid_{y}", "decade_grid", y, ((i % 12) + 1), ((i % 28) + 1), (i % 24), (i * 3) % 60, "male")

    # --- Additional boundary fill (reach 100+ cases) ---
    extra_boundaries = [
        ("ext_19840204", 1984, 2, 4, 23, 59, "male", "Li Chun 1984 end of day"),
        ("ext_19840205", 1984, 2, 5, 0, 1, "male", "Li Chun 1984 start of day"),
        ("ext_20240204", 2024, 2, 4, 12, 0, "female", "Leap year Li Chun 2024"),
        ("ext_20240229", 2024, 2, 29, 23, 0, "female", "Leap day late night"),
        ("ext_19991231", 1999, 12, 31, 23, 59, "male", "Year boundary"),
        ("ext_20000101", 2000, 1, 1, 0, 0, "male", "Y2K midnight"),
        ("ext_19870121_0000", 1987, 1, 21, 0, 0, "male", "Critical date midnight"),
        ("ext_19870121_2300", 1987, 1, 21, 23, 0, "male", "Critical date late Zi"),
        ("ext_19900515_1200_f", 1990, 5, 15, 12, 0, "female", "Standard female"),
        ("ext_20160808_0808", 2016, 8, 8, 8, 8, "male", "Repeating digits"),
        ("ext_19760229", 1976, 2, 29, 6, 30, "female", "1976 leap Feb 29"),
        ("ext_2100_0301", 2100, 3, 1, 12, 0, "male", "Century non-leap year"),
    ]
    for id_, y, m, d, h, mi, g, notes in extra_boundaries:
        add(id_, "extra_boundary", y, m, d, h, mi, g, notes)

    # --- Invalid input (API error handling — expect 422) ---
    add("invalid_no_year", "invalid_input", 0, 0, 0, 0, 0, None, "Missing fields", 422, False)
    add("invalid_month_13", "invalid_input", 1990, 13, 1, 0, 0, "male", "month>12", 422, False)
    add("invalid_day_32", "invalid_input", 1990, 1, 32, 0, 0, "male", "day>31", 422, False)
    add("invalid_hour_25", "invalid_input", 1990, 1, 1, 25, 0, "male", "hour>23", 422, False)

    return cases


def _check_portal_fields(data: dict[str, Any]) -> list[str]:
    """Return list of missing portal-required field paths."""
    missing: list[str] = []
    for stage, fields in PORTAL_REQUIRED.items():
        block = data.get(stage)
        if not isinstance(block, dict):
            missing.append(f"{stage}:missing_block")
            continue
        for key in fields:
            if key not in block:
                missing.append(f"{stage}.{key}")
            elif block[key] is None:
                missing.append(f"{stage}.{key}:null")
    return missing


def _check_internal_leaks(data: dict[str, Any]) -> list[str]:
    """Detect internal fields that should not appear on wire."""
    leaks: list[str] = []
    interp = data.get("interpretation") or {}
    for key in ("summary", "matched_rule_count", "resolved_rule_count", "rules_used"):
        if key in interp:
            leaks.append(f"interpretation.{key}")
    score = data.get("score") or {}
    for key in ("details", "modules", "execution_time", "weighted_score"):
        if key in score:
            leaks.append(f"score.{key}")
    report = data.get("report") or {}
    if "templates_used" in report:
        leaks.append("report.templates_used")
    return leaks


def _check_reference_bazi(data: dict[str, Any], case: SmokeCase) -> list[str]:
    """Validate critical reference pillars for 1987-01-21."""
    if case.id not in ("ref_1987_0121", "ref_1987_0121_0430", "ref_production_readiness"):
        return []
    bazi = data.get("bazi") or {}
    errors: list[str] = []
    expected = {
        "year_pillar": ("Bính", "Dần"),
        "month_pillar": ("Tân", "Sửu"),
        "day_pillar": ("Canh", "Ngọ"),
        "hour_pillar": ("Mậu", "Dần"),
    }
    for pillar, (stem, branch) in expected.items():
        p = bazi.get(pillar) or {}
        if p.get("stem") != stem or p.get("branch") != branch:
            errors.append(
                f"bazi.{pillar} expected {stem}/{branch} got {p.get('stem')}/{p.get('branch')}"
            )
    if bazi.get("day_master") != "Canh":
        errors.append(f"bazi.day_master expected Canh got {bazi.get('day_master')}")
    return errors


def run_smoke() -> dict[str, Any]:
    """Execute full smoke suite and return report dict."""
    from fastapi.testclient import TestClient

    from applications.api.app import create_app

    client = TestClient(create_app())
    cases = _build_case_library()
    results: list[dict[str, Any]] = []
    pass_count = 0
    fail_count = 0

    for case in cases:
        body = {
            "year": case.year,
            "month": case.month,
            "day": case.day,
            "hour": case.hour,
            "minute": case.minute,
            "gender": case.gender,
            "timezone": case.timezone,
            "full_name": "Smoke Test",
            "birth_place": "Hà Nội",
        }
        if case.category == "invalid_input":
            if case.id == "invalid_no_year":
                body = {"month": 5, "day": 15}

        t0 = time.perf_counter()
        try:
            response = client.post("/api/v1/analyze", json=body)
            elapsed_ms = (time.perf_counter() - t0) * 1000
            status = response.status_code
            payload = response.json() if response.content else {}
            data = payload.get("data") or {}

            errors: list[str] = []
            if status != case.expect_http:
                errors.append(f"http:{status} expected {case.expect_http}")

            if case.expect_pipeline and status == 200:
                pipeline = data.get("pipeline") or []
                if pipeline != REQUIRED_PIPELINE:
                    errors.append(f"pipeline:{pipeline}")
                missing = _check_portal_fields(data)
                errors.extend(missing)
                leaks = _check_internal_leaks(data)
                errors.extend(leaks)
                ref_errors = _check_reference_bazi(data, case)
                errors.extend(ref_errors)
                if not (data.get("interpretation", {}).get("sections")):
                    errors.append("interpretation.sections:empty")
                if not (data.get("report", {}).get("markdown")):
                    errors.append("report.markdown:empty")

            passed = not errors
            if passed:
                pass_count += 1
            else:
                fail_count += 1

            results.append(
                {
                    "id": case.id,
                    "category": case.category,
                    "status": "PASS" if passed else "FAIL",
                    "http": status,
                    "elapsed_ms": round(elapsed_ms, 1),
                    "errors": errors,
                    "notes": case.notes,
                    "input": {
                        "year": case.year,
                        "month": case.month,
                        "day": case.day,
                        "hour": case.hour,
                        "minute": case.minute,
                        "gender": case.gender,
                    },
                }
            )
        except Exception as exc:
            fail_count += 1
            results.append(
                {
                    "id": case.id,
                    "category": case.category,
                    "status": "FAIL",
                    "errors": [f"exception:{exc}"],
                    "notes": case.notes,
                }
            )

    return {
        "total": len(cases),
        "passed": pass_count,
        "failed": fail_count,
        "required_pipeline": REQUIRED_PIPELINE,
        "results": results,
        "categories": sorted({c.category for c in cases}),
    }


def main() -> None:
    """Run smoke suite and write JSON report."""
    report = run_smoke()
    out = ROOT / "validation" / "production_smoke_raw.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Smoke complete: {report['passed']}/{report['total']} PASS, {report['failed']} FAIL")
    print(f"Written: {out}")


if __name__ == "__main__":
    main()
