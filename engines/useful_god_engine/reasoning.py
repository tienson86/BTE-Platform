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
        short = (
            f"Nhật chủ {dm_label} {strength_vi} → có Chính Quan đủ điều kiện Chế → "
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
