"""Sentence assembly interface. No hard-coded sentences. No NLG."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping

from engines.interpretation_engine.sentence_engine.composer import Composer
from engines.interpretation_engine.sentence_engine.metadata import (
    SentenceComposition,
    SentenceRef,
)
from engines.interpretation_engine.sentence_engine.ranking import Ranking
from engines.interpretation_engine.sentence_engine.resolver import Resolver
from engines.interpretation_engine.sentence_engine.selector import Selector


class SentenceEngineInterface(ABC):
    """Sentence assembly interface over references only.

    Implementations must not load a sentence library or generate natural language.
    """

    @abstractmethod
    def assemble(
        self,
        refs: tuple[str, ...],
        context: Mapping[str, Any] | None = None,
    ) -> SentenceComposition:
        """Assemble sentence refs into a composition shell."""

    @abstractmethod
    def validate(self, refs: tuple[str, ...]) -> bool:
        """Validate sentence reference identifier structure."""


class SentenceEngine(SentenceEngineInterface):
    """Default Sentence Engine facade over selector/ranking/resolver/composer.

    Infrastructure only — no sentence library, no NLG.
    """

    def __init__(
        self,
        *,
        catalog: tuple[SentenceRef, ...] = (),
    ) -> None:
        """Initialize with an optional in-memory sentence-ref catalog."""
        self._catalog = catalog
        self._selector = Selector()
        self._ranking = Ranking()
        self._resolver = Resolver(
            ref_provider=lambda: self._catalog,
            selector=self._selector,
            ranking=self._ranking,
        )
        self._composer = Composer(
            selector=self._selector,
            ranking=self._ranking,
            resolver=self._resolver,
        )

    @property
    def selector(self) -> Selector:
        """Return the bound selector."""
        return self._selector

    @property
    def ranking(self) -> Ranking:
        """Return the bound ranking helper."""
        return self._ranking

    @property
    def resolver(self) -> Resolver:
        """Return the bound resolver."""
        return self._resolver

    @property
    def composer(self) -> Composer:
        """Return the bound composer."""
        return self._composer

    def set_catalog(self, catalog: tuple[SentenceRef, ...]) -> None:
        """Replace the in-memory sentence-ref catalog."""
        self._catalog = catalog

    def assemble(
        self,
        refs: tuple[str, ...],
        context: Mapping[str, Any] | None = None,
    ) -> SentenceComposition:
        """Assemble sentence refs into a composition shell (no NLG)."""
        if not self.validate(refs):
            from engines.interpretation_engine.exceptions.sentence_error import (
                SentenceEngineError,
            )

            raise SentenceEngineError("sentence_refs_invalid")
        return self._composer.compose_from_ids(
            refs,
            metadata=dict(context or {}),
        )

    def validate(self, refs: tuple[str, ...]) -> bool:
        """Validate that each ref id is a non-empty string."""
        if not refs:
            return False
        return all(isinstance(ref_id, str) and bool(ref_id.strip()) for ref_id in refs)
