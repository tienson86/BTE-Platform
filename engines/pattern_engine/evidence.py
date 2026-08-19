"""Pattern identification evidence. Does not rescore or qualify thành/phá cách."""

from __future__ import annotations

from typing import Any

from engines.bazi_engine.ten_god import STEM_META, ten_god_name


_PILLAR_ATTRS: tuple[tuple[str, str], ...] = (
    ("year_pillar", "Năm"),
    ("month_pillar", "Tháng"),
    ("hour_pillar", "Giờ"),
    ("day_pillar", "Ngày"),
)


def _pillar_stem(pillar: Any) -> str:
    """Read heavenly stem from a pillar object or 'Stem Branch' string."""
    if pillar is None:
        return ""
    if isinstance(pillar, str):
        parts = pillar.strip().split()
        return parts[0] if parts else ""
    return str(getattr(pillar, "stem", "") or "").strip()


def heavenly_stems(context: Any) -> list[dict[str, str]]:
    """Visible heavenly stems with pillar labels. Day stem is included as-is."""
    rows: list[dict[str, str]] = []
    day_master = str(getattr(context, "day_master", "") or "")
    for attr, label in _PILLAR_ATTRS:
        stem = _pillar_stem(getattr(context, attr, None))
        if not stem:
            continue
        god = "Nhật Chủ" if stem == day_master and attr == "day_pillar" else (
            ten_god_name(day_master, stem) if day_master else ""
        )
        rows.append(
            {
                "pillar": attr,
                "pillar_label": label,
                "stem": stem,
                "ten_god": god,
                "element": STEM_META[stem][0] if stem in STEM_META else "",
            }
        )
    return rows


def penetration_status(context: Any) -> dict[str, Any]:
    """
    Qualification evidence only. Exact stem ≠ same-element related stem.

    V1.0 does not change primary pattern from this status.
    """
    main_qi = str(getattr(context, "month_main_qi", "") or "").strip()
    day_master = str(getattr(context, "day_master", "") or "")
    stems = heavenly_stems(context)
    exact_hits = [row for row in stems if row["stem"] == main_qi]
    related: list[dict[str, str]] = []
    main_element = STEM_META[main_qi][0] if main_qi in STEM_META else ""
    for row in stems:
        if not main_qi or row["stem"] == main_qi:
            continue
        if main_element and row["element"] == main_element:
            related.append(row)
    return {
        "month_branch": str(getattr(context, "month_branch", "") or ""),
        "month_hidden_stems": list(getattr(context, "month_hidden_stems", []) or []),
        "month_main_qi": main_qi,
        "day_master": day_master,
        "month_main_qi_ten_god": str(
            getattr(context, "month_branch_ten_god", "") or ""
        ),
        "penetration_exact": bool(exact_hits) if main_qi else False,
        "penetration_exact_hits": exact_hits,
        "penetration_related": related,
    }


def compact_evidence(context: Any, *, winning_rule_id: str = "") -> str:
    """Compact identification evidence. No thành/phá/cách đẹp wording."""
    status = penetration_status(context)
    branch = status["month_branch"]
    main_qi = status["month_main_qi"]
    day_master = status["day_master"]
    ten_god = status["month_main_qi_ten_god"]
    parts: list[str] = []
    if branch:
        parts.append(f"Nguyệt lệnh {branch}")
    if main_qi:
        parts.append(f"khí chính {main_qi}")
    if main_qi and day_master and ten_god:
        parts.append(f"{main_qi} đối với {day_master} là {ten_god}")
    if main_qi:
        if status["penetration_exact"]:
            hits = status["penetration_exact_hits"]
            where = " · ".join(
                f"{item['stem']} tại trụ {item['pillar_label']}" for item in hits
            )
            parts.append(f"{main_qi} thấu trực tiếp ({where})" if where else f"{main_qi} thấu trực tiếp")
        else:
            parts.append(f"{main_qi} không thấu trực tiếp")
    for row in status["penetration_related"]:
        parts.append(
            f"{row['stem']} {row['ten_god']} thấu tại trụ {row['pillar_label']}"
        )
    if winning_rule_id:
        parts.append(f"rule {winning_rule_id}")
    return " · ".join(parts)


def attach_identification_evidence(
    payload: dict[str, Any],
    context: Any,
    winner: dict[str, Any] | None,
    candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    """Copy identification evidence onto a calculator payload. Does not rescore."""
    from .conflict import pattern_code

    status = penetration_status(context)
    rule_id = str((winner or {}).get("rule_id") or "")
    payload["winning_rule_id"] = rule_id
    payload["fallback_used"] = rule_id == "pat_fallback"
    payload["month_branch"] = status["month_branch"]
    payload["month_hidden_stems"] = list(status["month_hidden_stems"])
    payload["month_main_qi"] = status["month_main_qi"]
    payload["month_main_qi_ten_god"] = status["month_main_qi_ten_god"]
    payload["day_master"] = status["day_master"]
    payload["penetration_exact"] = bool(status["penetration_exact"])
    payload["penetration_related"] = [
        {
            "stem": row["stem"],
            "ten_god": row["ten_god"],
            "pillar_label": row["pillar_label"],
            "element": row["element"],
        }
        for row in status["penetration_related"]
    ]
    payload["candidate_patterns"] = payload.get("candidate_patterns") or [
        pattern_code(item)
        for item in candidates
        if pattern_code(item)
    ]
    payload["evidence_compact"] = compact_evidence(context, winning_rule_id=rule_id)
    return payload
