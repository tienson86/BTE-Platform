"""Combination strength stage."""

from __future__ import annotations

from typing import Any

from . import run_rule_stage


def run_combination_stage(
    context: Any,
    rules: list[dict[str, Any]],
    matcher: Any,
) -> list[dict[str, Any]]:
    """Match combination (hợp hóa) rules."""
    matches = run_rule_stage(context, rules, matcher, "combination")
    day_element = str(getattr(context, "day_master_element", "") or "")
    produces = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
    controls = {"Mộc": "Thổ", "Hỏa": "Kim", "Thổ": "Thủy", "Kim": "Mộc", "Thủy": "Hỏa"}

    for index, combination in enumerate(
        getattr(context, "branch_combinations", []) or [], start=1
    ):
        element = str(combination.get("element") or "")
        transformed = bool(combination.get("transformed"))
        if element == day_element:
            score = 18 if transformed else 10
            relation = "đồng hành trợ thân"
        elif produces.get(element) == day_element:
            score = 16 if transformed else 8
            relation = "sinh trợ Nhật chủ"
        elif produces.get(day_element) == element:
            score = -12 if transformed else -6
            relation = "tiết khí Nhật chủ"
        elif controls.get(day_element) == element:
            score = -10 if transformed else -5
            relation = "hao thân sinh Tài"
        elif controls.get(element) == day_element:
            score = -14 if transformed else -7
            relation = "khắc chế Nhật chủ"
        else:
            continue
        label = "Tam hội" if combination.get("kind") == "tam_hoi" else "Tam hợp"
        branches = "-".join(combination.get("branches") or [])
        matches.append(
            {
                "rule_id": f"auto_full_combination_{index}",
                "rule_group": "combination",
                "score_target": "combination",
                "priority": 98,
                "score": score,
                "reason": f"{label} {branches} thành thế {element}",
                "description": f"{combination.get('reason')}; {relation}",
                "status": "active",
                "enabled": True,
            }
        )
    return matches
