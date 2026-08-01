"""Sentence Engine composer — compose ordered sentence reference shells.

Composes reference sequences into ``SentenceComposition`` artifacts.
No sentence library. No natural language generation.
"""

from __future__ import annotations

from typing import Any, Mapping

from engines.interpretation_engine.exceptions.sentence_error import SentenceEngineError
from engines.interpretation_engine.sentence_engine.metadata import (
    SentenceCandidate,
    SentenceComposition,
    SentenceRef,
)
from engines.interpretation_engine.sentence_engine.ranking import Ranking
from engines.interpretation_engine.sentence_engine.resolver import Resolver
from engines.interpretation_engine.sentence_engine.selector import Selector
from engines.interpretation_engine.utils.ids import new_id


class Composer:
    """Compose ordered sentence-reference compositions.

    Output contains reference ids and candidate shells only — never prose.
    """

    def __init__(
        self,
        *,
        selector: Selector | None = None,
        ranking: Ranking | None = None,
        resolver: Resolver | None = None,
    ) -> None:
        """Initialize composition collaborators."""
        self._selector = selector or Selector()
        self._ranking = ranking or Ranking()
        self._resolver = resolver

    def compose(
        self,
        candidates: tuple[SentenceCandidate, ...],
        *,
        composition_id: str | None = None,
        metadata: Mapping[str, Any] | None = None,
        rank: bool = True,
        limit: int | None = None,
    ) -> SentenceComposition:
        """Compose a composition shell from candidates."""
        if rank:
            ordered = self._ranking.rank(candidates, limit=limit)
        else:
            ordered = candidates if limit is None else candidates[:limit]

        ref_ids = tuple(item.ref.ref_id for item in ordered)
        return SentenceComposition(
            composition_id=composition_id or new_id("scomp"),
            ref_ids=ref_ids,
            candidates=ordered,
            metadata=dict(metadata or {}),
        )

    def compose_from_refs(
        self,
        refs: tuple[SentenceRef, ...],
        *,
        composition_id: str | None = None,
        metadata: Mapping[str, Any] | None = None,
        domain: str | None = None,
        section: str | None = None,
        locale: str | None = None,
        status: str | None = None,
        tags: tuple[str, ...] = (),
        limit: int | None = None,
    ) -> SentenceComposition:
        """Select, rank, and compose from a caller-supplied ref catalog."""
        selected = self._selector.select(
            refs,
            domain=domain,
            section=section,
            locale=locale,
            status=status,
            tags=tags,
        )
        return self.compose(
            selected,
            composition_id=composition_id,
            metadata=metadata,
            rank=True,
            limit=limit,
        )

    def compose_from_ids(
        self,
        ref_ids: tuple[str, ...],
        *,
        composition_id: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> SentenceComposition:
        """Compose a ref-id-only shell without hydrating candidates.

        When a resolver is bound, candidates are hydrated from the catalog.
        Still never generates natural language.
        """
        if not ref_ids:
            raise SentenceEngineError("composition_ref_ids_required")

        candidates: tuple[SentenceCandidate, ...] = ()
        if self._resolver is not None:
            resolved = self._resolver.resolve_many(ref_ids)
            candidates = tuple(
                SentenceCandidate(
                    ref=ref,
                    score=float(ref.priority),
                    rank=index,
                    reasons=("composed_from_ids",),
                )
                for index, ref in enumerate(resolved, start=1)
            )

        return SentenceComposition(
            composition_id=composition_id or new_id("scomp"),
            ref_ids=ref_ids,
            candidates=candidates,
            metadata=dict(metadata or {}),
        )

    def validate(self, composition: SentenceComposition) -> bool:
        """Validate composition structural contract."""
        return composition.validate()
