"""Indexed Integrated Narrative lines for editorial composition."""

from __future__ import annotations

from typing import Any, Mapping, NamedTuple

from engines.commercial_composer.contracts import INTEGRATED_SLOTS, RISK_PATH_MARKERS, SECTION_SOURCES
from engines.commercial_composer.models import CommercialSentence
from engines.commercial_composer.rules import integrated_sentence_id


class IntegratedLine(NamedTuple):
    """One published Integrated sentence with its original index."""

    text: str
    integrated_slot: str
    source_path: str
    topic_id: str
    index: int


def as_record(value: Any) -> Mapping[str, Any]:
    """Return a mapping from a unit, dict, or empty input."""
    if value is None:
        return {}
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        payload = to_dict()
        return payload if isinstance(payload, dict) else {}
    if isinstance(value, dict):
        return value
    return {}


def iter_integrated_lines(payload: Mapping[str, Any], slot: str) -> tuple[IntegratedLine, ...]:
    """Copy published sentences from one Integrated block, keeping original indexes."""
    record = as_record(payload.get(slot))
    sentences = record.get("sentences") or ()
    paths = list(record.get("source_paths") or ())
    topics = list(record.get("topic_ids") or ())
    lines: list[IntegratedLine] = []
    for index, raw in enumerate(sentences):
        text = str(raw).strip()
        if not text:
            continue
        path = str(paths[index]) if index < len(paths) else slot
        topic = str(topics[index]) if index < len(topics) else ""
        lines.append(
            IntegratedLine(
                text=text,
                integrated_slot=slot,
                source_path=path,
                topic_id=topic,
                index=index,
            )
        )
    return tuple(lines)


def lines_for_section(payload: Mapping[str, Any], commercial_slot: str) -> tuple[IntegratedLine, ...]:
    """Collect Integrated lines mapped to one INT-03A commercial section."""
    collected: list[IntegratedLine] = []
    for integrated_slot in SECTION_SOURCES[commercial_slot]:
        collected.extend(iter_integrated_lines(payload, integrated_slot))
    if commercial_slot == "risks":
        collected = [line for line in collected if _is_risk_path(line.source_path)]
    return tuple(collected)


def to_sentences(slot: str, lines: tuple[IntegratedLine, ...]) -> tuple[CommercialSentence, ...]:
    """Wrap published Integrated lines as traced commercial sentences."""
    return tuple(
        CommercialSentence(
            text=line.text,
            slot=slot,
            integrated_slots=(line.integrated_slot,),
            source_paths=(line.source_path,) if line.source_path else (),
            topic_ids=(line.topic_id,) if line.topic_id else (),
            integrated_sentence_ids=(integrated_sentence_id(line.integrated_slot, line.index),),
        )
        for line in lines
    )


def _is_risk_path(path: str) -> bool:
    token = path.lower()
    return any(marker in token for marker in RISK_PATH_MARKERS)


def integrated_slot_names() -> tuple[str, ...]:
    """Frozen Integrated slots the composer may read."""
    return INTEGRATED_SLOTS
