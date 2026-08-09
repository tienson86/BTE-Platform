"""Deterministic RE-3 renderer registry."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from engines.report_engine.rendering.rendering_context import RENDER_VERSION, RenderingError

RENDERER_PDF = "pdf"
RENDERER_DOCX = "docx"
RENDERER_HTML = "html"
RENDERER_MARKDOWN = "markdown"
RENDERER_JSON = "json"
RENDERER_XLSX = "xlsx"
RENDERER_PPTX = "pptx"

MIME_PDF = "application/pdf"
MIME_DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
MIME_HTML = "text/html"
MIME_MARKDOWN = "text/markdown"
MIME_JSON = "application/json"

ACTIVE_RENDERERS: tuple[str, ...] = (
    RENDERER_PDF,
    RENDERER_DOCX,
    RENDERER_HTML,
    RENDERER_MARKDOWN,
    RENDERER_JSON,
)

FUTURE_RENDERERS: tuple[str, ...] = (
    RENDERER_XLSX,
    RENDERER_PPTX,
)


@dataclass(frozen=True, slots=True)
class RendererRecord:
    """Immutable catalog entry for one renderer plugin."""

    renderer_id: str
    component: str
    version: str
    mime_type: str
    enabled: bool
    deterministic: bool

    def to_dict(self) -> dict[str, object]:
        """Serialize the renderer catalog record."""
        return {
            "renderer_id": self.renderer_id,
            "component": self.component,
            "version": self.version,
            "mime_type": self.mime_type,
            "enabled": self.enabled,
            "deterministic": self.deterministic,
        }


def _record(renderer_id: str, mime_type: str, *, enabled: bool) -> RendererRecord:
    return RendererRecord(
        renderer_id=renderer_id,
        component=f"{renderer_id}_renderer",
        version=RENDER_VERSION,
        mime_type=mime_type,
        enabled=enabled,
        deterministic=True,
    )


def _default_records() -> tuple[RendererRecord, ...]:
    return (
        _record(RENDERER_PDF, MIME_PDF, enabled=True),
        _record(RENDERER_DOCX, MIME_DOCX, enabled=True),
        _record(RENDERER_HTML, MIME_HTML, enabled=True),
        _record(RENDERER_MARKDOWN, MIME_MARKDOWN, enabled=True),
        _record(RENDERER_JSON, MIME_JSON, enabled=True),
        _record(RENDERER_XLSX, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", enabled=False),
        _record(RENDERER_PPTX, "application/vnd.openxmlformats-officedocument.presentationml.presentation", enabled=False),
    )


class RendererRegistry:
    """Read-only catalog of RE-3 renderers."""

    def __init__(self, records: Iterable[RendererRecord] | None = None) -> None:
        """Load default or injected renderer records."""
        catalog = tuple(records) if records is not None else _default_records()
        ids = [item.renderer_id for item in catalog]
        if len(ids) != len(set(ids)):
            raise RenderingError("duplicate_renderer_id")
        self._records = catalog
        self._by_id = {item.renderer_id: item for item in catalog}

    @classmethod
    def default(cls) -> RendererRegistry:
        """Return the frozen default renderer catalog."""
        return cls()

    def get(self, renderer_id: str) -> RendererRecord:
        """Return one renderer record or raise."""
        try:
            return self._by_id[renderer_id]
        except KeyError as exc:
            raise RenderingError(f"unknown_renderer:{renderer_id}") from exc

    def enabled_ids(self) -> tuple[str, ...]:
        """Return enabled renderer identifiers."""
        return tuple(item.renderer_id for item in self._records if item.enabled)

    def disabled_ids(self) -> tuple[str, ...]:
        """Return registered but inactive future renderer identifiers."""
        return tuple(item.renderer_id for item in self._records if not item.enabled)

    def require_enabled(self, renderer_id: str) -> RendererRecord:
        """Return an enabled renderer or raise."""
        record = self.get(renderer_id)
        if not record.enabled:
            raise RenderingError(f"renderer_disabled:{renderer_id}")
        return record

    def to_list(self) -> list[dict[str, object]]:
        """Serialize the full renderer registry."""
        return [item.to_dict() for item in self._records]
