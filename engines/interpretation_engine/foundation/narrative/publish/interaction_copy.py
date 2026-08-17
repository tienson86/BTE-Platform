"""Copy Interaction Truth facts into customer sentences. No calculation."""

from __future__ import annotations

from typing import Any, Mapping

from engines.interpretation_engine.foundation.narrative.text import normalize_text


def interaction_from_payload(payload: Mapping[str, Any] | None) -> dict[str, Any]:
    """Read stamped Interaction Truth. Empty when missing."""
    if not isinstance(payload, Mapping):
        return {}
    metadata = payload.get("metadata")
    if not isinstance(metadata, Mapping):
        return {}
    raw = metadata.get("interaction_truth")
    return dict(raw) if isinstance(raw, Mapping) else {}


def luck_paragraphs_from_interaction(data: Mapping[str, Any]) -> list[str]:
    """Current Da Yun consultation from Interaction Facts only. Not natal thesis."""
    if not data:
        return []
    period = data.get("current_period_identity") or {}
    summary = data.get("interaction_summary") or {}
    status = str(data.get("status") or "")
    label = str(period.get("label") or summary.get("period_label") or "").strip()
    if not label:
        return []
    if status == "missing":
        return [
            (
                f"Đại vận đang sống là {label}. "
                "Chưa đủ dữ liệu tương tác để luận thập niên này, "
                "không lặp luận giải gốc."
            )
        ]

    paragraphs = [
        (
            f"Đại vận đang sống là {label}. "
            "Đây là thập niên đang luận, không phải toàn bộ chuỗi đại vận."
        ),
        _summary_sentence(label, summary),
        _helpful_sentence(label, data),
        _pressure_sentence(label, data),
        _supported_sentence(label, data),
        _restricted_sentence(label, data),
        _next_sentence(label, period),
    ]
    return [normalize_text(item) for item in paragraphs if item]


def career_overlay_from_interaction(data: Mapping[str, Any]) -> str:
    """Optional career overlay from evidenced overlap. Not a natal thesis paste."""
    return _domain_overlay(data, area="sự nghiệp")


def finance_overlay_from_interaction(data: Mapping[str, Any]) -> str:
    """Optional finance overlay from evidenced overlap."""
    return _domain_overlay(data, area="tài chính")


def relationship_overlay_from_interaction(data: Mapping[str, Any]) -> str:
    """Optional relationship overlay from evidenced overlap."""
    return _domain_overlay(data, area="quan hệ")


def health_overlay_from_interaction(data: Mapping[str, Any]) -> str:
    """Optional health overlay from evidenced overlap."""
    return _domain_overlay(data, area="sức khỏe")


def recommendation_overlay_from_interaction(data: Mapping[str, Any]) -> str:
    """Now-only recommendation when period identity overlaps natal support."""
    label = _label(data)
    helpful = _factor_names(data.get("helpful_factors") or [])
    if not label:
        return ""
    if helpful:
        names = ", ".join(helpful)
        return (
            f"Trong {label}, ưu tiên hướng đã trùng danh tính Đại vận: {names}. "
            "Không đổi Dụng thần đã luận trên lá số."
        )
    return (
        f"Trong {label}, chưa có danh tính Đại vận trùng Dụng thần hoặc Hỷ thần; "
        "giữ hướng đã luận, không gắn khuyến nghị gốc vào thập niên."
    )


def conclusion_overlay_from_interaction(data: Mapping[str, Any]) -> str:
    """One period-true close. Not a second natal thesis."""
    label = _label(data)
    if not label:
        return ""
    summary = data.get("interaction_summary") or {}
    useful = str(summary.get("useful_god") or "").strip() or "đã chọn"
    if summary.get("empty_overlap"):
        return (
            f"Trong {label}, lá số vẫn do Dụng {useful} giữ; "
            "chưa có danh tính Đại vận trùng Hỷ thần hoặc Kỵ thần đã công bố."
        )
    helpful = _factor_names(data.get("helpful_factors") or [])
    pressure = _factor_names(data.get("pressure_factors") or [])
    parts = [f"Thập niên {label} gặp danh tính Đại vận đã công bố"]
    if helpful:
        parts.append(f"trùng hỗ trợ {', '.join(helpful)}")
    if pressure:
        parts.append(f"trùng áp lực {', '.join(pressure)}")
    return "; ".join(parts) + ". Không đổi quyết định đã luận trên lá số."


def _summary_sentence(label: str, summary: Mapping[str, Any]) -> str:
    """Governors in force plus overlap flag."""
    pattern = str(summary.get("pattern") or "").strip() or "cục đã luận"
    strength = str(summary.get("strength") or "").strip() or "thân đã luận"
    useful = str(summary.get("useful_god") or "").strip() or "Dụng đã chọn"
    if summary.get("empty_overlap"):
        overlap = "không trùng danh tính nào với Dụng thần, Hỷ thần hoặc Kỵ thần đã công bố"
    else:
        count = int(summary.get("overlap_count") or 0)
        overlap = f"trùng {count} danh tính đã công bố với Dụng thần, Hỷ thần hoặc Kỵ thần"
    return (
        f"Trong {label}, lá số vẫn do {pattern}, {strength}, Dụng {useful} giữ. "
        f"So khớp danh tính Đại vận đã công bố: {overlap}."
    )


