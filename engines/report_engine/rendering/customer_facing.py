"""Customer-facing Report V1 helpers. Presentation only; no engine rescoring."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

PROMINENCE_VISIBLE = "Lộ rõ"
PROMINENCE_HIDDEN_STRONG = "Ẩn nổi bật"
PROMINENCE_HIDDEN = "Có ẩn"
PROMINENCE_ABSENT = "Không hiện"
SHENSHA_PROMINENT = "Nổi bật"

_FEATURED_LIMIT = 5
_FEATURED_MIN = 3
_HIDDEN_STRONG_COUNT = 3
_HIDDEN_REPEAT_COUNT = 2

_RULE_PHRASE_RE = re.compile(r"(?:^|\s|[·|,;])rule\s+[a-z][a-z0-9_]{1,40}", re.IGNORECASE)
_INTERNAL_ID_RE = re.compile(
    r"\b(?:cli|com_san|pat|str|sea|tmp|flo|flw|ctl|sup|spc|cmb|root)_[a-z0-9_]+\b",
    re.IGNORECASE,
)
_SEPARATOR_RE = re.compile(r"\s*[·|,;]\s*")

_PILLAR_LABELS = {
    "year": "Năm",
    "month": "Tháng",
    "day": "Ngày",
    "hour": "Giờ",
}

_DAY_MASTER_LABELS = frozenset({"nhật chủ", "nhat chu", "day_master"})


def strip_internal_rule_ids(text: str) -> str:
    """Remove internal rule tokens from customer-facing copy."""
    if not text:
        return ""
    cleaned = _RULE_PHRASE_RE.sub(" ", text)
    cleaned = _INTERNAL_ID_RE.sub(" ", cleaned)
    return collapse_separators(cleaned)


def has_internal_rule_id(text: str) -> bool:
    """True when customer copy still contains an internal rule token."""
    if not text:
        return False
    return bool(_RULE_PHRASE_RE.search(text) or _INTERNAL_ID_RE.search(text))


def collapse_separators(text: str) -> str:
    """Normalize leftover punctuation after stripping rule tokens."""
    parts = [part.strip() for part in _SEPARATOR_RE.split(text) if part.strip()]
    return " · ".join(parts)


def temperature_customer_evidence(compact: str) -> str:
    """Rewrite climate evidence without rule IDs. Does not become Useful God."""
    cleaned = strip_internal_rule_ids(compact)
    branch = _token(cleaned, r"nguyệt lệnh\s+(\S+)")
    season = _token(cleaned, r"mùa\s+(\S+)")
    climate = _token(cleaned, r"khí hậu\s+(\S+)")
    if branch and climate:
        climate_bit = (
            f"khí mùa {season} thiên {climate.lower()}"
            if season
            else f"khí hậu {climate.lower()}"
        )
        return f"Sinh tháng {branch}, {climate_bit}."
    return cleaned


def ten_gods_prominence(
    visible_entries: Sequence[Mapping[str, Any]],
    hidden_entries: Sequence[Mapping[str, Any]],
    *,
    day_master_stem: str = "",
) -> dict[str, Any]:
    """Rank Ten Gods for customer cards. Does not change G1-01 mapping."""
    visible = [
        dict(item)
        for item in visible_entries
        if isinstance(item, Mapping) and not _is_day_master_visible(item, day_master_stem)
    ]
    hidden = [dict(item) for item in hidden_entries if isinstance(item, Mapping)]
    names: list[str] = []
    for item in visible + hidden:
        name = str(item.get("ten_god") or "").strip()
        if name and name not in names and not _is_day_master_label(name):
            names.append(name)
    ranked = [_rank_one(name, visible, hidden) for name in names]
    ranked.sort(key=_prominence_sort_key)
    featured = _pick_featured(ranked)
    featured_names = {item["name"] for item in featured}
    others = [item for item in ranked if item["name"] not in featured_names]
    others_line = ""
    if others:
        others_line = "Các thần khác: " + " · ".join(item["name"] for item in others)
    return {
        "featured": featured,
        "others": others,
        "others_line": others_line,
        "all": ranked,
    }


def shensha_customer_line(item: Any) -> tuple[str, str, str]:
    """Return (name, presence, position evidence) from canonical occurrences."""
    payload = item.to_dict() if hasattr(item, "to_dict") else dict(item)
    name = str(payload.get("canonical_name") or payload.get("name") or "").strip()
    occurrences = payload.get("occurrences") or []
    pillars: list[str] = []
    for row in occurrences:
        if not isinstance(row, Mapping):
            continue
        pillar = str(row.get("pillar") or "").strip()
        if pillar and pillar not in pillars:
            pillars.append(pillar)
    labels = [_PILLAR_LABELS.get(pillar, pillar) for pillar in pillars]
    prominent = len(labels) >= 2
    presence = SHENSHA_PROMINENT if prominent else "Có"
    if labels:
        evidence = "Có tại trụ " + " · ".join(labels)
    else:
        evidence = strip_internal_rule_ids(str(payload.get("evidence") or "").strip())
    return name, presence, evidence


def _rank_one(
    name: str,
    visible: Sequence[Mapping[str, Any]],
    hidden: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    vis = [item for item in visible if str(item.get("ten_god") or "").strip() == name]
    hid = [item for item in hidden if str(item.get("ten_god") or "").strip() == name]
    pillars = []
    for item in vis + hid:
        pillar = str(item.get("pillar") or "").strip()
        if pillar and pillar not in pillars:
            pillars.append(pillar)
    visible_count = len(vis)
    hidden_count = len(hid)
    klass = _classify(visible_count, hidden_count, len(pillars))
    return {
        "name": name,
        "klass": klass,
        "evidence": _evidence(name, vis, hid, klass),
        "visible_count": visible_count,
        "hidden_count": hidden_count,
        "total_count": visible_count + hidden_count,
        "pillar_spread": len(pillars),
    }


def _classify(visible_count: int, hidden_count: int, pillar_spread: int) -> str:
    if visible_count >= 1:
        return PROMINENCE_VISIBLE
    if hidden_count >= _HIDDEN_STRONG_COUNT or (
        hidden_count >= _HIDDEN_REPEAT_COUNT and pillar_spread >= 2
    ):
        return PROMINENCE_HIDDEN_STRONG
    if hidden_count >= 1:
        return PROMINENCE_HIDDEN
    return PROMINENCE_ABSENT


def _prominence_sort_key(item: Mapping[str, Any]) -> tuple[int, str]:
    score = (
        int(item.get("visible_count") or 0) * 100
        + (50 if item.get("klass") == PROMINENCE_HIDDEN_STRONG else 0)
        + int(item.get("hidden_count") or 0) * 10
        + int(item.get("pillar_spread") or 0)
    )
    return (-score, str(item.get("name") or ""))


def _pick_featured(ranked: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    picked = [
        dict(item)
        for item in ranked
        if item.get("klass") in {PROMINENCE_VISIBLE, PROMINENCE_HIDDEN_STRONG}
    ][:_FEATURED_LIMIT]
    names = {str(item.get("name") or "") for item in picked}
    if len(picked) < _FEATURED_MIN:
        for item in ranked:
            if len(picked) >= _FEATURED_MIN:
                break
            name = str(item.get("name") or "")
            if item.get("klass") == PROMINENCE_HIDDEN and name not in names:
                picked.append(dict(item))
                names.add(name)
    return picked[:_FEATURED_LIMIT]


def _evidence(
    name: str,
    visible: Sequence[Mapping[str, Any]],
    hidden: Sequence[Mapping[str, Any]],
    klass: str,
) -> str:
    if klass == PROMINENCE_VISIBLE:
        stem = _first_stem(visible)
        where = []
        for item in visible:
            label = _PILLAR_LABELS.get(str(item.get("pillar") or ""), "")
            if label:
                where.append(f"trụ {label}")
        unique_where: list[str] = []
        for part in where:
            if part not in unique_where:
                unique_where.append(part)
        if name == "Tỷ Kiên":
            return f"{stem} xuất hiện ngoài Nhật can" if stem else "Xuất hiện ngoài Nhật can"
        visible_bit = f"{stem} lộ {' · '.join(unique_where)}" if stem else " · ".join(unique_where)
        if hidden:
            return f"{visible_bit}, đồng thời có tàng"
        return visible_bit
    stem = _first_stem(hidden)
    branches: list[str] = []
    for item in hidden:
        branch = str(item.get("branch") or "").strip()
        if branch and branch not in branches:
            branches.append(branch)
    if stem and len(branches) == 1 and len(hidden) >= 2:
        return f"{stem} xuất hiện tại {len(hidden)} chi {branches[0]}"
    pillars: list[str] = []
    for item in hidden:
        label = _PILLAR_LABELS.get(str(item.get("pillar") or ""), "")
        if label and label not in pillars:
            pillars.append(label)
    if stem and pillars:
        if len(hidden) >= 2:
            return f"{stem} xuất hiện lặp trong tàng can ({' · '.join(pillars)})"
        return f"{stem} tàng trụ {pillars[0]}"
    return "Có tàng can" if hidden else ""


def _is_day_master_visible(item: Mapping[str, Any], day_master_stem: str) -> bool:
    if str(item.get("pillar") or "") == "day":
        return True
    if _is_day_master_label(str(item.get("ten_god") or "")):
        return True
    if str(item.get("god_id") or "") == "day_master":
        return True
    if day_master_stem and str(item.get("stem") or "") == day_master_stem:
        return str(item.get("pillar") or "") == "day"
    return False


def _is_day_master_label(name: str) -> bool:
    return name.strip().lower() in _DAY_MASTER_LABELS


def _first_stem(items: Sequence[Mapping[str, Any]]) -> str:
    for item in items:
        stem = str(item.get("stem") or item.get("hidden_stem") or "").strip()
        if stem:
            return stem
    return ""


def _token(text: str, pattern: str) -> str:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        return ""
    return match.group(1).rstrip(".,;")
