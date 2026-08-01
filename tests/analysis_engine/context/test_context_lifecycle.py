"""Context lifecycle integration tests."""

from __future__ import annotations

import pytest

from engines.analysis_engine.context.context_builder import ContextBuilder
from engines.analysis_engine.context.context_factory import ContextFactory
from engines.analysis_engine.context.context_manager import ContextManager
from engines.analysis_engine.context.context_revision import ContextLifecyclePhase
from engines.analysis_engine.context.context_serializer import ContextSerializer
from engines.analysis_engine.exceptions.context_error import ContextError


class TestContextLifecycleIntegration:
    """Integration coverage for Analysis Context runtime lifecycle."""

    def test_full_lifecycle_create_to_dispose(self) -> None:
        """Context manager should support the Pack 02 lifecycle phases."""
        manager = ContextManager()
        created = manager.create(pipeline_id="pipe-ctx", context_id="ctx-1")
        assert manager.phase == ContextLifecyclePhase.CREATED
        assert created.id == "ctx-1"

        initialized = manager.initialize(
            chart_id="chart-1",
            chart_attributes={"day_master": "mock"},
        )
        assert manager.phase == ContextLifecyclePhase.INITIALIZED
        assert initialized.chart_id == "chart-1"

        expanded = manager.expand(
            {"mock_strength": {"score": 1}},
            stage_id="mock_strength",
            analyzer_id="mock_analyzer",
        )
        assert manager.phase == ContextLifecyclePhase.EXPANDED
        assert expanded.attributes["mock_strength"]["score"] == 1

        assert manager.validate() is True
        assert manager.phase == ContextLifecyclePhase.VALIDATED

        finalized = manager.finalize()
        assert manager.phase == ContextLifecyclePhase.FINALIZED
        assert finalized.timestamps.completed_at is not None

        snapshot = manager.snapshot(label="audit")
        assert snapshot.label == "audit"
        assert snapshot.context.id == "ctx-1"

        manager.dispose()
        assert manager.phase == ContextLifecyclePhase.DISPOSED
        assert manager.history is not None
        assert manager.history.revision_count() >= 5

    def test_expand_after_validate_is_rejected(self) -> None:
        """Expand should not be allowed after validate."""
        manager = ContextManager()
        manager.create(pipeline_id="p")
        manager.initialize()
        manager.expand({"a": 1})
        manager.validate()
        with pytest.raises(ContextError):
            manager.expand({"b": 2})

    def test_serializer_roundtrip(self) -> None:
        """Serializer should preserve context identity and attributes."""
        context = (
            ContextBuilder()
            .with_context_id("ser-1")
            .with_pipeline_id("pipe-ser")
            .with_attribute("k", "v")
            .with_trace("t1")
            .build_analysis_context()
        )
        serializer = ContextSerializer()
        restored = serializer.from_json(serializer.to_json(context))
        assert restored.id == context.id
        assert restored.attributes["k"] == "v"
        assert restored.validate() is True

    def test_factory_from_runtime(self) -> None:
        """Factory should create AnalysisContext from RuntimeContext."""
        factory = ContextFactory()
        runtime = factory.create_runtime(pipeline_id="p", context_id="r1", chart_id="c1")
        runtime.set("x", 1)
        analysis = factory.create_from_runtime(runtime)
        assert analysis.id == "r1"
        assert analysis.attributes["x"] == 1

    def test_snapshot_restore(self) -> None:
        """Manager should restore state from a snapshot."""
        manager = ContextManager()
        manager.create(pipeline_id="p", context_id="restore-1")
        manager.initialize(chart_id="chart-x")
        snap = manager.snapshot(label="checkpoint")
        manager.expand({"n": 1})
        restored = manager.restore_snapshot(snap)
        assert restored.chart_id == "chart-x"
        assert manager.phase == ContextLifecyclePhase.INITIALIZED
