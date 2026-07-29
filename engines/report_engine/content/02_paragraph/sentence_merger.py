"""Merge sentences that share topic within the same section and polarity."""

from __future__ import annotations

from collections import OrderedDict
from typing import Iterable

from .paragraph_models import SentenceUnit


class SentenceMerger:
    """
    Group sentence units for paragraph assembly.

    Constraints
    -----------
    - Same topic_key only
    - Same polarity only
    - Never across different sections
    - Does not create new sentence text
    """

    def merge(self, units: Iterable[SentenceUnit]) -> list[list[SentenceUnit]]:
        """
        Return ordered groups of mergeable sentences.

        Groups are keyed by (section, polarity, topic_key) preserving first-seen order.
        """
        buckets: OrderedDict[tuple[str, str, str], list[SentenceUnit]] = OrderedDict()
        for unit in units:
            if not unit.text.strip():
                continue
            key = (unit.section, unit.polarity, unit.topic_key or "general")
            buckets.setdefault(key, []).append(unit)

        groups: list[list[SentenceUnit]] = []
        for group in buckets.values():
            # Stable priority ordering inside group (no text invention)
            ordered = sorted(group, key=lambda item: item.priority, reverse=True)
            groups.append(ordered)
        return groups
