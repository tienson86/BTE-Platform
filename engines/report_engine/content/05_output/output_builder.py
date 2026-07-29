"""Output builder — ConsistentParagraphContext → ContentOutput."""

from __future__ import annotations

import importlib
from typing import Any, Mapping

from .api_serializer import ApiSerializer
from .html_optimizer import HtmlOptimizer
from .markdown_optimizer import MarkdownOptimizer
from .output_models import ContentOutput
from .pdf_optimizer import PdfOptimizer

_consistency = importlib.import_module(
    "engines.report_engine.content.04_consistency.consistency_models"
)
ConsistentParagraphContext = _consistency.ConsistentParagraphContext


class OutputBuilder:
    """
    Independent Output Optimization Layer entry point.

    Normalizes existing consistent paragraphs for HTML / Markdown / PDF / API.
    Does not invent or rewrite narrative content.
    """

    def __init__(self) -> None:
        self.html = HtmlOptimizer()
        self.markdown = MarkdownOptimizer()
        self.pdf = PdfOptimizer()
        self.api = ApiSerializer()

    def build(
        self,
        consistent: ConsistentParagraphContext | Mapping[str, Any],
        *,
        title: str = "BTE Content",
    ) -> ContentOutput:
        """Produce ContentOutput from a consistency context."""
        ctx = self._as_consistent(consistent)
        html_ready = self.html.optimize(ctx, title=title)
        markdown_ready = self.markdown.optimize(ctx, title=title)
        pdf_ready = self.pdf.optimize(ctx, title=title)
        api_ready = self.api.serialize(
            ctx,
            title=title,
            html=html_ready,
            markdown=markdown_ready,
            pdf_ready=pdf_ready,
        )
        return ContentOutput(
            html_ready=html_ready,
            markdown_ready=markdown_ready,
            pdf_ready=pdf_ready,
            api_ready=api_ready,
            metadata={
                "paragraph_count": len(getattr(ctx, "checked_paragraphs", []) or []),
                "title": title,
            },
        )

    def _as_consistent(
        self,
        value: ConsistentParagraphContext | Mapping[str, Any],
    ) -> ConsistentParagraphContext:
        if isinstance(value, ConsistentParagraphContext):
            return value
        return ConsistentParagraphContext(
            checked_paragraphs=list(value.get("checked_paragraphs") or []),
            removed_duplicates=list(value.get("removed_duplicates") or []),
            contradiction_report=list(value.get("contradiction_report") or []),
            coherence_report=list(value.get("coherence_report") or []),
            warnings=list(value.get("warnings") or []),
            tone=str(value.get("tone") or "neutral"),
            emphasis_levels=dict(value.get("emphasis_levels") or {}),
            metadata=dict(value.get("metadata") or {}),
        )
