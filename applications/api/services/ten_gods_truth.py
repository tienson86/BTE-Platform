"""Public Ten Gods contract from TenGodsEngine. Copies facts; does not recalculate."""

from __future__ import annotations

from typing import Any, Mapping

from engines.ten_gods_engine.models import TenGodsResult

TEN_GODS_NOTE = "Xác định theo quan hệ Ngũ hành và âm dương với Nhật chủ."
TEN_GODS_SOURCE = "engines.ten_gods_engine"


def ten_gods_source_fingerprint() -> dict[str, str]:
    """Provenance block for API meta."""
    return {
        "engine": "engines.ten_gods_engine.engine.TenGodsEngine",
        "method": "calculate",
        "contract": "ten_gods_result_v1",
        "view": "applications.api.services.ten_gods_truth.shape_ten_gods_payload",
    }


def shape_ten_gods_payload(result: TenGodsResult | Mapping[str, Any] | None) -> dict[str, Any]:
    """Publish structured visible and hidden Ten Gods without recalculating.

    ``hidden`` is mapped Ten God occurrences, not a raw tàng can name list.
    Compact label lists remain for older string consumers.
    """
    if result is None:
        return {
            "visible": [],
            "hidden": [],
            "visible_labels": [],
            "hidden_labels": [],
            "visible_summary": "",
            "hidden_summary": "",
            "summary": "",
            "note": TEN_GODS_NOTE,
            "source": TEN_GODS_SOURCE,
        }
    raw = result.to_dict() if hasattr(result, "to_dict") else dict(result)
    visible = [_public_visible(item) for item in (raw.get("visible") or [])]
    hidden = [_public_hidden(item) for item in (raw.get("hidden") or [])]
    visible_labels = [str(item.get("ten_god") or "") for item in visible if item.get("ten_god")]
    hidden_labels = [str(item.get("ten_god") or "") for item in hidden if item.get("ten_god")]
    visible_summary = " · ".join(visible_labels)
    hidden_summary = " · ".join(_unique(hidden_labels))
    day_master = raw.get("day_master") if isinstance(raw.get("day_master"), Mapping) else {}
    return {
        "day_master": dict(day_master or {}),
        "visible": visible,
        "hidden": hidden,
        "visible_labels": visible_labels,
        "hidden_labels": hidden_labels,
        "visible_summary": visible_summary,
        "hidden_summary": hidden_summary,
        "summary": visible_summary,
        "note": TEN_GODS_NOTE,
        "source": TEN_GODS_SOURCE,
    }


def format_hidden_line(item: Mapping[str, Any]) -> str:
    """Compact hidden occurrence: Giáp · Mộc · Thiên Tài."""
    stem = str(item.get("hidden_stem") or item.get("stem") or "").strip()
    element = str(item.get("element") or "").strip()
    ten_god = str(item.get("ten_god") or "").strip()
    parts = [part for part in (stem, element, ten_god) if part]
    return " · ".join(parts)


def format_visible_line(item: Mapping[str, Any]) -> str:
    """Compact visible occurrence: Bính · Hỏa / Thất Sát."""
    stem = str(item.get("stem") or "").strip()
    element = str(item.get("element") or "").strip()
    ten_god = str(item.get("ten_god") or "").strip()
    head = " · ".join(part for part in (stem, element) if part)
    if head and ten_god:
        return f"{head} / {ten_god}"
    return ten_god or head


def _public_visible(item: Mapping[str, Any]) -> dict[str, Any]:
    """Copy one visible engine entry for Portal / Report."""
    return {
        "pillar": str(item.get("pillar") or ""),
        "stem": str(item.get("stem") or ""),
        "element": str(item.get("element") or ""),
        "yin_yang": str(item.get("yin_yang") or ""),
        "element_relation": str(item.get("element_relation") or ""),
        "polarity_relation": str(item.get("polarity_relation") or ""),
        "ten_god": str(item.get("ten_god") or ""),
        "god_id": str(item.get("god_id") or ""),
        "visibility": str(item.get("visibility") or "visible"),
        "evidence": str(item.get("evidence") or ""),
    }


def _public_hidden(item: Mapping[str, Any]) -> dict[str, Any]:
    """Copy one hidden engine entry for Portal / Report."""
    return {
        "pillar": str(item.get("pillar") or ""),
        "branch": str(item.get("branch") or ""),
        "position_name": str(item.get("position_name") or ""),
        "hidden_position": item.get("hidden_position"),
        "hidden_stem": str(item.get("hidden_stem") or ""),
        "stem": str(item.get("hidden_stem") or ""),
        "element": str(item.get("element") or ""),
        "yin_yang": str(item.get("yin_yang") or ""),
        "element_relation": str(item.get("element_relation") or ""),
        "polarity_relation": str(item.get("polarity_relation") or ""),
        "ten_god": str(item.get("ten_god") or ""),
        "god_id": str(item.get("god_id") or ""),
        "visibility": "hidden",
        "weight": item.get("weight"),
        "evidence": str(item.get("evidence") or ""),
        "display": format_hidden_line(item),
    }


def _unique(values: list[str]) -> list[str]:
    """Keep first occurrence of each label."""
    return list(dict.fromkeys(item for item in values if item))
