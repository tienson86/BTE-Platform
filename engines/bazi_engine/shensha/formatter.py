"""Format ShenSha provenance for V1.0 presentation. No scoring, no interpretation."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from engines.bazi_engine.shensha.catalog import PILLAR_LABELS_VI, SOURCE_LABELS_VI


def pillar_label(pillar: str) -> str:
    """Vietnamese pillar label."""
    return PILLAR_LABELS_VI.get(pillar, pillar)


def source_label(source_type: str) -> str:
    """Vietnamese source label (Nhật can, Niên chi, …)."""
    return SOURCE_LABELS_VI.get(source_type, source_type)


def presence_label(occurrences: Sequence[Any]) -> str:
    """Build `Có · trụ Tháng` (all unique pillars, order preserved)."""
    labels: list[str] = []
    seen: set[str] = set()
    for item in occurrences:
        pillar = str(getattr(item, "pillar", "") or "")
        if not pillar or pillar in seen:
            continue
        seen.add(pillar)
        labels.append(f"trụ {pillar_label(pillar)}")
    if not labels:
        return "Có"
    return "Có · " + " · ".join(labels)


def evidence_text(
    source_type: str,
    source_value: str,
    occurrences: Sequence[Any],
    fallback_target: str = "",
) -> str:
    """Build `Nhật can Canh → gặp Sửu` from stored source/target."""
    targets: list[str] = []
    seen: set[str] = set()
    for item in occurrences:
        value = str(getattr(item, "target_value", "") or "")
        if not value or value in seen:
            continue
        seen.add(value)
        targets.append(value)
    if not targets and fallback_target:
        targets.append(fallback_target)
    source = f"{source_label(source_type)} {source_value}".strip()
    target = "、".join(targets)
    if source and target:
        return f"{source} → gặp {target}"
    return source or target
