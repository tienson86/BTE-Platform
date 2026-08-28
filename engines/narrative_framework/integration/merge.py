"""Merge and deduplicate sentences from frozen topic narrative units."""

from __future__ import annotations

from typing import Any

from engines.narrative_framework.integration.constants import (
    RESTATEMENT_MARKERS,
    SPEECH_SLOTS,
    TOPIC_ORDER,
)

MergedLine = tuple[str, str, str]


def _norm(text: str) -> str:
    return " ".join(text.strip().rstrip(".").lower().split())


def _stated_fact(text: str) -> str:
    lowered = text.lower()
    for marker in RESTATEMENT_MARKERS:
        index = lowered.find(marker)
        if index < 0:
            continue
        return _norm(text[index + len(marker) :])
    return ""


def _is_advice(text: str) -> bool:
    stripped = text.strip()
    return stripped.startswith(("Ưu tiên", "Hạn chế", "Hỷ thần", "Hướng điều hậu", "Giữ"))


def _redundant(
    candidate: str,
    kept: list[str],
    *,
    restatement: bool,
    collapse_contained: bool = False,
) -> bool:
    cnorm = _norm(candidate)
    if not cnorm:
        return True
    for previous in kept:
        pnorm = _norm(previous)
        if cnorm == pnorm or cnorm in pnorm:
            return True
        if collapse_contained and pnorm in cnorm:
            return True
    if not restatement or _is_advice(candidate):
        return False
    fact = _stated_fact(candidate)
    if not fact:
        return False
    for previous in kept:
        prev_fact = _stated_fact(previous)
        if prev_fact and fact == prev_fact:
            return True
        if fact == _norm(previous):
            return True
    return False


def _block_lines(unit: Any, slot: str) -> tuple[MergedLine, ...]:
    block = getattr(unit, slot, None)
    if block is None or not getattr(block, "available", False):
        return ()
    sentences = tuple(getattr(block, "sentences", ()) or ())
    paths = tuple(getattr(block, "source_paths", ()) or ())
    topic_id = str(getattr(unit, "topic_id", "") or "")
    lines: list[MergedLine] = []
    for index, sentence in enumerate(sentences):
        text = str(sentence).strip()
        if not text:
            continue
        path = paths[index] if index < len(paths) else f"{topic_id}.{slot}"
        lines.append((text, str(path), topic_id))
    return tuple(lines)


def ordered_units(*units: Any) -> tuple[Any, ...]:
    """Return present topic units in canonical commercial order."""
    by_id = {
        str(getattr(unit, "topic_id", "") or ""): unit
        for unit in units
        if unit is not None
    }
    return tuple(by_id[topic] for topic in TOPIC_ORDER if topic in by_id)


def merge_slot(
    units: tuple[Any, ...],
    slot: str,
    *,
    restatement: bool,
    collapse_contained: bool = False,
) -> tuple[MergedLine, ...]:
    """Concatenate one speech slot across topics, dropping duplicate facts."""
    kept_text: list[str] = []
    kept_lines: list[MergedLine] = []
    for unit in units:
        for line in _block_lines(unit, slot):
            if _redundant(
                line[0],
                kept_text,
                restatement=restatement,
                collapse_contained=collapse_contained,
            ):
                continue
            kept_text.append(line[0])
            kept_lines.append(line)
    return tuple(kept_lines)


def merge_topics(units: tuple[Any, ...]) -> dict[str, tuple[MergedLine, ...]]:
    """Merge the four speech slots. Recommendations collapse contained advice."""
    merged: dict[str, tuple[MergedLine, ...]] = {}
    for slot in SPEECH_SLOTS:
        merged[slot] = merge_slot(
            units,
            slot,
            restatement=slot != "recommendation",
            collapse_contained=slot == "recommendation",
        )
    return merged


def executive_lines(units: tuple[Any, ...]) -> tuple[MergedLine, ...]:
    """One lead observation fact per topic. No new wording."""
    kept_text: list[str] = []
    kept_lines: list[MergedLine] = []
    for unit in units:
        lines = _block_lines(unit, "observation")
        if not lines:
            continue
        lead = lines[0]
        if _redundant(lead[0], kept_text, restatement=True):
            continue
        kept_text.append(lead[0])
        kept_lines.append(lead)
    return tuple(kept_lines)


def drop_used(
    lines: tuple[MergedLine, ...],
    used: tuple[MergedLine, ...],
    *,
    restatement: bool = False,
) -> tuple[MergedLine, ...]:
    """Remove sentences already placed in an earlier integrated block."""
    kept_text = [line[0] for line in used]
    kept: list[MergedLine] = []
    for line in lines:
        if _redundant(line[0], kept_text, restatement=restatement):
            continue
        kept.append(line)
        kept_text.append(line[0])
    return tuple(kept)
