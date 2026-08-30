"""Narrative content hashes for export parity. Hash content, not file bytes."""

from __future__ import annotations

from typing import Any, Mapping

from engines.narrative_v2.export.export_builder import build_export_context
from engines.narrative_v2.export.export_errors import IncompatiblePresentationVersion
from engines.narrative_v2.export.export_serializer import presentation_from_mapping
from engines.narrative_v2.export.json_export import export_json
from engines.narrative_v2.export.pdf_export import extract_html_texts, render_export_html
from engines.narrative_v2.export.portal_export import export_portal
from engines.narrative_v2.golden.golden_serializer import stable_hash
from engines.narrative_v2.presentation.presentation_model import NarrativeV2Presentation
from engines.narrative_v2.release.release_health import HEALTH_FAIL, HEALTH_PASS, HEALTH_UNKNOWN

CONSUMERS: tuple[str, ...] = ("portal", "pdf", "docx", "json")


def content_hash(texts: tuple[str, ...] | list[str]) -> str:
    """SHA-256 of ordered Narrative strings."""
    return stable_hash(list(texts))


def parity_hashes(
    presentation: NarrativeV2Presentation | Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Compare Portal / PDF / DOCX / JSON Narrative content hashes."""
    if presentation is None:
        empty = {name: "" for name in CONSUMERS}
        return {
            **empty,
            "matched": False,
            "status": HEALTH_UNKNOWN,
            "reason": "presentation_unavailable",
        }
    try:
        model = (
            presentation
            if isinstance(presentation, NarrativeV2Presentation)
            else presentation_from_mapping(presentation)
        )
        context = build_export_context(model)
    except (IncompatiblePresentationVersion, TypeError, ValueError) as exc:
        empty = {name: "" for name in CONSUMERS}
        return {
            **empty,
            "matched": False,
            "status": HEALTH_FAIL,
            "reason": type(exc).__name__,
        }
    block_texts = tuple(block.text for block in context.blocks)
    portal = content_hash(tuple(block.text for block in export_portal(context).blocks))
    json_hash = content_hash(tuple(block.text for block in export_json(context).blocks))
    pdf = content_hash(extract_html_texts(render_export_html(context)))
    docx = content_hash(block_texts)
    hashes = {"portal": portal, "pdf": pdf, "docx": docx, "json": json_hash}
    matched = len(set(hashes.values())) == 1
    return {
        **hashes,
        "matched": matched,
        "status": HEALTH_PASS if matched else HEALTH_FAIL,
        "reason": "" if matched else "content_hash_mismatch",
    }
