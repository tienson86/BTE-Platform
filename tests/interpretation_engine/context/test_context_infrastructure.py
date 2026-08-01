"""Context lifecycle infrastructure tests (mock FinalResult only)."""

from __future__ import annotations

import pytest

from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context import (
    ContextBuilder,
    ContextFactory,
    ContextLifecyclePhase,
    ContextManager,
    ContextSerializer,
    PackInterpretationContext,
)
from engines.interpretation_engine.exceptions.context_error import InterpretationContextError
from engines.interpretation_engine.models.final_analysis_input import FinalAnalysisInput


class TestContextLifecycle:
    """Mock-only interpretation context coverage."""

    def test_full_lifecycle_and_serialize(self, final_result_stub: FinalResult) -> None:
        """Create → initialize → expand → validate → finalize → snapshot → dispose."""
        manager = ContextManager()
        created = manager.create(final_result=final_result_stub, context_id="ctx_1")
        assert isinstance(created, PackInterpretationContext)
        assert manager.phase == ContextLifecyclePhase.CREATED

        manager.initialize(init_attributes={"locale": "vi"})
        manager.expand({"section": "personality"})
        assert manager.validate() is True
        finalized = manager.finalize()
        assert finalized.completed_at is not None
        snap = manager.snapshot(label="final")
        payload = manager.serialize()
        assert "fr_stub_1" in payload
        snap_json = manager.serialize_snapshot(snap)
        restored_snap = ContextSerializer().snapshot_from_json(snap_json)
        assert restored_snap.context_id == created.id
        manager.dispose()
        assert manager.phase == ContextLifecyclePhase.DISPOSED

    def test_builder_interface_and_factory_clone(
        self,
        final_result_stub: FinalResult,
    ) -> None:
        """Builder/factory create and clone contexts from FinalResult."""
        final_input = FinalAnalysisInput(
            id="inp_1",
            version="1.0.0",
            final_result=final_result_stub,
            metadata={"k": "v"},
        )
        builder = ContextBuilder().with_final_result(final_result_stub)
        assert builder.validate(final_input) is True
        model = builder.build(final_input)
        assert model.id
        context = ContextFactory().create_from_final_result(final_result_stub)
        cloned = ContextFactory().clone_with_attributes(
            context,
            {"extra": 1},
            trace_item="expand",
        )
        assert cloned.attributes["extra"] == 1
        assert "expand" in cloned.trace

    def test_manager_phase_guards(self, final_result_stub: FinalResult) -> None:
        """Lifecycle guards reject invalid transitions."""
        manager = ContextManager()
        with pytest.raises(InterpretationContextError, match="context_not_created"):
            manager.validate()
        manager.create(final_result=final_result_stub)
        with pytest.raises(InterpretationContextError, match="context_already_active"):
            manager.create(final_result=final_result_stub)
        with pytest.raises(InterpretationContextError, match="context_not_ready_for_validate"):
            manager.validate()
        manager.initialize()
        with pytest.raises(InterpretationContextError, match="expand_attributes_required"):
            manager.expand({})
        manager.expand({"a": 1})
        manager.validate()
        manager.finalize()
        manager.dispose()
        with pytest.raises(InterpretationContextError, match="context_disposed"):
            manager.expand({"b": 2})

    def test_restore_snapshot(self, final_result_stub: FinalResult) -> None:
        """Snapshot restore reloads manager state."""
        manager = ContextManager()
        manager.create(final_result=final_result_stub, context_id="ctx_snap")
        manager.initialize()
        snap = manager.snapshot(label="init")
        manager.expand({"x": 1})
        restored = manager.restore_snapshot(snap)
        assert manager.phase == ContextLifecyclePhase.INITIALIZED
        assert restored.id == "ctx_snap"

    def test_serializer_roundtrip_and_errors(
        self,
        final_result_stub: FinalResult,
    ) -> None:
        """Serializer round-trips and rejects invalid payloads."""
        context = ContextFactory().create(final_result=final_result_stub)
        serializer = ContextSerializer()
        restored = serializer.from_json(serializer.to_json(context))
        assert restored.source_final_result_id == context.source_final_result_id
        with pytest.raises(InterpretationContextError, match="context_json_invalid"):
            serializer.from_json("{")
        with pytest.raises(InterpretationContextError, match="context_json_payload_invalid"):
            serializer.from_json("[]")
        with pytest.raises(InterpretationContextError):
            serializer.from_dict({"id": "x"})
