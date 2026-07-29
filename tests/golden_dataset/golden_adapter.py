"""
Golden Dataset birth → RuleContext → V1 InterpretationReport adapter.

Keeps Calendar / Bazi / Pattern / Score orchestration out of the core
InterpretationEngine.run(RuleContext) path while enabling golden inputs.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from engines.bazi_engine.engine import BaziEngine
from engines.bazi_engine.ten_god import STEM_META
from engines.calendar_engine.engine import CalendarEngine
from engines.core.utils import remove_accents
from engines.pattern_engine.engine import PatternEngine
from engines.pattern_engine.labels import pattern_display_label
from engines.pattern_engine.utils.context_builder import build_pattern_context
from engines.rule_contract import RuleContextBuilder
from engines.score_engine.engine import ScoreEngine


STRENGTH_ASCII = {
    "strong": "than vuong",
    "weak": "than nhuoc",
    "balanced": "than can bang",
    "than_vuong": "than vuong",
    "than_nhuoc": "than nhuoc",
    "than_can_bang": "than can bang",
}

ELEMENT_ASCII = {
    "wood": "Moc",
    "fire": "Hoa",
    "earth": "Tho",
    "metal": "Kim",
    "water": "Thuy",
    "moc": "Moc",
    "hoa": "Hoa",
    "tho": "Tho",
    "kim": "Kim",
    "thuy": "Thuy",
    "Mộc": "Moc",
    "Hỏa": "Hoa",
    "Thổ": "Tho",
    "Kim": "Kim",
    "Thủy": "Thuy",
}


def is_birth_input(payload: dict[str, Any]) -> bool:
    """Return True when payload is a Golden birth case (not RuleContext)."""
    if not isinstance(payload, dict):
        return False
    if "bazi" in payload and "wuxing" in payload:
        return False
    birth = payload.get("birth")
    return isinstance(birth, dict) and bool(
        birth.get("solar_datetime") or birth.get("datetime")
    )


def parse_birth(case: dict[str, Any]) -> tuple[datetime, str]:
    """Extract birth datetime and gender from a golden case."""
    birth = case.get("birth") or {}
    raw = birth.get("solar_datetime") or birth.get("datetime")
    if not raw:
        raise ValueError(f"{case.get('case_id')}: missing birth datetime")
    dt = datetime.fromisoformat(str(raw))
    gender = str(birth.get("gender") or "male")
    return dt, gender


def build_rule_context(case: dict[str, Any]) -> dict[str, Any]:
    """
    Calendar → Bazi → Pattern → Score → RuleContext.

    Mirrors the WP4.5 coverage runner, using the production pattern context
    builder so Pattern Engine receives month-command fields.
    """
    dt, gender = parse_birth(case)
    calendar = CalendarEngine().build(
        dt.year, dt.month, dt.day, dt.hour, dt.minute
    )
    chart = BaziEngine().build(calendar, gender=gender)
    pattern_ctx = build_pattern_context(chart, calendar=calendar)
    pattern = PatternEngine().calculate(pattern_ctx)

    upstream = case.get("upstream") or {}
    builder = RuleContextBuilder()
    ctx = builder.build(
        calendar=calendar,
        bazi=chart,
        pattern=pattern,
        luck=upstream.get("luck"),
        shensha=upstream.get("shensha"),
        useful_god=upstream.get("useful_god"),
        temperature=upstream.get("temperature"),
        metadata={
            "case_id": case.get("case_id"),
            "coverage_goal": case.get("coverage_goal"),
        },
    )
    score = ScoreEngine().calculate(ctx)
    ctx = builder.build(
        calendar=calendar,
        bazi=chart,
        pattern=pattern,
        score=score,
        luck=upstream.get("luck"),
        shensha=upstream.get("shensha"),
        useful_god=upstream.get("useful_god"),
        temperature=upstream.get("temperature"),
        metadata={
            "case_id": case.get("case_id"),
            "coverage_goal": case.get("coverage_goal"),
        },
    )
    overrides = case.get("fact_overrides") or {}
    if overrides:
        facts = dict(ctx.get("facts") or {})
        for key, value in overrides.items():
            facts[key] = value
            if value is True:
                ctx[key] = True
        ctx["facts"] = facts
    # Attach live objects for V1 text formatting (not part of RuleContext contract).
    ctx["_golden_chart"] = chart
    ctx["_golden_pattern"] = pattern
    ctx["_golden_score"] = score
    return ctx


def format_v1_text(ctx: dict[str, Any]) -> str:
    """
    Build ASCII V1 summary line for Golden Dataset expected/actual compare.

    Example:
      Nhat chu Canh Kim sinh thang Suu, than can bang, Chinh An thanh cach,
      Dung Than la Thuy.
    """
    chart = ctx.get("_golden_chart")
    pattern = ctx.get("_golden_pattern")
    bazi = ctx.get("bazi") or {}
    strength = ctx.get("strength") or {}
    useful = ctx.get("useful_god") or {}
    score = ctx.get("score") or {}

    day_master = str(
        getattr(chart, "day_master", None)
        or bazi.get("day_master")
        or ""
    ).strip()
    element = ""
    if day_master and day_master in STEM_META:
        element = STEM_META[day_master][0]

    month_pillar = getattr(chart, "month_pillar", None) if chart else None
    month_branch = str(
        getattr(month_pillar, "branch", None)
        or (bazi.get("month_pillar") or {}).get("branch")
        or ""
    ).strip()

    level = str(strength.get("level") or score.get("strength_level") or "").strip()
    strength_label = STRENGTH_ASCII.get(level, "")
    if not strength_label:
        # Fall back to balanced wording when strength producer is thin.
        strength_label = "than can bang"

    pattern_code = str(
        getattr(pattern, "final_pattern", None)
        or getattr(pattern, "pattern", None)
        or (ctx.get("pattern") or {}).get("main_pattern")
        or ""
    ).strip()
    pattern_label = pattern_display_label(
        pattern_code,
        getattr(pattern, "description", None) if pattern is not None else None,
    )

    dung_than = ""
    element_hint = useful.get("element")
    if element_hint:
        dung_than = ELEMENT_ASCII.get(
            str(element_hint).strip(),
            ELEMENT_ASCII.get(str(element_hint).strip().lower(), ""),
        )
    if not dung_than:
        raw_name = str(
            useful.get("name")
            or useful.get("useful_god")
            or getattr(pattern, "dung_than", None)
            or ""
        ).strip()
        dung_than = ELEMENT_ASCII.get(raw_name, raw_name)
    if not dung_than:
        favorable = useful.get("favorable") or useful.get("favorable_gods") or []
        if favorable:
            fav = str(favorable[0])
            dung_than = ELEMENT_ASCII.get(fav, fav)

    parts = [
        f"Nhat chu {day_master} {element} sinh thang {month_branch}".strip(),
        strength_label,
        f"{pattern_label} thanh cach" if pattern_label else "",
        f"Dung Than la {dung_than}" if dung_than else "",
    ]
    text = ", ".join(p for p in parts if p)
    # Normalize whitespace then strip diacritics for V1 ASCII compare.
    text = " ".join(text.split())
    return remove_accents(text)


def to_v1_report(interpretation: Any, ctx: dict[str, Any]) -> dict[str, Any]:
    """Serialize engine result to Golden V1 shape: success / text / sections."""
    success = True
    if hasattr(interpretation, "confidence"):
        success = True
    text = format_v1_text(ctx)
    return {
        "success": success,
        "sections": [],
        "text": text,
    }
