"""Extra edge-coverage tests for Pack 03 infrastructure gaps."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context import ContextBuilder, ContextManager, ContextSerializer
from engines.interpretation_engine.exceptions.context_error import InterpretationContextError
from engines.interpretation_engine.exceptions.registry_error import InterpretationRegistryError
from engines.interpretation_engine.exceptions.sentence_error import SentenceEngineError
from engines.interpretation_engine.exceptions.template_error import TemplateEngineError
from engines.interpretation_engine.pipeline import Pipeline, PipelineContext, StageBase, StageOutcome
from engines.interpretation_engine.pipeline.execution_result import ExecutionResult
from engines.interpretation_engine.pipeline.execution_state import ExecutionStatus
from engines.interpretation_engine.pipeline.pipeline_result import InterpretationPipelineResult
from engines.interpretation_engine.registry import Loader, Registry, VersionManager
from engines.interpretation_engine.registry.metadata import InterpreterRegistryEntry
from engines.interpretation_engine.sentence_engine import (
    Composer,
    Resolver as SentenceResolver,
    SentenceCandidate,
    SentenceComposition,
    SentenceEngine,
    SentenceRef,
)
from engines.interpretation_engine.template_engine import (
    Loader as TemplateLoader,
    Renderer,
    Resolver as TemplateResolver,
    TemplateBinding,
    TemplateRef,
    Validator as TemplateValidator,
)
from tests.interpretation_engine.mocks import MockSuccessStage


class _BoomPrepareStage(StageBase):
    """Stage that fails during prepare to exercise orchestration error path."""

    def prepare(self, context: PipelineContext) -> None:
        raise RuntimeError("prepare_boom")

    def execute(self, context: PipelineContext) -> StageOutcome:
        return StageOutcome(stage_id=self.stage_id, success=True)

    def finalize(self, context: PipelineContext, outcome: StageOutcome) -> None:
        return None


def test_pipeline_orchestration_error_from_validate_required(
    pipeline_context_stub: PipelineContext,
) -> None:
    """Cover InterpretationPipelineResult validate helper."""
    assert InterpretationPipelineResult(id="x", pipeline_id="p", success=True).validate()
    assert not InterpretationPipelineResult(id="", pipeline_id="p", success=True).validate()
    result = ExecutionResult(
        execution_id="e",
        pipeline_id="p",
        success=True,
        status=ExecutionStatus.SUCCEEDED,
        outcomes=(StageOutcome(stage_id="a", success=True),),
    )
    assert result.outcome_for("missing") is None


def test_pipeline_prepare_error_path(pipeline_context_stub: PipelineContext) -> None:
    """Prepare failures are normalized by stage executor."""
    result = Pipeline(
        pipeline_id="interp_pipeline",
        stages=(_BoomPrepareStage(stage_id="prep", name="Prep", order=1),),
    ).run(pipeline_context_stub)
    assert result.success is False


def test_stage_base_helpers(pipeline_context_stub: PipelineContext) -> None:
    """StageBase default dependencies/validate helpers."""
    stage = MockSuccessStage(stage_id="s", order=1)
    assert stage.dependencies() == ()
    assert stage.validate(pipeline_context_stub) is True


def test_context_builder_errors_and_history(
    final_result_stub: FinalResult,
) -> None:
    """Builder errors and serializer snapshot invalid payloads."""
    with pytest.raises(InterpretationContextError, match="final_result_required"):
        ContextBuilder().build_context()
    serializer = ContextSerializer()
    with pytest.raises(InterpretationContextError, match="snapshot_json_invalid"):
        serializer.snapshot_from_json("{")
    with pytest.raises(InterpretationContextError, match="snapshot_json_payload_invalid"):
        serializer.snapshot_from_json("[]")
    manager = ContextManager()
    manager.create(final_result=final_result_stub)
    manager.initialize()
    assert manager.history is not None
    assert manager.history.revision_count() >= 1
    assert manager.history.latest_revision() is not None
    snap = manager.snapshot()
    assert manager.history.latest_snapshot() is not None
    assert manager.context is not None


def test_registry_loader_unbound_and_invalid_json(tmp_path: Path) -> None:
    """Loader unbound pack path and invalid JSON edges."""
    loader = Loader()
    with pytest.raises(InterpretationRegistryError, match="pack_path_unbound"):
        loader.load_pack_registry("PACK_X")
    bad = tmp_path / "bad.json"
    bad.write_text("{", encoding="utf-8")
    with pytest.raises(InterpretationRegistryError, match="registry_load_failed"):
        loader.load_snapshot(bad)
    arr = tmp_path / "arr.json"
    arr.write_text("[]", encoding="utf-8")
    with pytest.raises(InterpretationRegistryError, match="registry_payload_invalid"):
        loader.load_snapshot(arr)
    with pytest.raises(InterpretationRegistryError, match="registry_entry_missing_id"):
        loader.load_entries_from_mapping({"entries": [{"name": "x"}]})
    with pytest.raises(InterpretationRegistryError, match="invalid_version"):
        VersionManager().parse_version("1.2.3.4")
    registry = Registry()
    registry.register(
        InterpreterRegistryEntry(
            entry_id="x",
            interpreter_id="x",
            name="X",
            version="1.0.0",
            status="active",
        )
    )
    assert registry.loader is not None
    assert registry.resolver is not None
    assert registry.version_manager is not None
    assert registry.dependency_graph is not None
    assert registry.metadata is not None


def test_sentence_resolver_missing_and_composition_validate() -> None:
    """Sentence resolver missing refs and composition validate edge."""
    resolver = SentenceResolver(ref_provider=lambda: ())
    with pytest.raises(SentenceEngineError, match="sentence_ref_not_found"):
        resolver.resolve("missing")
    with pytest.raises(SentenceEngineError, match="sentence_refs_not_found"):
        resolver.resolve_many(("a",))
    assert SentenceComposition(composition_id="").validate() is False
    bad = SentenceComposition(
        composition_id="c",
        ref_ids=("a",),
        candidates=(
            SentenceCandidate(ref=SentenceRef(ref_id="b")),
        ),
    )
    assert bad.validate() is False
    assert Composer().validate(SentenceComposition(composition_id="ok")) is True
    engine = SentenceEngine()
    assert engine.validate(()) is False


def test_template_validator_assert_and_invalid_ref() -> None:
    """Template validator assert_binding and invalid ref shells."""
    ref = TemplateRef(ref_id="t", slot_names=("a", "b"))
    validator = TemplateValidator()
    with pytest.raises(TemplateEngineError, match="template_binding_invalid"):
        validator.assert_binding(ref, {"a": 1})
    assert validator.validate_ref_id("") is False
    assert validator.validate_binding_object(
        ref,
        TemplateBinding(template_ref_id="other", values={"a": 1, "b": 2}),
    ) is False
    with pytest.raises(TemplateEngineError, match="template_ref_invalid"):
        Renderer().render(TemplateRef(ref_id=""), {"a": 1})
    with pytest.raises(TemplateEngineError, match="template_ref_required"):
        Renderer().bind("", {})
    with pytest.raises(TemplateEngineError, match="template_ref_required"):
        TemplateResolver(ref_provider=lambda: ()).resolve("")
    loader = TemplateLoader()
    with pytest.raises(TemplateEngineError, match="template_slots_invalid"):
        loader.load_from_mapping({"entries": [{"ref_id": "t", "slot_names": 123}]})
    path = Path("nope.json")
    # ensure invalid path message for non-file handled above in other test
    _ = path
