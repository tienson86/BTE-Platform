"""Template engine infrastructure tests (mock refs only, no templates)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from engines.interpretation_engine.exceptions.template_error import TemplateEngineError
from engines.interpretation_engine.template_engine import (
    Loader,
    Metadata,
    Renderer,
    Resolver,
    TemplateBinding,
    TemplateEngine,
    TemplateRef,
    TemplateRenderShell,
    Validator,
)


class TestTemplateEngineInfrastructure:
    """Mock-only template reference infrastructure coverage."""

    def test_loader_mapping_file_and_body_rejection(self, tmp_path: Path) -> None:
        """Loader loads descriptors and rejects template bodies."""
        loader = Loader()
        refs = loader.load_from_mapping(
            {
                "entries": [
                    {
                        "ref_id": "tpl_x",
                        "slot_names": "solo",
                        "version": "1.0.0",
                        "owner": "test",
                    }
                ]
            }
        )
        assert refs[0].slot_names == ("solo",)
        single = loader.load_from_mapping({"ref_id": "tpl_y", "slots": ["a", "b"]})
        assert single[0].ref_id == "tpl_y"
        path = tmp_path / "tpl.json"
        path.write_text(
            json.dumps({"templates": [{"ref_id": "tpl_f", "slot_names": ["z"]}]}),
            encoding="utf-8",
        )
        assert loader.list_ref_ids(path) == ("tpl_f",)
        with pytest.raises(TemplateEngineError, match="template_body_not_allowed"):
            loader.load_from_mapping(
                {"entries": [{"ref_id": "bad", "slot_names": ["a"], "text": "Hi"}]}
            )
        with pytest.raises(TemplateEngineError, match="template_descriptor_payload_unsupported"):
            loader.load_from_mapping({"foo": 1})
        with pytest.raises(TemplateEngineError, match="template_descriptor_path_not_found"):
            loader.load_from_path(tmp_path / "missing.json")

    def test_resolver_validator_renderer(
        self,
        template_ref_catalog: tuple[TemplateRef, ...],
    ) -> None:
        """Resolver/validator/renderer produce shells without prose."""
        resolver = Resolver(ref_provider=lambda: template_ref_catalog)
        assert resolver.resolve("tpl_a").slot_names == ("subject", "tone")
        assert resolver.resolve_many(("tpl_b", "tpl_a"))[0].ref_id == "tpl_b"
        assert resolver.resolve_by_domain("career")[0].ref_id == "tpl_b"
        assert resolver.resolve_metadata("tpl_a")["ref_id"] == "tpl_a"
        validator = Validator()
        ref = resolver.resolve("tpl_a")
        assert validator.validate_binding(ref, {"subject": "s", "tone": "t"}) is True
        assert validator.validate_binding(ref, {"subject": "s"}) is False
        assert validator.validate_binding_object(
            ref,
            TemplateBinding(template_ref_id="tpl_a", values={"subject": "s", "tone": "t"}),
        )
        renderer = Renderer(resolver=resolver, validator=validator)
        shell = renderer.render_by_id("tpl_b", {"role": "r1"})
        assert shell.validate() is True
        assert not hasattr(shell, "text")
        binding = renderer.bind("tpl_a", {"subject": "s", "tone": "calm"})
        assert binding.template_ref_id == "tpl_a"
        with pytest.raises(TemplateEngineError, match="template_resolver_required"):
            Renderer().render_by_id("tpl_a", {"subject": "s", "tone": "t"})
        with pytest.raises(TemplateEngineError, match="template_refs_not_found"):
            resolver.resolve_many(("missing",))
        with pytest.raises(TemplateEngineError, match="template_domain_required"):
            resolver.resolve_by_domain("")

    def test_metadata_and_engine_facade(
        self,
        template_ref_catalog: tuple[TemplateRef, ...],
    ) -> None:
        """Metadata helper and TemplateEngine facade."""
        ref = template_ref_catalog[0]
        meta = Metadata()
        assert meta.from_ref(ref)["slot_names"] == ["subject", "tone"]
        binding = TemplateBinding(template_ref_id="tpl_a", values={"subject": "s", "tone": "t"})
        assert meta.from_binding(binding)["template_ref_id"] == "tpl_a"
        shell = TemplateRenderShell(
            render_id="r1",
            template_ref=ref,
            binding=binding,
        )
        assert meta.from_render_shell(shell)["render_id"] == "r1"
        assert meta.from_mapping({"ref_id": "x"})["ref_id"] == "x"
        assert meta.from_mapping({"metadata": {"k": 1}, "ref_id": "r"})["k"] == 1
        with pytest.raises(TemplateEngineError):
            meta.from_mapping({"foo": 1})
        assert TemplateRef(ref_id="", slot_names=("a",)).validate() is False
        assert TemplateRef(ref_id="t", slot_names=("",)).validate() is False

        engine = TemplateEngine(catalog=template_ref_catalog)
        engine.set_catalog(template_ref_catalog)
        assert engine.loader is not None
        assert engine.resolver is not None
        assert engine.validator is not None
        assert engine.renderer is not None
        assert engine.validate("tpl_a") is True
        assert engine.validate("") is False
        assert engine.validate("missing") is False
        bound = engine.bind("tpl_b", {"role": "x"})
        assert bound.values["role"] == "x"
        rendered = engine.render("tpl_b", {"role": "y"})
        assert rendered.status == "bound"
        assert Validator().validate_render_shell(rendered) is True
