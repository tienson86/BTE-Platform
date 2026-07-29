"""Adapters between UnifiedAnalysisContext and RuleContext."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from engines.rule_contract import RuleContextBuilder

from .models import UnifiedAnalysisContext


def adapt_useful_god_payload(unified: UnifiedAnalysisContext) -> dict[str, Any]:
    """Map unified useful_god section to RuleContextBuilder payload."""
    ug = unified.useful_god
    status = "PRESENT" if ug.primary else None
    return {
        "status": status,
        "name": ug.primary or None,
        "favorable": list(ug.favorable),
        "unfavorable": list(ug.unfavorable),
        "score": float(ug.confidence),
        "than_status": status,
        "support_elements": list(ug.favorable),
        "avoid_elements": list(ug.unfavorable),
    }


def adapt_temperature_payload(unified: UnifiedAnalysisContext) -> dict[str, Any]:
    """Map unified temperature section to RuleContextBuilder temperature payload."""
    temp = unified.temperature
    status = temp.type or temp.level or "warm"
    return {
        "status": status,
        "result": status,
        "profile": temp.level,
        "index": temp.score,
        "cold_score": temp.cold_score,
        "hot_score": temp.warm_score,
        "dry_score": temp.dry_score,
        "damp_score": temp.humid_score,
        "humidity": temp.humid_score,
        "comment": temp.reasoning or None,
    }


def adapt_strength_overlay(unified: UnifiedAnalysisContext) -> dict[str, Any]:
    """Map unified strength section to RuleContext strength namespace."""
    s = unified.strength
    return {
        "level": s.level,
        "score": s.score,
        "season_score": s.season_score,
        "root_score": s.root_score,
        "support_score": s.support_score,
        "drain_score": s.drain_score,
        "control_score": s.control_score,
        "confidence": s.confidence,
        "matched_rules": list(s.matched_rules),
        "reasoning": s.reasoning,
        "source": "strength_engine_v2",
        "success": s.success,
    }


def adapt_pattern_overlay(unified: UnifiedAnalysisContext) -> dict[str, Any]:
    """Partial pattern overlay for RuleContext pattern section."""
    p = unified.pattern
    return {
        "main_pattern": p.main or p.main_pattern,
        "name": p.name or p.main,
        "follow_type": p.follow or p.follow_type,
        "score": p.score,
        "priority": p.priority,
        "matched_rules": list(p.matched_rules),
        "success": p.success,
        "description": p.description,
    }


def to_rule_context(
    unified: UnifiedAnalysisContext,
    *,
    calendar: Any = None,
    bazi: Any = None,
    pattern: Any = None,
    score: Any = None,
    luck: Any = None,
    shensha: Any = None,
) -> dict[str, Any]:
    """
    Convert UnifiedAnalysisContext to RuleContext dict.

    Uses RuleContextBuilder for derived namespaces, then overlays V2 engine SSOT
    fields from unified context without changing engine logic.
    """
    builder = RuleContextBuilder()
    context = builder.build(
        calendar=calendar,
        bazi=bazi,
        pattern=pattern,
        score=score,
        luck=luck,
        shensha=shensha,
        useful_god=adapt_useful_god_payload(unified),
        temperature=adapt_temperature_payload(unified),
        metadata={
            "unified_context_version": unified.metadata.schema_version,
            "unified_context_contract": unified.metadata.contract,
        },
    )

    strength_overlay = adapt_strength_overlay(unified)
    context["strength"] = {**context.get("strength", {}), **strength_overlay}
    context["root"] = {
        "level": context["strength"].get("root_level"),
        "status": context["strength"].get("root_level"),
    }
    context["support"] = {
        "type": context["strength"].get("support_type"),
        "status": context["strength"].get("support_type"),
    }
    context["control"] = {
        "type": context["strength"].get("control_type"),
        "status": context["strength"].get("control_type"),
    }

    pattern_overlay = adapt_pattern_overlay(unified)
    existing_pattern = dict(context.get("pattern") or {})
    existing_pattern.update({k: v for k, v in pattern_overlay.items() if v is not None})
    context["pattern"] = existing_pattern

    context["strength_score"] = unified.strength.score
    context["temperature_type"] = unified.temperature.type

    context["unified_context"] = unified.to_dict()
    context["metadata"] = {
        **dict(context.get("metadata") or {}),
        "trace": [asdict(entry) for entry in unified.metadata.trace],
        "validation": unified.metadata.validation,
    }
    return context
