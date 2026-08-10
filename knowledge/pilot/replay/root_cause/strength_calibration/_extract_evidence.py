"""PILOT-1B Strength calibration extractor — read-only, no production patches."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from applications.api.utils.serializers import to_jsonable
from engines.bazi_engine.engine import BaziEngine
from engines.calendar_engine.engine import CalendarEngine
from engines.strength_engine.engine import StrengthEngine
from engines.strength_engine.utils.context_builder import build_strength_context
from engines.temperature_engine.engine import TemperatureEngine
from engines.temperature_engine.utils.context_builder import build_temperature_context

OUT = Path("knowledge/pilot/replay/root_cause/strength_calibration/evidence")

CASES = [
    {"case_id": "CASE-0001", "expert": "balanced / slightly weak", "expert_vi": "Thân trung bình / thiên nhược",
     "y": 1987, "m": 1, "d": 21, "h": 4, "mi": 30, "g": "male"},
    {"case_id": "CASE-0002", "expert": "very strong", "expert_vi": "Thân rất vượng",
     "y": 1977, "m": 2, "d": 18, "h": 6, "mi": 30, "g": "male"},
    {"case_id": "CASE-0003", "expert": "slightly weak", "expert_vi": "Thân hơi nhược",
     "y": 2015, "m": 8, "d": 14, "h": 7, "mi": 20, "g": "male", "boundary": True},
    {"case_id": "CASE-0004", "expert": "strong", "expert_vi": "Thân vượng",
     "y": 2013, "m": 8, "d": 20, "h": 13, "mi": 40, "g": "male"},
    {"case_id": "CASE-0005", "expert": "balanced / slightly strong", "expert_vi": "Thân trung bình thiên vượng",
     "y": 1966, "m": 9, "d": 24, "h": 4, "mi": 15, "g": None},
    {"case_id": "CASE-0006", "expert": "balanced / slightly weak", "expert_vi": "Thân trung bình thiên nhược",
     "y": 1988, "m": 6, "d": 7, "h": 20, "mi": 45, "g": "female",
     "corrected_chart_note": "PILOT-1A: use live Mậu Ngọ month (not invalid expert Đinh Tỵ)"},
    {"case_id": "CASE-0007", "expert": "strong", "expert_vi": "Thân vượng",
     "y": 1984, "m": 7, "d": 13, "h": 21, "mi": 1, "g": "female"},
]

POLARITY = {
    "season": "strengthen",
    "root": "strengthen",
    "support": "strengthen",
    "drain": "weaken",
    "control": "weaken",
    "combination": "context",
    "special": "context",
}


def pillar_text(p: Any) -> str:
    return f"{getattr(p, 'stem', '')} {getattr(p, 'branch', '')}".strip()


def extract_case(case: dict[str, Any], strength_engine: StrengthEngine) -> dict[str, Any]:
    calendar = CalendarEngine().build(case["y"], case["m"], case["d"], case["h"], case["mi"])
    bazi = BaziEngine().build(calendar, gender=case["g"])
    ctx = build_strength_context(bazi, calendar=calendar)

    # Temperature (exposed via separate engine; may be NOT_EXPOSED to StrengthContext)
    temp_ctx = build_temperature_context(
        bazi,
        calendar=calendar,
        strength_level=None,
        strength_score=None,
    )
    temp = TemperatureEngine().calculate(temp_ctx)

    grouped = strength_engine.loader.load_rule_groups()
    priority_rules = strength_engine.loader.load_priority_rules()
    level_rules = strength_engine.loader.load_level_rules()
    config = strength_engine.loader.load_config()
    analysis = strength_engine.analyzer.analyze(ctx, grouped)
    from engines.strength_engine.priority import StrengthPriorityResolver
    resolver = StrengthPriorityResolver(priority_rules)
    scored = strength_engine.scorer.score(
        ctx, analysis, config, level_rules, strength_engine.matcher, resolver
    )
    result = strength_engine.calculate(ctx)

    ledger = []
    for rule in analysis.get("all_matches") or []:
        group = str(rule.get("score_target") or rule.get("rule_group") or "")
        score = float(rule.get("score") or 0.0)
        runtime_pol = POLARITY.get(group, "unknown")
        if score < 0:
            runtime_pol = "weaken"
        elif score > 0 and group in ("season", "root", "support"):
            runtime_pol = "strengthen"
        elif score > 0 and group == "special":
            runtime_pol = "strengthen"  # positive special adds to total
        elif score > 0 and group == "control":
            runtime_pol = "INCONSISTENT_POSITIVE_CONTROL"
        ledger.append({
            "rule_id": rule.get("rule_id"),
            "group": group,
            "score": score,
            "contribution_normalized": score / float(config.get("scale") or 100.0),
            "priority": rule.get("priority"),
            "reason": rule.get("reason") or rule.get("description"),
            "conditions": rule.get("conditions"),
            "runtime_polarity": runtime_pol,
            "expected_polarity_by_group": POLARITY.get(group),
            "polarity_correct_vs_group_convention": (
                (score >= 0 and POLARITY.get(group) == "strengthen")
                or (score <= 0 and POLARITY.get(group) == "weaken")
                or POLARITY.get(group) == "context"
            ),
        })

    context_fields = {
        "day_master": getattr(ctx, "day_master", None),
        "day_master_element": getattr(ctx, "day_master_element", None),
        "day_master_yin_yang": getattr(ctx, "day_master_yin_yang", None),
        "month_branch": getattr(ctx, "month_branch", None),
        "month_stem": getattr(ctx, "month_stem", None),
        "month_status": getattr(ctx, "month_status", None),
        "month_branch_element": getattr(ctx, "month_branch_element", None),
        "month_branch_ten_god": getattr(ctx, "month_branch_ten_god", None),
        "season": getattr(ctx, "season", None),
        "season_phase": getattr(ctx, "season_phase", None),
        "temperature_type": getattr(ctx, "temperature_type", None),
        "root_level": getattr(ctx, "root_level", None),
        "root_count": getattr(ctx, "root_count", None),
        "support_type": getattr(ctx, "support_type", None),
        "control_type": getattr(ctx, "control_type", None),
        "drain_type": getattr(ctx, "drain_type", None),
        "officer_elements": list(getattr(ctx, "officer_elements", []) or []),
        "wealth_elements": list(getattr(ctx, "wealth_elements", []) or []),
        "resource_elements": list(getattr(ctx, "resource_elements", []) or []),
        "output_elements": list(getattr(ctx, "output_elements", []) or []),
        "companion_elements": list(getattr(ctx, "companion_elements", []) or []),
        "drain_count": getattr(ctx, "drain_count", None),
        "hidden_stems": list(getattr(ctx, "hidden_stems", []) or []) if hasattr(ctx, "hidden_stems") else "NOT_EXPOSED",
    }

    # Probe optional attrs
    for key in ("supporting_elements", "restricting_elements", "ten_gods", "branches"):
        if hasattr(ctx, key):
            context_fields[key] = getattr(ctx, key)
        else:
            context_fields[key] = "NOT_EXPOSED"

    buckets = {
        "season": sum(x["score"] for x in ledger if x["group"] == "season"),
        "root": sum(x["score"] for x in ledger if x["group"] == "root"),
        "support": sum(x["score"] for x in ledger if x["group"] == "support"),
        "drain": sum(x["score"] for x in ledger if x["group"] == "drain"),
        "control": sum(x["score"] for x in ledger if x["group"] == "control"),
        "combination": sum(x["score"] for x in ledger if x["group"] == "combination"),
        "special": sum(x["score"] for x in ledger if x["group"] == "special"),
    }

    return {
        "case_id": case["case_id"],
        "expert_reference": {"en": case["expert"], "vi": case["expert_vi"]},
        "boundary": bool(case.get("boundary")),
        "corrected_chart_note": case.get("corrected_chart_note"),
        "input": {"year": case["y"], "month": case["m"], "day": case["d"], "hour": case["h"], "minute": case["mi"], "gender": case["g"]},
        "chart": {
            "year": pillar_text(bazi.year_pillar),
            "month": pillar_text(bazi.month_pillar),
            "day": pillar_text(bazi.day_pillar),
            "hour": pillar_text(bazi.hour_pillar),
            "day_master": bazi.day_master,
        },
        "calendar_solar_term": {
            "name": getattr(getattr(calendar, "solar_term", None), "name", None),
            "index": getattr(getattr(calendar, "solar_term", None), "index", None),
        },
        "pipeline": {
            "season_context": {
                "season": context_fields["season"],
                "season_phase": context_fields["season_phase"],
                "month_status": context_fields["month_status"],
                "month_branch": context_fields["month_branch"],
            },
            "temperature_context": {
                "from_strength_context": context_fields["temperature_type"],
                "from_temperature_engine": {
                    "temperature_level": getattr(temp, "temperature_level", None),
                    "temperature_score": getattr(temp, "temperature_score", None),
                    "reasoning": getattr(temp, "reasoning", None),
                },
                "note": "TemperatureEngine runs separately; StrengthContext.temperature_type may be branch-derived only",
            },
            "supporting_elements": context_fields.get("companion_elements"),
            "resource_elements": context_fields.get("resource_elements"),
            "restricting_elements": {
                "officer": context_fields.get("officer_elements"),
                "output": context_fields.get("output_elements"),
                "wealth": context_fields.get("wealth_elements"),
            },
            "root_resource_evidence": {
                "root_level": context_fields["root_level"],
                "root_count": context_fields["root_count"],
                "support_type": context_fields["support_type"],
            },
            "strength_evidence_ledger": ledger,
            "weighted_buckets_raw": buckets,
            "raw_strength_score": scored.get("raw_total"),
            "normalized_score": scored.get("strength_score"),
            "baseline": config.get("baseline"),
            "scale": config.get("scale"),
            "normalization_formula": "(raw_total + baseline) / scale clamped [0,1]",
            "current_band": scored.get("strength_level"),
            "current_label": scored.get("reasoning"),
            "confidence": scored.get("confidence"),
            "confidence_formula": "min(1, len(matched)/5) + 0.2 if level_rule else 0",
            "level_rule": scored.get("level_rule"),
            "published_contract": result.to_dict() if hasattr(result, "to_dict") else {
                "strength_level": result.strength_level,
                "strength_score": result.strength_score,
                "season_score": result.season_score,
                "root_score": result.root_score,
                "support_score": result.support_score,
                "drain_score": result.drain_score,
                "control_score": result.control_score,
                "confidence": result.confidence,
                "reasoning": result.reasoning,
                "matched_rules": result.matched_rules,
            },
            "context_fields": context_fields,
        },
    }


def main() -> None:
    engine = StrengthEngine()
    rows = []
    for case in CASES:
        print("extract", case["case_id"])
        data = extract_case(case, engine)
        rows.append(data)
        path = OUT / f"{case['case_id']}.json"
        path.write_text(json.dumps(to_jsonable(data), ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {
        "cases": [
            {
                "case_id": r["case_id"],
                "expert": r["expert_reference"],
                "chart_month": r["chart"]["month"],
                "raw": r["pipeline"]["raw_strength_score"],
                "normalized": r["pipeline"]["normalized_score"],
                "band": r["pipeline"]["current_band"],
                "label": r["pipeline"]["current_label"],
                "confidence": r["pipeline"]["confidence"],
                "buckets": r["pipeline"]["weighted_buckets_raw"],
                "n_rules": len(r["pipeline"]["strength_evidence_ledger"]),
            }
            for r in rows
        ]
    }
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
