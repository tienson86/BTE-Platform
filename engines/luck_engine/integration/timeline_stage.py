"""Luck Pipeline wrapper for LE-1 Timeline construction."""

from __future__ import annotations

from typing import Any, Mapping

from engines.luck_engine.exceptions import (
    LuckContractViolationError,
    LuckMissingInputError,
    TimelineValidationError,
)
from engines.luck_engine.pipeline.diagnostics import DIAG_TIMELINE_MISSING
from engines.luck_engine.pipeline.pipeline_executor import LuckPipelineContext
from engines.luck_engine.timeline.builder import construct_timeline


class TimelineStage:
    """Integrate released Luck Timeline Foundation into the canonical pipeline."""

    def execute(self, context: LuckPipelineContext) -> Mapping[str, Any]:
        """Construct or admit a timeline snapshot. Does not score fortune."""
        raw = context.timeline_input
        if raw is None:
            raise LuckMissingInputError(DIAG_TIMELINE_MISSING, "Missing timeline input")
        try:
            timeline_dict = self._to_timeline_dict(raw)
        except TimelineValidationError as exc:
            raise LuckContractViolationError(str(exc)) from exc
        except TypeError as exc:
            raise LuckContractViolationError(f"invalid_timeline_input:{exc}") from exc
        return {"timeline_result": timeline_dict}

    def _to_timeline_dict(self, raw: Any) -> dict[str, Any]:
        if hasattr(raw, "to_dict"):
            payload = dict(raw.to_dict())
            return payload
        if not isinstance(raw, Mapping):
            raise TypeError("timeline_must_be_mapping")
        if "timeline_version" in raw and "natal_chart" in raw and "timeline_id" not in raw:
            return dict(raw)
        return construct_timeline(**dict(raw)).to_dict()
