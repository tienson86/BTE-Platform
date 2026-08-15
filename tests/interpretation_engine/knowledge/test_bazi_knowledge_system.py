"""Sprint K1 — BaZi Knowledge System tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.models import ProductionRequest
from engines.interpretation_engine.foundation.interpreters.useful_god import UsefulGodInterpreter
from engines.interpretation_engine.foundation.knowledge import (
    JsonKnowledgeLoader,
    KnowledgeEntity,
    KnowledgeRegistry,
    KnowledgeStatus,
    KnowledgeValidator,
    retrieve_knowledge,
)
from engines.interpretation_engine.foundation.knowledge.registry import DEFAULT_KNOWLEDGE_ROOT

HUYNH = ProductionRequest(
    year=1966,
    month=9,
    day=24,
    hour=4,
    minute=15,
    gender="male",
)


@pytest.fixture(scope="module")
def registry() -> KnowledgeRegistry:
    """Default knowledge registry."""
    return KnowledgeRegistry.default()


def test_registry_works(registry: KnowledgeRegistry) -> None:
    """Registry loads and indexes entities."""
    assert registry.exists("UsefulGod", "Đinh")
    assert registry.get("UsefulGod", "Missing") is None
    assert "UsefulGod" in registry.list_domains()


def test_loader_works() -> None:
    """JSON loader reads registry and domain files."""
    loader = JsonKnowledgeLoader(DEFAULT_KNOWLEDGE_ROOT)
    registry_data = loader.load_registry()
    assert "UsefulGod" in registry_data["domains"]
    entities = loader.load_all()
    assert len(entities) >= 1
    assert entities[0].domain == "UsefulGod"


def test_validation_passes(registry: KnowledgeRegistry) -> None:
    """Default knowledge passes validation."""
    result = registry.validate()
    assert result.passed is True
    assert result.issues == ()


def test_duplicate_id_detection() -> None:
    """Validator detects duplicate ids."""
    meta = _example_metadata()
    entities = [
        KnowledgeEntity(
            id="dup.id",
            domain="UsefulGod",
            key="A",
            title="A",
            metadata=meta,
        ),
        KnowledgeEntity(
            id="dup.id",
            domain="UsefulGod",
            key="B",
            title="B",
            metadata=meta,
        ),
    ]
    result = KnowledgeValidator().validate(entities)
    assert result.passed is False
    assert any(issue.code == "duplicate_id" for issue in result.issues)


def test_missing_key_detection() -> None:
    """Validator detects missing key."""
    entity = KnowledgeEntity(
        id="test.nokey",
        domain="UsefulGod",
        key="",
        title="T",
        metadata=_example_metadata(),
    )
    result = KnowledgeValidator().validate([entity])
    assert any(issue.code == "missing_key" for issue in result.issues)


def test_knowledge_lookup(registry: KnowledgeRegistry) -> None:
    """get(domain, key) returns KnowledgeEntity."""
    entity = registry.get("UsefulGod", "Đinh")
    assert entity is not None
    assert entity.key == "Đinh"
    assert entity.metadata.status == KnowledgeStatus.APPROVED
    assert "Hỏa" in entity.meaning


def test_generic_api(registry: KnowledgeRegistry) -> None:
    """Registry exposes get, exists, list, validate."""
    assert registry.exists("UsefulGod", "Đinh")
    items = registry.list("UsefulGod")
    assert len(items) >= 1
    assert any(item.key == "Đinh" for item in items)
    validation = registry.validate()
    assert validation.passed


def test_example_entity_loads(registry: KnowledgeRegistry) -> None:
    """Golden example UsefulGod/Đinh loads with expected fields."""
    entity = registry.get("UsefulGod", "Đinh")
    assert entity is not None
    assert entity.id == "knowledge.useful_god.dinh"
    assert entity.title
    assert entity.meaning
    assert entity.positive_meaning
    assert "career" in entity.applications


def test_interpreter_can_retrieve_example() -> None:
    """Decision explainer selected value maps to knowledge lookup."""
    output = ProductionEngineRunner().run(HUYNH)
    foundation = output.interpretation_foundation
    assert foundation is not None
    explanation = foundation.useful_god_explanation
    assert explanation is not None
    assert explanation.decision is not None

    selected = explanation.decision.selected
    entity = retrieve_knowledge("UsefulGod", selected)
    assert entity is not None
    assert entity.key == selected == "Đinh"


def test_broken_reference_detection() -> None:
    """Validator detects unresolved related_entities."""
    from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntityReference

    meta = _example_metadata()
    entity = KnowledgeEntity(
        id="test.ref",
        domain="UsefulGod",
        key="X",
        title="X",
        metadata=meta,
        related_entities=(
            KnowledgeEntityReference(domain="Strength", key="missing"),
        ),
    )
    result = KnowledgeValidator().validate([entity])
    assert any(issue.code == "broken_reference" for issue in result.issues)


def test_unknown_domain_detection() -> None:
    """Validator flags unknown domain."""
    entity = KnowledgeEntity(
        id="test.unknown",
        domain="NotARealDomain",
        key="K",
        title="T",
        metadata=_example_metadata(),
    )
    result = KnowledgeValidator().validate([entity])
    assert any(issue.code == "unknown_domain" for issue in result.issues)


def test_no_ui_dependency() -> None:
    """Knowledge runtime has no portal imports."""
    import engines.interpretation_engine.foundation.knowledge.registry as mod

    assert "customer_portal" not in (mod.__file__ or "")


def _example_metadata():
    from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeMetadata

    return KnowledgeMetadata(
        author="test",
        version="1.0.0",
        status=KnowledgeStatus.DRAFT,
        source="test",
    )
