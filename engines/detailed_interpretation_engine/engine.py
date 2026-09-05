"""Pack 07 Detailed Interpretation Engine — foundation only.

This engine instantiates and serializes frozen contracts.
It does not interpret, score, or compose narrative.
"""

from __future__ import annotations

from typing import Any, Mapping

from engines.detailed_interpretation_engine.builders import (
    build_canonical_analysis_context_from_payload,
)
from engines.detailed_interpretation_engine.context import InterpretationContext
from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.diagnostics import (
    Pack07RuntimeDiagnostics,
    build_pack07_diagnostics,
)
from engines.detailed_interpretation_engine.factories import empty_canonical_runtime_result
from engines.detailed_interpretation_engine.runtime import CanonicalRuntimeResult
from engines.detailed_interpretation_engine.serialization import (
    deserialize_runtime_result,
    serialize_runtime_result,
)
from engines.detailed_interpretation_engine.validation import ValidationResult
from engines.detailed_interpretation_engine.validators import (
    assert_valid,
    validate_canonical_runtime,
    validate_pack07_context,
)


class DetailedInterpretationEngine:
    """Foundation engine: empty contract shells and context builders."""

    name: str = "detailed_interpretation"
    version: str = "1.0.0"

    def empty_result(
        self,
        analysis_id: str,
        *,
        chart_id: str = "",
        context: InterpretationContext | None = None,
    ) -> CanonicalRuntimeResult:
        """Return a not-evaluated CanonicalRuntimeResult for analysis_id."""
        resolved_chart = chart_id or (context.chart_id if context is not None else "")
        return empty_canonical_runtime_result(analysis_id, chart_id=resolved_chart)

    def build_contexts(self, payload: Mapping[str, Any]) -> CanonicalAnalysisContext:
        """Build Pack 07 context chain from upstream payload. No reasoning."""
        return build_canonical_analysis_context_from_payload(payload)

    def serialize(self, result: CanonicalRuntimeResult) -> dict[str, object]:
        """Serialize a published result."""
        return serialize_runtime_result(result)

    def deserialize(self, payload: dict[str, object]) -> CanonicalRuntimeResult:
        """Deserialize a published result."""
        return deserialize_runtime_result(payload)

    def validate_contexts(self, context: CanonicalAnalysisContext) -> ValidationResult:
        """Validate Pack 07 context. Fail closed on critical corruption."""
        result = validate_pack07_context(context)
        assert_valid(result)
        return result

    def validate_runtime(self, result: CanonicalRuntimeResult) -> ValidationResult:
        """Validate CanonicalRuntimeResult. Fail closed on critical corruption."""
        outcome = validate_canonical_runtime(result)
        assert_valid(outcome)
        return outcome

    def diagnostics(self, context: CanonicalAnalysisContext) -> Pack07RuntimeDiagnostics:
        """Development-only runtime diagnostics."""
        return build_pack07_diagnostics(context)
