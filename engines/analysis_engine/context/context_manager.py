"""Analysis context manager for Pack 02 lifecycle orchestration."""

from __future__ import annotations

from typing import Any, Mapping
from uuid import uuid4

from engines.analysis_engine.context.context_builder import utc_now
from engines.analysis_engine.context.context_factory import ContextFactory
from engines.analysis_engine.context.context_history import ContextHistory
from engines.analysis_engine.context.context_revision import (
    ContextLifecyclePhase,
    ContextRevision,
)
from engines.analysis_engine.context.context_serializer import ContextSerializer
from engines.analysis_engine.context.context_snapshot import ContextSnapshot
from engines.analysis_engine.exceptions.context_error import ContextError
from engines.analysis_engine.models.analysis_context import AnalysisContext
from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps

_PHASE_ORDER: tuple[ContextLifecyclePhase, ...] = (
    ContextLifecyclePhase.CREATED,
    ContextLifecyclePhase.INITIALIZED,
    ContextLifecyclePhase.EXPANDED,
    ContextLifecyclePhase.VALIDATED,
    ContextLifecyclePhase.FINALIZED,
    ContextLifecyclePhase.DISPOSED,
)


class ContextManager:
    """Manages Analysis Context lifecycle without analyzer business logic.

    Lifecycle: Create → Initialize → Expand → Validate → Finalize → Dispose.
    Context instances remain immutable; updates produce new revisions.
    """

    def __init__(
        self,
        *,
        factory: ContextFactory | None = None,
        serializer: ContextSerializer | None = None,
    ) -> None:
        """Initialize context lifecycle collaborators."""
        self._factory = factory or ContextFactory()
        self._serializer = serializer or ContextSerializer()
        self._context: AnalysisContext | None = None
        self._phase: ContextLifecyclePhase | None = None
        self._history: ContextHistory | None = None
        self._revision_number = 0

    @property
    def phase(self) -> ContextLifecyclePhase | None:
        """Return the current lifecycle phase."""
        return self._phase

    @property
    def context(self) -> AnalysisContext | None:
        """Return the current immutable Analysis Context."""
        return self._context

    @property
    def history(self) -> ContextHistory | None:
        """Return the immutable revision/snapshot history."""
        return self._history

    def create(
        self,
        *,
        pipeline_id: str,
        context_id: str | None = None,
        chart_id: str | None = None,
        attributes: Mapping[str, Any] | None = None,
        pipeline_run_id: str | None = None,
    ) -> AnalysisContext:
        """Create and activate a new Analysis Context."""
        if self._context is not None and self._phase != ContextLifecyclePhase.DISPOSED:
            raise ContextError("context_already_active")
        context = self._factory.create(
            pipeline_id=pipeline_id,
            context_id=context_id,
            chart_id=chart_id,
            attributes=attributes,
        )
        self._context = context
        self._phase = ContextLifecyclePhase.CREATED
        self._revision_number = 0
        self._history = ContextHistory(context_id=context.id)
        self._record_revision(
            phase=ContextLifecyclePhase.CREATED,
            pipeline_run_id=pipeline_run_id,
            messages=("context_created",),
        )
        return context

    def initialize(
        self,
        *,
        chart_id: str | None = None,
        chart_attributes: Mapping[str, Any] | None = None,
        stage_id: str | None = None,
        pipeline_run_id: str | None = None,
    ) -> AnalysisContext:
        """Initialize context with chart-level data (Initialize phase)."""
        context = self._require_context()
        self._assert_phase_at_most(ContextLifecyclePhase.CREATED)
        attrs: dict[str, Any] = {}
        if chart_attributes:
            attrs["chart_context"] = dict(chart_attributes)
        updated = self._factory.clone_with_attributes(
            context,
            attrs,
            trace_item="initialize",
        )
        if chart_id is not None:
            updated = AnalysisContext(
                id=updated.id,
                version=updated.version,
                metadata=updated.metadata,
                trace=updated.trace,
                timestamps=updated.timestamps,
                pipeline_id=updated.pipeline_id,
                chart_id=chart_id,
                attributes=updated.attributes,
            )
        self._context = updated
        self._phase = ContextLifecyclePhase.INITIALIZED
        self._record_revision(
            phase=ContextLifecyclePhase.INITIALIZED,
            stage_id=stage_id,
            pipeline_run_id=pipeline_run_id,
            attribute_keys=tuple(sorted(attrs.keys())),
            messages=("context_initialized",),
        )
        return updated

    def expand(
        self,
        attributes: Mapping[str, Any],
        *,
        stage_id: str | None = None,
        analyzer_id: str | None = None,
        pipeline_run_id: str | None = None,
        trace_item: str | None = None,
    ) -> AnalysisContext:
        """Expand context with opaque attributes (Expand phase).

        Callers supply already-produced values. This method does not run analyzers.
        """
        context = self._require_context()
        self._assert_expandable()
        if not attributes:
            raise ContextError("expand_attributes_required")
        updated = self._factory.clone_with_attributes(
            context,
            attributes,
            trace_item=trace_item or stage_id or analyzer_id or "expand",
        )
        self._context = updated
        self._phase = ContextLifecyclePhase.EXPANDED
        self._record_revision(
            phase=ContextLifecyclePhase.EXPANDED,
            stage_id=stage_id,
            analyzer_id=analyzer_id,
            pipeline_run_id=pipeline_run_id,
            attribute_keys=tuple(sorted(attributes.keys())),
            messages=("context_expanded",),
        )
        return updated

    def validate(self) -> bool:
        """Validate context integrity (Validate phase)."""
        context = self._require_context()
        self._assert_not_disposed()
        if self._phase in {
            ContextLifecyclePhase.CREATED,
        }:
            raise ContextError("context_not_ready_for_validate")
        ok = self._validate_structure(context)
        if not ok:
            raise ContextError("context_integrity_failed")
        self._phase = ContextLifecyclePhase.VALIDATED
        self._record_revision(
            phase=ContextLifecyclePhase.VALIDATED,
            messages=("context_validated",),
        )
        return True

    def finalize(self) -> AnalysisContext:
        """Finalize context and mark completion (Finalize phase)."""
        context = self._require_context()
        self._assert_not_disposed()
        if self._phase not in {
            ContextLifecyclePhase.INITIALIZED,
            ContextLifecyclePhase.EXPANDED,
            ContextLifecyclePhase.VALIDATED,
        }:
            raise ContextError(f"invalid_finalize_phase:{self._phase}")
        if self._phase != ContextLifecyclePhase.VALIDATED:
            self.validate()
            context = self._require_context()
        stamp = utc_now()
        timestamps = ModelTimestamps(
            created_at=context.timestamps.created_at,
            updated_at=stamp,
            completed_at=stamp,
        )
        metadata = AnalysisMetadata(
            id=context.metadata.id,
            version=context.metadata.version,
            metadata=dict(context.metadata.metadata),
            trace=context.trace + ("finalize",),
            timestamps=timestamps,
        )
        finalized = AnalysisContext(
            id=context.id,
            version=context.version,
            metadata=metadata,
            trace=context.trace + ("finalize",),
            timestamps=timestamps,
            pipeline_id=context.pipeline_id,
            chart_id=context.chart_id,
            attributes=dict(context.attributes),
        )
        self._context = finalized
        self._phase = ContextLifecyclePhase.FINALIZED
        self._record_revision(
            phase=ContextLifecyclePhase.FINALIZED,
            messages=("context_finalized",),
        )
        return finalized

    def dispose(self) -> None:
        """Dispose runtime context after pipeline completion (Dispose phase)."""
        self._require_context()
        self._assert_not_disposed()
        if self._phase not in {
            ContextLifecyclePhase.FINALIZED,
            ContextLifecyclePhase.VALIDATED,
            ContextLifecyclePhase.EXPANDED,
            ContextLifecyclePhase.INITIALIZED,
        }:
            raise ContextError(f"invalid_dispose_phase:{self._phase}")
        self._phase = ContextLifecyclePhase.DISPOSED
        self._record_revision(
            phase=ContextLifecyclePhase.DISPOSED,
            messages=("context_disposed",),
        )
        # Keep history and last context for audit; mark disposed.
        return None

    def snapshot(self, *, label: str | None = None) -> ContextSnapshot:
        """Capture an immutable snapshot of the current context."""
        context = self._require_context()
        if self._phase is None:
            raise ContextError("context_phase_missing")
        snap = ContextSnapshot(
            snapshot_id=str(uuid4()),
            context_id=context.id,
            phase=self._phase,
            revision_number=self._revision_number,
            context=context,
            created_at=utc_now(),
            label=label,
        )
        if self._history is None:
            raise ContextError("context_history_missing")
        self._history = self._history.with_snapshot(snap)
        return snap

    def restore_snapshot(self, snapshot: ContextSnapshot) -> AnalysisContext:
        """Restore manager state from a previously captured snapshot."""
        if (
            self._context is not None
            and self._phase not in {None, ContextLifecyclePhase.DISPOSED}
            and self._context.id != snapshot.context_id
        ):
            raise ContextError("snapshot_restore_context_mismatch")
        self._context = snapshot.context
        self._phase = snapshot.phase
        self._revision_number = snapshot.revision_number
        if self._history is None or self._history.context_id != snapshot.context_id:
            self._history = ContextHistory(context_id=snapshot.context_id)
        return snapshot.context

    def serialize(self) -> str:
        """Serialize the current context to JSON."""
        return self._serializer.to_json(self._require_context())

    def serialize_snapshot(self, snapshot: ContextSnapshot) -> str:
        """Serialize a snapshot to JSON."""
        return self._serializer.snapshot_to_json(snapshot)

    def _record_revision(
        self,
        *,
        phase: ContextLifecyclePhase,
        stage_id: str | None = None,
        analyzer_id: str | None = None,
        pipeline_run_id: str | None = None,
        attribute_keys: tuple[str, ...] = (),
        messages: tuple[str, ...] = (),
    ) -> ContextRevision:
        """Append a monotonic revision to history."""
        if self._context is None or self._history is None:
            raise ContextError("context_not_initialized")
        self._revision_number += 1
        revision = ContextRevision(
            revision_number=self._revision_number,
            context_id=self._context.id,
            phase=phase,
            timestamp=utc_now(),
            stage_id=stage_id,
            analyzer_id=analyzer_id,
            pipeline_run_id=pipeline_run_id,
            attribute_keys=attribute_keys,
            messages=messages,
        )
        self._history = self._history.with_revision(revision)
        return revision

    def _require_context(self) -> AnalysisContext:
        """Return the active context or raise."""
        if self._context is None:
            raise ContextError("context_not_created")
        return self._context

    def _assert_not_disposed(self) -> None:
        """Reject operations after dispose."""
        if self._phase == ContextLifecyclePhase.DISPOSED:
            raise ContextError("context_disposed")

    def _assert_expandable(self) -> None:
        """Allow expand only from initialized or expanded phases."""
        self._assert_not_disposed()
        if self._phase not in {
            ContextLifecyclePhase.INITIALIZED,
            ContextLifecyclePhase.EXPANDED,
        }:
            raise ContextError(f"invalid_expand_phase:{self._phase}")

    def _assert_phase_at_most(self, phase: ContextLifecyclePhase) -> None:
        """Ensure current phase has not progressed beyond ``phase``."""
        self._assert_not_disposed()
        if self._phase is None:
            raise ContextError("context_phase_missing")
        if _PHASE_ORDER.index(self._phase) > _PHASE_ORDER.index(phase):
            raise ContextError(f"invalid_phase_transition:{self._phase}:{phase}")

    def _validate_structure(self, context: AnalysisContext) -> bool:
        """Validate structural integrity only (no analyzer semantics)."""
        if not context.id:
            return False
        if not context.pipeline_id:
            return False
        if not context.version:
            return False
        if context.timestamps.created_at is None:
            return False
        if context.metadata.id is None:
            return False
        return True
