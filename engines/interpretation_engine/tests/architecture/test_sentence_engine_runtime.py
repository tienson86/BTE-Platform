"""Architecture tests for sentence engine infrastructure."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.exceptions import SentenceEngineError
from engines.interpretation_engine.sentence_engine import (
    Composer,
    Ranking,
    Resolver,
    Selector,
    SentenceEngine,
    SentenceRef,
)


def _refs() -> tuple[SentenceRef, ...]:
    """Build a small in-memory sentence-ref catalog (no text bodies)."""
    return (
        SentenceRef(
            ref_id="s_personality_a",
            domain="personality",
            section="intro",
            status="active",
            priority=10,
            tags=("core",),
        ),
        SentenceRef(
            ref_id="s_personality_b",
            domain="personality",
            section="intro",
            status="active",
            priority=5,
            tags=("alt",),
        ),
        SentenceRef(
            ref_id="s_career_a",
            domain="career",
            section="body",
            status="active",
            priority=8,
            tags=("core",),
        ),
        SentenceRef(
            ref_id="s_draft",
            domain="personality",
            section="intro",
            status="draft",
            priority=99,
        ),
    )


def test_selector_filters_by_domain_and_status() -> None:
    """Selector returns structural candidates only."""
    selected = Selector().select(_refs(), domain="personality", status="active")
    assert {item.ref.ref_id for item in selected} == {
        "s_personality_a",
        "s_personality_b",
    }


def test_ranking_orders_by_score_then_priority() -> None:
    """Ranking is deterministic and does not use NLG signals."""
    selected = Selector().select(_refs(), domain="personality", status="active")
    ranked = Ranking().rank(selected)
    assert [item.ref.ref_id for item in ranked] == [
        "s_personality_a",
        "s_personality_b",
    ]
    assert ranked[0].rank == 1


def test_resolver_resolves_ids() -> None:
    """Resolver hydrates refs from catalog without loading a sentence library."""
    resolver = Resolver(ref_provider=_refs)
    ref = resolver.resolve("s_career_a")
    assert ref.domain == "career"
    with pytest.raises(SentenceEngineError, match="sentence_ref_not_found"):
        resolver.resolve("missing")


def test_composer_builds_ref_only_composition() -> None:
    """Composer output contains ref ids, not natural language."""
    composition = Composer().compose_from_refs(
        _refs(),
        domain="personality",
        status="active",
        limit=1,
    )
    assert composition.validate() is True
    assert composition.ref_ids == ("s_personality_a",)
    assert "text" not in composition.metadata
    assert all(not hasattr(item.ref, "text") for item in composition.candidates)


def test_sentence_engine_assemble() -> None:
    """Facade assembles composition shells from ref ids only."""
    engine = SentenceEngine(catalog=_refs())
    composition = engine.assemble(("s_career_a", "s_personality_a"))
    assert composition.ref_ids == ("s_career_a", "s_personality_a")
    assert len(composition.candidates) == 2
    assert engine.validate(("s_career_a",)) is True
    assert engine.validate(("",)) is False
