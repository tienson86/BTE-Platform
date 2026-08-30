"""Pack05 Legacy Narrative Archive. Read-only. Not a production provider."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping

from engines.narrative_v2.presentation import PRESENTATION_VERSION

PACK05_CONTRACT = "pack05_narrative_result_v1"
PRODUCTION_PROVIDER = "v2"
EXPORT_SOURCE_V2 = "v2"
EXPORT_SOURCE_ARCHIVE = "archive_pack05"

_TRUTHY_LEGACY = frozenset({"1", "true", "pack05", "yes"})


@dataclass(frozen=True, slots=True)
class Pack05Archive:
    """Stored Pack05 narrative. Read-only. Never a production selection."""

    available: bool
    read_only: bool
    contract: str | None
    payload: Mapping[str, Any] | None


def resolve_production_provider(requested: str | None = None) -> str:
    """Ignore pack05/auto flags. Production is Narrative V2 only."""
    del requested
    return PRODUCTION_PROVIDER


def pack05_legacy_enabled(environ: Mapping[str, str] | None = None) -> bool:
    """True when Pack05 may be read as a historical archive."""
    bag = os.environ if environ is None else environ
    raw = str(bag.get("PACK05_LEGACY") or "").strip().lower()
    return raw in _TRUTHY_LEGACY


def load_pack05_archive(data: Mapping[str, Any] | None) -> Pack05Archive:
    """Return stored Pack05 without mutation or overwrite."""
    if not isinstance(data, Mapping):
        return Pack05Archive(available=False, read_only=True, contract=None, payload=None)
    raw = data.get("narrative_result")
    if not isinstance(raw, Mapping):
        return Pack05Archive(available=False, read_only=True, contract=None, payload=None)
    contract = raw.get("contract")
    contract_text = contract if isinstance(contract, str) else None
    return Pack05Archive(
        available=True,
        read_only=True,
        contract=contract_text,
        payload=raw,
    )


def presentation_payload(data: Mapping[str, Any] | None) -> Mapping[str, Any] | None:
    """Return a valid Narrative V2 Presentation mapping, or None."""
    if not isinstance(data, Mapping):
        return None
    shadow = data.get("narrative_v2_shadow")
    if not isinstance(shadow, Mapping):
        return None
    if str(shadow.get("status") or "") != "ok":
        return None
    presentation = shadow.get("presentation")
    if not isinstance(presentation, Mapping):
        return None
    metadata = presentation.get("metadata")
    version = metadata.get("version") if isinstance(metadata, Mapping) else None
    if version != PRESENTATION_VERSION:
        return None
    return presentation


def select_export_source(
    data: Mapping[str, Any] | None,
    *,
    legacy: bool | None = None,
) -> str:
    """Production exports Narrative V2. PACK05_LEGACY reads the archive."""
    archive = pack05_legacy_enabled() if legacy is None else legacy
    if archive:
        return EXPORT_SOURCE_ARCHIVE
    if presentation_payload(data) is not None:
        return EXPORT_SOURCE_V2
    return EXPORT_SOURCE_ARCHIVE
