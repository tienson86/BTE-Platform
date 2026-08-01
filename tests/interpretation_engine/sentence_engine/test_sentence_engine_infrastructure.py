"""Sentence engine infrastructure tests (mock refs only, no NLG)."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.exceptions.sentence_error import SentenceEngineError
from engines.interpretation_engine.sentence_engine import (
    Composer,
    Metadata,
    Ranking,
    Resolver,
    Selector,
    SentenceCandidate,
    SentenceComposition,
    SentenceEngine,
    SentenceRef,
)


class TestSentenceEngineInfrastructure:
    """Mock-only sentence reference infrastructure coverage."""

    def test_selector_filters_tags_and_ids(
        self,
        sentence_ref_catalog: tuple[SentenceRef, ...],
    ) -> None:
        """Selector filters by domain/tags and by ids."""
        selector = Selector()
        selected = selector.select(
            sentence_ref_catalog,
            domain="personality",
            status="active",
            tags=("core",),
        )
        assert [item.ref.ref_id for item in selected] == ["s_a"]
        all_tags = selector.select(
            sentence_ref_catalog,
            domain="personality",
            tags=("core", "vi"),
            require_all_tags=True,
        )
        assert len(all_tags) == 1
        by_ids = selector.select_by_ids(sentence_ref_catalog, ("s_b", "s_a"))
        assert [item.ref.ref_id for item in by_ids] == ["s_b", "s_a"]
        from_attrs = selector.select_from_attributes(
            sentence_ref_catalog,
            {"domain": "career", "status": "draft", "tags": ["core"]},
        )
        assert from_attrs[0].ref.ref_id == "s_c"
        with pytest.raises(SentenceEngineError, match="sentence_refs_not_found"):
            selector.select_by_ids(sentence_ref_catalog, ("missing",))
        assert selector.select(()) == ()

    def test_ranking_compare_and_top(
        self,
        sentence_ref_catalog: tuple[SentenceRef, ...],
    ) -> None:
        """Ranking orders, tops, and compares candidates."""
        candidates = Selector().select(sentence_ref_catalog, status="active")
        ranking = Ranking()
        ranked = ranking.rank(candidates)
        assert ranked[0].ref.ref_id == "s_a"
        assert ranking.top(candidates, 1)[0].ref.ref_id == "s_a"
        ascending = ranking.rank(candidates, descending=False)
        assert ascending[0].score <= ascending[-1].score
        assert ranking.compare(ranked[0], ranked[1]) == 1
        assert ranking.compare(ranked[1], ranked[0]) == -1
        assert ranking.compare(ranked[0], ranked[0]) == 0
        with pytest.raises(SentenceEngineError, match="ranking_limit_invalid"):
            ranking.rank(candidates, limit=-1)
        with pytest.raises(SentenceEngineError, match="ranking_top_n_invalid"):
            ranking.top(candidates, 0)

    def test_resolver_and_composer(
        self,
        sentence_ref_catalog: tuple[SentenceRef, ...],
    ) -> None:
        """Resolver/composer produce composition shells without NLG."""
        resolver = Resolver(ref_provider=lambda: sentence_ref_catalog)
        assert resolver.resolve("s_a").domain == "personality"
        assert resolver.resolve_many(("s_b", "s_a"))[0].ref_id == "s_b"
        cands = resolver.resolve_candidates(domain="personality", status="active", limit=1)
        assert len(cands) == 1
        assert resolver.resolve_metadata("s_a")["ref_id"] == "s_a"
        composer = Composer(resolver=resolver)
        composition = composer.compose_from_refs(
            sentence_ref_catalog,
            domain="personality",
            status="active",
            limit=1,
        )
        assert composition.validate() is True
        assert "text" not in composition.metadata
        from_ids = composer.compose_from_ids(("s_a", "s_b"))
        assert from_ids.ref_ids == ("s_a", "s_b")
        unranked = composer.compose(cands, rank=False)
        assert unranked.candidates
        with pytest.raises(SentenceEngineError, match="composition_ref_ids_required"):
            composer.compose_from_ids(())

    def test_metadata_and_engine_facade(
        self,
        sentence_ref_catalog: tuple[SentenceRef, ...],
    ) -> None:
        """Metadata helper and SentenceEngine facade."""
        ref = sentence_ref_catalog[0]
        meta = Metadata()
        assert meta.from_ref(ref)["domain"] == "personality"
        composition = SentenceComposition(composition_id="c1", ref_ids=("s_a",))
        assert meta.from_composition(composition)["composition_id"] == "c1"
        assert meta.from_mapping({"ref_id": "x"})["ref_id"] == "x"
        assert meta.from_mapping({"metadata": {"k": 1}, "ref_id": "r"})["k"] == 1
        with pytest.raises(SentenceEngineError):
            meta.from_mapping({"foo": 1})
        assert SentenceCandidate(ref=ref).validate() is True
        assert SentenceRef(ref_id="").validate() is False

        engine = SentenceEngine(catalog=sentence_ref_catalog)
        engine.set_catalog(sentence_ref_catalog)
        assert engine.selector is not None
        assert engine.ranking is not None
        assert engine.resolver is not None
        assert engine.composer is not None
        assembled = engine.assemble(("s_a",), {"locale": "vi"})
        assert assembled.ref_ids == ("s_a",)
        assert engine.validate(("s_a",)) is True
        with pytest.raises(SentenceEngineError, match="sentence_refs_invalid"):
            engine.assemble(("",))
