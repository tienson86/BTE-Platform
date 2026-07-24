"""RC1 audit runner — generates validation/real_cases and perf_raw.json (read-only wrt engines)."""

from __future__ import annotations

import json
import time
import tracemalloc
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    warns: list[str] = []

    def showwarning(message, category, filename, lineno, file=None, line=None):  # noqa: ANN001
        warns.append(f"{category.__name__}: {message} ({filename}:{lineno})")

    warnings.showwarning = showwarning

    from applications.api.services.orchestrator import OrchestratorService
    from engines.bazi_engine.engine import BaziEngine
    from engines.calendar_engine.engine import CalendarEngine
    from engines.interpretation_engine.engine import InterpretationEngine
    from engines.narrative_engine.engine import NarrativeEngine
    from engines.pattern_engine.context import PatternContext
    from engines.pattern_engine.engine import PatternEngine
    from engines.report_engine.engine import ReportEngine
    from engines.score_engine.engine import ScoreEngine

    cases = [
        {"id": "case_01", "year": 1990, "month": 5, "day": 15, "hour": 10, "minute": 30, "gender": "male", "timezone": "Asia/Ho_Chi_Minh"},
        {"id": "case_02", "year": 1988, "month": 1, "day": 8, "hour": 6, "minute": 0, "gender": "female", "timezone": "Asia/Ho_Chi_Minh"},
        {"id": "case_03", "year": 1975, "month": 12, "day": 31, "hour": 23, "minute": 45, "gender": "male", "timezone": "Asia/Ho_Chi_Minh"},
        {"id": "case_04", "year": 2000, "month": 2, "day": 29, "hour": 12, "minute": 0, "gender": "female", "timezone": "Asia/Ho_Chi_Minh"},
        {"id": "case_05", "year": 1960, "month": 7, "day": 4, "hour": 4, "minute": 20, "gender": "male", "timezone": "Asia/Bangkok"},
        {"id": "case_06", "year": 1995, "month": 9, "day": 9, "hour": 9, "minute": 9, "gender": "female", "timezone": "Asia/Ho_Chi_Minh"},
        {"id": "case_07", "year": 1982, "month": 3, "day": 21, "hour": 15, "minute": 15, "gender": "male", "timezone": "Asia/Ho_Chi_Minh"},
        {"id": "case_08", "year": 1999, "month": 11, "day": 11, "hour": 11, "minute": 11, "gender": "female", "timezone": "Asia/Singapore"},
        {"id": "case_09", "year": 1970, "month": 6, "day": 1, "hour": 0, "minute": 0, "gender": "male", "timezone": "Asia/Ho_Chi_Minh"},
        {"id": "case_10", "year": 2010, "month": 8, "day": 20, "hour": 18, "minute": 30, "gender": "female", "timezone": "Asia/Ho_Chi_Minh"},
        {"id": "case_11", "year": 1985, "month": 4, "day": 12, "hour": 7, "minute": 45, "gender": "male", "timezone": "Asia/Ho_Chi_Minh"},
        {"id": "case_12", "year": 1992, "month": 10, "day": 3, "hour": 21, "minute": 10, "gender": "female", "timezone": "Asia/Ho_Chi_Minh"},
        {"id": "case_13", "year": 1968, "month": 2, "day": 14, "hour": 8, "minute": 0, "gender": "male", "timezone": "Asia/Ho_Chi_Minh"},
        {"id": "case_14", "year": 2005, "month": 5, "day": 5, "hour": 5, "minute": 5, "gender": "female", "timezone": "Asia/Ho_Chi_Minh"},
        {"id": "case_15", "year": 1978, "month": 8, "day": 18, "hour": 14, "minute": 0, "gender": "male", "timezone": "Asia/Jakarta"},
        {"id": "case_16", "year": 1993, "month": 1, "day": 1, "hour": 1, "minute": 1, "gender": "female", "timezone": "Asia/Ho_Chi_Minh"},
        {"id": "case_17", "year": 1980, "month": 12, "day": 25, "hour": 19, "minute": 30, "gender": "male", "timezone": "Asia/Ho_Chi_Minh"},
        {"id": "case_18", "year": 1997, "month": 7, "day": 7, "hour": 17, "minute": 0, "gender": "female", "timezone": "Asia/Ho_Chi_Minh"},
        {"id": "case_19", "year": 1965, "month": 9, "day": 30, "hour": 3, "minute": 15, "gender": "male", "timezone": "Asia/Ho_Chi_Minh"},
        {"id": "case_20", "year": 2001, "month": 3, "day": 8, "hour": 13, "minute": 45, "gender": "female", "timezone": "Asia/Ho_Chi_Minh"},
    ]

    def pillar_text(pillar: object) -> str:
        return f"{getattr(pillar, 'stem', '')} {getattr(pillar, 'branch', '')}".strip()

    def stage_run(inp: dict) -> tuple[dict, int, dict]:
        times: dict[str, float] = {}
        tracemalloc.start()
        t0 = time.perf_counter()
        cal = CalendarEngine().build(inp["year"], inp["month"], inp["day"], inp["hour"], inp["minute"])
        times["calendar"] = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        bazi = BaziEngine().build(cal, gender=inp["gender"])
        times["bazi"] = (time.perf_counter() - t0) * 1000

        ctx = PatternContext(
            year_pillar=pillar_text(bazi.year_pillar),
            month_pillar=pillar_text(bazi.month_pillar),
            day_pillar=pillar_text(bazi.day_pillar),
            hour_pillar=pillar_text(bazi.hour_pillar),
            day_master=bazi.day_master,
            ten_gods={"list": list(bazi.ten_gods or [])},
            shensha=list(bazi.shensha or []),
        )
        t0 = time.perf_counter()
        pattern = PatternEngine().calculate(ctx)
        times["pattern"] = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        score = ScoreEngine().calculate({"calendar": cal, "bazi": bazi, "pattern": pattern})
        times["score"] = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        interp = InterpretationEngine().run(
            {"calendar": cal, "bazi": bazi, "pattern": pattern, "score": score}
        )
        times["interpretation"] = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        report = ReportEngine().render(interp)
        times["report"] = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        narr = NarrativeEngine().compose(interp, report)
        times["narrative"] = (time.perf_counter() - t0) * 1000

        peak = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        meta = {
            "interpretation_summary": getattr(interp, "summary", ""),
            "sentence_count": getattr(interp, "sentence_count", 0),
            "report_title": getattr(getattr(report, "metadata", None), "title", ""),
            "narrative_title": getattr(narr, "title", ""),
            "day_master": getattr(bazi, "day_master", None),
        }
        return times, peak, meta

    orch = OrchestratorService()
    cases_root = ROOT / "validation" / "real_cases"
    cases_root.mkdir(parents=True, exist_ok=True)

    t0 = time.perf_counter()
    orch.analyze(year=1990, month=5, day=15, hour=10, minute=30, gender="male")
    cold = (time.perf_counter() - t0) * 1000
    t0 = time.perf_counter()
    orch.analyze(year=1990, month=5, day=15, hour=10, minute=30, gender="male")
    warm = (time.perf_counter() - t0) * 1000

    stage_times, peak, sample_meta = stage_run(
        {k: v for k, v in cases[0].items() if k != "id"}
    )

    perf: dict = {
        "cold_analyze_ms": round(cold, 2),
        "warm_analyze_ms": round(warm, 2),
        "stage_sample": {
            "times_ms": {k: round(v, 2) for k, v in stage_times.items()},
            "peak_traced_bytes": peak,
            "meta": sample_meta,
        },
        "cases": [],
        "errors": [],
        "warnings": [],
    }

    expected = {
        "pipeline": [
            "calendar",
            "bazi",
            "pattern",
            "score",
            "interpretation",
            "report",
            "narrative",
        ],
        "has_interpretation": True,
        "has_report_html": True,
        "has_narrative_html": True,
        # API JSON currently omits bazi.day_master (engine has it; serializer drops it)
        "day_pillar_present": True,
    }

    for case in cases:
        case_dir = cases_root / case["id"]
        case_dir.mkdir(exist_ok=True)
        inp = {k: v for k, v in case.items() if k != "id"}
        (case_dir / "input.json").write_text(
            json.dumps(inp, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (case_dir / "expected.json").write_text(
            json.dumps(expected, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        t0 = time.perf_counter()
        try:
            data = orch.analyze(**inp)
            elapsed = (time.perf_counter() - t0) * 1000
            bazi = data.get("bazi") if isinstance(data.get("bazi"), dict) else {}
            day_pillar = bazi.get("day_pillar")
            actual = {
                "pipeline": data.get("pipeline"),
                "day_master_api": bazi.get("day_master"),
                "day_pillar": day_pillar,
                "interpretation": data.get("interpretation"),
                "report": {
                    "title": (data.get("report") or {}).get("title"),
                    "section_count": (data.get("report") or {}).get("section_count"),
                    "has_html": bool((data.get("report") or {}).get("html")),
                    "has_markdown": bool((data.get("report") or {}).get("markdown")),
                },
                "narrative": {
                    "title": (data.get("narrative") or {}).get("title"),
                    "tone": (data.get("narrative") or {}).get("tone"),
                    "has_html": bool((data.get("narrative") or {}).get("html")),
                    "has_markdown": bool((data.get("narrative") or {}).get("markdown")),
                },
                "elapsed_ms": round(elapsed, 2),
            }
            (case_dir / "actual.json").write_text(
                json.dumps(actual, ensure_ascii=False, indent=2, default=str),
                encoding="utf-8",
            )
            diffs: list[str] = []
            if actual.get("pipeline") != expected["pipeline"]:
                diffs.append(f"- pipeline mismatch: {actual.get('pipeline')}")
            if not actual.get("interpretation"):
                diffs.append("- missing interpretation")
            if not actual["report"]["has_html"]:
                diffs.append("- missing report html")
            if not actual["narrative"]["has_html"]:
                diffs.append("- missing narrative html")
            if not day_pillar:
                diffs.append("- missing day_pillar")
            if actual.get("day_master_api") in (None, ""):
                diffs.append(
                    "- NOTE: bazi.day_master missing in API JSON "
                    "(engine has value; serializer gap)"
                )
            # Structural pass ignores day_master serializer note
            hard = [d for d in diffs if not d.startswith("- NOTE:")]
            status = "PASS" if not hard else "FAIL"
            body = "\n".join(diffs) if diffs else "No structural differences vs RC1 expected contract."
            (case_dir / "diff.md").write_text(
                f"# {case['id']} diff\n\nStatus: **{status}**\n\n{body}\n\n"
                f"Elapsed: {actual['elapsed_ms']} ms\n",
                encoding="utf-8",
            )
            perf["cases"].append(
                {
                    "id": case["id"],
                    "status": status,
                    "elapsed_ms": actual["elapsed_ms"],
                    "day_pillar": day_pillar,
                    "day_master_api_missing": actual.get("day_master_api") in (None, ""),
                }
            )
            print(status, case["id"], round(elapsed, 1), "ms")
        except Exception as exc:  # noqa: BLE001 - audit capture
            perf["errors"].append({"id": case["id"], "error": str(exc)})
            (case_dir / "actual.json").write_text(
                json.dumps({"error": str(exc)}, indent=2), encoding="utf-8"
            )
            (case_dir / "diff.md").write_text(
                f"# {case['id']}\n\nStatus: **FAIL**\n\nException: {exc}\n",
                encoding="utf-8",
            )
            print("FAIL", case["id"], exc)

    perf["warnings"] = warns
    out = ROOT / "validation" / "perf_raw.json"
    out.write_text(json.dumps(perf, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    passed = sum(1 for item in perf["cases"] if item["status"] == "PASS")
    print("PASS", passed, "/", len(cases))
    print("WARN_COUNT", len(warns))
    print("ERRORS", len(perf["errors"]))


if __name__ == "__main__":
    main()
