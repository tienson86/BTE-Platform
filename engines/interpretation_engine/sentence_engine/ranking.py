"""Sentence Engine ranking — rank sentence reference candidates.

Ranks by structural score/priority only.
No natural language quality scoring. No sentence library.
"""

from __future__ import annotations

from engines.interpretation_engine.exceptions.sentence_error import SentenceEngineError
from engines.interpretation_engine.sentence_engine.metadata import SentenceCandidate


class Ranking:
    """Rank sentence reference candidates deterministically.

    Default key: ``(-score, -priority, ref_id)`` so higher score/priority win,
    with ascending ``ref_id`` as a stable tie-break.
    Ranking never inspects or generates sentence text.
    """

    def rank(
        self,
        candidates: tuple[SentenceCandidate, ...],
        *,
        descending: bool = True,
        limit: int | None = None,
    ) -> tuple[SentenceCandidate, ...]:
        """Return ranked candidates with sequential ``rank`` values starting at 1."""
        if limit is not None and limit < 0:
            raise SentenceEngineError("ranking_limit_invalid")

        def sort_key(item: SentenceCandidate) -> tuple[float, int, str]:
            if descending:
                return (-item.score, -item.ref.priority, item.ref.ref_id)
            return (item.score, item.ref.priority, item.ref.ref_id)

        ordered = sorted(candidates, key=sort_key)
        if limit is not None:
            ordered = ordered[:limit]

        ranked: list[SentenceCandidate] = []
        for index, candidate in enumerate(ordered, start=1):
            ranked.append(
                SentenceCandidate(
                    ref=candidate.ref,
                    score=candidate.score,
                    rank=index,
                    reasons=candidate.reasons + ("ranked",),
                )
            )
        return tuple(ranked)

    def top(
        self,
        candidates: tuple[SentenceCandidate, ...],
        n: int = 1,
    ) -> tuple[SentenceCandidate, ...]:
        """Return the top-N ranked candidates."""
        if n < 1:
            raise SentenceEngineError("ranking_top_n_invalid")
        return self.rank(candidates, descending=True, limit=n)

    def compare(self, left: SentenceCandidate, right: SentenceCandidate) -> int:
        """Compare two candidates. Return -1, 0, or 1 (higher score wins)."""
        left_key = (left.score, left.ref.priority, left.ref.ref_id)
        right_key = (right.score, right.ref.priority, right.ref.ref_id)
        if left_key < right_key:
            return -1
        if left_key > right_key:
            return 1
        return 0
