"""Select a renderer and return an in-memory RenderArtifact. No persistence."""

from __future__ import annotations

from typing import Mapping, Protocol

from engines.report_engine.rendering.docx_renderer import DocxRenderer
from engines.report_engine.rendering.html_renderer import HtmlRenderer
from engines.report_engine.rendering.json_renderer import JsonRenderer
from engines.report_engine.rendering.markdown_renderer import MarkdownRenderer
from engines.report_engine.rendering.pdf_renderer import PdfRenderer
from engines.report_engine.rendering.render_model import RenderArtifact, RenderModel
from engines.report_engine.rendering.renderer_registry import (
    RENDERER_DOCX,
    RENDERER_HTML,
    RENDERER_JSON,
    RENDERER_MARKDOWN,
    RENDERER_PDF,
    RendererRegistry,
)
from engines.report_engine.rendering.rendering_context import RenderingError


class RendererProtocol(Protocol):
    """In-memory renderer plugin."""

    renderer_id: str
    mime_type: str

    def render(self, model: RenderModel) -> RenderArtifact:
        """Produce a memory artifact."""


def default_renderers() -> dict[str, RendererProtocol]:
    """Return the enabled built-in renderer plugins."""
    return {
        RENDERER_PDF: PdfRenderer(),
        RENDERER_DOCX: DocxRenderer(),
        RENDERER_HTML: HtmlRenderer(),
        RENDERER_MARKDOWN: MarkdownRenderer(),
        RENDERER_JSON: JsonRenderer(),
    }


class ExportManager:
    """Dispatch Canonical render models to an enabled renderer."""

    def __init__(
        self,
        *,
        registry: RendererRegistry | None = None,
        renderers: Mapping[str, RendererProtocol] | None = None,
    ) -> None:
        """Bind registry and renderer plugins."""
        self._registry = registry or RendererRegistry.default()
        self._renderers = dict(renderers or default_renderers())

    def export(self, *, renderer_id: str, model: RenderModel) -> RenderArtifact:
        """Select a renderer and return an in-memory artifact. No storage."""
        record = self._registry.require_enabled(renderer_id)
        renderer = self._renderers.get(renderer_id)
        if renderer is None:
            raise RenderingError(f"renderer_plugin_missing:{renderer_id}")
        artifact = renderer.render(model)
        if artifact.mime_type != record.mime_type:
            raise RenderingError(f"mime_mismatch:{artifact.mime_type}:{record.mime_type}")
        return artifact
