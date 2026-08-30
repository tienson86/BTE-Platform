"""Canonical JSON export. Must equal Presentation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping

from engines.narrative_v2.export.export_context import ExportBlock, ExportContext
from engines.narrative_v2.export.export_errors import ExportValidationError


@dataclass(frozen=True, slots=True)
class JsonExport:
    """JSON serialization of Presentation. No wrapper narrative."""

    version: str
    status: str
    payload: Mapping[str, Any]
    blocks: tuple[ExportBlock, ...]
    text: str


def export_json(context: ExportContext) -> JsonExport:
    """Dump Presentation JSON. Content must equal serialize_customer."""
    text = json.dumps(context.presentation, ensure_ascii=False, indent=2)
    canonical = json.loads(json.dumps(context.presentation, ensure_ascii=False))
    parsed = json.loads(text)
    if parsed != canonical:
        raise ExportValidationError("json_not_equal_presentation")
    return JsonExport(
        version=context.version,
        status=context.status,
        payload=context.presentation,
        blocks=context.blocks,
        text=text,
    )
