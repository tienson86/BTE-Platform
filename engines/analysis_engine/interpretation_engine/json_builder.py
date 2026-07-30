"""JSON Builder — render InterpretationResult as deterministic JSON text."""

from __future__ import annotations

import json
from typing import Any, Mapping

from engines.analysis_engine.interpretation_engine.models import InterpretationResult


def dumps_json(payload: Mapping[str, Any]) -> str:
    """Serialize JSON with stable key ordering."""
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
    ) + "\n"


class JsonBuilder:
    """Build deterministic JSON envelope from InterpretationResult."""

    def build(self, result: InterpretationResult) -> str:
        """Render JSON text for the interpretation."""
        payload = {
            "format": "interpretation_json",
            "schema_version": "1.0.0",
            "interpretation": result.to_dict(),
        }
        # Avoid embedding render artifacts inside nested interpretation to
        # prevent recursive duplication of markdown/html/json_text.
        interpretation = dict(payload["interpretation"])
        interpretation.pop("markdown", None)
        interpretation.pop("html", None)
        interpretation.pop("json_text", None)
        payload["interpretation"] = interpretation
        return dumps_json(payload)
