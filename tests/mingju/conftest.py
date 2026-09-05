"""Shared MC-01 test fixtures. No CASE-0001 expected conclusions."""

from __future__ import annotations

from typing import Any

from engines.mingju import build_mingju_context


def visible(pillar: str, god_id: str, ten_god: str, stem: str = "Giáp") -> dict[str, str]:
    return {"pillar": pillar, "god_id": god_id, "ten_god": ten_god, "stem": stem, "element": ""}


def hidden(
    pillar: str,
    god_id: str,
    ten_god: str,
    position_name: str = "tertiary",
) -> dict[str, str]:
    return {
        "pillar": pillar,
        "god_id": god_id,
        "ten_god": ten_god,
        "position_name": position_name,
        "hidden_stem": "Ất",
        "element": "",
    }


def base_payload(**overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "analysis_id": "an-mc01-test-001",
        "chart_id": "1987-01-21",
        "pattern": {
            "success": True,
            "pattern": "chinh_an",
            "cach_cuc": "Chính Ấn",
            "month_branch": "Sửu",
            "month_main_qi": "Kỷ",
            "month_main_qi_ten_god": "Chính Ấn",
            "day_master": "Canh",
        },
        "strength": {"strength_level": "balanced", "strength_score": 52.0},
        "useful_god": {"useful_display": "Hỏa", "useful_ten_god": "Thực Thần", "useful_element": "Hỏa"},
        "temperature": {"climate_state": "warm"},
        "five_elements": {"wood": {"count": 1}},
        "ten_gods": {
            "visible": [
                visible("month", "zheng_yin", "Chính Ấn", "Ất"),
                visible("hour", "zheng_yin", "Chính Ấn", "Đinh"),
            ],
            "hidden": [hidden("month", "zheng_yin", "Chính Ấn", "primary")],
        },
        "identity": {
            "person": {"solar_birth": "1987-01-21"},
            "four_pillars": {"hour": {"stem": "Đinh", "branch": "Mão"}},
        },
        "bazi": {"day_master": "Canh", "hour_pillar": {"stem": "Đinh", "branch": "Mão"}},
    }
    payload.update(overrides)
    return payload


def context_from(**overrides: Any):
    return build_mingju_context(payload=base_payload(**overrides))
