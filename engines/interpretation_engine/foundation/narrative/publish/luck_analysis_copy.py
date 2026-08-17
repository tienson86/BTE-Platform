"""Copy LuckAnalysisFacts into customer sentences. No calculation. No overlap inference."""

from __future__ import annotations

from typing import Any, Mapping

from engines.interpretation_engine.foundation.narrative.text import normalize_text

_INSUFFICIENT = (
    "phân tích production hiện tại chưa xác định thêm tương tác ngoài luận giải gốc"
)


def luck_analysis_from_payload(payload: Mapping[str, Any] | None) -> dict[str, Any]:
    """Read stamped Luck Analysis. Empty when missing."""
    if not isinstance(payload, Mapping):
        return {}
    metadata = payload.get("metadata")
    if not isinstance(metadata, Mapping):
        return {}
    raw = metadata.get("luck_analysis")
    return dict(raw) if isinstance(raw, Mapping) else {}


def luck_paragraphs_from_analysis(data: Mapping[str, Any]) -> list[str]:
    """Current Da Yun consultation from Luck Analysis Facts only."""
    if not data:
        return []
    period = data.get("current_period_identity") or {}
    status = str(data.get("status") or "")
    label = str(period.get("label") or "").strip()
    if not label:
        return []
    if status == "missing":
        return [
            (
                f"Đại vận đang sống là {label}. "
                f"{_INSUFFICIENT.capitalize()}. Không lặp luận giải gốc."
            )
        ]
    paragraphs = [
        _identity_sentence(label, period),
        _period_roles_sentence(label, period),
        _natal_governors_sentence(label, data),
        _helpful_sentence(label, data),
        _pressure_sentence(label, data),
        _direction_sentence(label, data),
        _next_sentence(label, period),
    ]
    return [normalize_text(item) for item in paragraphs if item]


def career_overlay_from_analysis(data: Mapping[str, Any]) -> str:
    """Career overlay from production luck analysis. Not natal thesis."""
    return _area_overlay(data, area="sự nghiệp")


def finance_overlay_from_analysis(data: Mapping[str, Any]) -> str:
    """Finance overlay from production luck analysis."""
    return _area_overlay(data, area="tài chính")


def relationship_overlay_from_analysis(data: Mapping[str, Any]) -> str:
    """Relationship overlay from production luck analysis."""
    return _area_overlay(data, area="quan hệ")


def health_overlay_from_analysis(data: Mapping[str, Any]) -> str:
    """Health overlay from production luck analysis."""
    return _area_overlay(data, area="sức khỏe")


def recommendation_overlay_from_analysis(data: Mapping[str, Any]) -> str:
    """Now-only recommendation from production relations, or honest gap."""
    label = _label(data)
    if not label:
        return ""
    helpful = _relation_names(data.get("helpful_relations") or [])
    if helpful:
        return (
            f"Trong {label}, ưu tiên hướng production đã công bố hỗ trợ: "
            f"{', '.join(helpful)}. Không đổi Dụng thần đã luận trên lá số."
        )
    return f"Trong {label}, {_INSUFFICIENT}. Không gắn khuyến nghị gốc vào thập niên."


def conclusion_overlay_from_analysis(data: Mapping[str, Any]) -> str:
    """Period-true close from Luck Analysis. Not a second natal thesis."""
    label = _label(data)
    if not label:
        return ""
    period = data.get("current_period_identity") or {}
    ten_god = str(period.get("ten_god") or "").strip()
    helpful = _relation_names(data.get("helpful_relations") or [])
    pressure = _relation_names(data.get("pressure_relations") or [])
    if helpful or pressure:
        bits: list[str] = []
        if helpful:
            bits.append(f"hỗ trợ {', '.join(helpful)}")
        if pressure:
            bits.append(f"áp lực {', '.join(pressure)}")
        return (
            f"Thập niên {label} giữ thập thần Đại vận đã công bố"
            f"{f' {ten_god}' if ten_god else ''}; production công bố {'; '.join(bits)}. "
            "Không đổi quyết định đã luận trên lá số."
        )
    extra = f" Thập thần Đại vận đã công bố là {ten_god}." if ten_god else ""
    return f"Trong {label}, {_INSUFFICIENT}.{extra} Không lặp luận giải gốc."


def _identity_sentence(label: str, period: Mapping[str, Any]) -> str:
    """Name the living decade from LuckEngine identity."""
    return (
        f"Đại vận đang sống là {label}. "
        "Đây là thập niên đang luận, không phải toàn bộ chuỗi đại vận."
    )


