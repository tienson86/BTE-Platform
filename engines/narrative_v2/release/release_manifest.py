"""Narrative V2 V1.0 Release Manifest. Freeze record only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.narrative_v2.certification.certification_result import CERTIFICATION_VERSION
from engines.narrative_v2.golden.golden_case import GOLDEN_SCHEMA_VERSION
from engines.narrative_v2.language.language_asset_status import SENTENCE_LIBRARY_VERSION
from engines.narrative_v2.presentation.presentation_status import (
    NARRATIVE_VERSION,
    PRESENTATION_VERSION,
)
from engines.narrative_v2.release.pack05_archive import PRODUCTION_PROVIDER
from engines.narrative_v2.release.release_events import utc_now
from engines.narrative_v2.runtime.narrative_runtime import RUNTIME_VERSION

RELEASE_VERSION = "1.0"
FREEZE_STATUS_FROZEN = "FROZEN"
PACK05_STATUS_ARCHIVED = "archived"
NARRATIVE_PRODUCTION_ON = "ON"
NARRATIVE_PRODUCTION_OFF = "OFF"
NEXT_VERSION = "1.1"

FROZEN_SURFACES: tuple[str, ...] = (
    "runtime",
    "presentation_contract",
    "commercial_communication",
    "language_assets",
    "export_layer",
    "narrative_studio",
    "certification",
    "golden_dataset",
    "release_configuration",
)


@dataclass(frozen=True, slots=True)
class ReleaseManifest:
    """Official production baseline. Immutable after Freeze."""

    release_version: str
    narrative_version: str
    presentation_version: str
    language_asset_version: str
    golden_version: str
    certification_version: str
    runtime_version: str
    release_date: str
    pack05_status: str
    freeze_status: str
    metadata: Mapping[str, Any]

    def to_record(self) -> dict[str, Any]:
        """JSON-safe freeze record."""
        return {
            "release_version": self.release_version,
            "narrative_version": self.narrative_version,
            "presentation_version": self.presentation_version,
            "language_asset_version": self.language_asset_version,
            "golden_version": self.golden_version,
            "certification_version": self.certification_version,
            "runtime_version": self.runtime_version,
            "release_date": self.release_date,
            "pack05_status": self.pack05_status,
            "freeze_status": self.freeze_status,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_record(cls, row: Mapping[str, Any]) -> "ReleaseManifest":
        """Hydrate a freeze record. Does not invent versions."""
        metadata = row.get("metadata")
        return cls(
            release_version=str(row.get("release_version") or ""),
            narrative_version=str(row.get("narrative_version") or ""),
            presentation_version=str(row.get("presentation_version") or ""),
            language_asset_version=str(row.get("language_asset_version") or ""),
            golden_version=str(row.get("golden_version") or ""),
            certification_version=str(row.get("certification_version") or ""),
            runtime_version=str(row.get("runtime_version") or ""),
            release_date=str(row.get("release_date") or ""),
            pack05_status=str(row.get("pack05_status") or ""),
            freeze_status=str(row.get("freeze_status") or ""),
            metadata=dict(metadata) if isinstance(metadata, Mapping) else {},
        )


def build_v1_manifest(*, release_date: str | None = None) -> ReleaseManifest:
    """Record the V1.0 production baseline from current frozen constants."""
    return ReleaseManifest(
        release_version=RELEASE_VERSION,
        narrative_version=NARRATIVE_VERSION,
        presentation_version=PRESENTATION_VERSION,
        language_asset_version=SENTENCE_LIBRARY_VERSION,
        golden_version=GOLDEN_SCHEMA_VERSION,
        certification_version=CERTIFICATION_VERSION,
        runtime_version=RUNTIME_VERSION,
        release_date=release_date or utc_now(),
        pack05_status=PACK05_STATUS_ARCHIVED,
        freeze_status=FREEZE_STATUS_FROZEN,
        metadata={
            "official_name": "Narrative V2 V1.0",
            "narrative_v2_production": NARRATIVE_PRODUCTION_ON,
            "pack05_production": NARRATIVE_PRODUCTION_OFF,
            "pack05_access": "read_only",
            "production_provider": PRODUCTION_PROVIDER,
            "next_version_required": NEXT_VERSION,
            "frozen_surfaces": list(FROZEN_SURFACES),
            "specifications": "knowledge/narrative_v2/",
            "implementation_archive": "implementation/narrative_v2/",
            "release_archive": "implementation/narrative_release/",
            "studio": "historical_compare_only",
            "export": "presentation_export_layer",
            "golden_baseline": {"case_id": "CASE-0001", "version": 1, "status": "FROZEN"},
            "certification_baseline": {
                "case_id": "CASE-0001",
                "status": "CERTIFIED",
                "history": "append_only",
            },
            "runtime": "runtime",
            "presentation": "presentation_contract",
            "language_assets": "language_assets",
            "certification": "certification",
            "golden": "golden_dataset",
            "pack05": "archived",
            "release": "release_configuration",
        },
    )
