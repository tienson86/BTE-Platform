"""
RuleContext publication helpers.

Pattern Engine is the sole producer of RuleContext (attached to PatternResult).
Downstream engines (Score, Interpretation, Report) must consume the published
context and must not rebuild it.
"""

from __future__ import annotations

from typing import Any

from engines.bazi_engine.ten_god import day_master_element

from .follow_tokens import canonicalize_follow_token, follow_display_label
from .labels import STRENGTH_LEVEL_LABELS, pattern_display_label
from .override_eligibility import classify_pattern_override

# Relation slots — published only when an upstream combination producer fills them.
_RELATION_KEYS: tuple[str, ...] = (
    "tam_hop",
    "luc_hop",
    "luc_xung",
    "tam_hinh",
    "hai",
    "pha",
    "ban_hop",
    "hoa",
)


def build_rule_context(
    *,
    calendar: Any,
    bazi: Any,
    pattern: Any,
    useful_god: Any = None,
    strength: Any = None,
    temperature: Any = None,
    score: Any = None,
    luck: Any = None,
    shensha: Any = None,
) -> dict[str, Any]:
    """
    Publish RuleContext (Pattern Engine sole-producer entry).

    Delegates to ContextEngine V2 for unified aggregation, then enriches summaries.
    """
    from engines.context_engine.engine import ContextEngine

    engine = ContextEngine()
    unified, context = engine.build_and_publish(
        calendar=calendar,
        bazi=bazi,
        strength=strength,
        temperature=temperature,
        pattern=pattern,
        useful_god=useful_god,
        score=score,
        luck=luck,
        shensha=shensha,
    )
    context["_unified_context"] = unified.to_dict()
    return context


def merge_upstream_into_rule_context(
    rule_context: dict[str, Any],
    *,
    useful_god: Any = None,
    strength: Any = None,
    temperature: Any = None,
) -> dict[str, Any]:
    """
    Overlay post-Pattern engine payloads onto an existing RuleContext.

    Does not rebuild RuleContext — only refreshes useful_god / strength /
    temperature sections already published by Pattern Engine.
    """
    from engines.rule_contract.context_builder import RuleContextBuilder

    builder = RuleContextBuilder()
    context = rule_context

    if strength is not None:
        existing = dict(context.get("strength") or {})
        if isinstance(strength, dict):
            existing.update(
                {
                    "level": strength.get("level")
                    or strength.get("strength_level")
                    or existing.get("level"),
                    "score": float(
                        strength.get("score", strength.get("strength_score", existing.get("score", 0.0)))
                        or 0.0
                    ),
                    "source": strength.get("source") or "strength_engine_v2",
                }
            )
        else:
            existing.update(
                {
                    "level": getattr(strength, "strength_level", None)
                    or existing.get("level"),
                    "score": float(
                        getattr(strength, "strength_score", existing.get("score", 0.0))
                        or 0.0
                    ),
                    "season_score": float(getattr(strength, "season_score", 0.0) or 0.0),
                    "root_score": float(getattr(strength, "root_score", 0.0) or 0.0),
                    "support_score": float(
                        getattr(strength, "support_score", 0.0) or 0.0
                    ),
                    "drain_score": float(getattr(strength, "drain_score", 0.0) or 0.0),
                    "control_score": float(
                        getattr(strength, "control_score", 0.0) or 0.0
                    ),
                    "confidence": float(getattr(strength, "confidence", 0.0) or 0.0),
                    "matched_rules": list(
                        getattr(strength, "matched_rules", []) or []
                    ),
                    "reasoning": str(getattr(strength, "reasoning", "") or ""),
                    "source": "strength_engine_v2",
                    "success": bool(getattr(strength, "success", True)),
                }
            )
        context["strength"] = existing
        context["strength_score"] = existing.get("score", 0.0)

    if temperature is not None:
        context["temperature"] = builder._build_temperature(
            temperature
            if isinstance(temperature, dict)
            else {
                "status": (
                    temperature.to_pattern_temperature_type()
                    if hasattr(temperature, "to_pattern_temperature_type")
                    else getattr(temperature, "temperature_level", None)
                ),
                "result": (
                    temperature.to_pattern_temperature_type()
                    if hasattr(temperature, "to_pattern_temperature_type")
                    else getattr(temperature, "temperature_level", None)
                ),
                "profile": getattr(temperature, "temperature_level", None),
                "index": getattr(temperature, "temperature_score", None),
                "cold_score": getattr(temperature, "cold_score", None),
                "hot_score": getattr(temperature, "warm_score", None),
                "dry_score": getattr(temperature, "dry_score", None),
                "damp_score": getattr(temperature, "humid_score", None),
                "humidity": getattr(temperature, "humid_score", None),
                "comment": getattr(temperature, "reasoning", None),
            },
            context.get("bazi") or {},
            context.get("wuxing"),
        )
        context["temperature_type"] = context["temperature"].get("status")

    if useful_god is not None:
        context["useful_god"] = builder._build_useful_god(
            None,
            useful_god,
            context.get("pattern") or {},
            context.get("bazi") or {},
            context.get("hidden_stems") or {},
            context.get("ten_gods") or {},
        )
        _refresh_useful_god_facts(context)

    return context


