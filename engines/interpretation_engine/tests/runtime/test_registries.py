"""Runtime registry contract tests."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.explanation_runtime.registry import (
    ExplanationRuntimeRegistry,
)
from engines.interpretation_engine.interpreter_runtime.registry import (
    InterpreterRuntimeRegistry,
)
from engines.interpretation_engine.placeholder_runtime.binder import PlaceholderRuntimeBinder
from engines.interpretation_engine.placeholder_runtime.registry import (
    PlaceholderRuntimeRegistry,
)
from engines.interpretation_engine.runtime.registry_base import RegistryError
from engines.interpretation_engine.sentence_runtime.registry import SentenceRuntimeRegistry
from engines.interpretation_engine.sentence_runtime.selector import SentenceRuntimeSelector
from engines.interpretation_engine.template_runtime.registry import TemplateRuntimeRegistry
from engines.interpretation_engine.template_runtime.resolver import TemplateRuntimeResolver


@pytest.mark.parametrize(
    "registry_cls",
    [
        InterpreterRuntimeRegistry,
        SentenceRuntimeRegistry,
        TemplateRuntimeRegistry,
        PlaceholderRuntimeRegistry,
        ExplanationRuntimeRegistry,
    ],
)
def test_registry_contract(registry_cls: type) -> None:
    """Every registry supports register/unregister/lookup/list/validate."""
    registry = registry_cls()
    assert registry.validate() is True
    registry.register("alpha", {"id": "alpha"})
    registry.register("beta", {"id": "beta", "domain": "career"})
    assert registry.lookup("alpha") == {"id": "alpha"}
    assert registry.list() == ("alpha", "beta")
    registry.unregister("alpha")
    assert registry.lookup("alpha") is None
    assert registry.list() == ("beta",)


def test_registry_rejects_invalid_entries() -> None:
    """Registry rejects empty ids and None entries."""
    registry = SentenceRuntimeRegistry()
    with pytest.raises(RegistryError):
        registry.register("", {"id": "x"})
    with pytest.raises(RegistryError):
        registry.register("x", None)  # type: ignore[arg-type]


def test_sentence_selector_and_template_resolver() -> None:
    """Selector/resolver operate on registry refs only."""
    sentence_registry = SentenceRuntimeRegistry()
    sentence_registry.register("s1", {"domain": "career"})
    sentence_registry.register("s2", {"domain": "health"})
    selector = SentenceRuntimeSelector(sentence_registry)
    assert selector.select(domain="career") == ("s1",)
    assert set(selector.select()) == {"s1", "s2"}

    template_registry = TemplateRuntimeRegistry()
    template_registry.register("t1", {"ref": "t1"})
    resolver = TemplateRuntimeResolver(template_registry)
    assert resolver.resolve("t1") == {"ref": "t1"}
    with pytest.raises(RegistryError, match="template_ref_not_found"):
        resolver.resolve("missing")


def test_placeholder_binder() -> None:
    """Binder scopes values to registered placeholder ids only."""
    registry = PlaceholderRuntimeRegistry()
    registry.register("p1", {"id": "p1"})
    registry.register("p2", {"id": "p2"})
    binder = PlaceholderRuntimeBinder(registry)
    bound = binder.bind({"p1": "opaque", "p3": "ignored"})
    assert bound == {"p1": "opaque"}
