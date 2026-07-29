"""Pattern Engine Audit Script — 50 representative charts."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from engines.pattern_engine.engine import PatternEngine, DEFAULT_DATABASE_PATH
from engines.pattern_engine.context import PatternContext
from engines.pattern_engine.utils.context_builder import build_pattern_context
from engines.calendar_engine.engine import CalendarEngine
from engines.bazi_engine.engine import BaziEngine
from applications.api.services.orchestrator import OrchestratorService

DATASET_100 = [
    # Additional 50 cases for 100-chart regression
    ("51_M_1953",      1953, 4, 10, 8, 0, "male"),
    ("52_F_1956",      1956, 8, 20, 14, 0, "female"),
    ("53_M_1959",      1959, 11, 5, 6, 0, "male"),
    ("54_F_1963",      1963, 3, 18, 20, 0, "female"),
    ("55_M_1966",      1966, 7, 7, 10, 0, "male"),
    ("56_F_1969",      1969, 9, 14, 0, 0, "female"),
    ("57_M_1976",      1976, 1, 30, 16, 0, "male"),
    ("58_F_1979",      1979, 6, 11, 8, 0, "female"),
    ("59_M_1982",      1982, 10, 25, 22, 0, "male"),
    ("60_F_1986",      1986, 2, 7, 4, 0, "female"),
    ("61_M_1988",      1988, 11, 19, 12, 0, "male"),
    ("62_F_1991",      1991, 4, 3, 18, 0, "female"),
    ("63_M_1994",      1994, 8, 29, 6, 0, "male"),
    ("64_F_1995",      1995, 1, 16, 14, 0, "female"),
    ("65_M_1999",      1999, 5, 22, 10, 0, "male"),
    ("66_F_2000",      2000, 9, 9, 20, 0, "female"),
    ("67_M_2006",      2006, 3, 14, 8, 0, "male"),
    ("68_F_2009",      2009, 7, 20, 0, 0, "female"),
    ("69_M_2010",      2010, 12, 12, 12, 0, "male"),
    ("70_F_2015",      2015, 6, 21, 6, 0, "female"),
    ("71_M_1942",      1942, 2, 2, 2, 0, "male"),
    ("72_F_1948",      1948, 10, 10, 10, 0, "female"),
    ("73_M_1954",      1954, 5, 5, 5, 0, "male"),
    ("74_F_1957",      1957, 9, 9, 9, 0, "female"),
    ("75_M_1961",      1961, 3, 3, 3, 0, "male"),
    ("76_F_1964",      1964, 7, 7, 7, 0, "female"),
    ("77_M_1968",      1968, 11, 11, 11, 0, "male"),
    ("78_F_1970",      1970, 2, 28, 18, 0, "female"),
    ("79_M_1973",      1973, 6, 15, 14, 0, "male"),
    ("80_F_1975",      1975, 10, 20, 10, 0, "female"),
    ("81_M_1976",      1976, 4, 4, 4, 0, "male"),
    ("82_F_1979",      1979, 8, 8, 8, 0, "female"),
    ("83_M_1983",      1983, 12, 21, 6, 0, "male"),
    ("84_F_1985",      1985, 4, 18, 16, 0, "female"),
    ("85_M_1990",      1990, 9, 30, 12, 0, "male"),
    ("86_F_1992",      1992, 1, 8, 8, 0, "female"),
    ("87_M_1994",      1994, 5, 14, 14, 0, "male"),
    ("88_F_1997",      1997, 2, 22, 20, 0, "female"),
    ("89_M_2001",      2001, 6, 30, 6, 0, "male"),
    ("90_F_2005",      2005, 11, 15, 10, 0, "female"),
    ("91_M_2011",      2011, 3, 8, 8, 0, "male"),
    ("92_F_2013",      2013, 7, 14, 14, 0, "female"),
    ("93_M_2016",      2016, 1, 21, 20, 0, "male"),
    ("94_F_2018",      2018, 5, 5, 4, 0, "female"),
    ("95_M_2019",      2019, 9, 19, 18, 0, "male"),
    ("96_F_2020",      2020, 2, 14, 6, 0, "female"),
    ("97_M_1971",      1971, 8, 18, 14, 0, "male"),
    ("98_F_1974",      1974, 3, 30, 8, 0, "female"),
    ("99_M_1977",      1977, 11, 22, 16, 0, "male"),
    ("100_F_1981",     1981, 6, 26, 10, 0, "female"),
]

DATASET_50 = [
    # (label, year, month, day, hour, minute, gender)
    ("01_CQ_M_1987",   1987, 1, 21, 4, 30, "male"),
    ("02_CQ_F_1983",   1983, 7, 7, 14, 0, "female"),
    ("03_VU_M_1990",   1990, 6, 15, 10, 0, "male"),
    ("04_NHU_F_1995",  1995, 12, 22, 2, 0, "female"),
    ("05_CT_M_1975",   1975, 9, 10, 8, 0, "male"),
    ("06_THTT_F_1982", 1982, 3, 3, 6, 0, "female"),
    ("07_ThucThan_M",  1991, 5, 5, 12, 0, "male"),
    ("08_TQ_F_1988",   1988, 8, 8, 20, 0, "female"),
    ("09_TONG_M_1964", 1964, 4, 4, 0, 0, "male"),
    ("10_HOA_F_1972",  1972, 10, 10, 16, 0, "female"),
    ("11_CQ_M_2000",   2000, 2, 14, 9, 0, "male"),
    ("12_CQ_F_1999",   1999, 11, 11, 3, 0, "female"),
    ("13_CQ_M_1985",   1985, 1, 5, 6, 0, "male"),
    ("14_CQ_F_1993",   1993, 7, 20, 14, 0, "female"),
    ("15_SS_M_1970",   1970, 8, 15, 0, 0, "male"),
    ("16_SS_F_2005",   2005, 6, 1, 12, 0, "female"),
    ("17_XUAN_M_1986", 1986, 4, 10, 8, 0, "male"),
    ("18_THU_F_1994",  1994, 10, 5, 18, 0, "female"),
    ("19_HA_M_2001",   2001, 7, 10, 13, 0, "male"),
    ("20_DONG_F_1968", 1968, 12, 15, 5, 0, "female"),
    # Additional 30 cases
    ("21_M_1960",      1960, 3, 15, 6, 0, "male"),
    ("22_F_1965",      1965, 9, 21, 18, 0, "female"),
    ("23_M_1973",      1973, 11, 3, 12, 0, "male"),
    ("24_F_1978",      1978, 5, 17, 8, 0, "female"),
    ("25_M_1980",      1980, 2, 28, 0, 0, "male"),
    ("26_F_1984",      1984, 8, 10, 14, 0, "female"),
    ("27_M_1989",      1989, 6, 22, 10, 0, "male"),
    ("28_F_1992",      1992, 12, 5, 20, 0, "female"),
    ("29_M_1996",      1996, 4, 18, 6, 0, "male"),
    ("30_F_1998",      1998, 10, 30, 16, 0, "female"),
    ("31_M_2003",      2003, 3, 8, 4, 0, "male"),
    ("32_F_2007",      2007, 7, 14, 22, 0, "female"),
    ("33_M_1958",      1958, 1, 10, 8, 0, "male"),
    ("34_F_1962",      1962, 6, 25, 14, 0, "female"),
    ("35_M_1967",      1967, 9, 9, 0, 0, "male"),
    ("36_F_1971",      1971, 4, 2, 10, 0, "female"),
    ("37_M_1974",      1974, 12, 20, 18, 0, "male"),
    ("38_F_1977",      1977, 8, 8, 12, 0, "female"),
    ("39_M_1981",      1981, 2, 4, 6, 0, "male"),
    ("40_F_1983",      1983, 5, 19, 20, 0, "female"),
    ("41_M_1987",      1987, 10, 15, 4, 0, "male"),
    ("42_F_1990",      1990, 3, 27, 16, 0, "female"),
    ("43_M_1993",      1993, 11, 11, 10, 0, "male"),
    ("44_F_1997",      1997, 7, 7, 8, 0, "female"),
    ("45_M_2002",      2002, 1, 22, 14, 0, "male"),
    ("46_F_2004",      2004, 9, 9, 0, 0, "female"),
    ("47_M_2008",      2008, 5, 5, 22, 0, "male"),
    ("48_F_1955",      1955, 12, 12, 12, 0, "female"),
    ("49_M_1950",      1950, 6, 6, 6, 0, "male"),
    ("50_F_1945",      1945, 3, 3, 3, 0, "female"),
]


def trace_one(label: str, y: int, mo: int, d: int, h: int, mi: int, g: str) -> dict:
    """Run full pipeline and trace pattern selection step by step."""
    cal = CalendarEngine().build(y, mo, d, h, mi)
    bazi = BaziEngine().build(cal, gender=g)
    ctx = build_pattern_context(bazi, calendar=cal)

    # Load rules directly to inspect
    from engines.pattern_engine.loader import PatternLoader
    from engines.pattern_engine.matcher import PatternMatcher
    loader = PatternLoader(DEFAULT_DATABASE_PATH)
    df = loader.load_rules()
    rules = df.to_dict("records")
    matcher = PatternMatcher()

    candidates = []
    for rule in rules:
        import json
        import pandas as pd
        normalized = dict(rule)
        raw_cond = normalized.get("conditions")
        try:
            if pd.isna(raw_cond):
                raw_cond = "[]"
        except TypeError:
            pass
        if isinstance(raw_cond, str):
            try:
                normalized["conditions"] = json.loads(raw_cond)
            except Exception:
                normalized["conditions"] = []
        elif not isinstance(raw_cond, list):
            normalized["conditions"] = []
        else:
            normalized["conditions"] = raw_cond

        if normalized.get("enabled", "1") in ("0", "false", "no", False):
            continue

        matched = matcher.match(ctx, normalized)
        candidates.append({
            "rule_id": normalized.get("rule_id"),
            "pattern": normalized.get("pattern"),
            "priority": int(normalized.get("priority", 0) or 0),
            "score": float(normalized.get("score", 0) or 0),
            "conditions_count": len(normalized["conditions"]),
            "matched": matched,
        })

    from engines.pattern_engine.calculators.follow_pattern import FollowPatternCalculator
    follow_type = FollowPatternCalculator().detect(ctx)

    engine = PatternEngine()
    result = engine.calculate(ctx)

    return {
        "label": label,
        "day_master": bazi.day_master,
        "month_branch": bazi.month_pillar.branch,
        "ten_gods": list(bazi.ten_gods or []),
        "hidden_stems": list(bazi.hidden_stems or [])[:6],
        "shensha_count": len(bazi.shensha or []),
        "candidates": candidates,
        "matched_candidates": [c for c in candidates if c["matched"]],
        "follow_type": follow_type,
        "selected_pattern": result.pattern,
        "selected_cach_cuc": result.cach_cuc,
        "selected_score": result.score,
        "selected_priority": result.priority,
        "matched_rules": result.matched_rules,
    }


def main():
    all_cases = DATASET_50 + DATASET_100
    print(f"Running Pattern Engine Audit — {len(all_cases)} charts\n")
    results = []
    errors = []

    for label, y, mo, d, h, mi, g in all_cases:
        try:
            r = trace_one(label, y, mo, d, h, mi, g)
            results.append(r)
        except Exception as ex:
            errors.append({"label": label, "error": str(ex)})
            results.append({
                "label": label,
                "selected_pattern": "ERROR",
                "selected_cach_cuc": str(ex)[:80],
                "error": str(ex),
            })

    # Distribution
    dist = Counter(r.get("selected_pattern") or "NONE" for r in results)
    total = len(results)
    error_count = len(errors)

    print(f"{'='*60}")
    print(f"Pattern Distribution ({total} charts, {error_count} errors)")
    print(f"{'='*60}")
    for pat, cnt in dist.most_common():
        pct = 100 * cnt / total
        flag = " *** DOMINANT ***" if pct > 70 else ""
        print(f"  {pat:<25} {cnt:>3}  ({pct:5.1f}%){flag}")
    print()

    # Show conditions analysis
    if results:
        sample = next((r for r in results if r.get("candidates")), None)
        if sample:
            print("Rule Database Analysis:")
            print(f"  Total rules loaded: {len(sample['candidates'])}")
            conds_zero = sum(1 for c in sample["candidates"] if c["conditions_count"] == 0)
            print(f"  Rules with conditions=[] (match ALL): {conds_zero}/{len(sample['candidates'])}")
            print(f"  Rules with real conditions: {len(sample['candidates']) - conds_zero}")
            print()
            print("Rules detail:")
            for c in sample["candidates"]:
                print(f"    {c['rule_id']:<15} pattern={c['pattern']:<15} priority={c['priority']} "
                      f"score={c['score']} conditions={c['conditions_count']} matched={c['matched']}")

    print()
    print("Follow-type detection per chart:")
    for r in results:
        ft = r.get("follow_type")
        if ft:
            print(f"  {r['label']}: {ft}")
    follow_count = sum(1 for r in results if r.get("follow_type"))
    print(f"  Total charts with follow_type detected: {follow_count}/{total}")

    # Save full trace
    out = {
        "total": total,
        "errors": error_count,
        "distribution": dict(dist.most_common()),
        "results": results,
        "errors_detail": errors,
    }
    out_path = Path(__file__).parent / "pattern_audit_raw.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nFull trace saved to: {out_path}")
    return out


if __name__ == "__main__":
    main()
