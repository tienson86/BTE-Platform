"""Additional context infrastructure edge-case tests."""

from __future__ import annotations

import pytest

from engines.analysis_engine.context.context_factory import ContextFactory
from engines.analysis_engine.context.context_history import ContextHistory
from engines.analysis_engine.context.context_manager import ContextManager
from engines.analysis_engine.context.context_revision import (
    ContextLifecyclePhase,
    ContextRevision,
)
from engines.analysis_engine.context.context_serializer import ContextSerializer
from engines.analysis_engine.context.context_snapshot import ContextSnapshot
from engines.analysis_engine.context.runtime_context import RuntimeContext
from engines.analysis_engine.exceptions.context_error import ContextError


class TestContextInfrastructureEdges:
    """Extra coverage for context history/serializer/runtime edges."""

    def test_history_latest_helpers(self) -> None:
        """History should expose latest revision and snapshot helpers."""
        history = ContextHistory(context_id="h1")
        assert history.latest_revision() is None
        assert history.latest_snapshot() is None
        revision = ContextRevision(
            revision_number=1,
            context_id="h1",
            phase=ContextLifecyclePhase.CREATED,
            timestamp="2026-08-01T00:00:00Z",
        )
        history = history.with_revision(revision)
        assert history.latest_revision() is revision
        with pytest.raises(ContextError):
            history.with_revision(
                ContextRevision(
                    revision_number=1,
                    context_id="h1",
                    phase=ContextLifecyclePhase.CREATED,
                    timestamp="2026-08-01T00:00:00Z",
                )
            )

    def test_snapshot_serializer_roundtrip(self) -> None:
        """Context snapshots should serialize and deserialize."""
        manager = ContextManager()
        manager.create(pipeline_id="p", context_id="snap-ser")
        manager.initialize()
        snap = manager.snapshot(label="L")
        serializer = ContextSerializer()
        restored = serializer.snapshot_from_json(serializer.snapshot_to_json(snap))
        assert restored.snapshot_id == snap.snapshot_id
        assert restored.label == "L"
        assert isinstance(restored, ContextSnapshot)

    def test_runtime_context_accessors(self) -> None:
        """RuntimeContext interface methods should work."""
        runtime = RuntimeContext(id="r1", pipeline_id="p", attributes={}, stage_outputs={})
        assert runtime.context_id() == "r1"
        runtime.set("a", 1)
        assert runtime.get("a") == 1
        runtime.stage_outputs["s1"] = {"ok": True}
        assert runtime.get_stage_output("s1") == {"ok": True}

    def test_factory_rejects_incomplete_runtime(self) -> None:
        """Factory should reject runtime shells missing required ids."""
        factory = ContextFactory()
        with pytest.raises(ContextError):
            factory.create_from_runtime(RuntimeContext(id="", pipeline_id="p"))
        with pytest.raises(ContextError):
            factory.create_from_runtime(RuntimeContext(id="x", pipeline_id=None))

    def test_dispose_then_recreate(self) -> None:
        """Manager should allow create after dispose."""
        manager = ContextManager()
        manager.create(pipeline_id="p1", context_id="c1")
        manager.initialize()
        manager.dispose()
        created = manager.create(pipeline_id="p2", context_id="c2")
        assert created.id == "c2"
