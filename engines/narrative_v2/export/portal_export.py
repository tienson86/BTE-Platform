"""Portal shadow export. Does not change production Portal rendering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.narrative_v2.export.export_context import ExportBlock, ExportContext


@dataclass(frozen=True, slots=True)
class PortalExport:
    """Shadow Portal payload. Presentation copy only."""

    version: str
    status: str
    language: str
    shadow_mode: bool
    replaces_pack05: bool
    presentation: Mapping[str, Any]
    blocks: tuple[ExportBlock, ...]


def export_portal(context: ExportContext) -> PortalExport:
    """Copy Presentation for Portal shadow. No rewrite."""
    return PortalExport(
        version=context.version,
        status=context.status,
        language=context.language,
        shadow_mode=True,
        replaces_pack05=False,
        presentation=context.presentation,
        blocks=context.blocks,
    )
