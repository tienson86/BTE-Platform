"""Narrative V2 envelope for Portal. Dual-stored with Pack05. Isolated failures."""

from __future__ import annotations

import logging
import time
from typing import Any, Mapping

from engines.narrative_v2.presentation import PRESENTATION_VERSION, serialize_customer
from engines.narrative_v2.runtime import NarrativeRuntime

logger = logging.getLogger(__name__)

PORTAL_CONNECTION_SHADOW = "true_shadow"
SHADOW_ERROR_CODE = "shadow_runtime_failed"
INCOMPATIBLE_VERSION = "incompatible_presentation_version"


def attach_narrative_v2_shadow(canonical_analysis: Mapping[str, Any] | None) -> dict[str, Any]:
    """Build a customer-safe V2 envelope. Isolate all V2 failures from Analyze."""
    started = time.perf_counter()
    try:
        runtime = NarrativeRuntime()
        result = runtime.run(dict(canonical_analysis or {}))
        presentation = result.presentation
        duration_ms = _elapsed_ms(started)
        if presentation is None:
            _log_runtime("error", None, duration_ms)
            return _error_envelope("presentation_unavailable", duration_ms)
        payload = serialize_customer(presentation)
        version = _presentation_version(payload)
        if version != PRESENTATION_VERSION:
            _log_runtime("error", version, duration_ms)
            return _error_envelope(INCOMPATIBLE_VERSION, duration_ms)
        _log_runtime("ok", version, duration_ms)
        return {
            "status": "ok",
            "portal_connection": PORTAL_CONNECTION_SHADOW,
            "replaces_pack05": False,
            "presentation": payload,
            "error": None,
            "runtime_ms": duration_ms,
            "presentation_version": version,
        }
    except Exception:
        duration_ms = _elapsed_ms(started)
        logger.exception("narrative_v2.runtime_failed")
        _log_runtime("error", None, duration_ms)
        return _error_envelope(SHADOW_ERROR_CODE, duration_ms)


def _elapsed_ms(started: float) -> int:
    return max(0, int((time.perf_counter() - started) * 1000))


def _configured_provider() -> str:
    return "v2"


def _log_runtime(status: str, version: str | None, duration_ms: int) -> None:
    logger.info(
        "narrative.release provider=%s status=%s presentation_version=%s duration_ms=%s",
        _configured_provider(),
        status,
        version or "",
        duration_ms,
    )


def _presentation_version(payload: Mapping[str, Any]) -> str | None:
    metadata = payload.get("metadata")
    if not isinstance(metadata, Mapping):
        return None
    version = metadata.get("version")
    return version if isinstance(version, str) else None


def _error_envelope(code: str, duration_ms: int = 0) -> dict[str, Any]:
    return {
        "status": "error",
        "portal_connection": PORTAL_CONNECTION_SHADOW,
        "replaces_pack05": False,
        "presentation": None,
        "error": code,
        "runtime_ms": duration_ms,
        "presentation_version": None,
    }
