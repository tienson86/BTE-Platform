"""Interpretation context serializer for lifecycle persistence."""

from __future__ import annotations

import json
from typing import Any, Mapping

from engines.analysis_engine.models.analysis_decision import AnalysisDecision
from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps
from engines.analysis_engine.models.analysis_result import AnalysisResult
from engines.analysis_engine.models.analysis_score import AnalysisScore
from engines.analysis_engine.models.final_result import FinalResult
from engines.analysis_engine.models.module_result import ModuleResult
from engines.interpretation_engine.context.interpretation_context import InterpretationContext
from engines.interpretation_engine.context.revision import ContextLifecyclePhase
from engines.interpretation_engine.context.snapshot import ContextSnapshot
from engines.interpretation_engine.exceptions.context_error import InterpretationContextError


class ContextSerializer:
    """Serialize and deserialize Interpretation Context lifecycle artifacts.

    Persists structural context and Pack 02 FinalResult references.
    Does not embed interpretation narrative content.
    """

    def to_dict(self, context: InterpretationContext) -> dict[str, Any]:
        """Convert an Interpretation Context to a JSON-compatible dictionary."""
        return {
            "id": context.id,
            "version": context.version,
            "pipeline_id": context.pipeline_id,
            "source_final_result_id": context.source_final_result_id,
            "trace": list(context.trace),
            "attributes": dict(context.attributes),
            "metadata": dict(context.metadata),
            "created_at": context.created_at,
            "updated_at": context.updated_at,
            "completed_at": context.completed_at,
            "final_result": self._final_result_to_dict(context.final_result),
        }

    def from_dict(self, payload: Mapping[str, Any]) -> InterpretationContext:
        """Restore an Interpretation Context from a dictionary payload."""
        try:
            final_raw = payload["final_result"]
            if not isinstance(final_raw, Mapping):
                raise InterpretationContextError("final_result_payload_invalid")
            final_result = self._final_result_from_dict(final_raw)
            return InterpretationContext(
                id=str(payload["id"]),
                version=str(payload.get("version") or "0.0.0-architecture"),
                pipeline_id=str(payload["pipeline_id"]),
                source_final_result_id=str(payload["source_final_result_id"]),
                final_result=final_result,
                attributes=dict(payload.get("attributes") or {}),
                trace=tuple(payload.get("trace") or ()),
                created_at=str(payload["created_at"]),
                updated_at=payload.get("updated_at"),
                completed_at=payload.get("completed_at"),
                metadata=dict(payload.get("metadata") or {}),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise InterpretationContextError(
                f"context_deserialize_failed:{exc}"
            ) from exc

    def to_json(self, context: InterpretationContext, *, indent: int | None = 2) -> str:
        """Serialize an Interpretation Context to a JSON string."""
        return json.dumps(
            self.to_dict(context),
            ensure_ascii=False,
            indent=indent,
            sort_keys=True,
        )

    def from_json(self, payload: str) -> InterpretationContext:
        """Deserialize an Interpretation Context from a JSON string."""
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise InterpretationContextError("context_json_invalid") from exc
        if not isinstance(data, dict):
            raise InterpretationContextError("context_json_payload_invalid")
        return self.from_dict(data)

    def snapshot_to_dict(self, snapshot: ContextSnapshot) -> dict[str, Any]:
        """Serialize a context snapshot to a dictionary."""
        return {
            "snapshot_id": snapshot.snapshot_id,
            "context_id": snapshot.context_id,
            "phase": snapshot.phase.value,
            "revision_number": snapshot.revision_number,
            "created_at": snapshot.created_at,
            "label": snapshot.label,
            "context": self.to_dict(snapshot.context),
        }

    def snapshot_from_dict(self, payload: Mapping[str, Any]) -> ContextSnapshot:
        """Deserialize a context snapshot from a dictionary."""
        try:
            phase = ContextLifecyclePhase(str(payload["phase"]))
            context_payload = payload["context"]
            if not isinstance(context_payload, Mapping):
                raise InterpretationContextError("snapshot_context_payload_invalid")
            return ContextSnapshot(
                snapshot_id=str(payload["snapshot_id"]),
                context_id=str(payload["context_id"]),
                phase=phase,
                revision_number=int(payload["revision_number"]),
                context=self.from_dict(context_payload),
                created_at=str(payload["created_at"]),
                label=payload.get("label"),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise InterpretationContextError(
                f"snapshot_deserialize_failed:{exc}"
            ) from exc

    def snapshot_to_json(
        self,
        snapshot: ContextSnapshot,
        *,
        indent: int | None = 2,
    ) -> str:
        """Serialize a context snapshot to JSON."""
        return json.dumps(
            self.snapshot_to_dict(snapshot),
            ensure_ascii=False,
            indent=indent,
            sort_keys=True,
        )

    def snapshot_from_json(self, payload: str) -> ContextSnapshot:
        """Deserialize a context snapshot from JSON."""
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise InterpretationContextError("snapshot_json_invalid") from exc
        if not isinstance(data, dict):
            raise InterpretationContextError("snapshot_json_payload_invalid")
        return self.snapshot_from_dict(data)

    def _final_result_to_dict(self, final_result: FinalResult) -> dict[str, Any]:
        """Serialize Pack 02 FinalResult structural fields only."""
        return {
            "id": final_result.id,
            "version": final_result.version,
            "pipeline_id": final_result.pipeline_id,
            "success": final_result.success,
            "trace": list(final_result.trace),
            "summary_codes": list(final_result.summary_codes),
            "timestamps": {
                "created_at": final_result.timestamps.created_at,
                "updated_at": final_result.timestamps.updated_at,
                "completed_at": final_result.timestamps.completed_at,
            },
            "metadata": {
                "id": final_result.metadata.id,
                "version": final_result.metadata.version,
                "metadata": dict(final_result.metadata.metadata),
                "trace": list(final_result.metadata.trace),
            },
            # Nested analysis payloads are intentionally omitted from context
            # persistence to keep serialization infrastructure-only.
            "module_results": [],
            "scores": [],
            "decisions": [],
            "analysis_result": None,
        }

    def _final_result_from_dict(self, payload: Mapping[str, Any]) -> FinalResult:
        """Restore a minimal Pack 02 FinalResult from serialized context."""
        timestamps_raw = payload.get("timestamps") or {}
        timestamps = ModelTimestamps(
            created_at=str(timestamps_raw["created_at"]),
            updated_at=timestamps_raw.get("updated_at"),
            completed_at=timestamps_raw.get("completed_at"),
        )
        metadata_raw = payload.get("metadata") or {}
        metadata = AnalysisMetadata(
            id=str(metadata_raw.get("id") or f"meta_{payload['id']}"),
            version=str(metadata_raw.get("version") or payload.get("version") or "1.0.0"),
            metadata=dict(metadata_raw.get("metadata") or {}),
            trace=tuple(metadata_raw.get("trace") or ()),
            timestamps=timestamps,
        )
        analysis_result: AnalysisResult | None = None
        module_results: tuple[ModuleResult, ...] = ()
        scores: tuple[AnalysisScore, ...] = ()
        decisions: tuple[AnalysisDecision, ...] = ()
        return FinalResult(
            id=str(payload["id"]),
            version=str(payload.get("version") or "1.0.0"),
            metadata=metadata,
            trace=tuple(payload.get("trace") or ()),
            timestamps=timestamps,
            pipeline_id=str(payload["pipeline_id"]),
            success=bool(payload.get("success", True)),
            analysis_result=analysis_result,
            module_results=module_results,
            scores=scores,
            decisions=decisions,
            summary_codes=tuple(payload.get("summary_codes") or ()),
        )
