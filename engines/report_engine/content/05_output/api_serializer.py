"""Serialize ConsistentParagraphContext into API-ready JSON structure."""

from __future__ import annotations

from typing import Any, Mapping

from ._helpers import iter_paragraphs, paragraph_id, paragraph_section, paragraph_text


class ApiSerializer:
    """
    Build a stable API envelope without inventing narrative content.
    """

    def serialize(
        self,
        context: Any,
        *,
        title: str = "",
        html: str = "",
        markdown: str = "",
        pdf_ready: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Return JSON-serializable API payload."""
        paragraphs: list[dict[str, Any]] = []
        for paragraph in iter_paragraphs(context):
            text = paragraph_text(paragraph)
            if not text:
                continue
            item: dict[str, Any] = {
                "paragraph_id": paragraph_id(paragraph),
                "section": paragraph_section(paragraph),
                "text": text,
                "polarity": str(getattr(paragraph, "polarity", "") or ""),
                "score": float(getattr(paragraph, "score", 0) or 0),
                "emphasis": str(getattr(paragraph, "emphasis", "") or ""),
            }
            if hasattr(paragraph, "to_dict"):
                # Include original structured fields without altering text
                raw = paragraph.to_dict()
                item["sentences"] = raw.get("sentences") or []
            paragraphs.append(item)

        if isinstance(context, Mapping):
            tone = str(context.get("tone") or "neutral")
            warnings = list(context.get("warnings") or [])
            metadata = dict(context.get("metadata") or {})
            emphasis = dict(context.get("emphasis_levels") or {})
            removed = list(context.get("removed_duplicates") or [])
            contradictions = list(context.get("contradiction_report") or [])
            coherence = list(context.get("coherence_report") or [])
        else:
            tone = str(getattr(context, "tone", "neutral") or "neutral")
            warnings = list(getattr(context, "warnings", None) or [])
            metadata = dict(getattr(context, "metadata", None) or {})
            emphasis = dict(getattr(context, "emphasis_levels", None) or {})
            removed = list(getattr(context, "removed_duplicates", None) or [])
            contradictions = list(getattr(context, "contradiction_report", None) or [])
            coherence = list(getattr(context, "coherence_report", None) or [])

        return {
            "title": title,
            "tone": tone,
            "paragraphs": paragraphs,
            "emphasis_levels": emphasis,
            "warnings": warnings,
            "removed_duplicates": removed,
            "contradiction_report": contradictions,
            "coherence_report": coherence,
            "formats": {
                "html": html,
                "markdown": markdown,
                "pdf": dict(pdf_ready or {}),
            },
            "metadata": metadata,
        }
