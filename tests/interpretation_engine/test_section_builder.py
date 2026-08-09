"""IE-3 section builder tests."""

from __future__ import annotations

from engines.interpretation_engine.composition.composition_context import build_assembly_context
from engines.interpretation_engine.composition.section_builder import SectionBuilder
from tests.interpretation_engine.ie3_support import assemble_inputs


def test_section_builder_groups_candidates_without_rendering() -> None:
    """Sections carry candidate identities only. No prose or style keys."""
    payload = assemble_inputs()
    context = build_assembly_context(**payload)
    sections = SectionBuilder().build(context)
    ids = [item.section_id for item in sections]
    assert ids == ["SEC-overview", "SEC-luck", "SEC-summary"]
    overview = sections[0]
    assert "SC-KN-IE2-AN-SEASONAL" in overview.candidate_ids
    assert "KN-IE2-AN-USEFUL_GOD" in overview.knowledge_ids
    assert overview.status == "assembled"
    for item in sections:
        encoded = item.to_dict()
        assert "narrative" not in encoded
        assert "html" not in encoded
        assert "css" not in encoded
