"""Sprint K1.5 — BaZi Concept Layer tests."""

from __future__ import annotations

import pytest

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.models import ProductionRequest
from engines.interpretation_engine.foundation.concepts import (
    ConceptEntity,
    ConceptMetadata,
    ConceptRegistry,
    ConceptRelationship,
    ConceptRelationshipType,
    ConceptValidator,
    JsonConceptLoader,
    retrieve_concept,
    retrieve_concepts_for_knowledge,
)
from engines.interpretation_engine.foundation.concepts.registry import DEFAULT_CONCEPT_ROOT
from engines.interpretation_engine.foundation.knowledge import (
    KnowledgeRegistry,
    KnowledgeStatus,
    retrieve_knowledge,
)

HUYNH = ProductionRequest(
    year=1966,
    month=9,
    day=24,
    hour=4,
    minute=15,
    gender="male",
)


@pytest.fixture(scope="module")
def concept_registry() -> ConceptRegistry:
    """Default concept registry."""
    return ConceptRegistry.default()


@pytest.fixture(scope="module")
def knowledge_registry() -> KnowledgeRegistry:
    """Default knowledge registry."""
    return KnowledgeRegistry.default()


def test_concept_registry_works(concept_registry: ConceptRegistry) -> None:
    """Registry loads and indexes concepts."""
    assert concept_registry.exists("refining_metal")
    assert concept_registry.get("missing") is None
    assert "core" in concept_registry.list_categories()


def test_graph_links_model(concept_registry: ConceptRegistry) -> None:
    """Graph relationships are modeled on ConceptEntity."""
    concept = concept_registry.get("refining_metal")
    assert concept is not None
    assert concept.related_concepts == ()
    assert concept_registry.related("refining_metal") == ()


def test_entity_mapping(knowledge_registry: KnowledgeRegistry) -> None:
    """Knowledge entity references concept_ids without duplicating concept content."""
    entity = knowledge_registry.get("UsefulGod", "Đinh")
    assert entity is not None
    assert entity.concept_ids == ("refining_metal",)
    assert "Đinh" in entity.meaning
    concept = retrieve_concept("refining_metal")
    assert concept is not None
    assert "tôi luyện" in concept.meaning.lower() or "luyện kim" in concept.title.lower()


def test_concept_lookup(concept_registry: ConceptRegistry) -> None:
    """get(id) returns ConceptEntity."""
    concept = concept_registry.get("refining_metal")
    assert concept is not None
    assert concept.id == "refining_metal"
    assert concept.category == "core"
    assert concept.metadata.status == KnowledgeStatus.APPROVED


def test_validation_passes(concept_registry: ConceptRegistry) -> None:
    """Default concepts pass validation."""
    result = concept_registry.validate()
    assert result.passed is True
    assert result.issues == ()


def test_cross_layer_validation(knowledge_registry: KnowledgeRegistry) -> None:
    """Knowledge entities validate against known concept ids."""
    result = knowledge_registry.validate()
    assert result.passed is True


def test_duplicate_id_detection() -> None:
    """Validator detects duplicate concept ids."""
    meta = _example_concept_metadata()
    concepts = [
        ConceptEntity(id="dup", category="core", title="A", metadata=meta),
        ConceptEntity(id="dup", category="core", title="B", metadata=meta),
    ]
    result = ConceptValidator().validate(concepts)
    assert any(issue.code == "duplicate_id" for issue in result.issues)


def test_circular_self_reference_detection() -> None:
    """Validator detects self-referencing graph edges."""
    meta = _example_concept_metadata()
    concept = ConceptEntity(
        id="self_ref",
        category="core",
        title="Self",
        metadata=meta,
        related_concepts=(
            ConceptRelationship(
                target_id="self_ref",
                relationship=ConceptRelationshipType.SUPPORTS,
            ),
        ),
    )
    result = ConceptValidator().validate([concept])
    assert any(issue.code == "circular_self_reference" for issue in result.issues)


def test_unknown_relationship_detection() -> None:
    """Loader rejects invalid relationship types at parse time."""
    from engines.interpretation_engine.foundation.concepts.loader import ConceptLoadError

    loader = JsonConceptLoader(DEFAULT_CONCEPT_ROOT)
    with pytest.raises(ConceptLoadError, match="invalid relationship"):
        loader._parse_concept(
            {
                "id": "bad_rel",
                "category": "core",
                "title": "Bad",
                "related_concepts": [{"target_id": "x", "relationship": "invalid_type"}],
                "metadata": {
                    "author": "test",
                    "version": "1.0.0",
                    "status": "draft",
                    "source": "test",
                },
            }
        )


def test_broken_reference_detection() -> None:
    """Validator detects unresolved concept graph references."""
    meta = _example_concept_metadata()
    concept = ConceptEntity(
        id="broken",
        category="core",
        title="Broken",
        metadata=meta,
        related_concepts=(
            ConceptRelationship(
                target_id="missing_concept",
                relationship=ConceptRelationshipType.REQUIRES,
            ),
        ),
    )
    result = ConceptValidator().validate([concept])
    assert any(issue.code == "broken_reference" for issue in result.issues)


def test_generic_registry_api(concept_registry: ConceptRegistry) -> None:
    """Registry exposes get, exists, list, validate, related."""
    assert concept_registry.exists("refining_metal")
    items = concept_registry.list("core")
    assert len(items) == 1
    assert items[0].id == "refining_metal"
    assert concept_registry.validate().passed
    assert concept_registry.related("refining_metal") == ()


def test_golden_example_mapping() -> None:
    """UsefulGod/Đinh maps to refining_metal concept."""
    entity = retrieve_knowledge("UsefulGod", "Đinh")
    assert entity is not None
    concepts = retrieve_concepts_for_knowledge("UsefulGod", "Đinh")
    assert len(concepts) == 1
    assert concepts[0].id == "refining_metal"
    assert ("UsefulGod", "Đinh") in {
        (ref.domain, ref.key) for ref in concepts[0].related_entities
    }


def test_interpreter_retrieves_concepts_through_entity() -> None:
    """Decision explanation selected key resolves entity then concepts."""
    output = ProductionEngineRunner().run(HUYNH)
    foundation = output.interpretation_foundation
    assert foundation is not None
    explanation = foundation.useful_god_explanation
    assert explanation is not None
    assert explanation.decision is not None

    selected = explanation.decision.selected
    concepts = retrieve_concepts_for_knowledge("UsefulGod", selected)
    assert len(concepts) == 1
    assert concepts[0].id == "refining_metal"


def test_loader_works() -> None:
    """JSON loader reads concept registry and category files."""
    loader = JsonConceptLoader(DEFAULT_CONCEPT_ROOT)
    registry_data = loader.load_registry()
    assert "core" in registry_data["categories"]
    concepts = loader.load_all()
    assert len(concepts) >= 1
    assert concepts[0].category == "core"


def _example_concept_metadata() -> ConceptMetadata:
    return ConceptMetadata(
        author="test",
        version="1.0.0",
        status=KnowledgeStatus.DRAFT,
        source="test",
    )
