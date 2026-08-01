"""Result serializer for infrastructure persistence and audit."""

from __future__ import annotations

import json
from typing import Any, Mapping

from engines.analysis_engine.exceptions.result_error import ResultError
from engines.analysis_engine.models.analysis_decision import AnalysisDecision
from engines.analysis_engine.models.analysis_evidence import AnalysisEvidence
from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps
from engines.analysis_engine.models.analysis_result import AnalysisResult
from engines.analysis_engine.models.analysis_score import AnalysisScore
from engines.analysis_engine.models.final_result import FinalResult
from engines.analysis_engine.models.module_result import ModuleResult
from engines.analysis_engine.models.stage_result import StageResult


class ResultSerializer:
    """Serialize and deserialize immutable result contracts.

    Preserves identifiers, versions, metadata, decisions, evidence, scores, and trace.
    Does not generate interpretive content.
    """

    def analysis_to_dict(self, result: AnalysisResult) -> dict[str, Any]:
        """Convert an analysis result to a JSON-compatible dictionary."""
        return {
            "id": result.id,
            "version": result.version,
            "pipeline_id": result.pipeline_id,
            "success": result.success,
            "trace": list(result.trace),
            "timestamps": self._timestamps_to_dict(result.timestamps),
            "metadata": self._metadata_to_dict(result.metadata),
            "stage_results": [self.stage_to_dict(item) for item in result.stage_results],
            "module_results": [self.module_to_dict(item) for item in result.module_results],
            "scores": [self.score_to_dict(item) for item in result.scores],
            "decisions": [self.decision_to_dict(item) for item in result.decisions],
        }

    def analysis_from_dict(self, payload: Mapping[str, Any]) -> AnalysisResult:
        """Restore an analysis result from a dictionary."""
        try:
            return AnalysisResult(
                id=str(payload["id"]),
                version=str(payload.get("version") or "1.0.0"),
                metadata=self._metadata_from_dict(payload.get("metadata") or {}),
                trace=tuple(payload.get("trace") or ()),
                timestamps=self._timestamps_from_dict(payload.get("timestamps") or {}),
                pipeline_id=str(payload["pipeline_id"]),
                success=bool(payload.get("success", True)),
                stage_results=tuple(
                    self.stage_from_dict(item)
                    for item in payload.get("stage_results") or ()
                    if isinstance(item, Mapping)
                ),
                module_results=tuple(
                    self.module_from_dict(item)
                    for item in payload.get("module_results") or ()
                    if isinstance(item, Mapping)
                ),
                scores=tuple(
                    self.score_from_dict(item)
                    for item in payload.get("scores") or ()
                    if isinstance(item, Mapping)
                ),
                decisions=tuple(
                    self.decision_from_dict(item)
                    for item in payload.get("decisions") or ()
                    if isinstance(item, Mapping)
                ),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ResultError(f"analysis_result_deserialize_failed:{exc}") from exc

    def final_to_dict(self, result: FinalResult) -> dict[str, Any]:
        """Convert a final result to a JSON-compatible dictionary."""
        return {
            "id": result.id,
            "version": result.version,
            "pipeline_id": result.pipeline_id,
            "success": result.success,
            "trace": list(result.trace),
            "timestamps": self._timestamps_to_dict(result.timestamps),
            "metadata": self._metadata_to_dict(result.metadata),
            "analysis_result": (
                self.analysis_to_dict(result.analysis_result)
                if result.analysis_result is not None
                else None
            ),
            "module_results": [self.module_to_dict(item) for item in result.module_results],
            "scores": [self.score_to_dict(item) for item in result.scores],
            "decisions": [self.decision_to_dict(item) for item in result.decisions],
            "summary_codes": list(result.summary_codes),
        }

    def final_from_dict(self, payload: Mapping[str, Any]) -> FinalResult:
        """Restore a final result from a dictionary."""
        try:
            analysis_payload = payload.get("analysis_result")
            analysis_result = (
                self.analysis_from_dict(analysis_payload)
                if isinstance(analysis_payload, Mapping)
                else None
            )
            return FinalResult(
                id=str(payload["id"]),
                version=str(payload.get("version") or "1.0.0"),
                metadata=self._metadata_from_dict(payload.get("metadata") or {}),
                trace=tuple(payload.get("trace") or ()),
                timestamps=self._timestamps_from_dict(payload.get("timestamps") or {}),
                pipeline_id=str(payload["pipeline_id"]),
                success=bool(payload.get("success", True)),
                analysis_result=analysis_result,
                module_results=tuple(
                    self.module_from_dict(item)
                    for item in payload.get("module_results") or ()
                    if isinstance(item, Mapping)
                ),
                scores=tuple(
                    self.score_from_dict(item)
                    for item in payload.get("scores") or ()
                    if isinstance(item, Mapping)
                ),
                decisions=tuple(
                    self.decision_from_dict(item)
                    for item in payload.get("decisions") or ()
                    if isinstance(item, Mapping)
                ),
                summary_codes=tuple(payload.get("summary_codes") or ()),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ResultError(f"final_result_deserialize_failed:{exc}") from exc

    def stage_to_dict(self, result: StageResult) -> dict[str, Any]:
        """Convert a stage result to a dictionary."""
        return {
            "id": result.id,
            "version": result.version,
            "stage_id": result.stage_id,
            "success": result.success,
            "trace": list(result.trace),
            "timestamps": self._timestamps_to_dict(result.timestamps),
            "metadata": self._metadata_to_dict(result.metadata),
            "scores": [self.score_to_dict(item) for item in result.scores],
            "decisions": [self.decision_to_dict(item) for item in result.decisions],
            "payload": dict(result.payload),
        }

    def stage_from_dict(self, payload: Mapping[str, Any]) -> StageResult:
        """Restore a stage result from a dictionary."""
        return StageResult(
            id=str(payload["id"]),
            version=str(payload.get("version") or "1.0.0"),
            metadata=self._metadata_from_dict(payload.get("metadata") or {}),
            trace=tuple(payload.get("trace") or ()),
            timestamps=self._timestamps_from_dict(payload.get("timestamps") or {}),
            stage_id=str(payload["stage_id"]),
            success=bool(payload.get("success", True)),
            scores=tuple(
                self.score_from_dict(item)
                for item in payload.get("scores") or ()
                if isinstance(item, Mapping)
            ),
            decisions=tuple(
                self.decision_from_dict(item)
                for item in payload.get("decisions") or ()
                if isinstance(item, Mapping)
            ),
            payload=dict(payload.get("payload") or {}),
        )

    def module_to_dict(self, result: ModuleResult) -> dict[str, Any]:
        """Convert a module result to a dictionary."""
        return {
            "id": result.id,
            "version": result.version,
            "module_id": result.module_id,
            "success": result.success,
            "trace": list(result.trace),
            "timestamps": self._timestamps_to_dict(result.timestamps),
            "metadata": self._metadata_to_dict(result.metadata),
            "stage_results": [self.stage_to_dict(item) for item in result.stage_results],
            "scores": [self.score_to_dict(item) for item in result.scores],
            "decisions": [self.decision_to_dict(item) for item in result.decisions],
            "payload": dict(result.payload),
        }

    def module_from_dict(self, payload: Mapping[str, Any]) -> ModuleResult:
        """Restore a module result from a dictionary."""
        return ModuleResult(
            id=str(payload["id"]),
            version=str(payload.get("version") or "1.0.0"),
            metadata=self._metadata_from_dict(payload.get("metadata") or {}),
            trace=tuple(payload.get("trace") or ()),
            timestamps=self._timestamps_from_dict(payload.get("timestamps") or {}),
            module_id=str(payload["module_id"]),
            success=bool(payload.get("success", True)),
            stage_results=tuple(
                self.stage_from_dict(item)
                for item in payload.get("stage_results") or ()
                if isinstance(item, Mapping)
            ),
            scores=tuple(
                self.score_from_dict(item)
                for item in payload.get("scores") or ()
                if isinstance(item, Mapping)
            ),
            decisions=tuple(
                self.decision_from_dict(item)
                for item in payload.get("decisions") or ()
                if isinstance(item, Mapping)
            ),
            payload=dict(payload.get("payload") or {}),
        )

    def score_to_dict(self, score: AnalysisScore) -> dict[str, Any]:
        """Convert a score to a dictionary."""
        return {
            "id": score.id,
            "version": score.version,
            "dimension": score.dimension,
            "value": score.value,
            "unit": score.unit,
            "trace": list(score.trace),
            "timestamps": self._timestamps_to_dict(score.timestamps),
            "metadata": self._metadata_to_dict(score.metadata),
        }

    def score_from_dict(self, payload: Mapping[str, Any]) -> AnalysisScore:
        """Restore a score from a dictionary."""
        return AnalysisScore(
            id=str(payload["id"]),
            version=str(payload.get("version") or "1.0.0"),
            metadata=self._metadata_from_dict(payload.get("metadata") or {}),
            trace=tuple(payload.get("trace") or ()),
            timestamps=self._timestamps_from_dict(payload.get("timestamps") or {}),
            dimension=str(payload["dimension"]),
            value=float(payload["value"]),
            unit=payload.get("unit"),
        )

    def decision_to_dict(self, decision: AnalysisDecision) -> dict[str, Any]:
        """Convert a decision to a dictionary."""
        return {
            "id": decision.id,
            "version": decision.version,
            "decision_type": decision.decision_type,
            "outcome": decision.outcome,
            "confidence": decision.confidence,
            "trace": list(decision.trace),
            "timestamps": self._timestamps_to_dict(decision.timestamps),
            "metadata": self._metadata_to_dict(decision.metadata),
            "evidence": [self.evidence_to_dict(item) for item in decision.evidence],
        }

    def decision_from_dict(self, payload: Mapping[str, Any]) -> AnalysisDecision:
        """Restore a decision from a dictionary."""
        return AnalysisDecision(
            id=str(payload["id"]),
            version=str(payload.get("version") or "1.0.0"),
            metadata=self._metadata_from_dict(payload.get("metadata") or {}),
            trace=tuple(payload.get("trace") or ()),
            timestamps=self._timestamps_from_dict(payload.get("timestamps") or {}),
            decision_type=str(payload["decision_type"]),
            outcome=str(payload["outcome"]),
            confidence=payload.get("confidence"),
            evidence=tuple(
                self.evidence_from_dict(item)
                for item in payload.get("evidence") or ()
                if isinstance(item, Mapping)
            ),
        )

    def evidence_to_dict(self, evidence: AnalysisEvidence) -> dict[str, Any]:
        """Convert evidence to a dictionary."""
        return {
            "id": evidence.id,
            "version": evidence.version,
            "source": evidence.source,
            "reference_ids": list(evidence.reference_ids),
            "payload": dict(evidence.payload),
            "trace": list(evidence.trace),
            "timestamps": self._timestamps_to_dict(evidence.timestamps),
            "metadata": self._metadata_to_dict(evidence.metadata),
        }

    def evidence_from_dict(self, payload: Mapping[str, Any]) -> AnalysisEvidence:
        """Restore evidence from a dictionary."""
        return AnalysisEvidence(
            id=str(payload["id"]),
            version=str(payload.get("version") or "1.0.0"),
            metadata=self._metadata_from_dict(payload.get("metadata") or {}),
            trace=tuple(payload.get("trace") or ()),
            timestamps=self._timestamps_from_dict(payload.get("timestamps") or {}),
            source=str(payload["source"]),
            reference_ids=tuple(payload.get("reference_ids") or ()),
            payload=dict(payload.get("payload") or {}),
        )

    def to_json(self, result: AnalysisResult | FinalResult, *, indent: int | None = 2) -> str:
        """Serialize an analysis or final result to JSON."""
        if isinstance(result, FinalResult):
            payload = self.final_to_dict(result)
        else:
            payload = self.analysis_to_dict(result)
        return json.dumps(payload, ensure_ascii=False, indent=indent, sort_keys=True)

    def analysis_from_json(self, payload: str) -> AnalysisResult:
        """Deserialize an analysis result from JSON."""
        return self.analysis_from_dict(self._load_json_object(payload))

    def final_from_json(self, payload: str) -> FinalResult:
        """Deserialize a final result from JSON."""
        return self.final_from_dict(self._load_json_object(payload))

    def _load_json_object(self, payload: str) -> dict[str, Any]:
        """Parse a JSON object payload."""
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise ResultError("result_json_invalid") from exc
        if not isinstance(data, dict):
            raise ResultError("result_json_payload_invalid")
        return data

    def _timestamps_to_dict(self, timestamps: ModelTimestamps) -> dict[str, Any]:
        """Serialize timestamps."""
        return {
            "created_at": timestamps.created_at,
            "updated_at": timestamps.updated_at,
            "completed_at": timestamps.completed_at,
        }

    def _timestamps_from_dict(self, payload: Mapping[str, Any]) -> ModelTimestamps:
        """Deserialize timestamps."""
        created_at = payload.get("created_at")
        if not created_at:
            raise ResultError("timestamps_created_at_required")
        return ModelTimestamps(
            created_at=str(created_at),
            updated_at=payload.get("updated_at"),
            completed_at=payload.get("completed_at"),
        )

    def _metadata_to_dict(self, metadata: AnalysisMetadata) -> dict[str, Any]:
        """Serialize metadata."""
        return {
            "id": metadata.id,
            "version": metadata.version,
            "metadata": dict(metadata.metadata),
            "trace": list(metadata.trace),
            "timestamps": (
                self._timestamps_to_dict(metadata.timestamps)
                if metadata.timestamps is not None
                else None
            ),
        }

    def _metadata_from_dict(self, payload: Mapping[str, Any]) -> AnalysisMetadata:
        """Deserialize metadata."""
        timestamps_payload = payload.get("timestamps")
        timestamps = (
            self._timestamps_from_dict(timestamps_payload)
            if isinstance(timestamps_payload, Mapping)
            else None
        )
        return AnalysisMetadata(
            id=str(payload.get("id") or "meta_unknown"),
            version=str(payload.get("version") or "1.0.0"),
            metadata=dict(payload.get("metadata") or {}),
            trace=tuple(payload.get("trace") or ()),
            timestamps=timestamps,
        )
