"""Customer-safe compact Life Optimization. No IDs, traces, or hashes."""

from __future__ import annotations

from typing import Any

from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.life_optimization.constants import (
    ELEMENT_FUNCTIONS,
    FORBIDDEN_CUSTOMER_TOKENS,
    MAIN_OPTIMIZATION_IDS,
)
from engines.detailed_interpretation_engine.life_optimization.labels import (
    ACTION_LABELS,
    ACTION_TYPE_LABELS,
    CAUTION_LABELS,
    CONFLICT_LABELS,
    DOMAIN_TITLES,
    EFFECT_LABELS,
    ELEMENT_DIRECTION_LABELS,
    FUNCTION_LABELS,
    GROUP_LABELS,
    PRIORITY_RANK_LABELS,
    REASON_LABELS,
    SCOPE_LABELS,
    TITLE,
)
from engines.detailed_interpretation_engine.life_optimization.models import (
    DomainOptimizationPlan,
    OptimizationAction,
)
from engines.detailed_interpretation_engine.optimization import LifeOptimizationResult

_LEAK = ("TR-P7-", "E-DI-", "E-OPT-", "DI-18-", "mingju", "0x", "opt.conflict.")


def present_life_optimization_customer(result: LifeOptimizationResult) -> dict[str, Any]:
    """Compact Action Plan for the existing consulting card."""
    if result.state in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        return {}
    if not result.actions:
        return {}
    by_id = {item.action_id: item for item in result.actions}
    top = [_priority_item(index, by_id[action_id]) for index, action_id in enumerate(result.top_priorities, start=1) if action_id in by_id]
    natal_items = [_action_item(item) for item in result.actions if item.time_scope == "natal_long_term"]
    temporal_items = [_action_item(item) for item in result.actions if item.time_scope != "natal_long_term"]
    payload = {
        "title": TITLE,
        "top_priorities": top,
        "groups": {
            "develop": _group(result.actions, {"strengthen", "develop", "support", "convert"}),
            "improve": _group(result.actions, {"stabilize", "retain", "recover"}),
            "control": _group(result.actions, {"protect", "reduce"}),
            "avoid": _group(result.actions, {"avoid"}),
            "temporal": temporal_items,
        },
        "natal": {
            "title": SCOPE_LABELS["natal_long_term"],
            "items": natal_items,
        },
        "temporal": {
            "title": _temporal_title(result),
            "year": result.temporal_plan.annual_window,
            "luck_window": result.temporal_plan.luck_window,
            "items": temporal_items,
        },
        "domains": [
            _domain_item(result.domain_plans[domain_id], result)
            for domain_id in MAIN_OPTIMIZATION_IDS
            if domain_id in result.domain_plans
            and result.domain_plans[domain_id].state is EvaluationStatus.RESOLVED
        ],
        "conflicts": [_conflict_item(item) for item in result.conflicts],
        "useful_god": _useful_item(result),
        "elements": [_element_item(item) for item in result.element_plan],
    }
    dump = str(payload).lower()
    for token in FORBIDDEN_CUSTOMER_TOKENS:
        if token in dump:
            payload["warnings"] = ["safety_filter"]
    if any(token in dump for token in _LEAK):
        payload = _strip_leak(payload)
    return payload


def _temporal_title(result: LifeOptimizationResult) -> str:
    year = result.temporal_plan.annual_window
    if year:
        return f"{SCOPE_LABELS['current_luck_cycle']} / Năm {year}"
    return SCOPE_LABELS["current_luck_cycle"]


def _priority_item(rank: int, action: OptimizationAction) -> dict[str, Any]:
    return {
        "rank": rank,
        "label": PRIORITY_RANK_LABELS.get(rank, f"Ưu tiên {rank}"),
        "domain": DOMAIN_TITLES.get(action.target_domain, action.target_domain),
        "title": _action_title(action),
        "reason": REASON_LABELS.get(action.reason_key, ""),
        "action": ACTION_TYPE_LABELS.get(action.action_type, action.action_type),
        "scope": SCOPE_LABELS.get(action.time_scope, ""),
        "priority": action.priority,
    }


def _action_item(action: OptimizationAction) -> dict[str, Any]:
    return {
        "domain": DOMAIN_TITLES.get(action.target_domain, action.target_domain),
        "title": _action_title(action),
        "reason": REASON_LABELS.get(action.reason_key, ""),
        "action": ACTION_TYPE_LABELS.get(action.action_type, action.action_type),
        "effect": EFFECT_LABELS.get(action.expected_structural_effect, ""),
        "scope": SCOPE_LABELS.get(action.time_scope, ""),
        "condition": _conditions(action.conditions),
        "caution": _cautions(action),
        "priority": action.priority,
        "group": _group_key(action),
    }


