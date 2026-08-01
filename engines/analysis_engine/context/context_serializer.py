"""Analysis context serializer for lifecycle persistence."""

from __future__ import annotations

import json
from typing import Any, Mapping

from engines.analysis_engine.context.context_revision import ContextLifecyclePhase
from engines.analysis_engine.context.context_snapshot import ContextSnapshot
from engines.analysis_engine.exceptions.context_error import ContextError
from engines.analysis_engine.models.analysis_context import AnalysisContext
from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps


class ContextSerializer:
    """Serialize and deserialize Analysis Context lifecycle artifacts.

    Supports JSON for debug, audit, snapshot, and testing.
    Does not persist temporary runtime execution state as authoritative data.
    """

    def to_dict(self, context: AnalysisContext) -> dict[str, Any]:
        """Convert an Analysis Context to a JSON-compatible dictionary."""
        return {
            "id": context.id,
            "version": context.version,
            "pipeline_id": context.pipeline_id,
            "chart_id": context.chart_id,
            "trace": list(context.trace),
            "attributes": dict(context.attributes),
            "timestamps": {
                "created_at": context.timestamps.created_at,
                "updated_at": context.timestamps.updated_at,
                "completed_at": context.timestamps.completed_at,
            },
            "metadata": {
                "id": context.metadata.id,
                "version": context.metadata.version,
                "metadata": dict(context.metadata.metadata),
                "trace": list(context.metadata.trace),
                "timestamps": (
                    {
                        "created_at": context.metadata.timestamps.created_at,
                        "updated_at": context.metadata.timestamps.updated_at,
                        "completed_at": context.metadata.timestamps.completed_at,
                    }
                    if context.metadata.timestamps is not None
                    else None
                ),
            },
        }

    def from_dict(self, payload: Mapping[str, Any]) -> AnalysisContext:
        """Restore an Analysis Context from a dictionary payload."""
        try:
            timestamps_raw = payload.get("timestamps") or {}
            timestamps = ModelTimestamps(
                created_at=str(timestamps_raw["created_at"]),
                updated_at=timestamps_raw.get("updated_at"),
                completed_at=timestamps_raw.get("completed_at"),
            )
            metadata_raw = payload.get("metadata") or {}
            meta_timestamps = None
            meta_ts_raw = metadata_raw.get("timestamps")
            if isinstance(meta_ts_raw, Mapping):
                meta_timestamps = ModelTimestamps(
                    created_at=str(meta_ts_raw["created_at"]),
                    updated_at=meta_ts_raw.get("updated_at"),
                    completed_at=meta_ts_raw.get("completed_at"),
                )
            metadata = AnalysisMetadata(
                id=str(metadata_raw.get("id") or f"meta_{payload['id']}"),
                version=str(metadata_raw.get("version") or payload.get("version") or "1.0.0"),
                metadata=dict(metadata_raw.get("metadata") or {}),
                trace=tuple(metadata_raw.get("trace") or ()),
                timestamps=meta_timestamps or timestamps,
            )
            return AnalysisContext(
                id=str(payload["id"]),
                version=str(payload.get("version") or "1.0.0"),
                metadata=metadata,
                trace=tuple(payload.get("trace") or ()),
                timestamps=timestamps,
                pipeline_id=str(payload["pipeline_id"]),
                chart_id=payload.get("chart_id"),
                attributes=dict(payload.get("attributes") or {}),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ContextError(f"context_deserialize_failed:{exc}") from exc

    def to_json(self, context: AnalysisContext, *, indent: int | None = 2) -> str:
        """Serialize an Analysis Context to a JSON string."""
        return json.dumps(self.to_dict(context), ensure_ascii=False, indent=indent, sort_keys=True)

    def from_json(self, payload: str) -> AnalysisContext:
        """Deserialize an Analysis Context from a JSON string."""
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise ContextError("context_json_invalid") from exc
        if not isinstance(data, dict):
            raise ContextError("context_json_payload_invalid")
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
                raise ContextError("snapshot_context_payload_invalid")
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
            raise ContextError(f"snapshot_deserialize_failed:{exc}") from exc

    def snapshot_to_json(self, snapshot: ContextSnapshot, *, indent: int | None = 2) -> str:
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
            raise ContextError("snapshot_json_invalid") from exc
        if not isinstance(data, dict):
            raise ContextError("snapshot_json_payload_invalid")
        return self.snapshot_from_dict(data)
