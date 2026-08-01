"""Sentence Engine resolver — resolve sentence references to shells.

Resolves reference identifiers to ``SentenceRef`` / candidate shells.
Does not load a sentence library. Does not generate natural language.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping

from engines.interpretation_engine.exceptions.sentence_error import SentenceEngineError
from engines.interpretation_engine.sentence_engine.metadata import (
    Metadata,
    SentenceCandidate,
    SentenceRef,
)
from engines.interpretation_engine.sentence_engine.ranking import Ranking
from engines.interpretation_engine.sentence_engine.selector import Selector


class Resolver:
    """Resolve sentence reference ids against a caller-supplied ref catalog.

    Resolution is identity/metadata hydration only — never NLG.
    """

    def __init__(
        self,
        *,
        ref_provider: Callable[[], tuple[SentenceRef, ...]] | None = None,
        selector: Selector | None = None,
        ranking: Ranking | None = None,
        metadata: Metadata | None = None,
    ) -> None:
        """Initialize resolver collaborators."""
        self._ref_provider = ref_provider or (lambda: ())
        self._selector = selector or Selector()
        self._ranking = ranking or Ranking()
        self._metadata = metadata or Metadata()

    @property
    def selector(self) -> Selector:
        """Return the bound selector."""
        return self._selector

    @property
    def ranking(self) -> Ranking:
        """Return the bound ranking helper."""
        return self._ranking

    @property
    def metadata(self) -> Metadata:
        """Return the bound metadata helper."""
        return self._metadata

    def resolve(self, ref_id: str) -> SentenceRef:
        """Resolve a single sentence reference by id."""
        for ref in self._ref_provider():
            if ref.ref_id == ref_id and ref.validate():
                return ref
        raise SentenceEngineError(f"sentence_ref_not_found:{ref_id}")

    def resolve_many(self, ref_ids: tuple[str, ...]) -> tuple[SentenceRef, ...]:
        """Resolve many sentence references, preserving request order."""
        if not ref_ids:
            return ()
        index = {
            ref.ref_id: ref for ref in self._ref_provider() if ref.validate()
        }
        resolved: list[SentenceRef] = []
        missing: list[str] = []
        for ref_id in ref_ids:
            ref = index.get(ref_id)
            if ref is None:
                missing.append(ref_id)
                continue
            resolved.append(ref)
        if missing:
            raise SentenceEngineError(f"sentence_refs_not_found:{','.join(missing)}")
        return tuple(resolved)

    def resolve_candidates(
        self,
        *,
        domain: str | None = None,
        section: str | None = None,
        locale: str | None = None,
        status: str | None = None,
        tags: tuple[str, ...] = (),
        limit: int | None = None,
    ) -> tuple[SentenceCandidate, ...]:
        """Select then rank candidates from the bound catalog."""
        selected = self._selector.select(
            self._ref_provider(),
            domain=domain,
            section=section,
            locale=locale,
            status=status,
            tags=tags,
        )
        return self._ranking.rank(selected, limit=limit)

    def resolve_metadata(self, ref_id: str) -> Mapping[str, object]:
        """Resolve normalized metadata for a sentence reference."""
        return self._metadata.from_ref(self.resolve(ref_id))
