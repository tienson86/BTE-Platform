"""Validate export outputs. No composition. No private traces."""

from __future__ import annotations

import json
from typing import Any, Mapping

from engines.narrative_v2.presentation.presentation_status import PRESENTATION_VERSION
from engines.narrative_v2.presentation.presentation_validator import FORBIDDEN_KEYS, FORBIDDEN_SUBSTRINGS

from engines.narrative_v2.export.export_context import ExportContext
from engines.narrative_v2.export.export_errors import ExportValidationError

PRIVATE_TOKENS: tuple[str, ...] = (
    "pipeline_trace",
    "runtime_metrics",
    "source_unit_ids",
    "knowledge.pattern.",
    "evidence.strength",
    "NR-REL-",
    "decision_id",
    "rewrite.pattern.",
)


class ExportValidator:
    """Confirm consumers received Presentation copy only."""

    def validate_context(self, context: ExportContext) -> None:
        """Reject incompatible version and leaked internals."""
        if context.version != PRESENTATION_VERSION:
            raise ExportValidationError("incompatible_presentation_version")
        if context.replaces_pack05:
            raise ExportValidationError("shadow_export_must_not_replace_pack05")
        if not context.shadow_mode:
            raise ExportValidationError("export_must_remain_shadow")
        self._assert_public(context.presentation)
        for block in context.blocks:
            self._assert_text(block.text)

    def assert_same_narrative(
        self,
        left: tuple[str, ...],
        right: tuple[str, ...],
        *,
        label: str,
    ) -> None:
        """Parity: same customer strings, same order."""
        if left != right:
            raise ExportValidationError(f"parity_mismatch:{label}")

    def _assert_public(self, payload: Mapping[str, Any]) -> None:
        raw = json.dumps(payload, ensure_ascii=False)
        for token in FORBIDDEN_SUBSTRINGS + PRIVATE_TOKENS:
            if token in raw:
                raise ExportValidationError(f"private_token:{token}")
        self._walk_keys(payload)

    def _walk_keys(self, value: object) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if key in FORBIDDEN_KEYS:
                    raise ExportValidationError(f"private_key:{key}")
                self._walk_keys(item)
        elif isinstance(value, list):
            for item in value:
                self._walk_keys(item)

    def _assert_text(self, text: str) -> None:
        for token in FORBIDDEN_SUBSTRINGS + PRIVATE_TOKENS:
            if token in text:
                raise ExportValidationError(f"private_token:{token}")
