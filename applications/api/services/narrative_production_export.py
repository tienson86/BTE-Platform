"""Production Narrative export. Presentation only. Pack05 is archive."""

from __future__ import annotations

import json
import logging
import tempfile
import uuid
from pathlib import Path
from typing import Any, Literal, Mapping

from applications.api.exceptions import CustomerExportError
from applications.api.services.customer_contract import RENDERER_FAILURE_MESSAGE
from engines.narrative_v2.export import PresentationExportLayer, presentation_from_mapping
from engines.narrative_v2.release.pack05_archive import (
    EXPORT_SOURCE_V2,
    presentation_payload,
    select_export_source,
)

logger = logging.getLogger(__name__)

ProductionExportFormat = Literal["pdf", "docx", "json"]

_EXPORT_ROOT = Path(tempfile.gettempdir()) / "bte_narrative_v2_export"


def export_production_json(data: Mapping[str, Any] | None) -> dict[str, Any]:
    """Serialize NarrativeV2Presentation. Pack05 cannot be selected."""
    presentation = _require_v2(data)
    exported = PresentationExportLayer().export_json(presentation)
    return dict(exported.payload)


def export_production_file(
    data: Mapping[str, Any] | None,
    fmt: ProductionExportFormat,
    *,
    output_path: Path | None = None,
) -> Path:
    """Render a production Narrative file from Presentation. V2 only."""
    presentation = _require_v2(data)
    layer = PresentationExportLayer()
    if fmt == "json":
        payload = layer.export_json(presentation)
        path = output_path or _unique_path("json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload.payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return path
    path = output_path or _unique_path(fmt)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        if fmt == "pdf":
            layer.export_pdf(presentation, path)
        elif fmt == "docx":
            layer.export_docx(presentation, path)
        else:
            raise CustomerExportError(RENDERER_FAILURE_MESSAGE, code="export_unsupported_format")
    except CustomerExportError:
        raise
    except Exception:
        logger.exception("narrative_production_export_failed format=%s", fmt)
        raise CustomerExportError(
            RENDERER_FAILURE_MESSAGE,
            status_code=500,
            code="export_renderer_failed",
        ) from None
    if not path.is_file() or path.stat().st_size == 0:
        raise CustomerExportError(
            RENDERER_FAILURE_MESSAGE,
            status_code=500,
            code="export_empty_file",
        )
    return path


def _require_v2(data: Mapping[str, Any] | None) -> Any:
    source = select_export_source(data, legacy=False)
    payload = presentation_payload(data)
    if source != EXPORT_SOURCE_V2 or payload is None:
        raise CustomerExportError(
            RENDERER_FAILURE_MESSAGE,
            status_code=409,
            code="export_presentation_unavailable",
        )
    return presentation_from_mapping(payload)


def _unique_path(fmt: str) -> Path:
    _EXPORT_ROOT.mkdir(parents=True, exist_ok=True)
    token = uuid.uuid4().hex[:12]
    return _EXPORT_ROOT / f"bte_narrative_{token}.{fmt}"
