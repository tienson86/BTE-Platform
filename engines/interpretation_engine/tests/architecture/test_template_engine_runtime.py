"""Architecture tests for template engine infrastructure."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from engines.interpretation_engine.exceptions import TemplateEngineError
from engines.interpretation_engine.template_engine import (
    Loader,
    Renderer,
    Resolver,
    TemplateEngine,
    TemplateRef,
    Validator,
)


def _catalog() -> tuple[TemplateRef, ...]:
    """Build a small in-memory template-ref catalog (no bodies)."""
    return (
        TemplateRef(
            ref_id="tpl_personality_intro",
            domain="personality",
            section="intro",
            status="active",
            slot_names=("subject", "tone"),
            tags=("core",),
        ),
        TemplateRef(
            ref_id="tpl_career_body",
            domain="career",
            section="body",
            status="active",
            slot_names=("role",),
        ),
    )


def test_loader_from_mapping_rejects_body() -> None:
    """Loader accepts descriptors and rejects embedded template bodies."""
    loader = Loader()
    refs = loader.load_from_mapping(
        {
            "entries": [
                {
                    "ref_id": "tpl_a",
                    "slot_names": ["x"],
                    "version": "1.0.0",
                }
            ]
        }
    )
    assert refs[0].ref_id == "tpl_a"
    with pytest.raises(TemplateEngineError, match="template_body_not_allowed"):
        loader.load_from_mapping(
            {
                "entries": [
                    {
                        "ref_id": "tpl_bad",
                        "slot_names": ["x"],
                        "body": "Hello {{x}}",
                    }
                ]
            }
        )


def test_loader_from_file(tmp_path: Path) -> None:
    """Loader reads JSON descriptor files without template content."""
    path = tmp_path / "template_refs.json"
    path.write_text(
        json.dumps(
            {
                "templates": [
                    {
                        "ref_id": "tpl_file",
                        "slot_names": ["a", "b"],
                        "status": "active",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    refs = Loader().load_from_path(path)
    assert refs[0].slot_names == ("a", "b")


def test_resolver_and_validator() -> None:
    """Resolver hydrates refs; validator checks slot bindings."""
    resolver = Resolver(ref_provider=_catalog)
    ref = resolver.resolve("tpl_personality_intro")
    validator = Validator()
    assert validator.validate_binding(ref, {"subject": "dm", "tone": "neutral"}) is True
    assert validator.validate_binding(ref, {"subject": "dm"}) is False
    with pytest.raises(TemplateEngineError, match="template_binding_invalid"):
        validator.assert_binding(ref, {"subject": "dm", "extra": 1})


def test_renderer_produces_shell_not_prose() -> None:
    """Renderer returns structural shells only."""
    resolver = Resolver(ref_provider=_catalog)
    renderer = Renderer(resolver=resolver)
    shell = renderer.render_by_id(
        "tpl_career_body",
        {"role": "ref_role_1"},
    )
    assert shell.validate() is True
    assert shell.template_ref.ref_id == "tpl_career_body"
    assert shell.binding.values == {"role": "ref_role_1"}
    assert "text" not in shell.metadata
    assert not hasattr(shell, "text")


def test_template_engine_facade() -> None:
    """Facade binds and validates template refs without templates."""
    engine = TemplateEngine(catalog=_catalog())
    binding = engine.bind("tpl_personality_intro", {"subject": "s1", "tone": "calm"})
    assert binding.template_ref_id == "tpl_personality_intro"
    assert engine.validate("tpl_personality_intro") is True
    assert engine.validate("") is False
    shell = engine.render("tpl_career_body", {"role": "r1"})
    assert shell.status == "bound"
