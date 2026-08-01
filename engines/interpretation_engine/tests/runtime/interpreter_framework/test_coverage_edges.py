"""Edge-case tests to raise Interpreter Framework coverage."""

from __future__ import annotations

import pytest

from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps
from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.interpreter_framework import (
    ConfigurationError,
    EmptyFrameworkInterpreter,
    ExecutionStatistics,
    FrameworkInterpreterContext,
    FrameworkInterpreterResult,
    InterpretationSectionBuilder,
    InterpreterCapability,
    InterpreterFactory,
    InterpreterMetadata,
    InterpreterTrace,
    InterpreterTraceEvent,
    InterpreterValidator,
    ValidationError,
)
from engines.interpretation_engine.interpreter_framework.interpreter_dependency import (
    DependencyResolver,
)
from engines.interpretation_engine.tests.runtime.conftest import make_pack_context


def test_capability_version_and_priority_types() -> None:
    """Capability rejects empty version and non-int priority."""
    assert (
        InterpreterCapability(
            interpreter_id="x", category="c", priority=1, version=""
        ).validate()
        is False
    )
    assert (
        InterpreterCapability(
            interpreter_id="x",
            category="c",
            priority="10",  # type: ignore[arg-type]
            version="1.0.0",
        ).validate()
        is False
    )


def test_builder_with_paragraphs_and_factory_none_constructor() -> None:
    """Builder with_paragraphs and factory None constructor paths."""
    section = (
        InterpretationSectionBuilder()
        .for_interpreter(interpreter_id="x", section_type="x")
        .with_paragraphs(())
        .build()
    )
    assert section.paragraphs == ()

    factory = InterpreterFactory()
    with pytest.raises(ConfigurationError):
        factory.register("x", None)  # type: ignore[arg-type]


def test_factory_rejects_blank_instance_id() -> None:
    """Factory rejects constructors that produce blank interpreter_id."""

    class _Blank(EmptyFrameworkInterpreter):
        interpreter_id = ""

    factory = InterpreterFactory()
    factory.register("blank", _Blank)
    # Instance interpreter_id is blank while registration key differs.
    with pytest.raises(ConfigurationError):
        factory.create("blank")


def test_context_invalid_pack_and_result_validate_branches() -> None:
    """Cover invalid pack context and result nested validate failures."""
    ts = ModelTimestamps(created_at="")
    meta = AnalysisMetadata(
        id="m", version="1.0.0", metadata={}, trace=(), timestamps=ts
    )
    fr = FinalResult(
        id="fr",
        version="1.0.0",
        metadata=meta,
        trace=(),
        timestamps=ts,
        pipeline_id="p",
        success=True,
    )
    pack = PackInterpretationContext(
        id="ctx",
        version="1.0.0",
        pipeline_id="ip",
        source_final_result_id="fr",
        final_result=fr,
        created_at="2026-01-01T00:00:00Z",
    )
    # final_result timestamps invalid -> pack validate False
    assert pack.validate() is False
    fw = FrameworkInterpreterContext.from_pack_context(pack)
    assert fw.validate() is False

    good = make_pack_context(result_id="fr_edge")
    section = (
        InterpretationSectionBuilder()
        .for_interpreter(interpreter_id="x", section_type="x", context_id=good.id)
        .build()
    )
    meta_ok = InterpreterMetadata(interpreter_id="x", version="1.0.0")

    bad_meta = FrameworkInterpreterResult(
        section=section,
        metadata=InterpreterMetadata(interpreter_id="", version="1.0.0"),
    )
    assert bad_meta.validate() is False

    bad_stats = FrameworkInterpreterResult(
        section=section,
        metadata=meta_ok,
        statistics=ExecutionStatistics(duration_ms=-1.0),
    )
    assert bad_stats.validate() is False

    bad_trace = FrameworkInterpreterResult(
        section=section,
        metadata=meta_ok,
        trace=InterpreterTrace(events=(InterpreterTraceEvent(name=""),)),
    )
    assert bad_trace.validate() is False

    # Force section invalid by bypassing builder validate: empty section_type impossible
    # via builder; use validate_section false path via empty id object mock.
    validator = InterpreterValidator()
    assert validator.validate_input(object()) is False
    with pytest.raises(ValidationError):
        validator.require_input(
            PackInterpretationContext(
                id="",
                version="1.0.0",
                pipeline_id="ip",
                source_final_result_id=good.final_result.id,
                final_result=good.final_result,
                created_at="2026-01-01T00:00:00Z",
            )
        )

    # require_section with invalid section
    invalid_section = section
    # Can't mutate frozen; call require_section on a broken synthetic by rebuilding wrong
    # Use validate_section False via a section with empty type through SectionResult direct
    from engines.interpretation_engine.models.section_result import SectionResult

    broken = SectionResult(id="", section_type="x")
    assert validator.validate_section(broken) is False
    with pytest.raises(ValidationError):
        validator.require_section(broken)

    broken_result = FrameworkInterpreterResult(
        section=broken,
        metadata=meta_ok,
    )
    assert broken_result.validate() is False
    with pytest.raises(ValidationError):
        validator.require_result(broken_result)


def test_dependency_skips_unavailable_optional_required_edge() -> None:
    """Resolver ignores required edges pointing outside the selected set only after check.

    Missing required already raises; this covers the continue branch when dep filtered.
    """
    resolver = DependencyResolver()
    # Include dep in ids so resolve succeeds; optional missing only.
    resolution = resolver.resolve(
        interpreter_ids=("a", "b"),
        required={"b": ("a",)},
        optional={"b": ("z",)},
    )
    assert resolution.order == ("a", "b")
    assert "b->z" in resolution.missing_optional


def test_base_health_metrics_passthrough() -> None:
    """Explicitly exercise health/metrics wrappers."""
    runtime = EmptyFrameworkInterpreter(builder=InterpretationSectionBuilder())
    runtime.initialize()
    _ = runtime.health()
    _ = runtime.metrics()
    _ = runtime.new_builder()
