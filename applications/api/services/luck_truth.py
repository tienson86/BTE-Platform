"""Public Luck / Đại Vận contract from LuckEngine output."""

from __future__ import annotations

from typing import Any, Mapping

from engines.bazi_engine.ten_god import branch_element, stem_element, stem_yin_yang
from engines.luck_engine.providers._common import (
    CURRENT_AGE_BASIS,
    DIRECTION_LABELS,
    GENDER_LABELS,
    METHOD_NOTE_VI,
    PRECISION_LEVEL,
)


def shape_luck_payload(luck: Any) -> dict[str, Any]:
    """
    Publish structured Luck data without recalculating Da Yun.

    Reads the existing engine sequence from ``current_dayun.metadata.sequence``.
    """
    raw = luck.to_dict() if hasattr(luck, "to_dict") else dict(luck or {})
    current = raw.get("current_dayun") or {}
    if not isinstance(current, Mapping):
        current = {}
    metadata = dict(current.get("metadata") or {})
    sequence = metadata.get("sequence") or []
    if not isinstance(sequence, list):
        sequence = []
    cycles = [_cycle_from_item(item, index) for index, item in enumerate(sequence)]
    direction = str(metadata.get("direction") or "")
    if not direction and sequence and isinstance(sequence[0], Mapping):
        direction = str((sequence[0].get("metadata") or {}).get("direction") or "")
    direction_label = str(
        metadata.get("direction_label") or DIRECTION_LABELS.get(direction, "")
    )
    start_age = None
    if cycles:
        start_age = cycles[0].get("age_start")
    calc = metadata.get("start_age_calc") or {}
    if not isinstance(calc, Mapping):
        calc = {}
    if start_age is None:
        start_age = calc.get("start_age") or calc.get("age")
    current_cycle = None
    if isinstance(current, Mapping) and current and current.get("heavenly_stem"):
        current_cycle = _cycle_from_item(current, int(current.get("index") or 0))
    elif cycles:
        current_cycle = cycles[0]
    gender = str(metadata.get("gender") or "")
    year_stem = str(metadata.get("year_stem") or "")
    polarity = str(metadata.get("year_stem_polarity") or stem_yin_yang(year_stem))
    gender_label = str(metadata.get("gender_label") or GENDER_LABELS.get(gender, ""))
    evidence = _evidence_line(gender_label, year_stem, polarity, direction_label)
    method_note = str(metadata.get("method_note") or METHOD_NOTE_VI)
    precision = str(metadata.get("precision") or PRECISION_LEVEL)
    current_age_for_luck = metadata.get("current_age_for_luck", metadata.get("age_at_reference"))
    payload = {
        "available": bool(raw.get("available")),
        "reason": raw.get("reason"),
        "direction": direction,
        "direction_label": direction_label,
        "start_age": start_age,
        "current_cycle": current_cycle,
        "cycles": cycles,
        "current_dayun": dict(current),
        "evidence": evidence,
        "method_note": method_note,
        "precision": precision,
        "current_age_for_luck": current_age_for_luck,
        "current_age_basis": str(metadata.get("current_age_basis") or CURRENT_AGE_BASIS),
        "gender": gender,
        "gender_label": gender_label,
        "year_stem": year_stem,
        "year_stem_polarity": polarity,
        "start_age_calc": dict(calc),
        "metadata": dict(raw.get("metadata") or {}),
        "support_elements": list(raw.get("support_elements") or []),
        "attack_elements": list(raw.get("attack_elements") or []),
        "support_level": raw.get("support_level"),
        "attack_level": raw.get("attack_level"),
        "luck_stage": raw.get("luck_stage"),
        "luck_strength": raw.get("luck_strength"),
        "luck_summary": raw.get("luck_summary"),
        "confidence": raw.get("confidence"),
    }
    annual_identity = _annual_identity(raw.get("current_liunian"))
    if annual_identity:
        payload["annual_identity"] = annual_identity
    return payload


def _evidence_line(
    gender_label: str,
    year_stem: str,
    polarity: str,
    direction_label: str,
) -> str:
    """Compact V1.0 direction evidence. Timeline only — no cát/hung."""
    parts = [part for part in (gender_label, ) if part]
    if year_stem and polarity:
        parts.append(f"Niên can {year_stem} {polarity}")
    elif year_stem:
        parts.append(f"Niên can {year_stem}")
    if direction_label:
        parts.append(direction_label)
    return " · ".join(parts)


def _cycle_from_item(item: Any, fallback_index: int) -> dict[str, Any]:
    data = item if isinstance(item, Mapping) else {}
    stem = str(data.get("heavenly_stem") or data.get("stem") or "")
    branch = str(data.get("earthly_branch") or data.get("branch") or "")
    gan_zhi = str(data.get("ganzhi") or data.get("gan_zhi") or "").strip()
    if not gan_zhi:
        gan_zhi = f"{stem} {branch}".strip()
    stem_el = str(data.get("stem_element") or data.get("element") or stem_element(stem))
    branch_el = str(data.get("branch_element") or branch_element(branch))
    return {
        "index": int(data.get("index") if data.get("index") is not None else fallback_index),
        "age_start": data.get("start_age", data.get("age_start")),
        "age_end": data.get("end_age", data.get("age_end")),
        "year_start": data.get("start_year", data.get("year_start")),
        "year_end": data.get("end_year", data.get("year_end")),
        "gan_zhi": gan_zhi,
        "stem": stem,
        "branch": branch,
        "stem_element": stem_el,
        "branch_element": branch_el,
    }


def _annual_identity(raw: Any) -> dict[str, Any] | None:
    """Compact canonical Lưu niên identity. Does not recalculate Gan-Zhi."""
    data = raw if isinstance(raw, Mapping) else {}
    if not data:
        return None
    stem = str(data.get("heavenly_stem") or data.get("stem") or "")
    branch = str(data.get("earthly_branch") or data.get("branch") or "")
    gan_zhi = str(data.get("ganzhi") or data.get("gan_zhi") or "").strip()
    if not gan_zhi:
        gan_zhi = f"{stem} {branch}".strip()
    if not gan_zhi:
        return None
    metadata = data.get("metadata") if isinstance(data.get("metadata"), Mapping) else {}
    stem_el = str(data.get("stem_element") or data.get("element") or stem_element(stem))
    branch_el = str(data.get("branch_element") or branch_element(branch))
    return {
        "year": data.get("year") or metadata.get("bazi_year"),
        "civil_year": metadata.get("civil_year") or data.get("civil_year") or data.get("year"),
        "gan_zhi": gan_zhi,
        "stem": stem,
        "branch": branch,
        "stem_element": stem_el,
        "branch_element": branch_el,
        "ten_god": str(data.get("ten_god") or "").strip(),
        "source": "engines.luck_engine.providers.liunian.DefaultLiunianProvider",
        "relations": list(data.get("relations") or metadata.get("relations") or []),
    }
