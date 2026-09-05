"""Pack 07 service layer — foundation orchestration only."""

from __future__ import annotations

from typing import Any, Mapping

from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.diagnostics import Pack07RuntimeDiagnostics
from engines.detailed_interpretation_engine.engine import DetailedInterpretationEngine
from engines.detailed_interpretation_engine.factories import (
    api_model_from_runtime,
    consulting_model_from_runtime,
    export_model_from_runtime,
)
from engines.detailed_interpretation_engine.runtime import (
    CanonicalAPIModel,
    CanonicalConsultingModel,
    CanonicalExportModel,
    CanonicalRuntimeResult,
)
from engines.detailed_interpretation_engine.serialization import (
    deserialize_runtime_result,
    serialize_runtime_result,
)
from engines.detailed_interpretation_engine.validation import ValidationResult


class DetailedInterpretationService:
    """Service wrapper around the foundation engine."""

    def __init__(self, engine: DetailedInterpretationEngine | None = None) -> None:
        self._engine = engine or DetailedInterpretationEngine()

    def empty_published_result(self, analysis_id: str, *, chart_id: str = "") -> CanonicalRuntimeResult:
        """Instantiate a serializable unpublished/not-evaluated contract."""
        return self._engine.empty_result(analysis_id, chart_id=chart_id)

    def build_contexts(self, payload: Mapping[str, Any]) -> CanonicalAnalysisContext:
        """Build Pack 07 context chain from upstream payload. No reasoning."""
        return self._engine.build_contexts(payload)

    def serialize(self, result: CanonicalRuntimeResult) -> dict[str, object]:
        """Serialize CanonicalRuntimeResult."""
        return serialize_runtime_result(result)

    def deserialize(self, payload: dict[str, object]) -> CanonicalRuntimeResult:
        """Deserialize CanonicalRuntimeResult."""
        return deserialize_runtime_result(payload)

    def export_projection(self, result: CanonicalRuntimeResult) -> CanonicalExportModel:
        """Build CanonicalExportModel from a published result."""
        return export_model_from_runtime(result)

    def api_projection(self, result: CanonicalRuntimeResult) -> CanonicalAPIModel:
        """Build CanonicalAPIModel from a published result."""
        return api_model_from_runtime(result)

    def consulting_projection(self, result: CanonicalRuntimeResult) -> CanonicalConsultingModel:
        """Build CanonicalConsultingModel from a published result."""
        return consulting_model_from_runtime(result)

    def validate_contexts(self, context: CanonicalAnalysisContext) -> ValidationResult:
        """Validate Pack 07 context chain."""
        return self._engine.validate_contexts(context)

    def validate_runtime(self, result: CanonicalRuntimeResult) -> ValidationResult:
        """Validate CanonicalRuntimeResult."""
        return self._engine.validate_runtime(result)

    def diagnostics(self, context: CanonicalAnalysisContext) -> Pack07RuntimeDiagnostics:
        """Development-only Pack 07 diagnostics."""
        return self._engine.diagnostics(context)