def _domain_item(plan: DomainOptimizationPlan, result: LifeOptimizationResult) -> dict[str, Any]:
    by_id = {item.action_id: item for item in result.actions}
    recommended = next((by_id[item] for item in plan.recommended_actions if item in by_id), None)
    avoid = next((by_id[item] for item in plan.avoid_actions if item in by_id), None)
    temporal = next((by_id[item] for item in plan.temporal_adjustments if item in by_id), None)
    primary = recommended or temporal
    return {
        "id": plan.domain,
        "title": DOMAIN_TITLES.get(plan.domain, plan.domain),
        "target": _action_title(recommended) if recommended else plan.bottleneck or _action_title(temporal),
        "driver": plan.driver,
        "bottleneck": plan.bottleneck,
        "leakage": plan.leakage,
        "why": REASON_LABELS.get(primary.reason_key, "") if primary else "",
        "action": _action_title(primary) if primary else "",
        "condition": _conditions(plan.conditions) or (_conditions(primary.conditions) if primary else ""),
        "caution": _action_title(avoid) if avoid else "",
        "temporal": _action_title(temporal) if temporal else "",
        "conversion": plan.conversion_efficiency.bottleneck or plan.conversion_efficiency.efficiency,
        "priority": plan.priority,
    }


def _conflict_item(conflict: Any) -> dict[str, Any]:
    key = conflict.conflict_id.replace("opt.conflict.", "")
    return {
        "title": CONFLICT_LABELS.get(key, "Cần cân bằng giữa hai hướng"),
        "domains": " · ".join(DOMAIN_TITLES.get(item, item) for item in conflict.domains),
        "resolution": "Giữ cả hai điều kiện, không chọn một bên im lặng",
        "condition": _conditions(conflict.conditions),
        "severity": conflict.severity,
    }


def _useful_item(result: LifeOptimizationResult) -> dict[str, Any]:
    plan = result.useful_god_plan
    if not plan.useful_god and not plan.functional_targets:
        return {}
    return {
        "element": plan.useful_god,
        "functions": [FUNCTION_LABELS.get(item, item) for item in plan.functional_targets],
        "domains": [DOMAIN_TITLES.get(item, item) for item in plan.domain_mappings],
        "reason": REASON_LABELS["useful_god.function"],
        "avoidance": "Kỵ là ngữ cảnh hạn chế khuếch đại, không cấm tuyệt đối"
        if plan.avoidance_context
        else "",
    }


def _element_item(plan: Any) -> dict[str, Any]:
    return {
        "element": plan.element,
        "function": ", ".join(
            FUNCTION_LABELS.get(item, item) for item in ELEMENT_FUNCTIONS.get(plan.element, ())
        ),
        "direction": ELEMENT_DIRECTION_LABELS.get(plan.action_direction, plan.action_direction),
        "role": plan.desired_role,
        "domains": [DOMAIN_TITLES.get(item, item) for item in plan.target_domains],
        "reason": REASON_LABELS.get(
            "ky.not_ban" if plan.current_role == "ky_context" else "element.function_support",
            "",
        ),
    }


def _group(actions: tuple[OptimizationAction, ...], types: set[str]) -> list[dict[str, Any]]:
    return [_action_item(item) for item in actions if item.action_type in types]


def _group_key(action: OptimizationAction) -> str:
    if action.time_scope != "natal_long_term":
        return "temporal"
    if action.action_type in {"strengthen", "develop", "support", "convert"}:
        return "develop"
    if action.action_type in {"stabilize", "retain", "recover"}:
        return "improve"
    if action.action_type in {"protect", "reduce"}:
        return "control"
    if action.action_type == "avoid":
        return "avoid"
    return "improve"


def _action_title(action: OptimizationAction | None) -> str:
    if action is None:
        return ""
    return ACTION_LABELS.get(action.recommended_action_key or action.action_id.split(".")[0], "") or ACTION_TYPE_LABELS.get(
        action.action_type, ""
    )


def _conditions(values: tuple[str, ...]) -> str:
    labels = [CAUTION_LABELS.get(item, "") for item in values]
    return " · ".join(item for item in labels if item)


def _cautions(action: OptimizationAction) -> str:
    keys = [item.reason_key for item in action.contraindications] + list(action.conditions)
    labels = [CAUTION_LABELS.get(item, "") for item in keys]
    return " · ".join(item for item in labels if item)


def _strip_leak(payload: Any) -> Any:
    if isinstance(payload, dict):
        return {key: _strip_leak(value) for key, value in payload.items() if key != "id"}
    if isinstance(payload, list):
        return [_strip_leak(item) for item in payload]
    if isinstance(payload, str) and any(token in payload for token in _LEAK):
        return ""
    return payload


def group_heading(key: str) -> str:
    """Customer group heading."""
    return GROUP_LABELS.get(key, key)
