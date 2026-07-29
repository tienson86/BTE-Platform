"""
Pattern conflict resolution — mutually exclusive pattern groups.

Standard (Lệnh Tháng) patterns cannot coexist as final/secondary peers.
Follow types and special/transformed patterns are exclusive within their group.
"""

from __future__ import annotations

from typing import Any


# Ten standard mutually-exclusive main patterns (Zheng/Pian families).
STANDARD_EXCLUSIVE_PATTERNS: frozenset[str] = frozenset(
    {
        "chinh_quan",
        "that_sat",
        "chinh_tai",  # Zheng Cai
        "thien_tai",  # Pian Cai
        "chinh_an",  # Zheng Yin
        "thien_an",  # Pian Yin
        "thuc_than",  # Shi Shen
        "thuong_quan",  # Shang Guan
        "ty_kien",  # Bi Jian
        "kiep_tai",  # Jie Cai
    }
)

FOLLOW_EXCLUSIVE_PATTERNS: frozenset[str] = frozenset(
    {
        "tong_vuong",
        "tong_tai",
        "tong_sat",
        "tong_quan",
        "tong_nhi",
        "tong_an",
    }
)

SPECIAL_EXCLUSIVE_PATTERNS: frozenset[str] = frozenset(
    {
        "khuc_truc",
        "viem_thuong",
        "nhuan_ha",
        "gia_sac",
        "jia_wang",
    }
)

EXCLUSIVE_GROUPS: tuple[tuple[str, frozenset[str]], ...] = (
    ("standard_main", STANDARD_EXCLUSIVE_PATTERNS),
    ("follow", FOLLOW_EXCLUSIVE_PATTERNS),
    ("special", SPECIAL_EXCLUSIVE_PATTERNS),
)


def pattern_code(candidate: dict[str, Any]) -> str:
    """Normalize pattern code from a candidate rule dict."""
    return str(candidate.get("pattern") or "").strip().lower()


def exclusive_group_for(candidate: dict[str, Any]) -> str | None:
    """Return exclusive group name when the candidate belongs to one."""
    code = pattern_code(candidate)
    for name, members in EXCLUSIVE_GROUPS:
        if code in members:
            return name
    return None


def category_section(candidate: dict[str, Any]) -> str:
    """
    Priority-Engine section key for a candidate.

    Exclusive groups share one section so diversity caps keep a single winner.
    """
    group = exclusive_group_for(candidate)
    if group:
        return group
    source = str(candidate.get("source") or "")
    if "combination" in source or source.startswith("04_"):
        return "combination"
    if "special" in source or source.startswith("02_"):
        return "special"
    if "follow" in source or source.startswith("03_"):
        return "follow"
    return "other"


def resolve_exclusive_conflicts(
    candidates: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Keep at most one candidate per exclusive group (highest priority, score).

    Returns (survivors, discarded).
    Non-exclusive candidates pass through unchanged.
    """
    by_group: dict[str, list[dict[str, Any]]] = {}
    passthrough: list[dict[str, Any]] = []

    for item in candidates:
        group = exclusive_group_for(item)
        if group is None:
            passthrough.append(item)
            continue
        by_group.setdefault(group, []).append(item)

    survivors: list[dict[str, Any]] = list(passthrough)
    discarded: list[dict[str, Any]] = []

    for group, items in by_group.items():
        ranked = sorted(items, key=_rank_key, reverse=True)
        winner = ranked[0]
        survivors.append(winner)
        for loser in ranked[1:]:
            discarded.append(
                {
                    **loser,
                    "_discard_reason": "exclusive_conflict",
                    "_discard_group": group,
                    "_kept_rule_id": winner.get("rule_id"),
                }
            )

    return survivors, discarded


def _rank_key(candidate: dict[str, Any]) -> tuple[float, float, str]:
    try:
        priority = float(candidate.get("priority", 0) or 0)
    except (TypeError, ValueError):
        priority = 0.0
    try:
        score = float(candidate.get("score", 0) or 0)
    except (TypeError, ValueError):
        score = 0.0
    rule_id = str(candidate.get("rule_id") or "")
    return (priority, score, rule_id)