def _helpful_sentence(label: str, data: Mapping[str, Any]) -> str:
    """Helpful overlaps, or honest empty list."""
    factors = list(data.get("helpful_factors") or [])
    if not factors:
        return (
            f"Không có danh tính Đại vận đã công bố trùng Dụng thần hoặc Hỷ thần trong {label}."
        )
    parts = [
        f"{item.get('natal_identity')} trùng {item.get('period_identity')} "
        f"qua {_field_label(str(item.get('period_field') or ''))}"
        for item in factors
        if isinstance(item, Mapping)
    ]
    return f"Yếu tố hỗ trợ đã trùng trong {label}: {'; '.join(parts)}."


def _pressure_sentence(label: str, data: Mapping[str, Any]) -> str:
    """Pressure overlaps, or honest empty list."""
    factors = list(data.get("pressure_factors") or [])
    if not factors:
        return (
            f"Không có danh tính Đại vận đã công bố trùng Kỵ thần trong {label}."
        )
    parts = [
        f"{item.get('natal_identity')} trùng {item.get('period_identity')} "
        f"qua {_field_label(str(item.get('period_field') or ''))}"
        for item in factors
        if isinstance(item, Mapping)
    ]
    return f"Yếu tố áp lực đã trùng trong {label}: {'; '.join(parts)}."


def _supported_sentence(label: str, data: Mapping[str, Any]) -> str:
    """Natal Useful God / Hỷ still in force, with overlap qualifier."""
    direction = data.get("supported_direction") or {}
    names = [str(item) for item in (direction.get("identities") or []) if item]
    named = ", ".join(names) if names else "Dụng thần / Hỷ thần đã luận"
    qualifier = _qualifier(str(direction.get("overlap_status") or ""))
    return f"Hướng được giữ trong {label} vẫn là {named}; {qualifier}."


def _restricted_sentence(label: str, data: Mapping[str, Any]) -> str:
    """Natal Kỵ still in force, with overlap qualifier."""
    direction = data.get("restricted_direction") or {}
    names = [str(item) for item in (direction.get("identities") or []) if item]
    if not names:
        return f"Không có Kỵ thần đã công bố để hạn chế trong {label}."
    qualifier = _qualifier(str(direction.get("overlap_status") or ""))
    return f"Hướng bị hạn chế trong {label} vẫn là {', '.join(names)}; {qualifier}."


def _next_sentence(label: str, period: Mapping[str, Any]) -> str:
    """Next cycle is identity only and not current."""
    nxt = str(period.get("next_label") or period.get("next_gan_zhi") or "").strip()
    if not nxt or nxt == label:
        return (
            f"Không luận toàn bộ chuỗi đại vận. Giữ hướng đã chọn đến hết {label}."
        )
    return (
        f"Đại vận kế tiếp đã có trên lá số là {nxt}; đó chưa phải thập niên đang sống. "
        f"Không luận mười vòng. Giữ hướng hiện tại đến hết {label}."
    )


def _domain_overlay(data: Mapping[str, Any], *, area: str) -> str:
    """One overlap overlay for a life area. Empty overlap does not paste natal thesis."""
    label = _label(data)
    if not label:
        return ""
    helpful = _factor_names(data.get("helpful_factors") or [])
    pressure = _factor_names(data.get("pressure_factors") or [])
    if helpful or pressure:
        bits: list[str] = []
        if helpful:
            bits.append(f"trùng hỗ trợ {', '.join(helpful)}")
        if pressure:
            bits.append(f"trùng áp lực {', '.join(pressure)}")
        return (
            f"Trong {label}, {area} chịu danh tính Đại vận đã công bố: {'; '.join(bits)}. "
            "Đây không phải luận giải gốc gắn nhãn thập niên."
        )
    return (
        f"Trong {label}, chưa có danh tính Đại vận trùng Dụng thần, Hỷ thần hoặc Kỵ thần "
        f"cho {area}; không lặp luận giải gốc như thể đó là hiệu ứng thập niên."
    )


def _qualifier(status: str) -> str:
    """Overlap qualifier copied from Interaction Facts."""
    if status == "overlapped":
        return "có trùng danh tính Đại vận đã công bố"
    if status == "missing":
        return "chưa đủ dữ liệu để so khớp danh tính"
    return "chưa có trùng danh tính Đại vận đã công bố"


def _field_label(field: str) -> str:
    """Customer label for a copied luck field path."""
    mapping = {
        "LuckEngine.current_dayun.heavenly_stem": "thiên can Đại vận",
        "LuckEngine.current_dayun.earthly_branch": "địa chi Đại vận",
        "LuckEngine.current_dayun.element": "ngũ hành Đại vận",
        "LuckEngine.current_dayun.ten_god": "thập thần Đại vận",
        "LuckEngine.current_dayun.hidden_stems": "tàng can Đại vận",
    }
    return mapping.get(field, "danh tính Đại vận đã công bố")


def _label(data: Mapping[str, Any]) -> str:
    """Current period label from stamped facts."""
    period = data.get("current_period_identity") or {}
    summary = data.get("interaction_summary") or {}
    return str(period.get("label") or summary.get("period_label") or "").strip()


def _factor_names(factors: list[Any]) -> list[str]:
    """Unique natal identities from overlap factors."""
    names: list[str] = []
    seen: set[str] = set()
    for item in factors:
        if not isinstance(item, Mapping):
            continue
        name = str(item.get("natal_identity") or "").strip()
        if not name or name in seen:
            continue
        seen.add(name)
        names.append(name)
    return names
