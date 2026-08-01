"""Sentence Engine selector — select sentence reference candidates.

Selects references by structural criteria only.
No sentence library lookup. No natural language generation.
"""

from __future__ import annotations

from typing import Any, Mapping

from engines.interpretation_engine.exceptions.sentence_error import SentenceEngineError
from engines.interpretation_engine.sentence_engine.metadata import SentenceCandidate, SentenceRef


class Selector:
    """Select sentence reference candidates from an in-memory catalog of refs.

    The catalog is a caller-supplied tuple of ``SentenceRef`` objects.
    This selector never loads a sentence library or produces text.
    """

    def select(
        self,
        refs: tuple[SentenceRef, ...],
        *,
        domain: str | None = None,
        section: str | None = None,
        locale: str | None = None,
        status: str | None = None,
        tags: tuple[str, ...] = (),
        require_all_tags: bool = False,
    ) -> tuple[SentenceCandidate, ...]:
        """Select matching sentence references as unscored candidates."""
        if not refs:
            return ()

        selected: list[SentenceCandidate] = []
        for ref in refs:
            if not ref.validate():
                continue
            if domain is not None and ref.domain != domain:
                continue
            if section is not None and ref.section != section:
                continue
            if locale is not None and ref.locale != locale:
                continue
            if status is not None and ref.status != status:
                continue
            if tags and not self._match_tags(ref.tags, tags, require_all=require_all_tags):
                continue
            selected.append(
                SentenceCandidate(
                    ref=ref,
                    score=float(ref.priority),
                    reasons=("selected",),
                )
            )
        return tuple(selected)

    def select_by_ids(
        self,
        refs: tuple[SentenceRef, ...],
        ref_ids: tuple[str, ...],
    ) -> tuple[SentenceCandidate, ...]:
        """Select candidates whose ``ref_id`` appears in ``ref_ids`` (order preserved)."""
        if not ref_ids:
            return ()
        index = {ref.ref_id: ref for ref in refs if ref.validate()}
        selected: list[SentenceCandidate] = []
        missing: list[str] = []
        for ref_id in ref_ids:
            ref = index.get(ref_id)
            if ref is None:
                missing.append(ref_id)
                continue
            selected.append(
                SentenceCandidate(ref=ref, score=float(ref.priority), reasons=("id_match",))
            )
        if missing:
            raise SentenceEngineError(f"sentence_refs_not_found:{','.join(missing)}")
        return tuple(selected)

    def select_from_attributes(
        self,
        refs: tuple[SentenceRef, ...],
        attributes: Mapping[str, Any],
    ) -> tuple[SentenceCandidate, ...]:
        """Select using opaque attribute keys commonly used by Pack 03 context."""
        tags_raw = attributes.get("tags") or ()
        tags = tuple(tags_raw) if isinstance(tags_raw, (list, tuple)) else ()
        return self.select(
            refs,
            domain=attributes.get("domain"),
            section=attributes.get("section"),
            locale=attributes.get("locale"),
            status=attributes.get("status"),
            tags=tags,
            require_all_tags=bool(attributes.get("require_all_tags", False)),
        )

    def _match_tags(
        self,
        ref_tags: tuple[str, ...],
        required: tuple[str, ...],
        *,
        require_all: bool,
    ) -> bool:
        """Match tags by any-or-all policy."""
        ref_set = set(ref_tags)
        req_set = set(required)
        if require_all:
            return req_set.issubset(ref_set)
        return bool(ref_set.intersection(req_set))
