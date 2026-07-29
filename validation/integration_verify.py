"""Integration Verification Script — BTE Result Page.

Runs 20 representative charts and verifies data completeness
across all pipeline layers: Engine -> Orchestrator -> Presenter fields.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from applications.api.services.orchestrator import OrchestratorService

DATASET = [
    # (label, year, month, day, hour, minute, gender, note)
    ("Than_Vuong_Nam_Ha",      1990,  6, 15, 10,  0, "male",   "Than vuong mua Ha"),
    ("Than_Nhuoc_Nu_Dong",     1995, 12, 22,  2,  0, "female", "Than nhuoc mua Dong"),
    ("Chinh_Quan_Nam",         1987,  1, 21,  4, 30, "male",   "Chinh Quan Cach"),
    ("That_Sat_Nu",            1983,  7,  7, 14,  0, "female", "That Sat Cach"),
    ("Chinh_Tai_Nam",          1975,  9, 10,  8,  0, "male",   "Chinh Tai Cach"),
    ("Thien_Tai_Nu",           1982,  3,  3,  6,  0, "female", "Thien Tai Cach"),
    ("Thuc_Than_Nam",          1991,  5,  5, 12,  0, "male",   "Thuc Than Cach"),
    ("Thuong_Quan_Nu",         1988,  8,  8, 20,  0, "female", "Thuong Quan Cach"),
    ("Tong_Cach_Nam",          1964,  4,  4,  0,  0, "male",   "Tong Cach"),
    ("Hoa_Cach_Nu",            1972, 10, 10, 16,  0, "female", "Hoa Cach"),
    ("Co_Dung_Than_Nam",       2000,  2, 14,  9,  0, "male",   "Co Dung than"),
    ("Khong_Dung_Than_Nu",     1999, 11, 11,  3,  0, "female", "Khong ro Dung than"),
    ("Co_Dieu_Hau_Nam",        1985,  1,  5,  6,  0, "male",   "Co Dieu hau"),
    ("Khong_Dieu_Hau_Nu",      1993,  7, 20, 14,  0, "female", "Khong Dieu hau"),
    ("Nhieu_Than_Sat_Nam",     1970,  8, 15,  0,  0, "male",   "Nhieu Than sat"),
    ("It_Than_Sat_Nu",         2005,  6,  1, 12,  0, "female", "It Than sat"),
    ("Nam_Menh_Xuan",          1986,  4, 10,  8,  0, "male",   "Nam menh mua Xuan"),
    ("Nu_Menh_Thu",            1994, 10,  5, 18,  0, "female", "Nu menh mua Thu"),
    ("La_So_Mua_Ha_2",         2001,  7, 10, 13,  0, "male",   "Mua Ha 2"),
    ("La_So_Mua_Dong_2",       1968, 12, 15,  5,  0, "female", "Mua Dong 2"),
]

# Pattern fields expected to be non-empty
PATTERN_FIELDS = ["than", "than_vuong_nhuoc", "cach_cuc", "dung_than", "hy_than", "ky_than", "dieu_hau"]
# Score fields expected to be present (0 is valid)
SCORE_FIELDS = ["total_score", "strength_score", "pattern_score", "grade", "confidence"]
# Calendar fields
CALENDAR_FIELDS = ["solar_date", "lunar_date"]
# Bazi fields
BAZI_FIELDS = ["day_master", "day_master_element", "day_master_yin_yang"]

# Internal rule code pattern — should NOT appear in interpretation bodies
INTERNAL_LINE_RE = re.compile(
    r"\b(?:FPR|SPR|PAT|PSC|PPR|SER|SDR|CBR|PC)\d+\b|status\s*=",
    re.IGNORECASE,
)
# "ln", "Kiep Tai Cach", "Tai Hon Tap", etc. — raw rule slugs from engine (min 2 chars)
RAW_UNACCENTED_RE = re.compile(r"^[A-Za-z][A-Za-z0-9 _\-/()]{1,}$")


def check_no_internal(text: str) -> list[str]:
    """Return lines that look like internal rule codes."""
    bad = []
    for line in str(text or "").split("\n"):
        s = line.strip()
        if not s:
            continue
        if INTERNAL_LINE_RE.search(s):
            bad.append(s[:80])
        elif RAW_UNACCENTED_RE.match(s):
            bad.append(s[:80])
    return bad


def verify_case(label: str, note: str, data: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []

    # ── Calendar ───────────────────────────────────────────────
    cal = data.get("calendar") or {}
    for f in CALENDAR_FIELDS:
        if not cal.get(f):
            issues.append(f"calendar.{f} missing")
    if not cal.get("solar_term"):
        warnings.append("calendar.solar_term missing (acceptable for some dates)")

    # ── Bazi ───────────────────────────────────────────────────
    bazi = data.get("bazi") or {}
    for f in BAZI_FIELDS:
        if not bazi.get(f):
            issues.append(f"bazi.{f} missing")
    if not bazi.get("ten_gods"):
        warnings.append("bazi.ten_gods empty")
    if not bazi.get("year_pillar"):
        issues.append("bazi.year_pillar missing")

    # ── Pattern ─────────────────────────────────────────────────
    pat = data.get("pattern") or {}
    for f in PATTERN_FIELDS:
        if not pat.get(f):
            issues.append(f"pattern.{f} missing")
    if pat.get("score") is None:
        warnings.append("pattern.score missing")
    if pat.get("priority") is None:
        warnings.append("pattern.priority missing")

    # ── Score ───────────────────────────────────────────────────
    sc = data.get("score") or {}
    for f in SCORE_FIELDS:
        if sc.get(f) is None:
            issues.append(f"score.{f} missing")
    wux = sc.get("wuxing_series") or []
    if not wux:
        warnings.append("score.wuxing_series empty")

    # ── Interpretation ──────────────────────────────────────────
    interp = data.get("interpretation") or {}
    sections = interp.get("sections") or []
    if len(sections) == 0:
        issues.append("interpretation.sections empty")
    else:
        section_ids = {s.get("id") for s in sections}
        for expected_id in ("summary", "career", "health"):
            if expected_id not in section_ids:
                warnings.append(f"interpretation section '{expected_id}' missing")
        # Check no internal rule codes in bodies
        for sec in sections:
            body = sec.get("body") or ""
            bad_lines = check_no_internal(body)
            if bad_lines:
                issues.append(
                    f"interpretation.{sec.get('id')} has internal lines: {bad_lines[:2]}"
                )
    if interp.get("confidence") is None:
        warnings.append("interpretation.confidence missing")

    # ── Report / Narrative ──────────────────────────────────────
    narrative = data.get("narrative") or data.get("report") or {}
    md = narrative.get("markdown") or ""
    if not md.strip():
        issues.append("narrative.markdown empty")
    else:
        bad = check_no_internal(md)
        if bad:
            issues.append(f"narrative has {len(bad)} raw rule lines: {bad[:2]}")

    return {
        "label": label,
        "note": note,
        "ok": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "pattern_cach": pat.get("cach_cuc"),
        "pattern_than": pat.get("than"),
        "pattern_than_vn": pat.get("than_vuong_nhuoc"),
        "score_total": sc.get("total_score"),
        "score_grade": sc.get("grade"),
        "score_confidence": sc.get("confidence"),
        "interp_sections": len(sections),
        "interp_confidence": interp.get("confidence"),
    }


def main() -> None:
    svc = OrchestratorService()
    case_results = []
    run_errors = []

    for label, y, mo, d, h, mi, g, note in DATASET:
        try:
            data = svc.analyze(year=y, month=mo, day=d, hour=h, minute=mi, gender=g)
            result = verify_case(label, note, data)
            case_results.append(result)
        except Exception as ex:
            run_errors.append({"label": label, "error": str(ex)})
            case_results.append(
                {
                    "label": label,
                    "note": note,
                    "ok": False,
                    "issues": [f"RUN_ERROR: {ex}"],
                    "warnings": [],
                }
            )

    # Save raw JSON for later reference
    out_dir = Path(__file__).parent
    raw_path = out_dir / "integration_verify_raw.json"
    raw_path.write_text(
        json.dumps(case_results, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Print summary table
    total = len(case_results)
    passed = sum(1 for r in case_results if r.get("ok"))
    failed = total - passed

    print(f"\n{'='*70}")
    print(f"BTE Integration Verification — {total} cases | PASS={passed} FAIL={failed}")
    print(f"{'='*70}")
    header = f"{'Label':<26} {'Cach':<18} {'Score':<8} {'Gr':<5} {'Sec':<5} {'Status'}"
    print(header)
    print("-" * 70)
    for r in case_results:
        status = "PASS" if r.get("ok") else "FAIL"
        print(
            f"{r['label']:<26} {str(r.get('pattern_cach','?'))[:17]:<18} "
            f"{str(r.get('score_total','?')):<8} {str(r.get('score_grade','?')):<5} "
            f"{str(r.get('interp_sections','?')):<5} {status}"
        )
        if not r.get("ok"):
            for iss in r.get("issues", []):
                print(f"  !! {iss}")
    print(f"{'='*70}")
    if run_errors:
        print("\nRun Errors:")
        for e in run_errors:
            print(f"  {e['label']}: {e['error']}")

    print(f"\nRaw JSON saved to: {raw_path}")
    return case_results


if __name__ == "__main__":
    main()