def _refresh_useful_god_facts(context: dict[str, Any]) -> None:
    """Keep RuleContext facts aligned with UsefulGodEngine-owned fields."""
    useful = context.get("useful_god") or {}
    facts = dict(context.get("facts") or {})
    status = useful.get("status")
    missing = {None, "", "MISSING", "Không có Dụng thần"}
    has_name = bool(useful.get("name") or useful.get("useful_god"))
    facts["useful_god_found"] = has_name
    facts["dung_than_da_xac_dinh"] = has_name
    facts["useful_god_active"] = has_name and status not in missing
    facts["hy_than_da_xac_dinh"] = bool(
        useful.get("favorable_gods") or useful.get("favorable")
    )
    facts["ky_than_da_xac_dinh"] = bool(
        useful.get("unfavorable_gods") or useful.get("unfavorable")
    )
    facts["harmful_god_present"] = bool(
        useful.get("unfavorable_gods") or useful.get("unfavorable")
    )
    facts["useful_god_blocked"] = status in {"MISSING", "Không có Dụng thần"}
    facts["useful_god_supported"] = bool(
        useful.get("in_stem") or useful.get("in_branch") or useful.get("in_hidden")
    )
    context["facts"] = facts
    for key, value in facts.items():
        if value is True:
            context[key] = True


