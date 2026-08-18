"""Professional Ten Gods consultation copy.

Writing only. Copies already-published chart facts and Knowledge fields.
Does not calculate Ten Gods, select Useful God, or rewrite Knowledge.
"""

from __future__ import annotations

from typing import Any, Mapping

from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntity
from engines.interpretation_engine.foundation.knowledge.entity_types import (
    TEN_GOD_DAY_MASTER_KEY,
    TEN_GOD_ROLE_KEYS,
    USEFUL_GOD_STEM_KEYS,
)
from engines.interpretation_engine.foundation.knowledge.service import retrieve_knowledge
from engines.interpretation_engine.foundation.narrative.publish.criteria import (
    word_count,
)
from engines.interpretation_engine.foundation.narrative.publish.editions import (
    MIN_CONSULTING_WORDS,
    PROFESSIONAL_SECTION_LIMITS,
)
from engines.interpretation_engine.foundation.narrative.publish.luck_analysis_copy import (
    luck_analysis_from_payload,
)
from engines.interpretation_engine.foundation.narrative.text import normalize_text

_TEN_GODS_DOMAIN = "TenGods"
_IMPORTANT_LIMIT = 3

_PILLAR_VI: Mapping[str, str] = {
    "year": "trụ năm",
    "month": "trụ tháng",
    "day": "trụ ngày",
    "hour": "trụ giờ",
}
_VIS_VI: Mapping[str, str] = {
    "visible": "lộ",
    "hidden": "tàng",
}
_STRENGTH_VI: Mapping[str, str] = {
    "strong": "Thân vượng",
    "balanced": "Trung hòa",
    "weak": "Thân nhược",
    "very_strong": "Thân vượng",
    "very_weak": "Thân nhược",
}

_GLOSSARY_MARKERS: tuple[str, ...] = (
    "là quan hệ nhật chủ",
    "là dụng thần:",
    "là hỷ thần:",
    "là kỵ thần hoặc",
    "thập thần là",
    "encyclopedia",
)


def ten_gods_consultation_from_payload(payload: Mapping[str, Any] | None) -> dict[str, Any]:
    """Read stamped Ten Gods consultation facts. Empty when missing."""
    if not isinstance(payload, Mapping):
        return {}
    metadata = payload.get("metadata")
    if not isinstance(metadata, Mapping):
        return {}
    raw = metadata.get("ten_gods_consultation")
    return dict(raw) if isinstance(raw, Mapping) else {}


def stamp_ten_gods_consultation(payload: dict[str, Any], engine_output: Any) -> dict[str, Any]:
    """Copy Ten Gods chart facts onto narrative metadata. Do not calculate them."""
    if not isinstance(payload, dict) or engine_output is None:
        return payload
    foundation = getattr(engine_output, "interpretation_foundation", None)
    if foundation is None:
        return payload
    facts = getattr(getattr(foundation, "facts", None), "ten_gods", None)
    if facts is None or not hasattr(facts, "to_dict"):
        return payload
    useful = getattr(foundation.facts, "useful_god", None)
    pattern = getattr(foundation.facts, "pattern", None)
    strength = getattr(foundation.facts, "strength", None)
    luck = getattr(foundation, "luck_analysis", None)
    period = {}
    if luck is not None and hasattr(luck, "to_dict"):
        period = dict((luck.to_dict() or {}).get("current_period_identity") or {})
    visible = [item.to_dict() for item in (facts.visible or ())]
    hidden = [item.to_dict() for item in (facts.hidden or ())]
    evidence = [
        str(item.get("evidence") or "")
        for item in (*visible, *hidden)
        if item.get("evidence")
    ]
    data = {
        "day_master": str(facts.day_master or ""),
        "day_master_element": str(facts.day_master_element or ""),
        "pattern_label": str(getattr(pattern, "label", "") or ""),
        "strength_level": str(getattr(strength, "level", "") or ""),
        "useful_god": str(getattr(useful, "selected", "") or ""),
        "useful_god_entity_type": str(getattr(useful, "selected_entity_type", "") or ""),
        "favorable_gods": list(getattr(useful, "favorable_gods", ()) or ()),
        "unfavorable_gods": list(getattr(useful, "unfavorable_gods", ()) or ()),
        "visible": visible,
        "hidden": hidden,
        "distribution": [dict(item) for item in (facts.distribution or ())],
        "current_dayun": str(period.get("label") or "").strip(),
        "dayun_ten_god": str(period.get("ten_god") or "").strip(),
        "owner": str(getattr(facts, "owner", "") or ""),
        "evidence": evidence,
        "status": str(getattr(getattr(facts, "status", None), "value", "") or ""),
    }
    out = dict(payload)
    metadata = dict(out.get("metadata") or {}) if isinstance(out.get("metadata"), dict) else {}
    metadata["ten_gods_consultation"] = data
    out["metadata"] = metadata
    return out


