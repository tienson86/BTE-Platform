"""RE-2 document builder tests."""

from __future__ import annotations

from engines.report_engine.layout.document_builder import DOCUMENT_ID, DocumentBuilder
from engines.report_engine.layout.layout_context import build_layout_context
from tests.report_engine.re2_support import assemble_layout_inputs


def test_document_builder_emits_pages_header_footer_title() -> None:
    """Document carries logical pages and identities without render fields."""
    payload = assemble_layout_inputs()
    context = build_layout_context(
        report_context=payload["report_context"],
        interpretation_result=payload["interpretation_result"],
    )
    document = DocumentBuilder().build(context)
    assert document.document_id == DOCUMENT_ID
    assert document.title.title_id == "TTL-primary"
    assert document.header.header_id == "HDR-primary"
    assert document.footer.footer_id == "FTR-primary"
    assert [page.page_id for page in document.pages][0] == "PAGE-cover"
    assert document.pages[-1].page_id == "PAGE-summary"
    encoded = document.to_dict()
    assert encoded["metadata"]["rendering"] is False
    assert "html" not in encoded
    assert "pdf" not in encoded
