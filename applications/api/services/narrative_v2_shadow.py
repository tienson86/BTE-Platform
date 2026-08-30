"""Narrative V2 shadow envelope for Portal diagnostic access.

Runs after Canonical Analysis + Pack05 production narrative.
Never replaces Pack05. Never raises into Analyze.
"""

from __future__ import annotations

import logging
from typing import Any, Mapping

from engines.narrative_v2.presentation import PRESENTATION_VERSION, serialize_customer
from engines.narrative_v2.runtime import NarrativeRuntime

logger = logging.getLogger(__name__)

PORTAL_CONNECTION_SHADOW = "true_shadow"
SHADOW_ERROR_CODE = "shadow_runtime_failed"
INCOMPATIBLE_VERSION = "incompatible_presentation_version"


def attach_narrative_v2_shadow(canonical_analysis: Mapping[str, Any] | None) -> dict[str, Any]:
    """Build a customer-safe shadow envelope. Isolate all V2 failures."""
    try:
        runtime = NarrativeRuntime()
        result = runtime.run(dict(canonical_analysis or {}))
        presentation = result.presentation
        if presentation is None:
            return _error_envelope("presentation_unavailable")
        payload = serialize_customer(presentation)
        version = _presentation_version(payload)
        if version != PRESENTATION_VERSION:
            return _error_envelope(INCOMPATIBLE_VERSION)
        return {
            "status": "ok",
            "portal_connection": PORTAL_CONNECTION_SHADOW,
            "replaces_pack05": False,
            "presentation": payload,
            "error": None,
        }
    except Exception:
        logger.exception("narrative_v2.shadow_failed")
        return _error_envelope(SHADOW_ERROR_CODE)


def _presentation_version(payload: Mapping[str, Any]) -> str | None:
    metadata = payload.get("metadata")
    if not isinstance(metadata, Mapping):
        return None
    version = metadata.get("version")
    return version if isinstance(version, str) else None


def _error_envelope(code: str) -> dict[str, Any]:
    return {
        "status": "error",
        "portal_connection": PORTAL_CONNECTION_SHADOW,
        "replaces_pack05": False,
        "presentation": None,
        "error": code,
    }