def assemble_ten_gods_consultation(
    payload: dict[str, Any],
    *,
    exclude: list[str],
) -> list[str]:
    """Build the Professional Ten Gods page from stamped chart facts + Knowledge."""
    data = ten_gods_consultation_from_payload(payload)
    if not data:
        data = _fallback_from_luck(payload)
    paragraphs = ten_gods_paragraphs_from_facts(data)
    return _unique_kept(paragraphs, exclude, PROFESSIONAL_SECTION_LIMITS["sec-ten_gods"])


def ten_gods_paragraphs_from_facts(data: Mapping[str, Any]) -> list[str]:
    """Consultation paragraphs for important natal Ten Gods only."""
    if not data:
        return []
    roles = _important_roles(data)
    if not roles:
        return [
            normalize_text(
                "Trong lá số này, chưa có thập thần nào đủ chỗ để luận thành tư vấn. "
                "Không giảng danh mục thập thần."
            )
        ]
    paragraphs = [_overview(data, roles)]
    for key in roles:
        entity = retrieve_knowledge(_TEN_GODS_DOMAIN, key)
        positions = _positions_for(data, key)
        paragraphs.extend(_role_block(key, entity, positions, data, roles))
    return [normalize_text(item) for item in paragraphs if item]


def _fallback_from_luck(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Keep dayun identity if Ten Gods stamp is missing. Do not invent roles."""
    luck = luck_analysis_from_payload(payload)
    period = luck.get("current_period_identity") or {}
    if not isinstance(period, Mapping):
        return {}
    return {
        "current_dayun": str(period.get("label") or "").strip(),
        "dayun_ten_god": str(period.get("ten_god") or "").strip(),
        "visible": [],
        "hidden": [],
        "distribution": [],
        "favorable_gods": [],
        "unfavorable_gods": [],
    }


def _important_roles(data: Mapping[str, Any]) -> list[str]:
    """Select chart-governing roles. Do not print the catalogue."""
    present = _present_roles(data)
    ranked: list[str] = []
    pattern = str(data.get("pattern_label") or "").strip()
    if pattern in TEN_GOD_ROLE_KEYS and pattern in present:
        ranked.append(pattern)
    useful = str(data.get("useful_god") or "").strip()
    if useful in TEN_GOD_ROLE_KEYS and useful in present:
        ranked.append(useful)
    stem_role = _role_of_useful_stem(data, useful)
    if stem_role in present:
        ranked.append(stem_role)
    weights = _weights(data)
    visible_unique = list(
        dict.fromkeys(
            str(item.get("name") or "")
            for item in (data.get("visible") or [])
            if str(item.get("name") or "") in TEN_GOD_ROLE_KEYS
        )
    )
    visible_unique.sort(key=lambda name: weights.get(name, 0.0), reverse=True)
    ranked.extend(visible_unique)
    return [name for name in dict.fromkeys(ranked) if name in present][:_IMPORTANT_LIMIT]


def _overview(data: Mapping[str, Any], roles: list[str]) -> str:
    """Open from this chart, not from the Ten Gods catalogue."""
    named = ", ".join(roles)
    dm = str(data.get("day_master") or "").strip() or "nhật chủ đã công bố"
    element = str(data.get("day_master_element") or "").strip()
    dm_text = f"{dm} ({element})" if element else dm
    pattern = str(data.get("pattern_label") or "").strip() or "cục đã luận"
    strength = _strength_label(data)
    useful = str(data.get("useful_god") or "").strip() or "Dụng đã luận"
    dayun = str(data.get("current_dayun") or "").strip()
    dayun_god = str(data.get("dayun_ten_god") or "").strip()
    useful_seat = _useful_presence(data, useful)
    ky = [str(item) for item in (data.get("unfavorable_gods") or []) if item]
    ky_bit = f" Kỵ đã luận: {', '.join(ky)}." if ky else ""
    period = ""
    if dayun:
        extra = f", thập thần Đại vận {dayun_god}" if dayun_god else ""
        period = f" Thập niên đang sống là {dayun}{extra}."
    return (
        f"Trong lá số này, tư vấn thập thần chỉ giữ {named} vì chúng đang quyết "
        f"cấu trúc của bạn. Nhật chủ {dm_text}, cục {pattern}, {strength}, "
        f"Dụng {useful}{useful_seat}.{period}{ky_bit} Không giảng danh mục thập thần."
    )


def _role_block(
    key: str,
    entity: KnowledgeEntity | None,
    positions: list[dict[str, Any]],
    data: Mapping[str, Any],
    roles: list[str],
) -> list[str]:
    """Six consultation slots for one chart-relevant Ten God."""
    channel = _channel(entity, key)
    location = _location(positions)
    others = [item for item in roles if item != key]
    return [
        _role_in_chart(key, channel, location, data),
        _current_influence(key, data, entity),
        _structure_contribution(key, data, entity, others),
        _opportunity(key, entity, data),
        _risk(key, entity, data),
        _practical(key, entity, data),
    ]


def _role_in_chart(
    key: str,
    channel: str,
    location: str,
    data: Mapping[str, Any],
) -> str:
    """Slot 1 — why this role is on THIS chart."""
    pattern = str(data.get("pattern_label") or "").strip()
    frame = (
        f" Đây đúng là cục {pattern} đang ngồi trên lá số."
        if key == pattern
        else f" Nó không thay cục {pattern or 'đã luận'}."
    )
    return (
        f"Trong lá số này, {key} đang đóng vai trò {channel} vì đang {location}."
        f"{frame}"
    )


def _current_influence(key: str, data: Mapping[str, Any], entity: KnowledgeEntity | None) -> str:
    """Slot 2 — living influence with strength and current decade."""
    del entity
    strength = _strength_label(data)
    seat = _seat_now(data, key)
    dayun = str(data.get("current_dayun") or "").strip()
    dayun_god = str(data.get("dayun_ten_god") or "").strip()
    if dayun and dayun_god == key:
        period = (
            f" Thập niên {dayun} đang kích đúng kênh này — đó là nhịp đang sống."
        )
    else:
        period = " Đây là ảnh hưởng gốc trên lá số, không phải nhịp Đại vận đang sống."
    return (
        f"Ảnh hưởng hiện tại của {key} trên cuộc sống này: {seat} "
        f"trong bối cảnh {strength}.{period}"
    )


def _structure_contribution(
    key: str,
    data: Mapping[str, Any],
    entity: KnowledgeEntity | None,
    others: list[str],
) -> str:
    """Slot 3 — Pattern / Useful God / peer roles already on the chart."""
    pattern = str(data.get("pattern_label") or "").strip() or "cục đã luận"
    useful = str(data.get("useful_god") or "").strip() or "Dụng đã luận"
    if key == pattern:
        frame = f"{key} chính là trục cục {pattern} trên lá số này."
    else:
        frame = f"{key} đứng cạnh cục {pattern}, không thay cục."
    useful_bit = ""
    if useful == key or _role_of_useful_stem(data, useful) == key:
        useful_bit = f" {_useful_relation(key, data, useful)}"
    peer = f" Cùng được luận với {', '.join(others)}." if others else ""
    related = _related_present(entity, key, data)
    return f"Với cấu trúc lá số này, {frame}{useful_bit}{peer}{related}"


def _opportunity(key: str, entity: KnowledgeEntity | None, data: Mapping[str, Any]) -> str:
    """Slot 4 — chart-bound opportunity from Knowledge positive + recommendation."""
    useful = str(data.get("useful_god") or "").strip() or "Dụng đã luận"
    positive = _clip(_positive(entity) or channel_fallback(entity, key))
    action = _clip(_first_action(entity))
    extra = f" Việc hữu ích: {action}." if action else ""
    return (
        f"Cơ hội từ {key} trong cuộc sống này: {positive}. "
        f"Hướng này chỉ có ích khi phục vụ Dụng {useful}."
        f"{extra}"
    )


def _risk(key: str, entity: KnowledgeEntity | None, data: Mapping[str, Any]) -> str:
    """Slot 5 — chart-bound risk from Knowledge negative + warning."""
    ky_bit = _ky_touch(key, data)
    negative = _clip(_negative(entity) or "dùng lệch kênh đang ngồi")
    warn = _clip(_first_risk(entity))
    warn_bit = f" Cụ thể: {warn}." if warn else ""
    return (
        f"Rủi ro của {key} ở bạn: {negative}.{ky_bit}{warn_bit} "
        "Đây là lệch trên lá số này, không phải lời nguyền của tên thập thần."
    )


def _practical(key: str, entity: KnowledgeEntity | None, data: Mapping[str, Any]) -> str:
    """Slot 6 — one practical implication for this customer."""
    action = _clip(
        _first_action(entity) or f"dùng {key} đúng ranh đã luận, không bung thành tính cách"
    )
    mitigation = _clip(_first_mitigation(entity))
    useful = str(data.get("useful_god") or "").strip() or "Dụng đã luận"
    dayun = str(data.get("current_dayun") or "").strip()
    now = f" trong {dayun}" if dayun else ""
    cover = f" Khi lệch, {mitigation}." if mitigation else ""
    return (
        f"Việc cần làm với {key}{now}: {action}. "
        f"Giữ Dụng {useful} làm trục; {key} là kênh đang ngồi, không phải nghề mới."
        f"{cover}"
    )


def _related_present(
    entity: KnowledgeEntity | None,
    key: str,
    data: Mapping[str, Any],
) -> str:
    """Name a related Ten God only when it already sits on this chart."""
    if entity is None:
        return ""
    present = _present_roles(data)
    names = [
        str(item.key)
        for item in entity.related_entities
        if str(getattr(item, "domain", "") or "") == _TEN_GODS_DOMAIN
        and str(item.key) in present
        and str(item.key) != key
    ]
    if not names:
        return ""
    return f" {names[0]} cũng đang xuất hiện trên lá số này."


def _ky_touch(key: str, data: Mapping[str, Any]) -> str:
    """Mention Kỵ only when this role or its sitting stems are already listed as Kỵ."""
    ky = [str(item) for item in (data.get("unfavorable_gods") or []) if item]
    if not ky:
        return ""
    if key in ky:
        return f" Hướng đã luận xếp {key} vào Kỵ trên lá số này."
    stems = [
        str(item.get("stem") or "")
        for item in _positions_for(data, key)
        if str(item.get("stem") or "") in ky
    ]
    unique = list(dict.fromkeys(stem for stem in stems if stem))
    if not unique:
        return ""
    return f" Can {', '.join(unique)} của kênh này đang nằm trong Kỵ đã luận."


def _clip(text: str) -> str:
    """Strip copied Knowledge punctuation before joining customer sentences."""
    return str(text or "").strip().rstrip(".;")


def _useful_relation(key: str, data: Mapping[str, Any], useful: str) -> str:
    """Copy Useful God seating without reselection."""
    if useful == key:
        return f"{key} chính là Dụng đã chọn và đang ngồi trên lá số."
    stem_role = _role_of_useful_stem(data, useful)
    if stem_role == key:
        return (
            f"Can Dụng {useful} đang ngồi trên lá số dưới nhãn {key}; "
            "không đổi Dụng thành tên thập thần."
        )
    present = _present_roles(data)
    if useful in TEN_GOD_ROLE_KEYS and useful not in present:
        return (
            f"Dụng đã chọn là {useful} nhưng chưa ngồi trên trụ; "
            f"{key} mới là kênh đang hiện."
        )
    if useful in USEFUL_GOD_STEM_KEYS and not stem_role:
        return (
            f"Dụng đã chọn là {useful} và chưa thấy ngồi trên trụ đã công bố; "
            f"{key} không thay Dụng."
        )
    return f"Dụng đã chọn vẫn là {useful}; {key} không thay Dụng."


def _useful_presence(data: Mapping[str, Any], useful: str) -> str:
    """One clause on whether Useful God is seated."""
    present = _present_roles(data)
    if useful in present:
        return " (đang ngồi trên lá số)"
    stem_role = _role_of_useful_stem(data, useful)
    if stem_role:
        return f" (can đang ngồi dưới nhãn {stem_role})"
    if useful:
        return " (chưa ngồi trên trụ)"
    return ""


def _role_of_useful_stem(data: Mapping[str, Any], useful: str) -> str:
    """Natal Ten God label of the Useful God stem when that stem is already on a pillar."""
    if useful not in USEFUL_GOD_STEM_KEYS:
        return ""
    for item in (*(data.get("visible") or []), *(data.get("hidden") or [])):
        if str(item.get("stem") or "") != useful:
            continue
        name = str(item.get("name") or "")
        if name in TEN_GOD_ROLE_KEYS:
            return name
    return ""


def _present_roles(data: Mapping[str, Any]) -> set[str]:
    """Visible + hidden role names excluding Nhật Chủ catalogue identity."""
    names: set[str] = set()
    for item in (*(data.get("visible") or []), *(data.get("hidden") or [])):
        name = str(item.get("name") or "")
        if name in TEN_GOD_ROLE_KEYS and name != TEN_GOD_DAY_MASTER_KEY:
            names.add(name)
    return names


def _positions_for(data: Mapping[str, Any], key: str) -> list[dict[str, Any]]:
    """Copy positions already published for one role."""
    rows: list[dict[str, Any]] = []
    for item in (*(data.get("visible") or []), *(data.get("hidden") or [])):
        if str(item.get("name") or "") == key:
            rows.append(dict(item))
    return rows


def _weights(data: Mapping[str, Any]) -> dict[str, float]:
    """Copy weighted contribution already published by TenGodsEngine."""
    weights: dict[str, float] = {}
    for row in data.get("distribution") or []:
        if not isinstance(row, Mapping):
            continue
        label = str(row.get("label") or "")
        try:
            weights[label] = float(row.get("weighted_contribution") or 0.0)
        except (TypeError, ValueError):
            continue
    return weights


def _seat_now(data: Mapping[str, Any], key: str) -> str:
    """Describe how this role is sitting now: lộ, tàng, or lệnh tháng."""
    positions = _positions_for(data, key)
    if not positions:
        return "đang có mặt trên lá số đã công bố"
    vis = {str(item.get("visibility") or "") for item in positions}
    pillars = {str(item.get("pillar") or "") for item in positions}
    if vis == {"visible"}:
        seat = "đang lộ"
    elif vis == {"hidden"}:
        seat = "đang tàng, chưa phải nhịp mặt"
    else:
        seat = "vừa lộ vừa tàng"
    if "month" in pillars:
        seat = f"{seat}, có chân ở lệnh tháng"
    return seat


def _location(positions: list[dict[str, Any]]) -> str:
    """Customer location string from copied pillar facts."""
    if not positions:
        return "có mặt trên lá số đã công bố"
    bits: list[str] = []
    for item in positions:
        pillar = _PILLAR_VI.get(str(item.get("pillar") or ""), str(item.get("pillar") or "trụ"))
        vis = _VIS_VI.get(str(item.get("visibility") or ""), str(item.get("visibility") or ""))
        stem = str(item.get("stem") or "").strip()
        branch = str(item.get("branch") or "").strip()
        if branch and stem:
            place = f"{pillar} ({branch}/{stem})"
        elif stem:
            place = f"{pillar} ({stem})"
        else:
            place = pillar
        bits.append(f"{vis} ở {place}".strip() if vis else place)
    return "; ".join(bit for bit in bits if bit)


def _channel(entity: KnowledgeEntity | None, key: str) -> str:
    """Use Knowledge title channel, not the dictionary opening."""
    if entity is None:
        return "kênh đã công bố"
    title = str(entity.title or "")
    if "—" in title:
        return title.split("—", 1)[1].strip()
    if " - " in title:
        return title.split(" - ", 1)[1].strip()
    return _positive(entity) or key


def channel_fallback(entity: KnowledgeEntity | None, key: str) -> str:
    """Positive field or key when a slot needs a Knowledge phrase."""
    return _positive(entity) or _channel(entity, key)


def _positive(entity: KnowledgeEntity | None) -> str:
    """Copy positive_meaning. Do not invent a new trait."""
    if entity is None:
        return ""
    return str(entity.positive_meaning or "").strip()


def _negative(entity: KnowledgeEntity | None) -> str:
    """Copy negative_meaning. Do not invent a curse."""
    if entity is None:
        return ""
    return str(entity.negative_meaning or "").strip()


def _first_action(entity: KnowledgeEntity | None) -> str:
    """Copy the first Knowledge recommendation action."""
    if entity is None:
        return ""
    for row in entity.recommendations:
        action = str(dict(row).get("action") or "").strip()
        if action:
            return action
    return ""


def _first_risk(entity: KnowledgeEntity | None) -> str:
    """Copy the first Knowledge warning risk."""
    if entity is None:
        return ""
    for row in entity.warnings:
        risk = str(dict(row).get("risk") or "").strip()
        if risk:
            return risk
    return ""


def _first_mitigation(entity: KnowledgeEntity | None) -> str:
    """Copy the first Knowledge warning mitigation."""
    if entity is None:
        return ""
    for row in entity.warnings:
        mitigation = str(dict(row).get("mitigation") or "").strip()
        if mitigation:
            return mitigation
    return ""


def _strength_label(data: Mapping[str, Any]) -> str:
    """Customer strength label already owned by Strength Engine."""
    raw = str(data.get("strength_level") or "").strip()
    return _STRENGTH_VI.get(raw, raw or "thân đã luận")


def _unique_kept(texts: list[str], exclude: list[str], limit: int) -> list[str]:
    """Drop empty, glossary, and duplicate paragraphs."""
    kept: list[str] = []
    blocked = [normalize_text(item) for item in exclude]
    for text in texts:
        blob = normalize_text(text)
        if word_count(blob) < MIN_CONSULTING_WORDS:
            continue
        lowered = blob.casefold()
        if any(marker in lowered for marker in _GLOSSARY_MARKERS):
            continue
        if blob in blocked:
            continue
        kept.append(blob)
        blocked.append(blob)
        if len(kept) >= limit:
            break
    return kept
