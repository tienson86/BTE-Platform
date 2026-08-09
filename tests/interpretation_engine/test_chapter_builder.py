"""IE-3 chapter builder tests."""

from __future__ import annotations

from engines.interpretation_engine.composition.chapter_builder import ChapterBuilder
from engines.interpretation_engine.composition.composition_context import build_assembly_context
from engines.interpretation_engine.composition.section_builder import SectionBuilder
from engines.interpretation_engine.foundation_constants import CANONICAL_MODULE_ORDER
from tests.interpretation_engine.ie3_support import assemble_inputs


def test_chapter_builder_emits_registered_chapters_in_order() -> None:
    """All nine registered chapters exist. Empty chapters stay empty."""
    payload = assemble_inputs()
    sections = SectionBuilder().build(build_assembly_context(**payload))
    chapters = ChapterBuilder().build(sections)
    assert [item.module_id for item in chapters] == list(CANONICAL_MODULE_ORDER)
    assert [item.chapter_id for item in chapters] == [f"CH-{item}" for item in CANONICAL_MODULE_ORDER]
    by_id = {item.chapter_id: item for item in chapters}
    assert by_id["CH-overview"].status == "assembled"
    assert by_id["CH-overview"].section_ids == ("SEC-overview",)
    assert by_id["CH-personality"].status == "empty"
    assert by_id["CH-summary"].section_ids == ("SEC-summary",)
