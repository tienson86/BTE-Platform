"""WP7E — Output Optimization Layer unit tests (runs independently)."""

from __future__ import annotations

import importlib

_style = importlib.import_module("engines.report_engine.content.03_style.style_models")
StyledParagraph = _style.StyledParagraph
StyledSentence = _style.StyledSentence

_consistency = importlib.import_module(
    "engines.report_engine.content.04_consistency.consistency_models"
)
ConsistentParagraphContext = _consistency.ConsistentParagraphContext

_output = importlib.import_module("engines.report_engine.content.05_output")
OutputBuilder = _output.OutputBuilder
ContentOutput = _output.ContentOutput
HtmlOptimizer = _output.HtmlOptimizer
MarkdownOptimizer = _output.MarkdownOptimizer
PdfOptimizer = _output.PdfOptimizer
ApiSerializer = _output.ApiSerializer


def _para(pid: str, section: str, text: str) -> StyledParagraph:
    return StyledParagraph(
        paragraph_id=pid,
        section=section,
        polarity="positive",
        text=text,
        original_text=text,
        emphasis="normal",
        score=80.0,
        sentences=[
            StyledSentence(
                original=text,
                rewritten=text,
                section=section,
                paragraph_id=pid,
                polarity="positive",
            )
        ],
    )


def _sample_consistent() -> ConsistentParagraphContext:
    return ConsistentParagraphContext(
        checked_paragraphs=[
            _para("P001", "career", "Su nghiep thuan loi."),
            _para("P002", "wealth", "Tai van on dinh <ok>."),
        ],
        removed_duplicates=["dup"],
        contradiction_report=[],
        coherence_report=[{"kind": "coherence", "detail": "note"}],
        warnings=["[coherence] note"],
        tone="neutral",
        emphasis_levels={"P001": "high", "P002": "normal"},
        metadata={"output_count": 2},
    )


def test_output_builder_returns_content_output():
    result = OutputBuilder().build(_sample_consistent(), title="Demo")
    assert isinstance(result, ContentOutput)
    assert result.html_ready
    assert result.markdown_ready
    assert result.pdf_ready
    assert result.api_ready


def test_content_output_to_dict_keys():
    payload = OutputBuilder().build(_sample_consistent()).to_dict()
    for key in ("html_ready", "markdown_ready", "pdf_ready", "api_ready"):
        assert key in payload


def test_html_escapes_but_keeps_text():
    html = HtmlOptimizer().optimize(_sample_consistent(), title="T")
    assert "<html>" in html
    assert "Su nghiep thuan loi." in html
    assert "&lt;ok&gt;" in html
    assert "<ok>" not in html


def test_markdown_keeps_original_sentences():
    md = MarkdownOptimizer().optimize(_sample_consistent(), title="T")
    assert "# T" in md
    assert "## career" in md
    assert "Su nghiep thuan loi." in md
    assert "Tai van on dinh <ok>." in md


def test_pdf_ready_has_lines_without_new_content():
    pdf = PdfOptimizer().optimize(_sample_consistent(), title="T")
    assert pdf["title"] == "T"
    assert "Su nghiep thuan loi." in pdf["lines"]
    assert "Tai van on dinh <ok>." in pdf["lines"]


def test_api_ready_structure():
    api = ApiSerializer().serialize(
        _sample_consistent(),
        title="T",
        html="<html></html>",
        markdown="# T",
        pdf_ready={"title": "T", "lines": []},
    )
    assert api["title"] == "T"
    assert len(api["paragraphs"]) == 2
    assert api["paragraphs"][0]["text"] == "Su nghiep thuan loi."
    assert "formats" in api


def test_does_not_invent_sentences():
    original = "Su nghiep thuan loi."
    result = OutputBuilder().build(_sample_consistent())
    assert original in result.html_ready
    assert original in result.markdown_ready
    assert original in result.pdf_ready["lines"]
    assert result.api_ready["paragraphs"][0]["text"] == original


def test_accepts_dict_input():
    payload = _sample_consistent().to_dict()
    result = OutputBuilder().build(payload, title="Dict")
    assert isinstance(result, ContentOutput)
    assert result.api_ready["title"] == "Dict"


def test_runs_independently_without_upstream_builders():
    """No ConsistencyBuilder / StyleBuilder / Report Engine required."""
    ctx = ConsistentParagraphContext(
        checked_paragraphs=[_para("X", "summary", "Hello world.")]
    )
    html = HtmlOptimizer().optimize(ctx, title="Solo")
    md = MarkdownOptimizer().optimize(ctx, title="Solo")
    pdf = PdfOptimizer().optimize(ctx, title="Solo")
    api = ApiSerializer().serialize(ctx, title="Solo", html=html, markdown=md, pdf_ready=pdf)
    out = OutputBuilder().build(ctx, title="Solo")
    assert "Hello world." in html
    assert "Hello world." in md
    assert "Hello world." in pdf["lines"]
    assert api["paragraphs"][0]["text"] == "Hello world."
    assert out.html_ready and out.markdown_ready and out.pdf_ready and out.api_ready
