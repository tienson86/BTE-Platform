"""Provenance mapping (read-only)."""

from __future__ import annotations

from typing import Any

from .ascii_utils import SCHEMA_VERSION
from .source_reader import RuntimeBundle


def map_provenance(
    bundle: RuntimeBundle,
    *,
    provenance_class: str = "engine_rule",
    availability: str = "observed",
    rule_id: str | None = None,
    source_path: str | None = None,
) -> dict[str, Any]:
    """Build StrengthProvenance from known source paths only."""
    return {
        "schema_version": SCHEMA_VERSION,
        "provenance_class": provenance_class,
        "availability": availability,
        "source_system": "strength_engine_v1_runtime_observation",
        "source_path": source_path or next(iter(bundle.source_paths.values()), None),
        "rule_id": rule_id,
        "observed_at": None,
        "notes": "REFERENCE_ONLY mapping; no new evidence invented",
    }


def map_root_provenance(bundle: RuntimeBundle) -> dict[str, Any]:
    """Top-level profile provenance."""
    cls = "synthetic" if bundle.population == "synthetic_stress" else "derived"
    return map_provenance(
        bundle,
        provenance_class=cls,
        availability="derived",
        source_path=";".join(bundle.source_paths.values()),
    )
