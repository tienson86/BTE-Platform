"""Tests for Pack 03 validation framework."""

from __future__ import annotations

from engines.interpretation_engine.interpreter_runtime.registries.interpreter_registry import (
    InterpreterRegistry,
)
from engines.interpretation_engine.interpreter_runtime.registries.graphs import (
    ExecutionGraph,
    GraphNode,
)
from engines.interpretation_engine.models.metadata import Metadata
from engines.interpretation_engine.models.version_info import VersionInfo
from engines.interpretation_engine.sentence_runtime.runtime import SentenceRuntime
from engines.interpretation_engine.sentence_runtime.registry import SentenceRuntimeRegistry
from engines.interpretation_engine.tests.runtime.conftest import (
    make_final_result,
    make_pack_context,
)
from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.validation import (
    ContextValidator,
    ContractValidator,
    DependencyValidator,
    MetadataValidator,
    RegistryValidator,
    ValidationFramework,
    ValidationIssue,
    ValidationReport,
    VersionValidator,
)


def test_validation_framework_validate_all_success() -> None:
    """Framework validates all six domains successfully."""
    runtime = SentenceRuntime()
    runtime.initialize()
    registry = InterpreterRegistry()
    registry.auto_register()
    context = make_pack_context(result_id="fr_val")
    metadata = Metadata(
        id="meta_1",
        version_info=VersionInfo(schema_version="1.0.0"),
        created_at="2026-01-01T00:00:00Z",
    )
    graph = ExecutionGraph()
    graph.rebuild_from_nodes(
        (
            GraphNode(node_id="a", priority=1, dependencies=()),
            GraphNode(node_id="b", priority=2, dependencies=("a",)),
        )
    )

    framework = ValidationFramework()
    report = framework.validate_all(
        runtime=runtime,
        registry=registry,
        context=context,
        metadata=metadata,
        required_dependencies=("a",),
        available_dependencies=("a", "b"),
        dependency_map={"a": (), "b": ("a",)},
        execution_graph=graph,
        version_info=metadata.version_info,
    )
    assert report.success is True
    assert "validation_framework_ok" in report.messages
    assert framework.contracts is not None
    assert framework.registries is not None
    assert framework.context is not None
    assert framework.metadata is not None
    assert framework.dependencies is not None
    assert framework.versions is not None


def test_domain_validators_failure_paths() -> None:
    """Each domain validator reports failures clearly."""
    assert ContractValidator().validate(None).success is False
    runtime = SentenceRuntime()
    assert ContractValidator().validate(runtime).success is False  # not initialized

    assert RegistryValidator().validate(None).success is False
    empty_registry = SentenceRuntimeRegistry()
    assert RegistryValidator().validate(empty_registry).success is True

    assert ContextValidator().validate(None).success is False
    assert ContextValidator().validate(object()).success is False
    final = make_final_result(result_id="fr_bad_ctx")
    invalid = PackInterpretationContext(
        id="",
        version="1.0.0",
        pipeline_id="p",
        source_final_result_id=final.id,
        final_result=final,
        created_at="2026-01-01T00:00:00Z",
    )
    assert ContextValidator().validate(invalid).success is False

    assert MetadataValidator().validate(None).success is False
    assert MetadataValidator().validate(object()).success is False
    bad_meta = Metadata(
        id="",
        version_info=VersionInfo(schema_version="1.0.0"),
        created_at="2026-01-01T00:00:00Z",
    )
    assert MetadataValidator().validate(bad_meta).success is False

    deps = DependencyValidator().validate(
        required=("x",),
        available=("y",),
        dependency_map={"a": ("missing",)},
        execution_graph=type("G", (), {"validate": lambda self: False})(),
    )
    assert deps.success is False
    assert deps.error_codes()

    versions = VersionValidator()
    assert versions.validate_version_string(None).success is False
    assert versions.validate_version_string("1").success is False
    assert versions.validate_version_info(None).success is False
    assert versions.validate_version_info(object()).success is False
    assert versions.validate_version_info(
        VersionInfo(schema_version="")
    ).success is False
    assert versions.validate_compatibility(current="1.0.0", minimum="2.0.0").success is False
    assert versions.validate_compatibility(current="2.1.0", minimum="2.0.0").success is True


def test_validation_report_merge_and_issue_model() -> None:
    """ValidationReport.merge aggregates domain reports."""
    left = ValidationReport(success=True, messages=("ok",), domain="a")
    right = ValidationReport(
        success=False,
        messages=("bad",),
        domain="b",
        issues=(
            ValidationIssue(code="x", domain="b", message="failed"),
        ),
    )
    merged = ValidationReport.merge(left, right)
    assert merged.success is False
    assert "bad" in merged.messages
    assert merged.error_codes() == ("x",)
    assert ValidationIssue(code="c", domain="d", message="m").validate() is True
    assert ValidationIssue(code="", domain="d", message="m").validate() is False
    assert ValidationReport(success=True, issues=()).validate() is True


def test_framework_noop_and_base_registry_path() -> None:
    """Framework noop and BaseRegistry path without validate_registry()."""
    framework = ValidationFramework()
    noop = framework.validate_all()
    assert noop.success is True
    assert "validation_framework_noop" in noop.messages

    registry = SentenceRuntimeRegistry()
    registry.register("s1", {"id": "s1"})
    report = framework.validate_all(registry=registry)
    assert report.success is True


def test_dependency_validator_empty_and_graph_ok() -> None:
    """Dependency validator handles empty input and valid graphs."""
    assert DependencyValidator().validate().success is True
    graph = ExecutionGraph()
    graph.rebuild_from_nodes((GraphNode(node_id="a", priority=1),))
    report = DependencyValidator().validate(
        dependency_map={"a": ()},
        execution_graph=graph,
    )
    assert report.success is True
