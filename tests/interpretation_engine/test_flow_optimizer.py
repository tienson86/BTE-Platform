"""IE-3 flow optimizer tests."""

from __future__ import annotations

from engines.interpretation_engine.composition.chapter_builder import ChapterBuilder
from engines.interpretation_engine.composition.composition_context import build_assembly_context
from engines.interpretation_engine.composition.flow_optimizer import FlowOptimizer
from engines.interpretation_engine.composition.section_builder import AssembledSection, SectionBuilder
from tests.interpretation_engine.ie3_support import assemble_inputs


def test_flow_optimizer_orders_and_groups_without_rewriting() -> None:
    """Optimizer may reorder/group only. Candidate ids stay unchanged."""
    payload = assemble_inputs()
    sections = list(SectionBuilder().build(build_assembly_context(**payload)))
    sections.reverse()
    chapters = ChapterBuilder().build(sections)
    optimized_sections, optimized_chapters, plan = FlowOptimizer().optimize(sections, chapters)
    assert [item.module_id for item in optimized_sections] == ["overview", "luck", "summary"]
    assert plan.operations == ("order_by_module", "group_overview_body_summary")
    original_ids = {item.section_id: item.candidate_ids for item in sections}
    for item in optimized_sections:
        assert item.candidate_ids == original_ids[item.section_id]
    assert "rewrite" not in plan.operations
    assert optimized_chapters[0].chapter_id == "CH-overview"
    assert isinstance(sections[0], AssembledSection)
