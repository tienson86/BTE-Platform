"""V1.0 customer reasoning chain for Overall Dụng — no new winner theory."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from engines.bazi_engine.ten_god import CONTROLS, GENERATES, stem_element

ARCHETYPE_SINH_TRO = "SINH / TRỢ"
ARCHETYPE_TIET = "TIẾT"
ARCHETYPE_CHE = "CHẾ"
ARCHETYPE_BALANCED_WEALTH = "BALANCED-WEALTH"
ARCHETYPE_FOLLOW = "FOLLOW / SPECIAL"
ARCHETYPE_OTHER = "OTHER"

STRENGTH_STATE_VI = {
    "strong": "thân vượng",
    "weak": "thân nhược",
    "balanced": "thân trung hòa",
}

_RULE_ARCHETYPE: dict[str, str] = {
    "str_001": ARCHETYPE_SINH_TRO,
    "str_002": ARCHETYPE_SINH_TRO,
    "str_003": ARCHETYPE_CHE,
    "str_004": ARCHETYPE_TIET,
    "str_005": ARCHETYPE_BALANCED_WEALTH,
    "str_cold_ox_metal": ARCHETYPE_CHE,
    "str_hot_strong_earth": ARCHETYPE_BALANCED_WEALTH,
    "str_strong_earth_killing": ARCHETYPE_CHE,
    "str_peak_rooster_metal": ARCHETYPE_CHE,
    "str_balanced_hot_wood_output": ARCHETYPE_SINH_TRO,
    "str_balanced_rooster_earth_output": ARCHETYPE_SINH_TRO,
    "str_balanced_cold_metal_sat_resource": ARCHETYPE_CHE,
    "str_cool_monkey_strong_water": ARCHETYPE_BALANCED_WEALTH,
    "str_cool_monkey_strong_metal": ARCHETYPE_CHE,
    "str_cold_pig_strong_water": ARCHETYPE_BALANCED_WEALTH,
    "str_warm_tiger_strong_fire": ARCHETYPE_CHE,
    "str_balanced_hot_snake_water": ARCHETYPE_SINH_TRO,
    "str_balanced_cool_rooster_fire_wealth": ARCHETYPE_SINH_TRO,
    "str_balanced_cold_cool_climate_fallback": ARCHETYPE_SINH_TRO,
    "str_balanced_warm_hot_climate_fallback": ARCHETYPE_BALANCED_WEALTH,
    "spc_001": ARCHETYPE_FOLLOW,
    "spc_002": ARCHETYPE_FOLLOW,
    "spc_003": ARCHETYPE_FOLLOW,
    "spc_004": ARCHETYPE_FOLLOW,
}

_RULE_NEED: dict[str, str] = {
    "str_001": "sinh trợ",
    "str_002": "sinh trợ",
    "str_003": "chế ước",
    "str_004": "tiết bớt khí",
    "str_005": "lưu thông",
    "str_cold_ox_metal": "ôn luyện và chế ước",
    "str_hot_strong_earth": "nhuận hạ và hao thân",
    "str_strong_earth_killing": "chế ước",
    "str_peak_rooster_metal": "luyện Kim và chế ước",
    "str_balanced_hot_wood_output": "nhuận sinh và giảm khô nóng",
    "str_balanced_rooster_earth_output": "sinh thân và chế Kim tiết khí",
    "str_balanced_cold_metal_sat_resource": "ôn luyện và chuyển Sát sinh thân",
    "str_cool_monkey_strong_water": "ôn ấm, hao thân và dẫn khí qua Mộc",
    "str_cool_monkey_strong_metal": "ôn luyện, chế Kim và dẫn khí qua Mộc",
    "str_cold_pig_strong_water": "ôn ấm, hao Thủy và dẫn khí qua Mộc",
    "str_warm_tiger_strong_fire": "chế Hỏa, sinh Thủy và dẫn khí qua Kim Thổ",
    "str_balanced_hot_snake_water": "nhuận hạ, trợ Thủy và dẫn nguồn qua Kim",
    "str_balanced_cool_rooster_fire_wealth": "sinh Hỏa, ôn trợ và giúp Nhật chủ đảm nhiệm Tài",
    "str_balanced_cold_cool_climate_fallback": "ôn ấm và dẫn khí qua Mộc Hỏa",
    "str_balanced_warm_hot_climate_fallback": "nhuận hạ và dẫn nguồn qua Kim Thủy",
    "spc_001": "đi theo Tài",
    "spc_002": "đi theo Quan",
    "spc_003": "đi theo Sát",
    "spc_004": "định khí chuyên cách",
}

_RULE_PROBLEM: dict[str, str] = {
    "str_001": "Nhật chủ nhược, cần dưỡng có căn Chính Ấn",
    "str_002": "Nhật chủ nhược, fallback dưỡng bằng Thiên Ấn",
    "str_003": "Nhật chủ vượng, có Chính Quan để chế",
    "str_004": "Nhật chủ vượng, đường thường dùng Tiết",
    "str_005": "Nhật chủ trung hòa, V1.0 ưu tiên lưu thông qua Chính Tài",
    "str_cold_ox_metal": "Kim vượng sinh tháng Sửu lạnh, cần Hỏa ôn luyện; Mộc trợ sinh Hỏa",
    "str_hot_strong_earth": "Thổ vượng gặp khí nóng, cần Thủy nhuận hạ; Kim tiết Thổ và sinh Thủy",
    "str_strong_earth_killing": "Thổ vượng có Thất Sát Mộc hữu dụng để chế thân; Thủy trợ Mộc có điều kiện",
    "str_peak_rooster_metal": "Kim vượng đắc lệnh tháng Dậu, cần Hỏa luyện Kim; Mộc và Thủy dùng có điều kiện",
    "str_balanced_hot_wood_output": "Giáp Mộc mùa nóng, Hỏa Thổ đã nặng, cần Thủy nhuận sinh; Mộc trợ có điều kiện",
    "str_balanced_rooster_earth_output": "Kỷ Thổ sinh tháng Dậu bị Kim tiết mạnh, cần Hỏa sinh thân đồng thời chế Kim",
    "str_balanced_cold_metal_sat_resource": "Canh Kim mùa đông khí hàn, có Sát Ấn tương sinh, cần Hỏa ôn luyện và Thổ chuyển Sát sinh thân",
    "str_cool_monkey_strong_water": "Nhâm Thủy vượng sinh tháng Thân khí mát, Thổ đã có nhiều căn, cần Hỏa ôn ấm và Mộc dẫn sinh",
    "str_cool_monkey_strong_metal": "Tân Kim vượng sinh tháng Thân khí mát, cần Hỏa chế luyện và Mộc sinh Hỏa; Thủy đã nhiều nên không làm Hỷ",
    "str_cold_pig_strong_water": "Nhâm Thủy vượng sinh tháng Hợi hàn, cần Hỏa điều hậu và hao thân; Mộc tiết Thủy sinh Hỏa, Thổ lạnh chưa đủ lực làm Dụng",
    "str_warm_tiger_strong_fire": "Bính Hỏa vượng sinh tháng Dần được Mộc sinh trợ, cần Thủy chế Hỏa; Kim sinh Thủy chế Mộc, Thổ dùng phụ để tiết Hỏa sinh Kim",
    "str_balanced_hot_snake_water": "Quý Thủy sinh tháng Tỵ khí nóng, Hỏa Thổ nặng, cần Nhâm Thủy nhuận hạ và Kim sinh Thủy",
    "str_balanced_cool_rooster_fire_wealth": "Đinh Hỏa sinh tháng Dậu, Kim đắc lệnh và khí mát, cần Giáp Mộc sinh thân; Bính Đinh Hỏa ôn trợ để đảm nhiệm Tài",
    "str_balanced_cold_cool_climate_fallback": "Nhật chủ trung hòa nhưng toàn cục thiên lạnh hoặc mát, chưa có cấu trúc chuyên biệt nên dùng Bính Hỏa điều hậu và Mộc dẫn sinh",
    "str_balanced_warm_hot_climate_fallback": "Nhật chủ trung hòa nhưng toàn cục thiên ấm hoặc nóng, chưa có cấu trúc chuyên biệt nên dùng Nhâm Thủy nhuận hạ và Kim dẫn nguồn",
    "spc_001": "Cách Tòng Tài đã công bố",
    "spc_002": "Cách Tòng Quan đã công bố",
    "spc_003": "Cách Tòng Sát đã công bố",
    "spc_004": "Chuyên cách ưu tiên Ấn",
}

_RULE_CANDIDATE_ROLE: dict[str, str] = {
    "str_001": "Chính Ấn",
    "str_002": "Thiên Ấn",
    "str_003": "Chính Quan",
    "str_004": "Thực Thần",
    "str_005": "Chính Tài",
    "str_cold_ox_metal": "Chính Quan",
    "str_hot_strong_earth": "Chính Tài",
    "str_strong_earth_killing": "Thất Sát",
    "str_peak_rooster_metal": "Chính Quan",
    "str_balanced_hot_wood_output": "Thiên Ấn",
    "str_balanced_rooster_earth_output": "Thiên Ấn",
    "str_balanced_cold_metal_sat_resource": "Thất Sát",
    "str_cool_monkey_strong_water": "Chính Tài",
    "str_cool_monkey_strong_metal": "Chính Quan",
    "str_cold_pig_strong_water": "Thiên Tài",
    "str_warm_tiger_strong_fire": "Thất Sát",
    "str_balanced_hot_snake_water": "Kiếp Tài",
    "str_balanced_cool_rooster_fire_wealth": "Chính Ấn",
    "str_balanced_cold_cool_climate_fallback": "Điều hậu Hỏa",
    "str_balanced_warm_hot_climate_fallback": "Điều hậu Thủy",
    "spc_001": "Chính Tài",
    "spc_002": "Chính Quan",
    "spc_003": "Thất Sát",
    "spc_004": "Thiên Ấn",
}

_PRINCIPLE_VI = {
    ARCHETYPE_SINH_TRO: "Sinh / Trợ",
    ARCHETYPE_TIET: "Tiết",
    ARCHETYPE_CHE: "Chế",
    ARCHETYPE_BALANCED_WEALTH: "Tài lưu thông",
    ARCHETYPE_FOLLOW: "Tòng / cách đặc biệt",
    ARCHETYPE_OTHER: "cân bằng hiện có",
}

FOLLOW_LABEL = {
    "tong_tai": "Tòng Tài",
    "tong_quan": "Tòng Quan",
    "tong_sat": "Tòng Sát",
}


@dataclass(slots=True)
class UsefulGodCustomerReason:
    """Presentation-safe Dụng reason. No rule IDs."""

    reason_archetype: str = ""
    strength_state: str = ""
    balancing_action: str = ""
    source_element: str = ""
    target_element: str = ""
    candidate_element: str = ""
    candidate_stem: str = ""
    candidate_ten_god: str = ""
    short_reason: str = ""
    problem: str = ""
    balancing_relation: str = ""
    candidate_role: str = ""

    def to_dict(self) -> dict[str, str]:
        """JSON-safe reason object for API / Report."""
        return {key: str(value or "") for key, value in asdict(self).items()}


def archetype_for_rule(rule_id: str) -> str:
    """Map an existing Overall rule id to a V1.0 reasoning archetype."""
    return _RULE_ARCHETYPE.get(str(rule_id or "").strip(), ARCHETYPE_OTHER)


def _relation_phrase(day_master: str, useful_stem: str, archetype: str) -> str:
    dm_el = stem_element(day_master)
    use_el = stem_element(useful_stem) or ""
    if not dm_el or not use_el:
        return ""
    if archetype == ARCHETYPE_TIET and GENERATES.get(dm_el) == use_el:
        return f"{dm_el} sinh {use_el}"
    if archetype == ARCHETYPE_SINH_TRO and GENERATES.get(use_el) == dm_el:
        return f"{use_el} sinh {dm_el}"
    if archetype == ARCHETYPE_CHE and CONTROLS.get(use_el) == dm_el:
        return f"{use_el} khắc {dm_el}"
    if archetype == ARCHETYPE_BALANCED_WEALTH and CONTROLS.get(dm_el) == use_el:
        return f"{dm_el} khắc {use_el}"
    if GENERATES.get(dm_el) == use_el:
        return f"{dm_el} sinh {use_el}"
    if GENERATES.get(use_el) == dm_el:
        return f"{use_el} sinh {dm_el}"
    if CONTROLS.get(use_el) == dm_el:
        return f"{use_el} khắc {dm_el}"
    if CONTROLS.get(dm_el) == use_el:
        return f"{dm_el} khắc {use_el}"
    return f"{dm_el}–{use_el}"


def _trace_context(result: Any) -> dict[str, Any]:
    meta = getattr(result, "metadata", None) or {}
    if not isinstance(meta, dict):
        return {}
    trace = meta.get("trace") or {}
    if not isinstance(trace, dict):
        return {}
    ctx = trace.get("context") or {}
    return ctx if isinstance(ctx, dict) else {}


def build_customer_reason(result: Any) -> UsefulGodCustomerReason:
    """Build the customer Dụng chain from an existing engine result."""
    ctx = _trace_context(result)
    rule_id = str(getattr(result, "winning_rule_id", "") or "")
    archetype = archetype_for_rule(rule_id)
    day_master = str(ctx.get("day_master") or "")
    strength = str(ctx.get("strength_level") or "")
    dm_el = str(ctx.get("day_master_element") or stem_element(day_master) or "")
    stem = str(getattr(result, "useful_stem", "") or "")
    ten_god = str(getattr(result, "useful_ten_god", "") or "")
    element = str(getattr(result, "useful_element", "") or stem_element(stem) or "")
    display = str(getattr(result, "useful_display", "") or "")
    follow = str(ctx.get("follow_pattern") or "")
    relation = _relation_phrase(day_master, stem, archetype)
    need = _RULE_NEED.get(rule_id, "cân bằng")
    principle = _PRINCIPLE_VI.get(archetype, "cân bằng hiện có")
    strength_vi = STRENGTH_STATE_VI.get(strength, strength or "chưa rõ thân khí")
    dm_label = " ".join(part for part in (day_master, dm_el) if part) or "nhật chủ"
    stem_map = (
        f"{stem} đối với {day_master} là {ten_god}"
        if day_master and stem and ten_god
        else f"can {stem} ứng với {ten_god}"
    )
    if archetype == ARCHETYPE_FOLLOW:
        follow_vi = FOLLOW_LABEL.get(follow, "cách đặc biệt đã công bố")
        short = (
            f"Nhật chủ {dm_label} theo {follow_vi} → "
            f"Dụng thần theo mô hình cân bằng V1.0 đi theo hướng đó → "
            f"chọn {display or ten_god} làm Dụng."
        )
    elif archetype == ARCHETYPE_BALANCED_WEALTH:
        short = (
            f"Nhật chủ {dm_label} {strength_vi} → cần {need} → "
            f"dùng nguyên tắc {principle} theo mô hình cân bằng V1.0 "
            f"(không đối chiếu sâu toàn cục) → "
            f"hành {element} có quan hệ {relation or 'Tài'} → "
            f"{stem_map} → chọn {display} làm Dụng."
        )
    elif archetype == ARCHETYPE_TIET:
        short = (
            f"Nhật chủ {dm_label} {strength_vi} → cần tiết bớt khí {dm_el} → "
            f"áp dụng nguyên tắc Tiết theo mô hình cân bằng V1.0 → "
            f"{relation} → {stem_map} → chọn {display} làm Dụng."
        )
    elif archetype == ARCHETYPE_CHE:
        controlling_role = _RULE_CANDIDATE_ROLE.get(rule_id, ten_god) or ten_god
        short = (
            f"Nhật chủ {dm_label} {strength_vi} → có {controlling_role} đủ điều kiện Chế → "
            f"áp dụng nguyên tắc Chế theo mô hình cân bằng V1.0 → "
            f"{relation} → {stem_map} → chọn {display} làm Dụng."
        )
    else:
        short = (
            f"Nhật chủ {dm_label} {strength_vi} → cần {need} → "
            f"dùng nguyên tắc {principle} theo mô hình cân bằng V1.0 → "
            f"hành {element} có quan hệ {relation} → "
            f"{stem_map} → chọn {display} làm Dụng."
        )
    return UsefulGodCustomerReason(
        reason_archetype=archetype,
        strength_state=strength,
        balancing_action=need,
        source_element=dm_el,
        target_element=element,
        candidate_element=element,
        candidate_stem=stem,
        candidate_ten_god=ten_god,
        short_reason=short,
        problem=_RULE_PROBLEM.get(rule_id, ""),
        balancing_relation=relation,
        candidate_role=_RULE_CANDIDATE_ROLE.get(rule_id, ten_god),
    )
