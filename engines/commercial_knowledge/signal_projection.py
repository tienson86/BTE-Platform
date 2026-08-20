"""Project Analysis dict into retrieval signals and evaluate KU conditions."""

from __future__ import annotations

import re
from typing import Any


def project_analysis_signals(analysis: dict[str, Any] | None) -> dict[str, Any]:
    """
    Project orchestrator analysis bag into flat retrieval signals.

    Does not invent analytical facts — only normalizes existing fields.
    """
    data = analysis if isinstance(analysis, dict) else {}
    bazi = _as_dict(data.get("bazi"))
    strength = _as_dict(data.get("strength"))
    useful = _as_dict(data.get("useful_god"))
    pattern = _as_dict(data.get("pattern"))
    score = _as_dict(data.get("score"))

    day_master = _text(bazi.get("day_master"))
    pattern_label = _text(pattern.get("cach_cuc") or pattern.get("pattern"))
    strength_band = _text(
        strength.get("strength_level")
        or strength.get("band")
        or strength.get("value")
        or ""
    ).lower()
    strength_score = strength.get("strength_score", score.get("strength_score"))
    useful_god = _text(
        useful.get("useful_display")
        or useful.get("useful_god")
        or useful.get("overall_useful_god")
    )
    unfavorable = useful.get("unfavorable_gods")
    if not isinstance(unfavorable, list):
        unfavorable = []
    ky_than = _text(useful.get("unfavorable_display"))
    has_enemy = bool(unfavorable) or bool(ky_than)

    favorable_strength = _is_favorable_strength(strength_band, strength_score)
    weak_strength = _is_weak_strength(strength_band, strength_score)
    strength_band_label = _commercial_strength_band_label(
        strength_band,
        strength_score,
        favorable=favorable_strength,
        weak=weak_strength,
    )
    weakness_frame = "thin" if weak_strength else ("opposed" if has_enemy else "none")
    weakness_signal_label = _weakness_label(
        unfavorable,
        ky_than,
        weak_strength=weak_strength,
        favorable_strength=favorable_strength,
        strength_band_label=strength_band_label,
    )

    return {
        "day_master": day_master,
        "day_master_label": day_master or "nền tảng ngày",
        "pattern_label": pattern_label or "cấu trúc nghề chính",
        "strength_band": strength_band,
        "strength_band_label": strength_band_label,
        "strength_score": strength_score,
        "strength_score_favorable": favorable_strength,
        "has_day_master": bool(day_master),
        "has_pattern_or_strength_band": bool(
            pattern_label or strength_band or strength_score is not None
        ),
        "has_useful_god": bool(useful_god),
        "useful_god": useful_god,
        "useful_god_label": useful_god or "trục hỗ trợ",
        "has_enemy_or_clash_caution": has_enemy or weak_strength,
        "weakness_frame": weakness_frame,
        "weakness_signal_label": weakness_signal_label,
        "weakness_statement": _weakness_statement(weakness_frame, weakness_signal_label),
        "weakness_risk": _weakness_risk(weakness_frame),
        "weakness_mitigation": _weakness_mitigation(weakness_frame),
        "grade": _text(score.get("grade")),
        "raw_strength_band": strength_band,
    }


def evaluate_condition(condition: str, signals: dict[str, Any]) -> bool:
    """Evaluate a Wave 1.1 KU condition string against projected signals."""
    text = (condition or "").strip()
    if not text:
        return False
    # Support simple AND chains.
    parts = [part.strip() for part in re.split(r"\bAND\b", text, flags=re.IGNORECASE)]
    return all(_eval_clause(part, signals) for part in parts if part)


def bind_placeholders(template: str, signals: dict[str, Any]) -> str | None:
    """
    Bind {placeholders} from signals.

    Returns None if any required placeholder is missing/empty.
    """
    text = template or ""
    missing: list[str] = []

    def _replace(match: re.Match[str]) -> str:
        key = match.group(1)
        value = signals.get(key)
        if value is None or str(value).strip() == "":
            missing.append(key)
            return match.group(0)
        return str(value)

    bound = re.sub(r"\{([a-zA-Z0-9_]+)\}", _replace, text)
    if missing:
        return None
    return bound.strip()


