"""Output Optimization Layer models (WP7E)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ContentOutput:
    """
    WP7E output from ConsistentParagraphContext.

    html_ready:
        Normalized HTML document string.
    markdown_ready:
        Normalized Markdown document string.
    pdf_ready:
        PDF-oriented payload (title + lines), ready for a PDF writer.
    api_ready:
        JSON-serializable API envelope.
    """

    html_ready: str = ""
    markdown_ready: str = ""
    pdf_ready: dict[str, Any] = field(default_factory=dict)
    api_ready: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize ContentOutput."""
        return {
            "html_ready": self.html_ready,
            "markdown_ready": self.markdown_ready,
            "pdf_ready": dict(self.pdf_ready),
            "api_ready": dict(self.api_ready),
            "metadata": dict(self.metadata),
        }
