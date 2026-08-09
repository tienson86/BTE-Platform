"""IE-3 cross-reference builder tests."""

from __future__ import annotations

from engines.interpretation_engine.composition.chapter_builder import ChapterBuilder
from engines.interpretation_engine.composition.composition_context import build_assembly_context
from engines.interpretation_engine.composition.cross_reference_builder import CrossReferenceBuilder
from engines.interpretation_engine.composition.section_builder import SectionBuilder
from tests.interpretation_engine.ie3_support import assemble_inputs


def test_cross_references_are_structured_identities() -> None:
    """References link ids only. No hyperlink fields."""
    payload = assemble_inputs()
    sections = SectionBuilder().build(build_assembly_context(**payload))
    chapters = ChapterBuilder().build(sections)
    references = CrossReferenceBuilder().build(sections, chapters)
    assert references
    payload_refs = [item.to_dict() for item in references]
    types = {(item["source_type"], item["target_type"]) for item in payload_refs}
    assert ("chapter", "section") in types
    assert ("section", "knowledge") in types
    assert ("section", "evidence") in types
    assert ("section", "reasoning") in types
    for item in payload_refs:
        assert "href" not in item
        assert "url" not in item
        assert "anchor" not in item
        assert item["reference_id"].startswith("XREF-")