def _eval_clause(clause: str, signals: dict[str, Any]) -> bool:
    clause = clause.strip()
    # analysis.foo = true/false
    eq = re.match(
        r"^analysis\.([a-zA-Z0-9_]+)\s*=\s*(true|false)$",
        clause,
        flags=re.IGNORECASE,
    )
    if eq:
        key = eq.group(1)
        expected = eq.group(2).lower() == "true"
        return bool(signals.get(key)) is expected

    # analysis.foo IN (a;b;c)
    inn = re.match(
        r"^analysis\.([a-zA-Z0-9_]+)\s+IN\s*\(([^)]*)\)$",
        clause,
        flags=re.IGNORECASE,
    )
    if inn:
        key = inn.group(1)
        options = [
            item.strip().lower()
            for item in inn.group(2).replace(",", ";").split(";")
            if item.strip()
        ]
        value = str(signals.get(key) or "").lower()
        if not value:
            return False
        return any(opt in value or value == opt for opt in options)

    # analysis.foo (truthy)
    bare = re.match(r"^analysis\.([a-zA-Z0-9_]+)$", clause, flags=re.IGNORECASE)
    if bare:
        return bool(signals.get(bare.group(1)))

    # OR inside clause
    if re.search(r"\bOR\b", clause, flags=re.IGNORECASE):
        return any(
            _eval_clause(part.strip(), signals)
            for part in re.split(r"\bOR\b", clause, flags=re.IGNORECASE)
            if part.strip()
        )
    return False


def _canonical_strength_unit(score: Any) -> float | None:
    """Map published Strength score onto 0–1. Never treat Score Engine 0–100 as thân."""
    try:
        value = float(score)
    except (TypeError, ValueError):
        return None
    if value > 1.5:
        return value / 100.0
    return value


def _is_favorable_strength(band: str, score: Any) -> bool:
    tokens = ("vuong", "vượng", "strong", "support")
    if any(token in band for token in tokens):
        return True
    if any(token in band for token in ("nhuoc", "nhược", "weak", "suy", "can", "cân", "balance")):
        return False
    unit = _canonical_strength_unit(score)
    if unit is None:
        return False
    return unit >= 0.60


def _is_weak_strength(band: str, score: Any) -> bool:
    tokens = ("nhuoc", "nhược", "weak", "overtaxed", "suy")
    if any(token in band for token in tokens):
        return True
    if any(token in band for token in ("vuong", "vượng", "strong", "can", "cân", "balance")):
        return False
    unit = _canonical_strength_unit(score)
    if unit is None:
        return False
    return unit < 0.40


def _commercial_strength_band_label(
    band: str,
    score: Any,
    *,
    favorable: bool,
    weak: bool,
) -> str:
    """Map Analysis band tokens to customer-facing commercial labels."""
    if weak:
        return "đang mỏng lực"
    lowered = (band or "").lower()
    if any(token in lowered for token in ("can", "cân", "balance")):
        return "đang cân bằng"
    if favorable or any(token in lowered for token in ("vuong", "vượng", "strong")):
        return "được nâng đỡ"
    if band:
        # Unknown band — never echo raw engine tokens to customers.
        return "chưa xác định rõ"
    unit = _canonical_strength_unit(score)
    if unit is None:
        return "chưa xác định rõ"
    if unit < 0.40:
        return "đang mỏng lực"
    if unit < 0.60:
        return "đang cân bằng"
    return "được nâng đỡ"


def _weakness_label(
    unfavorable: list[Any],
    ky_than: str,
    *,
    weak_strength: bool,
    favorable_strength: bool,
    strength_band_label: str,
) -> str:
    """Build a unique, commercial caution phrase (no duplicated enemies/bands)."""
    seen: set[str] = set()
    parts: list[str] = []

    def _add(raw: str) -> None:
        label = raw.strip()
        if not label:
            return
        key = label.casefold()
        if key in seen:
            return
        seen.add(key)
        parts.append(label)

    for item in unfavorable[:3]:
        _add(str(item))
    _add(ky_than)

    if weak_strength:
        _add("thân đang mỏng lực")
    elif favorable_strength and parts:
        # Frame B: unique opposition labels only — do not claim thin structure.
        return "; ".join(parts)
    elif not parts and strength_band_label:
        _add(f"thân {strength_band_label}")

    return "; ".join(parts) if parts else "điểm hạn chế cấu trúc"


def _weakness_statement(frame: str, signal_label: str) -> str:
    """Opening Weakness sentence for Frame A (thin) or Frame B (opposed)."""
    label = signal_label.strip() or "điểm hạn chế cấu trúc"
    if frame == "opposed":
        return (
            f"Điểm cần giữ không phải vì bạn thiếu nền, mà vì có phần dễ kéo lệch: {label}."
        )
    return (
        f"Điểm cần giữ của bạn là chỗ lực cấu trúc đang mỏng hoặc dễ bị kéo quá mức: {label}."
    )


def _weakness_risk(frame: str) -> str:
    if frame == "opposed":
        return "Nếu chạy theo phần kỵ, dễ mất lợi thế đang có."
    return "Nếu mở rộng khi chưa giữ mực, dễ lệch nhịp và hao lực."


def _weakness_mitigation(frame: str) -> str:
    if frame == "opposed":
        return "Giữ biên và giảm những việc nuôi phần kỵ trước."
    return "Giảm tải và giữ nhịp trước khi mở rộng."


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()
