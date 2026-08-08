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
    useful_god = _text(useful.get("useful_god") or pattern.get("dung_than"))
    unfavorable = useful.get("unfavorable_gods")
    if not isinstance(unfavorable, list):
        unfavorable = []
    ky_than = _text(pattern.get("ky_than"))
    has_enemy = bool(unfavorable) or bool(ky_than)

    favorable_strength = _is_favorable_strength(strength_band, strength_score)
    weak_strength = _is_weak_strength(strength_band, strength_score)

    return {
        "day_master": day_master,
        "day_master_label": day_master or "Nhật chủ",
        "pattern_label": pattern_label or "cấu trúc chính",
        "strength_band": strength_band,
        "strength_band_label": strength_band or "chưa xác định",
        "strength_score": strength_score,
        "strength_score_favorable": favorable_strength,
        "has_day_master": bool(day_master),
        "has_pattern_or_strength_band": bool(pattern_label or strength_band or strength_score is not None),
        "has_useful_god": bool(useful_god),
        "useful_god": useful_god,
        "useful_god_label": useful_god or "Dụng thần",
        "has_enemy_or_clash_caution": has_enemy or weak_strength,
        "weakness_signal_label": _weakness_label(unfavorable, ky_than, strength_band),
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


def _is_favorable_strength(band: str, score: Any) -> bool:
    tokens = ("vuong", "vượng", "can", "cân", "strong", "support", "vượng")
    if any(token in band for token in tokens):
        return True
    try:
        return float(score) >= 55.0
    except (TypeError, ValueError):
        return False


def _is_weak_strength(band: str, score: Any) -> bool:
    tokens = ("nhuoc", "nhược", "weak", "overtaxed", "suy")
    if any(token in band for token in tokens):
        return True
    try:
        return float(score) < 45.0
    except (TypeError, ValueError):
        return False


def _weakness_label(unfavorable: list[Any], ky_than: str, band: str) -> str:
    parts: list[str] = []
    if unfavorable:
        parts.append(", ".join(str(item) for item in unfavorable[:3]))
    if ky_than:
        parts.append(ky_than)
    if band:
        parts.append(f"mức thân {band}")
    return "; ".join(parts) if parts else "điểm hạn chế cấu trúc"


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()
