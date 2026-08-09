"""Build KX-1A Strength Core package artifacts. Run once, then delete."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PKG_ID = "bz_01_strength_core"
CREATED = "2026-08-09T14:00:00Z"
ZERO_HEX = "0" * 64

REF_SEASON = {"target": "REF-SKC-000001", "relation": "references"}
REF_ROOT = {"target": "REF-SKC-000002", "relation": "references"}
REF_HIDDEN = {"target": "REF-SKC-000003", "relation": "references"}
REF_STEM = {"target": "REF-SKC-000004", "relation": "references"}
REF_TG = {"target": "REF-SKC-000005", "relation": "references"}
REF_SCORE = {"target": "REF-SKC-000006", "relation": "references"}
REF_DOM = {"target": "REF-SKC-000007", "relation": "references"}
REF_LEVEL = {"target": "REF-SKC-000008", "relation": "references"}


def rule(
    n: int,
    *,
    category: str,
    code: str,
    name: str,
    tags: list[str],
    level: str,
    order: int,
    conditions: list[dict],
    result: dict,
    explanation: str,
    refs: list[dict],
    exclusive: bool = False,
    stackable: bool = False,
    max_stack: int = 1,
    group: str | None = None,
) -> dict:
    rid = f"SKC-{n:06d}"
    evaluation = {
        "weight": result.get("weight", 0),
        "stackable": stackable,
        "max_stack": max_stack,
        "exclusive": exclusive,
        "group": group,
    }
    return {
        "id": rid,
        "version": "1.0.0",
        "category": category,
        "type": "rule",
        "status": "official",
        "enabled": True,
        "language": "vi",
        "tags": tags,
        "priority": {"level": level, "order": order},
        "conditions": conditions,
        "result": result,
        "explanation": explanation,
        "references": refs,
        "code": code,
        "name": name,
        "metadata": {
            "package_id": PKG_ID,
            "domain_id": "DOM-STRENGTH",
            "school": "bazi_default",
            "author": "BTE Knowledge Board",
        },
        "payload": {
            "conditions": conditions,
            "result": result,
            "explanation": explanation,
            "evaluation": evaluation,
            "target": {"role": "day_master", "attribute": "strength_score"},
        },
    }


def cond(field: str, operator: str, value: object) -> dict:
    return {"field": field, "operator": operator, "value": value}


def score_result(effect: str, weight: int, signal: str | None = None, level: str | None = None) -> dict:
    out: dict = {"effect": effect, "weight": weight, "score_target": "day_master.strength_score"}
    if signal:
        out["signal"] = signal
    if level:
        out["strength_level"] = level
    return out


def build_rules() -> list[dict]:
    rules: list[dict] = []
    n = 1

    def add(**kwargs: object) -> None:
        nonlocal n
        rules.append(rule(n, **kwargs))  # type: ignore[arg-type]
        n += 1

    # --- seasonal influence: 5 status + 20 element x season = 25 ---
    season_status = [
        ("prosperous", "Đắc lệnh", 35, 100, "Tháng lệnh vượng (đắc lệnh) cộng sức Nhật Chủ."),
        ("growing", "Tướng", 25, 95, "Tháng lệnh tướng: hành Nhật Chủ được sinh hoặc đang vượng phụ."),
        ("rest", "Hưu", 10, 90, "Tháng lệnh hưu: mẹ khí nghỉ, sức Nhật Chủ trung bình thấp."),
        ("imprison", "Tù", -10, 95, "Tháng lệnh tù: Nhật Chủ bị hành tháng chế ước."),
        ("dead", "Tử", -25, 100, "Tháng lệnh tử: Nhật Chủ bị hành tháng khắc, sức yếu."),
    ]
    for status, label, weight, order, expl in season_status:
        add(
            category="seasonal_influence",
            code=f"season_{status}",
            name=f"Tháng lệnh {label}",
            tags=["strength", "season", status],
            level="high",
            order=order,
            conditions=[cond("month_status", "equals", status)],
            result=score_result(f"month_status={status}", weight, signal="month_command_score"),
            explanation=expl,
            refs=[REF_SEASON, REF_SCORE, REF_DOM],
            exclusive=True,
            group="month_status",
        )

    element_season = [
        ("wood", "spring", "prosperous", "Mộc vượng mùa xuân (Dần Mão)."),
        ("wood", "summer", "rest", "Mộc hưu mùa hạ vì sinh Hỏa."),
        ("wood", "autumn", "dead", "Mộc tử mùa thu vì Kim khắc Mộc."),
        ("wood", "winter", "growing", "Mộc tướng mùa đông vì Thủy sinh Mộc."),
        ("fire", "spring", "growing", "Hỏa tướng mùa xuân vì Mộc sinh Hỏa."),
        ("fire", "summer", "prosperous", "Hỏa vượng mùa hạ (Tỵ Ngọ)."),
        ("fire", "autumn", "dead", "Hỏa tử mùa thu vì Hỏa khắc Kim (hành khắc tháng)."),
        ("fire", "winter", "imprison", "Hỏa tù mùa đông vì Thủy khắc Hỏa."),
        ("earth", "spring", "imprison", "Thổ tù mùa xuân vì Mộc khắc Thổ."),
        ("earth", "summer", "growing", "Thổ tướng mùa hạ vì Hỏa sinh Thổ."),
        ("earth", "autumn", "rest", "Thổ hưu mùa thu vì sinh Kim."),
        ("earth", "winter", "dead", "Thổ tử mùa đông vì Thổ khắc Thủy (hành khắc tháng)."),
        ("metal", "spring", "dead", "Kim tử mùa xuân vì Mộc vượng chế Kim."),
        ("metal", "summer", "imprison", "Kim tù mùa hạ vì Hỏa khắc Kim."),
        ("metal", "autumn", "prosperous", "Kim vượng mùa thu (Thân Dậu)."),
        ("metal", "winter", "rest", "Kim hưu mùa đông vì sinh Thủy."),
        ("water", "spring", "rest", "Thủy hưu mùa xuân vì sinh Mộc."),
        ("water", "summer", "dead", "Thủy tử mùa hạ vì Hỏa vượng, Thủy khắc Hỏa."),
        ("water", "autumn", "growing", "Thủy tướng mùa thu vì Kim sinh Thủy."),
        ("water", "winter", "prosperous", "Thủy vượng mùa đông (Hợi Tý)."),
    ]
    for element, season, status, expl in element_season:
        add(
            category="seasonal_influence",
            code=f"dm_{element}_{season}_{status}",
            name=f"Nhật Chủ {element} mùa {season} → {status}",
            tags=["strength", "season", element, season, status],
            level="high",
            order=92,
            conditions=[
                cond("day_master_element", "equals", element),
                cond("season", "equals", season),
            ],
            result={
                "effect": f"infer_month_status={status}",
                "weight": 0,
                "signal": "month_status",
                "inferred_month_status": status,
                "score_target": "day_master.strength_score",
            },
            explanation=expl + " Quy chiếu 旺相休囚死; trọng số điểm lấy từ nhóm month_status.",
            refs=[REF_SEASON, REF_DOM],
            exclusive=True,
            group=f"element_season_{element}",
        )

    # --- month branch influence: 15 ---
    commands = [
        ("dan", "wood", "Dần"),
        ("mao", "wood", "Mão"),
        ("si", "fire", "Tỵ"),
        ("ngo", "fire", "Ngọ"),
        ("than", "metal", "Thân"),
        ("dau", "metal", "Dậu"),
        ("hoi", "water", "Hợi"),
        ("ty", "water", "Tý"),
        ("thin", "earth", "Thìn"),
        ("suu", "earth", "Sửu"),
        ("mui", "earth", "Mùi"),
        ("tuat", "earth", "Tuất"),
    ]
    for branch, element, label in commands:
        add(
            category="month_branch_influence",
            code=f"month_command_{branch}",
            name=f"Tháng {label} hành lệnh {element}",
            tags=["strength", "month_branch", branch, element],
            level="high",
            order=90,
            conditions=[cond("month_branch", "equals", branch)],
            result={
                "effect": f"month_command_element={element}",
                "weight": 0,
                "signal": "month_command_element",
                "month_command_element": element,
            },
            explanation=f"Địa chi tháng {label} lấy hành {element} làm tháng lệnh (chính khí).",
            refs=[REF_SEASON, REF_HIDDEN],
            exclusive=True,
            group="month_command_element",
        )

    add(
        category="month_branch_influence",
        code="month_branch_same_element",
        name="Chi tháng đồng hành Nhật Chủ",
        tags=["strength", "month_branch", "companion"],
        level="high",
        order=88,
        conditions=[cond("month_branch_element", "equals_field", "day_master_element")],
        result=score_result("month_branch_same_element", 8, signal="month_branch_support"),
        explanation="Chi tháng cùng ngũ hành Nhật Chủ vừa đắc lệnh vừa thông căn tháng.",
        refs=[REF_SEASON, REF_ROOT],
        stackable=False,
        group="month_branch_relation",
        exclusive=True,
    )
    add(
        category="month_branch_influence",
        code="month_branch_resource",
        name="Chi tháng Ấn sinh Nhật Chủ",
        tags=["strength", "month_branch", "resource"],
        level="high",
        order=87,
        conditions=[cond("month_branch_ten_god_group", "equals", "resource")],
        result=score_result("month_branch_resource", 10, signal="month_branch_support"),
        explanation="Chi tháng thuộc Ấn tinh sinh thân, trợ lực mạnh hơn đồng hành đơn thuần.",
        refs=[REF_TG, REF_SEASON],
        exclusive=True,
        group="month_branch_relation",
    )
    add(
        category="month_branch_influence",
        code="month_branch_output",
        name="Chi tháng Thực Thương tiết thân",
        tags=["strength", "month_branch", "output"],
        level="medium",
        order=86,
        conditions=[cond("month_branch_ten_god_group", "equals", "output")],
        result=score_result("month_branch_output", -8, signal="month_branch_drain"),
        explanation="Chi tháng Thực Thương khiến Nhật Chủ tiết khí theo tháng lệnh.",
        refs=[REF_TG, REF_SCORE],
        exclusive=True,
        group="month_branch_relation",
    )

    # --- root support: 12 ---
    roots = [
        ("root_three_plus", "root_level", "equals", "root_three_plus", 30, 100, "Thông căn từ ba chi trở lên, căn khí rất mạnh."),
        ("root_two", "root_level", "equals", "root_two", 22, 95, "Thông căn hai chi, căn khí mạnh."),
        ("root_one", "root_level", "equals", "root_one", 12, 90, "Thông căn một chi, có căn ổn định."),
        ("hidden_root", "root_level", "equals", "hidden_root", 6, 80, "Chỉ thông căn tàng can, căn khí mỏng."),
        ("no_root", "root_level", "equals", "no_root", -20, 100, "Vô căn: Nhật Chủ không bám địa chi."),
    ]
    for code, field, op, value, weight, order, expl in roots:
        add(
            category="root_support",
            code=code,
            name=code.replace("_", " "),
            tags=["strength", "root", code],
            level="high",
            order=order,
            conditions=[cond(field, op, value)],
            result=score_result(code, weight, signal="root_score"),
            explanation=expl,
            refs=[REF_ROOT, REF_SCORE],
            exclusive=True,
            group="root_level",
        )
    add(
        category="root_support",
        code="day_branch_root",
        name="Thông căn nhật chi",
        tags=["strength", "root", "day_branch"],
        level="high",
        order=88,
        conditions=[cond("day_branch_is_root", "equals", True)],
        result=score_result("day_branch_root", 6, signal="root_seat"),
        explanation="Nhật chi thông căn là chỗ ngồi của Nhật Chủ, trọng số cao hơn niên/thời.",
        refs=[REF_ROOT],
        stackable=True,
        max_stack=1,
    )
    add(
        category="root_support",
        code="year_branch_root",
        name="Thông căn niên chi",
        tags=["strength", "root", "year_branch"],
        level="medium",
        order=82,
        conditions=[cond("year_branch_is_root", "equals", True)],
        result=score_result("year_branch_root", 3, signal="root_seat"),
        explanation="Niên chi thông căn trợ căn xa, trọng số thấp hơn nhật/tháng.",
        refs=[REF_ROOT],
        stackable=True,
        max_stack=1,
    )
    add(
        category="root_support",
        code="hour_branch_root",
        name="Thông căn thời chi",
        tags=["strength", "root", "hour_branch"],
        level="medium",
        order=82,
        conditions=[cond("hour_branch_is_root", "equals", True)],
        result=score_result("hour_branch_root", 3, signal="root_seat"),
        explanation="Thời chi thông căn trợ căn gần, không thay thế nhật chi.",
        refs=[REF_ROOT],
        stackable=True,
        max_stack=1,
    )
    add(
        category="root_support",
        code="month_branch_root",
        name="Thông căn tháng chi",
        tags=["strength", "root", "month_branch"],
        level="high",
        order=89,
        conditions=[cond("month_branch_is_root", "equals", True)],
        result=score_result("month_branch_root", 5, signal="root_seat"),
        explanation="Tháng chi vừa lệnh vừa căn thì thân dễ vượng; không cộng trùng month_status.",
        refs=[REF_ROOT, REF_SEASON],
        stackable=True,
        max_stack=1,
    )
    add(
        category="root_support",
        code="storage_branch_root",
        name="Căn tại chi kho",
        tags=["strength", "root", "storage"],
        level="medium",
        order=78,
        conditions=[
            cond("root_branch_type", "equals", "storage"),
            cond("has_dm_root", "equals", True),
        ],
        result=score_result("storage_branch_root", -2, signal="root_quality"),
        explanation="Căn ở Thìn Tuất Sửu Mùi là căn kho, khí yếu hơn căn vượng/trưởng sinh.",
        refs=[REF_ROOT, REF_HIDDEN],
        stackable=True,
        max_stack=2,
    )
    add(
        category="root_support",
        code="wang_branch_root",
        name="Căn tại chi vượng",
        tags=["strength", "root", "wang"],
        level="high",
        order=84,
        conditions=[
            cond("root_branch_type", "equals", "wang"),
            cond("has_dm_root", "equals", True),
        ],
        result=score_result("wang_branch_root", 4, signal="root_quality"),
        explanation="Căn tại chi đế vượng (Mão/Ngọ/Dậu/Tý tùy hành) căn khí đầy.",
        refs=[REF_ROOT],
        stackable=True,
        max_stack=2,
    )
    add(
        category="root_support",
        code="mixed_branch_not_root",
        name="Chi đồng hiện nhưng khác hành không tính căn",
        tags=["strength", "root", "quality"],
        level="medium",
        order=76,
        conditions=[cond("foreign_element_branch_count", "greater_or_equal", 2)],
        result=score_result("mixed_branch_not_root", 0, signal="root_quality"),
        explanation="Nhiều địa chi khác hành không được đếm là thông căn Nhật Chủ.",
        refs=[REF_ROOT],
    )

    # --- hidden stem: 10 ---
    hidden = [
        ("hidden_main_qi_dm", "hidden_main_qi_is_dm", True, 8, 90, "Chính khí tàng can trùng Nhật Chủ, căn tàng mạnh."),
        ("hidden_middle_qi_dm", "hidden_middle_qi_is_dm", True, 4, 82, "Trung khí tàng can trùng Nhật Chủ, căn vừa."),
        ("hidden_residual_qi_dm", "hidden_residual_qi_is_dm", True, 2, 75, "Dư khí tàng can trùng Nhật Chủ, căn mỏng."),
        ("hidden_resource", "hidden_stem_has_resource", True, 5, 85, "Tàng can Ấn sinh thân."),
        ("hidden_officer", "hidden_stem_has_officer", True, -4, 84, "Tàng can Quan Sát khắc thân."),
        ("hidden_output", "hidden_stem_has_output", True, -3, 80, "Tàng can Thực Thương tiết thân."),
        ("hidden_wealth", "hidden_stem_has_wealth", True, -2, 78, "Tàng can Tài hao thân."),
    ]
    for code, field, value, weight, order, expl in hidden:
        add(
            category="hidden_stem_support",
            code=code,
            name=code.replace("_", " "),
            tags=["strength", "hidden_stem", code],
            level="high" if weight >= 5 or weight <= -4 else "medium",
            order=order,
            conditions=[cond(field, "equals", value)],
            result=score_result(code, weight, signal="hidden_stem_score"),
            explanation=expl,
            refs=[REF_HIDDEN, REF_TG],
            stackable=True,
            max_stack=4,
        )
    add(
        category="hidden_stem_support",
        code="hidden_exposed",
        name="Tàng can透出",
        tags=["strength", "hidden_stem", "exposed"],
        level="high",
        order=88,
        conditions=[cond("hidden_dm_qi_exposed_as_stem", "equals", True)],
        result=score_result("hidden_exposed", 6, signal="hidden_stem_score"),
        explanation="Tàng can Nhật Chủ lộ thiên can thì căn được kích hoạt rõ.",
        refs=[REF_HIDDEN, REF_STEM],
        stackable=True,
        max_stack=2,
    )
    add(
        category="hidden_stem_support",
        code="month_hidden_weight",
        name="Tàng can tháng nặng hơn niên thời",
        tags=["strength", "hidden_stem", "month"],
        level="high",
        order=86,
        conditions=[cond("month_hidden_qi_is_dm", "equals", True)],
        result=score_result("month_hidden_dm", 4, signal="hidden_stem_score"),
        explanation="Tàng can tháng gần lệnh, trọng số cao hơn tàng can niên/thời.",
        refs=[REF_HIDDEN, REF_SEASON],
        stackable=True,
        max_stack=1,
    )
    add(
        category="hidden_stem_support",
        code="multiple_hidden_dm",
        name="Nhiều tàng can Nhật Chủ",
        tags=["strength", "hidden_stem", "stack"],
        level="medium",
        order=80,
        conditions=[cond("hidden_dm_qi_count", "greater_or_equal", 2)],
        result=score_result("multiple_hidden_dm", 4, signal="hidden_stem_score"),
        explanation="Hai vị trí tàng can trở lên trùng Nhật Chủ gia tăng căn khí tàng.",
        refs=[REF_HIDDEN],
        stackable=False,
        max_stack=1,
    )

    # --- visible stem: 10 ---
    add(
        category="visible_stem_support",
        code="bijian_stem",
        name="Thiên can Tỷ Kiên",
        tags=["strength", "visible_stem", "companion"],
        level="high",
        order=88,
        conditions=[cond("visible_ten_god_contains", "contains", "bijian")],
        result=score_result("bijian_stem", 6, signal="stem_support"),
        explanation="Can đồng âm dương (Tỷ Kiên) trợ thân trực tiếp.",
        refs=[REF_STEM, REF_TG],
        stackable=True,
        max_stack=3,
    )
    add(
        category="visible_stem_support",
        code="jiecai_stem",
        name="Thiên can Kiếp Tài",
        tags=["strength", "visible_stem", "rob_wealth"],
        level="medium",
        order=86,
        conditions=[cond("visible_ten_god_contains", "contains", "jiecai")],
        result=score_result("jiecai_stem", 5, signal="stem_support"),
        explanation="Can đồng hành khác âm dương (Kiếp Tài) trợ thân nhưng dễ tranh tài.",
        refs=[REF_STEM, REF_TG],
        stackable=True,
        max_stack=3,
    )
    add(
        category="visible_stem_support",
        code="zheng_yin_stem",
        name="Thiên can Chính Ấn",
        tags=["strength", "visible_stem", "resource"],
        level="high",
        order=92,
        conditions=[cond("visible_ten_god_contains", "contains", "zheng_yin")],
        result=score_result("zheng_yin_stem", 10, signal="stem_support"),
        explanation="Chính Ấn sinh thân ôn hòa, trợ lực ổn định.",
        refs=[REF_STEM, REF_TG],
        stackable=True,
        max_stack=3,
    )
    add(
        category="visible_stem_support",
        code="pian_yin_stem",
        name="Thiên can Thiên Ấn",
        tags=["strength", "visible_stem", "resource"],
        level="high",
        order=90,
        conditions=[cond("visible_ten_god_contains", "contains", "pian_yin")],
        result=score_result("pian_yin_stem", 8, signal="stem_support"),
        explanation="Thiên Ấn (Thiên Tài/Thiên Ấn) sinh thân mạnh, dễ thiên lệch.",
        refs=[REF_STEM, REF_TG],
        stackable=True,
        max_stack=3,
    )
    add(
        category="visible_stem_support",
        code="adjacent_stem_support",
        name="Can trợ sát Nhật Chủ",
        tags=["strength", "visible_stem", "proximity"],
        level="medium",
        order=84,
        conditions=[cond("adjacent_stem_supports_dm", "equals", True)],
        result=score_result("adjacent_stem_support", 3, signal="stem_support"),
        explanation="Can tháng hoặc can thời kề Nhật Chủ trợ lực rõ hơn can niên.",
        refs=[REF_STEM],
        stackable=True,
        max_stack=2,
    )
    add(
        category="visible_stem_support",
        code="year_stem_support_weak",
        name="Can niên trợ xa",
        tags=["strength", "visible_stem", "year"],
        level="low",
        order=70,
        conditions=[cond("year_stem_supports_dm", "equals", True)],
        result=score_result("year_stem_support", 2, signal="stem_support"),
        explanation="Can niên trợ thân nhưng lực xa, không bằng can tháng/thời.",
        refs=[REF_STEM],
        stackable=True,
        max_stack=1,
    )
    add(
        category="visible_stem_support",
        code="stem_combo_to_dm",
        name="Hợp hóa thành hành Nhật Chủ",
        tags=["strength", "visible_stem", "combination"],
        level="high",
        order=96,
        conditions=[cond("stem_combination_transforms_to_dm_element", "equals", True)],
        result=score_result("stem_combo_to_dm", 12, signal="stem_support"),
        explanation="Thiên can hợp hóa thành hành Nhật Chủ thì trợ thân mạnh (tối đa 2 lần).",
        refs=[REF_STEM, REF_SCORE],
        stackable=True,
        max_stack=2,
    )
    add(
        category="visible_stem_support",
        code="stem_combo_away_dm",
        name="Hợp hóa mất hành Nhật Chủ",
        tags=["strength", "visible_stem", "combination"],
        level="high",
        order=94,
        conditions=[cond("stem_combination_transforms_dm_away", "equals", True)],
        result=score_result("stem_combo_away_dm", -10, signal="stem_drain"),
        explanation="Nhật Chủ hoặc căn can bị hợp hóa sang hành khác thì mất lực.",
        refs=[REF_STEM, REF_SCORE],
        stackable=True,
        max_stack=2,
    )
    add(
        category="visible_stem_support",
        code="no_visible_support",
        name="Không có can trợ",
        tags=["strength", "visible_stem", "absence"],
        level="medium",
        order=74,
        conditions=[
            cond("visible_companion_count", "equals", 0),
            cond("visible_resource_count", "equals", 0),
        ],
        result=score_result("no_visible_support", -4, signal="stem_support"),
        explanation="Không Tỷ Kiếp/Ấn trên thiên can: thân dựa chủ yếu vào lệnh và căn.",
        refs=[REF_STEM, REF_TG],
    )
    add(
        category="visible_stem_support",
        code="three_companion_stems",
        name="Ba can đồng hành trở lên",
        tags=["strength", "visible_stem", "companion"],
        level="high",
        order=85,
        conditions=[cond("visible_companion_count", "greater_or_equal", 3)],
        result=score_result("three_companion_stems", 6, signal="stem_support"),
        explanation="Nhiều Tỷ Kiếp lộ can: khuynh hướng thân vượng, cần xem tiết chế.",
        refs=[REF_STEM, REF_TG],
        stackable=False,
    )

    # --- element support: 8 ---
    add(
        category="element_support",
        code="same_element_count_1",
        name="Một vị trí đồng hành ngũ hành",
        tags=["strength", "element", "companion"],
        level="medium",
        order=80,
        conditions=[cond("same_element_pillar_count", "equals", 1)],
        result=score_result("same_element_count_1", 4, signal="element_support"),
        explanation="Một trụ đồng hành ngũ hành với Nhật Chủ, trợ vừa phải.",
        refs=[REF_TG, REF_SCORE],
        exclusive=True,
        group="same_element_count",
    )
    add(
        category="element_support",
        code="same_element_count_2",
        name="Hai vị trí đồng hành ngũ hành",
        tags=["strength", "element", "companion"],
        level="high",
        order=82,
        conditions=[cond("same_element_pillar_count", "equals", 2)],
        result=score_result("same_element_count_2", 8, signal="element_support"),
        explanation="Hai trụ đồng hành, lực tỷ kiếp rõ.",
        refs=[REF_TG, REF_SCORE],
        exclusive=True,
        group="same_element_count",
    )
    add(
        category="element_support",
        code="same_element_count_3plus",
        name="Ba vị trí đồng hành ngũ hành trở lên",
        tags=["strength", "element", "companion"],
        level="high",
        order=84,
        conditions=[cond("same_element_pillar_count", "greater_or_equal", 3)],
        result=score_result("same_element_count_3plus", 12, signal="element_support"),
        explanation="Đồng hành ngũ hành áp đảo, thân dễ cực vượng nếu không bị tiết khắc.",
        refs=[REF_TG, REF_SCORE],
        exclusive=True,
        group="same_element_count",
    )
    add(
        category="element_support",
        code="resource_element_present",
        name="Có hành Ấn trong cục",
        tags=["strength", "element", "resource"],
        level="high",
        order=88,
        conditions=[cond("resource_element_present", "equals", True)],
        result=score_result("resource_element_present", 6, signal="element_support"),
        explanation="Hành sinh Nhật Chủ hiện diện thì thân có nguồn sinh.",
        refs=[REF_TG],
        stackable=False,
    )
    add(
        category="element_support",
        code="resource_and_companion",
        name="Ấn và tỷ kiếp cùng hiện",
        tags=["strength", "element", "combination"],
        level="high",
        order=90,
        conditions=[
            cond("companion_count", "greater_or_equal", 2),
            cond("resource_count", "greater_or_equal", 1),
        ],
        result=score_result("resource_and_companion", 12, signal="element_support"),
        explanation="Ấn Kiếp hội tụ: sinh và đồng hành cùng trợ, thân dễ vượng.",
        refs=[REF_TG, REF_SCORE],
        stackable=False,
    )
    add(
        category="element_support",
        code="season_element_is_dm",
        name="Hành tháng trùng Nhật Chủ",
        tags=["strength", "element", "season"],
        level="high",
        order=91,
        conditions=[cond("season_element", "equals_field", "day_master_element")],
        result=score_result("season_element_is_dm", 6, signal="element_support"),
        explanation="Hành lệnh trùng Nhật Chủ củng cố đắc lệnh; không cộng trùng weight month_status.",
        refs=[REF_SEASON],
        stackable=False,
    )
    add(
        category="element_support",
        code="combination_produces_dm",
        name="Tam hội/tam hợp thành hành Nhật Chủ",
        tags=["strength", "element", "combination"],
        level="high",
        order=93,
        conditions=[cond("branch_combination_produces_dm_element", "equals", True)],
        result=score_result("combination_produces_dm", 10, signal="element_support"),
        explanation="Tam hợp/tam hội hóa thành hành Nhật Chủ gia tăng thế cục trợ thân.",
        refs=[REF_SCORE, REF_ROOT],
        stackable=True,
        max_stack=1,
    )
    add(
        category="element_support",
        code="no_resource_no_companion",
        name="Không Ấn không tỷ",
        tags=["strength", "element", "absence"],
        level="medium",
        order=72,
        conditions=[
            cond("resource_count", "equals", 0),
            cond("companion_count", "equals", 0),
        ],
        result=score_result("no_resource_no_companion", -6, signal="element_support"),
        explanation="Không sinh không đồng hành: thân dễ nhược trừ khi đắc lệnh và thông căn sâu.",
        refs=[REF_TG],
    )

    # --- element restriction: 12 ---
    restrictions = [
        ("zheng_guan_control", "officer_type_present", "equals", "zheng_guan", -8, 88, "Chính Quan khắc thân có chế ước."),
        ("qi_sha_control", "officer_type_present", "equals", "qi_sha", -10, 92, "Thất Sát khắc thân mạnh hơn Chính Quan."),
        ("shi_shen_drain", "output_type_present", "equals", "shi_shen", -6, 82, "Thực Thần tiết thân ôn hòa."),
        ("shang_guan_drain", "output_type_present", "equals", "shang_guan", -8, 86, "Thương Quan tiết thân mạnh, dễ làm thân nhược."),
        ("zheng_cai_drain", "wealth_type_present", "equals", "zheng_cai", -6, 80, "Chính Tài: thân sinh tài hao lực."),
        ("pian_cai_drain", "wealth_type_present", "equals", "pian_cai", -5, 78, "Thiên Tài hao thân nhẹ hơn Chính Tài đơn vị."),
        ("root_clash", "dm_root_clashed", "equals", True, -15, 100, "Căn chi bị xung phá thì mất chỗ dựa."),
        ("combo_loses_root", "root_lost_to_combination", "equals", True, -12, 95, "Hợp hóa kéo căn sang hành khác."),
        ("two_officers", "officer_count", "greater_or_equal", 2, -8, 90, "Hai Quan Sát trở lên: khắc chế chồng."),
        ("officer_plus_output", "has_officer_and_output", "equals", True, -12, 93, "Quan khắc và Thực tiết cùng lúc hại thân."),
        ("dead_plus_control", "dead_season_and_controlled", "equals", True, -10, 96, "Tháng tử lại bị khắc: thân rất yếu."),
        ("month_command_clashed", "month_branch_clashed", "equals", True, -10, 94, "Tháng lệnh bị xung: mất đắc lệnh thực tế."),
    ]
    for code, field, op, value, weight, order, expl in restrictions:
        add(
            category="element_restriction",
            code=code,
            name=code.replace("_", " "),
            tags=["strength", "restriction", code],
            level="high",
            order=order,
            conditions=[cond(field, op, value)],
            result=score_result(code, weight, signal="restriction_score"),
            explanation=expl,
            refs=[REF_TG, REF_SCORE],
            stackable=True,
            max_stack=4 if "count" not in code and "plus" not in code else 1,
        )

    # --- day master tendency: 10 ---
    add(
        category="day_master_tendency",
        code="strong_prosperous_with_root",
        name="Đắc lệnh có căn → thân vượng",
        tags=["strength", "tendency", "strong"],
        level="high",
        order=98,
        conditions=[
            cond("month_status", "equals", "prosperous"),
            cond("has_dm_root", "equals", True),
        ],
        result={**score_result("strong_tendency", 0, signal="strength_tendency", level="strong"), "tendency": "strong"},
        explanation="Đắc lệnh kèm thông căn là tổ hợp thân vượng cốt lõi.",
        refs=[REF_LEVEL, REF_SEASON, REF_ROOT],
    )
    add(
        category="day_master_tendency",
        code="false_strong_no_root_drained",
        name="Đắc lệnh vô căn bị tiết → không tự động vượng",
        tags=["strength", "tendency", "false_strong"],
        level="high",
        order=97,
        conditions=[
            cond("month_status", "equals", "prosperous"),
            cond("root_level", "equals", "no_root"),
            cond("output_count", "greater_or_equal", 1),
        ],
        result={**score_result("false_strong", -6, signal="strength_tendency", level="balanced"), "tendency": "false_strong"},
        explanation="Chỉ dựa tháng lệnh mà vô căn lại bị Thực Thương thì dễ giả vượng.",
        refs=[REF_LEVEL, REF_ROOT],
    )
    add(
        category="day_master_tendency",
        code="weak_dead_no_root",
        name="Tháng tử vô căn → thân nhược",
        tags=["strength", "tendency", "weak"],
        level="high",
        order=98,
        conditions=[
            cond("month_status", "equals", "dead"),
            cond("root_level", "equals", "no_root"),
        ],
        result={**score_result("weak_tendency", 0, signal="strength_tendency", level="weak"), "tendency": "weak"},
        explanation="Mất lệnh và vô căn: khuynh hướng thân nhược rõ.",
        refs=[REF_LEVEL, REF_SEASON, REF_ROOT],
    )
    add(
        category="day_master_tendency",
        code="weak_imprison_controlled",
        name="Tháng tù bị khắc → thân nhược",
        tags=["strength", "tendency", "weak"],
        level="high",
        order=96,
        conditions=[
            cond("month_status", "equals", "imprison"),
            cond("officer_count", "greater_or_equal", 1),
        ],
        result={**score_result("weak_imprison", 0, signal="strength_tendency", level="weak"), "tendency": "weak"},
        explanation="Tù khí cộng Quan Sát: thân bị chế.",
        refs=[REF_LEVEL, REF_TG],
    )
    add(
        category="day_master_tendency",
        code="balanced_rest_one_root",
        name="Hưu khí một căn → trung hòa",
        tags=["strength", "tendency", "balanced"],
        level="medium",
        order=85,
        conditions=[
            cond("month_status", "equals", "rest"),
            cond("root_level", "equals", "root_one"),
        ],
        result={**score_result("balanced_tendency", 0, signal="strength_tendency", level="balanced"), "tendency": "balanced"},
        explanation="Hưu kèm một căn thường trung hòa, cần xem Ấn/Tỷ và Quan/Thực.",
        refs=[REF_LEVEL, REF_ROOT],
    )
    add(
        category="day_master_tendency",
        code="level_strong_threshold",
        name="Ngưỡng thân vượng >= 0.65",
        tags=["strength", "tendency", "level"],
        level="high",
        order=100,
        conditions=[cond("strength_score_normalized", "greater_or_equal", 0.65)],
        result={**score_result("level_strong", 0, level="strong"), "strength_level": "strong"},
        explanation="Tổng điểm chuẩn hóa >= 0.65 xếp thân vượng (BTE strength config).",
        refs=[REF_LEVEL, REF_SCORE],
        exclusive=True,
        group="strength_level",
    )
    add(
        category="day_master_tendency",
        code="level_weak_threshold",
        name="Ngưỡng thân nhược <= 0.35",
        tags=["strength", "tendency", "level"],
        level="high",
        order=100,
        conditions=[cond("strength_score_normalized", "less_or_equal", 0.35)],
        result={**score_result("level_weak", 0, level="weak"), "strength_level": "weak"},
        explanation="Tổng điểm chuẩn hóa <= 0.35 xếp thân nhược.",
        refs=[REF_LEVEL, REF_SCORE],
        exclusive=True,
        group="strength_level",
    )
    add(
        category="day_master_tendency",
        code="level_balanced_band",
        name="Ngưỡng trung hòa 0.35–0.65",
        tags=["strength", "tendency", "level"],
        level="high",
        order=80,
        conditions=[
            cond("strength_score_normalized", "greater_than", 0.35),
            cond("strength_score_normalized", "less_than", 0.65),
        ],
        result={**score_result("level_balanced", 0, level="balanced"), "strength_level": "balanced"},
        explanation="Điểm nằm giữa 0.35 và 0.65 xếp trung hòa.",
        refs=[REF_LEVEL, REF_SCORE],
        exclusive=True,
        group="strength_level",
    )
    add(
        category="day_master_tendency",
        code="very_strong_band",
        name="Khuynh hướng cực vượng >= 0.75",
        tags=["strength", "tendency", "very_strong"],
        level="medium",
        order=90,
        conditions=[cond("strength_score_normalized", "greater_or_equal", 0.75)],
        result={**score_result("very_strong", 0, level="very_strong"), "strength_level": "very_strong"},
        explanation="Điểm rất cao: cực vượng; xét cách Tòng chỉ ở gói Pattern, không kết luận Tòng tại đây.",
        refs=[REF_LEVEL],
    )
    add(
        category="day_master_tendency",
        code="false_weak_dead_deep_root",
        name="Tháng tử nhưng căn sâu + Ấn → không cực nhược",
        tags=["strength", "tendency", "false_weak"],
        level="high",
        order=94,
        conditions=[
            cond("month_status", "equals", "dead"),
            cond("root_level", "in", ["root_two", "root_three_plus"]),
            cond("resource_count", "greater_or_equal", 1),
        ],
        result={**score_result("false_weak", 8, signal="strength_tendency", level="balanced"), "tendency": "false_weak"},
        explanation="Mất lệnh nhưng thông căn sâu và có Ấn: thân không yếu như điểm mùa đơn lẻ.",
        refs=[REF_LEVEL, REF_ROOT, REF_TG],
    )

    # --- basic scoring: 8 ---
    add(
        category="basic_scoring",
        code="baseline_score",
        name="Điểm nền 50",
        tags=["strength", "scoring", "baseline"],
        level="high",
        order=50,
        conditions=[cond("chart_valid", "equals", True)],
        result={"effect": "baseline", "weight": 50, "signal": "baseline", "score_target": "day_master.strength_score"},
        explanation="Mọi cục hợp lệ khởi điểm 50/100 trước khi cộng trừ nhân tố.",
        refs=[REF_SCORE],
    )
    add(
        category="basic_scoring",
        code="normalize_0_100",
        name="Chuẩn hóa thang 0–100",
        tags=["strength", "scoring", "normalize"],
        level="high",
        order=40,
        conditions=[cond("raw_strength_total", "exists", True)],
        result={"effect": "normalize", "weight": 0, "signal": "normalize", "scale_min": 0, "scale_max": 100},
        explanation="Tổng thô được kẹp và quy về 0–100 rồi chia 100 thành điểm chuẩn hóa.",
        refs=[REF_SCORE],
    )
    add(
        category="basic_scoring",
        code="month_status_exclusive",
        name="Nhóm month_status loại trừ lẫn nhau",
        tags=["strength", "scoring", "exclusive"],
        level="high",
        order=99,
        conditions=[cond("rule_group", "equals", "month_status")],
        result={"effect": "exclusive_group", "weight": 0, "signal": "priority", "group": "month_status"},
        explanation="Chỉ một trạng thái tháng lệnh được áp dụng.",
        refs=[REF_SCORE, REF_SEASON],
    )
    add(
        category="basic_scoring",
        code="support_max_stack_4",
        name="Trợ lực cộng dồn tối đa 4",
        tags=["strength", "scoring", "stack"],
        level="medium",
        order=70,
        conditions=[cond("rule_group", "equals", "support")],
        result={"effect": "max_stack", "weight": 0, "signal": "priority", "max_stack": 4},
        explanation="Các nhân tố trợ (can/chi/ấn/tỷ) stackable tối đa 4 lần theo CSV support.",
        refs=[REF_SCORE],
    )
    add(
        category="basic_scoring",
        code="control_max_stack_4",
        name="Khắc tiết cộng dồn tối đa 4",
        tags=["strength", "scoring", "stack"],
        level="medium",
        order=70,
        conditions=[cond("rule_group", "equals", "control")],
        result={"effect": "max_stack", "weight": 0, "signal": "priority", "max_stack": 4},
        explanation="Quan/Thực/Tài stackable tối đa 4 đơn vị.",
        refs=[REF_SCORE],
    )
    add(
        category="basic_scoring",
        code="priority_order",
        name="Thứ tự ưu tiên nhóm luật",
        tags=["strength", "scoring", "priority"],
        level="high",
        order=100,
        conditions=[cond("resolve_priorities", "equals", True)],
        result={
            "effect": "priority_order",
            "weight": 0,
            "signal": "priority",
            "order": ["special", "season", "root", "support", "control", "drain", "combination"],
        },
        explanation="Ưu tiên: đặc biệt > tháng lệnh > căn > trợ > khắc > tiết > hợp. Không đảo ngược pipeline.",
        refs=[REF_SCORE, REF_DOM],
    )
    add(
        category="basic_scoring",
        code="no_double_count_pillar",
        name="Không đếm trùng cùng một trụ",
        tags=["strength", "scoring", "integrity"],
        level="high",
        order=95,
        conditions=[cond("same_pillar_evidence", "equals", True)],
        result={"effect": "deduplicate_pillar", "weight": 0, "signal": "integrity"},
        explanation="Một trụ chỉ đóng góp một lần cho cùng nhóm (căn hoặc trợ), tránh cộng kép.",
        refs=[REF_SCORE],
    )
    add(
        category="basic_scoring",
        code="season_root_disagreement_confidence",
        name="Lệnh và căn trái dấu → độ tin cậy thấp",
        tags=["strength", "scoring", "confidence"],
        level="medium",
        order=60,
        conditions=[cond("season_root_polarity_disagree", "equals", True)],
        result={"effect": "low_confidence", "weight": 0, "signal": "confidence", "confidence": "low"},
        explanation="Đắc lệnh nhưng vô căn (hoặc tử mà căn sâu) cần đánh dấu confidence thấp, không bịa kết luận tuyệt đối.",
        refs=[REF_LEVEL, REF_SCORE],
    )

    return rules


def dump(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_rule_files(rules: list[dict]) -> list[str]:
    by_cat: dict[str, list[dict]] = {}
    for item in rules:
        by_cat.setdefault(item["category"], []).append(item)
    paths: list[str] = []
    for category, items in sorted(by_cat.items()):
        rel = f"rules/{category}.json"
        dump(
            ROOT / rel,
            {
                "schema_version": "2.0.0",
                "package_id": PKG_ID,
                "category": category,
                "count": len(items),
                "objects": items,
            },
        )
        paths.append(rel)
    return paths


def compute_checksum(scope: list[str]) -> str:
    chunks: list[bytes] = []
    for rel in scope:
        raw = (ROOT / rel).read_bytes()
        if rel == "PACKAGE.json":
            data = json.loads(raw.decode("utf-8"))
            data["checksum"]["value"] = None
            raw = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        elif rel == "RELEASE.json":
            data = json.loads(raw.decode("utf-8"))
            data["checksum"]["value"] = ZERO_HEX
            raw = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        chunks.append(f"{rel}\n{len(raw)}\n".encode("utf-8") + raw)
    return hashlib.sha256(b"\n".join(chunks)).hexdigest()


def main() -> None:
    rules = build_rules()
    assert 80 <= len(rules) <= 120, len(rules)
    ids = [r["id"] for r in rules]
    assert len(ids) == len(set(ids))
    rule_paths = write_rule_files(rules)
    print("rules", len(rules), "files", rule_paths)


if __name__ == "__main__":
    main()