def enrich_rule_context_summaries(
    rule_context: dict[str, Any],
    *,
    pattern: Any = None,
) -> dict[str, Any]:
    """
    Attach Stage 5 summary / Cách Cục fields from existing RuleContext sections.

    Does not recalculate Pattern/BaZi/Score business logic. Does not mutate
    PatternContext. Safe to call again after Score compose for strength labels.
    Missing upstream producers remain NULL with an explicit reason.
    """
    context = rule_context
    bazi_section = context.get("bazi") or {}
    strength = context.get("strength") or {}
    useful = context.get("useful_god") or {}
    month = context.get("month") or {}
    wuxing = context.get("wuxing") or {}
    pattern_section = dict(context.get("pattern") or {})
    ten_gods = context.get("ten_gods") or {}
    hidden = context.get("hidden_stems") or {}
    luck = dict(context.get("luck") or {})
    temperature = dict(context.get("temperature") or {})
    special = dict(context.get("special") or {})

    day_master = bazi_section.get("day_master")
    than = day_master_element(str(day_master)) if day_master else ""
    level = str(strength.get("level") or "unknown")
    than_vuong = STRENGTH_LEVEL_LABELS.get(level, "")
    if not than_vuong:
        than_vuong = str(month.get("status") or "").strip()

    pattern_code = pattern_section.get("main_pattern") or getattr(
        pattern, "pattern", None
    )
    follow_hint = (
        getattr(pattern, "follow_type", None)
        if pattern is not None
        else None
    ) or pattern_section.get("follow_type")
    override = classify_pattern_override(pattern_code, follow_hint)
    cach_cuc = pattern_display_label(
        pattern_code,
        getattr(pattern, "description", None) if pattern is not None else None,
        ug_override_eligible=override.ug_override_eligible,
    )
    follow = canonicalize_follow_token(pattern_section.get("follow_type"))
    # Tổng cách: follow display when present; otherwise standard cách cục label.
    tong_cach = follow_display_label(follow) or cach_cuc

    dung_than = str(useful.get("name") or useful.get("useful_god") or "").strip()
    hy_src = useful.get("favorable_gods") or useful.get("favorable") or []
    ky_src = useful.get("unfavorable_gods") or useful.get("unfavorable") or []
    hy_than = ", ".join(str(x) for x in hy_src if x)
    ky_than = ", ".join(str(x) for x in ky_src if x)
    # Điều hậu: month/season producer (not temperature — separate temperature_state).
    dieu_hau = str(month.get("status") or "").strip()
    if not dieu_hau:
        dieu_hau = str(
            wuxing.get("season_status") or wuxing.get("season") or ""
        ).strip()

    context["than"] = than or None
    context["than_vuong_nhuoc"] = than_vuong or None
    context["dung_than"] = dung_than or None
    context["hy_than"] = hy_than or None
    context["ky_than"] = ky_than or None
    context["dieu_hau"] = dieu_hau or None
    context["tong_cach"] = tong_cach or None

    # Useful-god aliases already produced in Builder — surface at top level once.
    context["than_status"] = useful.get("than_status") or useful.get("status")
    context["support_elements"] = list(
        useful.get("support_elements")
        or useful.get("favorable_gods")
        or useful.get("favorable")
        or []
    )
    context["avoid_elements"] = list(
        useful.get("avoid_elements")
        or useful.get("unfavorable_gods")
        or useful.get("unfavorable")
        or []
    )

    context["season"] = {
        "name": wuxing.get("season"),
        "status": wuxing.get("season_status") or month.get("status"),
        "month_branch": month.get("branch"),
        "solar_month": month.get("solar_month"),
    }
    context["element_balance"] = {
        "status": wuxing.get("status"),
        "counts": dict(wuxing.get("counts") or {}),
        "by_element": {
            element: dict(wuxing.get(element) or {})
            for element in ("wood", "fire", "earth", "metal", "water")
        },
    }
    context["ten_god_summary"] = {
        "items": list(ten_gods.get("items") or []),
        "unique": ten_gods.get("unique"),
        "status": ten_gods.get("status"),
        "month_commander_ten_god": ten_gods.get("month_commander_ten_god"),
    }
    context["hidden_stem_summary"] = {
        "count": hidden.get("count"),
        "flat": list(hidden.get("flat") or []),
        "status": hidden.get("status"),
    }

    clash_count = pattern_section.get("clash_count")
    combination_status = pattern_section.get("combination_status")
    clash_status = pattern_section.get("clash_status")
    relation_available = (
        clash_count is not None
        or combination_status is not None
        or clash_status is not None
    )
    context["branch_relation_summary"] = {
        "clash_count": clash_count,
        "clash_status": clash_status,
        "combination_status": combination_status,
        "available": relation_available,
        "reason": (
            None
            if relation_available
            else "missing_upstream_branch_relation_producer"
        ),
        "relations": {key: None for key in _RELATION_KEYS},
    }

    pattern_quality = pattern_section.get("pattern_quality")
    context["pattern_quality"] = pattern_quality  # NULL until Pattern Engine sets it
    context["pattern_metadata"] = {
        "main_pattern": pattern_section.get("main_pattern"),
        "cach_cuc": cach_cuc,
        "score": pattern_section.get("score"),
        "priority": pattern_section.get("priority"),
        "matched_rules": list(pattern_section.get("matched_rules") or []),
        "follow_type": follow,
        "pattern_rank": pattern_section.get("pattern_rank"),
        "pattern_quality": pattern_quality,
        "combination_status": combination_status,
        "clash_status": clash_status,
        "success": pattern_section.get("success"),
        "status": pattern_section.get("status"),
        "success_reason": pattern_section.get("success_reason"),
        "failure_reason": pattern_section.get("failure_reason"),
    }
    pattern_section["tong_cach"] = tong_cach
    pattern_section["cach_cuc"] = cach_cuc
    context["pattern"] = pattern_section

    combination = context.get("combination")
    if not isinstance(combination, dict):
        combination = {}
    combination_available = bool(
        combination.get("available")
        or combination_status
        or any(combination.get(key) for key in _RELATION_KEYS)
    )
    combination_payload = {
        "available": combination_available,
        "status": combination.get("status") or combination_status,
        "reason": (
            None
            if combination_available
            else "missing_upstream_combination_producer"
        ),
    }
    for key in _RELATION_KEYS:
        combination_payload[key] = combination.get(key)
    context["combination"] = combination_payload
    # Summaries only — no strength/effect math when producer is absent.
    context["combination_summary"] = {
        "available": combination_available,
        "status": combination_payload["status"],
        "reason": combination_payload["reason"],
        "relations": {key: combination_payload.get(key) for key in _RELATION_KEYS},
    }
    context["combination_strength"] = (
        combination.get("strength") if combination_available else None
    )
    context["combination_effect"] = (
        combination.get("effect") if combination_available else None
    )

    # Temperature: publish existing Builder section; no new climate math.
    context["temperature"] = temperature
    context["temperature_state"] = temperature.get("status") or temperature.get(
        "result"
    )
    context["temperature_comment"] = temperature.get("comment")  # NULL if absent
    context["temperature_summary"] = {
        "state": context["temperature_state"],
        "status": temperature.get("status"),
        "result": temperature.get("result"),
        "profile": temperature.get("profile"),
        "index": temperature.get("index"),
        "cold_score": temperature.get("cold_score"),
        "hot_score": temperature.get("hot_score"),
        "humidity": temperature.get("humidity"),
        "climate_pattern": temperature.get("climate_pattern"),
        "comment": temperature.get("comment"),
        "available": temperature.get("status") is not None
        or temperature.get("cold_score") is not None,
        "reason": (
            None
            if (
                temperature.get("status") is not None
                or temperature.get("cold_score") is not None
            )
            else "missing_upstream_temperature_producer"
        ),
    }

    case_name = special.get("case_name")
    # Prefer follow_type already published on pattern (same producer).
    if not case_name and follow:
        case_name = follow
        special = {
            "case_name": follow,
            "source": "follow_type",
            "available": True,
        }
    context["special_case"] = special if special else {"case_name": None}
    context["special_case_summary"] = (
        {
            "case_name": case_name,
            "available": True,
            "source": special.get("source") or "follow_type",
        }
        if case_name
        else {
            "case_name": None,
            "available": False,
            "reason": "missing_upstream_special_case_producer",
        }
    )

    # Pattern confidence: no PatternEngine producer — keep explicit null.
    context["pattern_confidence"] = pattern_section.get("pattern_confidence")

    luck.setdefault("available", bool(luck.get("pillars")))
    if not luck.get("available"):
        luck.setdefault("reason", "missing_upstream_luck_producer")
    context["luck"] = luck

    context["score_inputs"] = {
        "has_wuxing": bool(wuxing),
        "has_strength": bool(strength),
        "has_pattern": bool(pattern_section.get("main_pattern")),
        "has_ten_gods": bool(ten_gods.get("items")),
        "has_useful_god": bool(useful.get("name")),
        "has_shensha": bool((context.get("shensha") or {}).get("stars")),
        "luck_available": bool(luck.get("available")),
        "temperature_status": temperature.get("status"),
        "strength_level": strength.get("level"),
        "wuxing_status": wuxing.get("status"),
        "season_status": wuxing.get("season_status"),
    }
    return context


def enrich_result_from_rule_context(result: Any, rule_context: dict[str, Any]) -> None:
    """Populate PatternResult view fields from RuleContext signals."""
    # Ensure summaries exist (idempotent).
    if "tong_cach" not in rule_context or "than" not in rule_context:
        enrich_rule_context_summaries(rule_context, pattern=result)

    result.than = str(rule_context.get("than") or "").strip()
    result.than_vuong_nhuoc = str(rule_context.get("than_vuong_nhuoc") or "").strip()
    result.cach_cuc = str(
        (rule_context.get("pattern_metadata") or {}).get("cach_cuc")
        or pattern_display_label(
            getattr(result, "pattern", None),
            getattr(result, "description", None),
            ug_override_eligible=getattr(result, "ug_override_eligible", None),
        )
    ).strip()
    result.tong_cach = str(rule_context.get("tong_cach") or "").strip()
    result.dung_than = str(rule_context.get("dung_than") or "").strip()
    result.hy_than = str(rule_context.get("hy_than") or "").strip()
    result.ky_than = str(rule_context.get("ky_than") or "").strip()
    result.dieu_hau = str(rule_context.get("dieu_hau") or "").strip()
    result.rule_context = rule_context
