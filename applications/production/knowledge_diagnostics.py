"""Knowledge catalog status for production diagnostics."""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine_v2.strength.runtime.service import (
    StrengthInterpretationService,
)

PILOT_CATALOG_NOTE = (
    "PACK-01 catalog units remain Draft. Pilot runtime permits Draft catalog "
    "for pilot cases only — not Frozen production knowledge."
)


def build_knowledge_diagnostics(
    strength_service: StrengthInterpretationService,
) -> dict[str, Any]:
    """Expose catalog status/version in diagnostics — never in Customer Mode."""
    units = strength_service.units
    statuses = sorted({unit.status for unit in units})
    versions = sorted({unit.version for unit in units})
    return {
        "catalog_pack": "PACK_01_STRENGTH",
        "catalog_statuses": statuses,
        "catalog_is_draft": "Draft" in statuses,
        "catalog_versions": versions,
        "unit_count": len(units),
        "pilot_note": PILOT_CATALOG_NOTE,
    }