def _period_roles_sentence(label: str, period: Mapping[str, Any]) -> str:
    """Copy LuckEngine period analysis already published on the pillar."""
    stem = str(period.get("stem") or "").strip()
    branch = str(period.get("branch") or "").strip()
    element = str(period.get("element") or "").strip()
    yin_yang = str(period.get("yin_yang") or "").strip()
    ten_god = str(period.get("ten_god") or "").strip()
    hidden = [str(item) for item in (period.get("hidden_stems") or []) if item]
    details: list[str] = []
    if stem:
        detail = stem
        extras = [item for item in (yin_yang, element) if item]
        if extras:
            detail = f"{stem} ({', '.join(extras)})"
        details.append(f"thiên can {detail}")
    if branch:
        details.append(f"địa chi {branch}")
    if ten_god:
        details.append(f"thập thần Đại vận {ten_god}")
    body = ", ".join(details) if details else "cột trụ Đại vận đã công bố"
    sentence = f"Trong {label}, production đã công bố {body}."
    if hidden:
        sentence = f"{sentence} Tàng can đã công bố: {', '.join(hidden)}."
    return sentence


def _natal_governors_sentence(label: str, data: Mapping[str, Any]) -> str:
    """Natal governors remain natal. They are not decade effects."""
    natal = [
        str(item.get("name") or "")
        for item in (data.get("governing_roles") or [])
        if isinstance(item, Mapping) and item.get("scope") == "natal" and item.get("name")
    ]
    unique = list(dict.fromkeys(name for name in natal if name))
    named = ", ".join(unique[:4]) if unique else "các quyết định đã luận"
    return (
        f"Trong {label}, lá số vẫn do {named} giữ. "
        "Đây là luận giải gốc, không phải hiệu ứng thập niên."
    )


def _helpful_sentence(label: str, data: Mapping[str, Any]) -> str:
    """Production support only. Empty when LuckEngine left support UNKNOWN."""
    names = _relation_names(data.get("helpful_relations") or [])
    if names:
        return (
            f"Hành hỗ trợ production đã công bố trong {label}: {', '.join(names)}."
        )
    return f"Trong {label}, {_INSUFFICIENT}."


def _pressure_sentence(label: str, data: Mapping[str, Any]) -> str:
    """Production attack only. Skip a second insufficient sentence."""
    names = _relation_names(data.get("pressure_relations") or [])
    if names:
        return (
            f"Hành áp lực production đã công bố trong {label}: {', '.join(names)}."
        )
    if _relation_names(data.get("helpful_relations") or []):
        return (
            f"Trong {label}, production chưa công bố hành áp lực cụ thể cho thập niên này."
        )
    return ""


def _direction_sentence(label: str, data: Mapping[str, Any]) -> str:
    """Natal Useful God / Kỵ remain in force without decade overlap claims."""
    supported = [
        str(item)
        for item in ((data.get("supported_direction") or {}).get("identities") or [])
        if item
    ]
    restricted = [
        str(item)
        for item in ((data.get("restricted_direction") or {}).get("identities") or [])
        if item
    ]
    keep = ", ".join(supported) if supported else "Dụng thần đã luận"
    sentence = f"Hướng natal được giữ trong {label} vẫn là {keep}."
    if restricted:
        sentence = (
            f"{sentence} Hướng natal bị hạn chế vẫn là {', '.join(restricted)}."
        )
    return sentence


def _next_sentence(label: str, period: Mapping[str, Any]) -> str:
    """Next cycle is identity only and not current."""
    nxt = str(period.get("next_label") or period.get("next_gan_zhi") or "").strip()
    if not nxt or nxt == label:
        return f"Không luận toàn bộ chuỗi đại vận. Giữ hướng đã chọn đến hết {label}."
    return (
        f"Đại vận kế tiếp đã có trên lá số là {nxt}; đó chưa phải thập niên đang sống. "
        f"Không luận mười vòng. Giữ hướng hiện tại đến hết {label}."
    )


def _area_overlay(data: Mapping[str, Any], *, area: str) -> str:
    """One life-area overlay from production relations, or honest gap."""
    label = _label(data)
    if not label:
        return ""
    helpful = _relation_names(data.get("helpful_relations") or [])
    pressure = _relation_names(data.get("pressure_relations") or [])
    if helpful or pressure:
        bits: list[str] = []
        if helpful:
            bits.append(f"hỗ trợ {', '.join(helpful)}")
        if pressure:
            bits.append(f"áp lực {', '.join(pressure)}")
        return (
            f"Trong {label}, {area} chịu phân tích production đã công bố: "
            f"{'; '.join(bits)}. Không lấy luận giải gốc làm hiệu ứng thập niên."
        )
    return (
        f"Trong {label}, {_INSUFFICIENT}. "
        f"Không lặp luận giải gốc cho {area} như thể đó là Đại vận."
    )


def _relation_names(relations: list[Any]) -> list[str]:
    """Flatten production relation identities."""
    names: list[str] = []
    seen: set[str] = set()
    for item in relations:
        if not isinstance(item, Mapping):
            continue
        for name in item.get("identities") or []:
            text = str(name).strip()
            if not text or text in seen:
                continue
            seen.add(text)
            names.append(text)
    return names


def _label(data: Mapping[str, Any]) -> str:
    """Current period label from stamped facts."""
    period = data.get("current_period_identity") or {}
    return str(period.get("label") or "").strip()
