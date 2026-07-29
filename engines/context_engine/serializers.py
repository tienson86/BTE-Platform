"""Serializers for UnifiedAnalysisContext V2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import CONTEXT_CONTRACT, SCHEMA_VERSION, UnifiedAnalysisContext

ANALYSIS_CONTEXT_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://bte-platform.local/schemas/analysis_context.v2.json",
    "title": "UnifiedAnalysisContext",
    "type": "object",
    "required": ["calendar", "bazi", "strength", "temperature", "pattern", "useful_god", "metadata"],
    "properties": {
        "calendar": {"type": "object"},
        "bazi": {"type": "object"},
        "strength": {
            "type": "object",
            "required": ["level", "score"],
            "properties": {
                "level": {"type": "string"},
                "score": {"type": "number"},
            },
        },
        "temperature": {
            "type": "object",
            "required": ["level", "type", "score"],
            "properties": {
                "level": {"type": "string"},
                "type": {"type": "string"},
                "score": {"type": "number"},
            },
        },
        "pattern": {
            "type": "object",
            "required": ["main"],
            "properties": {
                "main": {"type": "string"},
                "follow": {"type": ["string", "null"]},
            },
        },
        "useful_god": {
            "type": "object",
            "required": ["primary"],
            "properties": {
                "primary": {"type": "string"},
                "favorable": {"type": "array"},
                "unfavorable": {"type": "array"},
            },
        },
        "metadata": {
            "type": "object",
            "required": ["schema_version", "contract"],
            "properties": {
                "schema_version": {"const": SCHEMA_VERSION},
                "contract": {"const": CONTEXT_CONTRACT},
                "trace": {"type": "array"},
            },
        },
    },
}


def serialize_context(context: UnifiedAnalysisContext) -> dict[str, Any]:
    """Serialize unified context to JSON-compatible dict with schema header."""
    payload = context.to_dict()
    payload["_schema"] = ANALYSIS_CONTEXT_SCHEMA["$id"]
    payload["_version"] = SCHEMA_VERSION
    return payload


def write_analysis_context_json(
    context: UnifiedAnalysisContext,
    path: str | Path,
) -> Path:
    """Write analysis_context.json to disk."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = serialize_context(context)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return target


def load_analysis_context_json(path: str | Path) -> dict[str, Any]:
    """Load analysis_context.json from disk."""
    return json.loads(Path(path).read_text(encoding="utf-8"))
