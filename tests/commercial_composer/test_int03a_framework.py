"""INT-03A Commercial Composer contract and mapping tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from engines.commercial_composer import (
    ALLOWED_OPERATIONS,
    COMMERCIAL_SECTIONS,
    COMPOSITION_STAGES,
    CONTRACT_ID,
    FORBIDDEN_OPERATIONS,
    FRAMEWORK_VERSION,
    INSUFFICIENT_COPY,
    SECTION_IDS,
    SECTION_SOURCES,
    SECTION_TITLES_VI,
    CommercialComposerError,
    CommercialNarrativeBlock,
    CommercialNarrativeUnit,
    CommercialSentence,
    commercial_composer_contract,
    compose_commercial_narrative,
    empty_commercial_unit,
)

ROOT = Path(__file__).resolve().parents[2]
COMPOSER_DIR = ROOT / "engines" / "commercial_composer"


def _block(
    *sentences: str,
    paths: tuple[str, ...] = (),
    topics: tuple[str, ...] = (),
) -> dict[str, object]:
    return {
        "sentences": list(sentences),
        "source_paths": list(paths or ("integrated",) * len(sentences)),
        "topic_ids": list(topics or ("strength",) * len(sentences)),
        "available": bool(sentences),
        "insufficient": not bool(sentences),
    }


def _integrated() -> dict[str, object]:
    return {
        "executive_summary": _block("Nhật chủ được đọc là Thân vượng."),
        "observation": _block("Điểm lực đã công bố là 0.87."),
        "reasoning": _block(
            "Yếu tố hỗ trợ lực Nhật chủ: Tướng.",
            "Yếu tố suy giảm lực Nhật chủ: Quan Sát.",
            '{"kind": "five_layer_luck_runtime_summary"}',
            paths=(
                "strength.evidence_pack.positive",
                "strength.evidence_pack.negative",
                "luck.luck_summary",
            ),
        ),
        "impact": _block("Với thế Thân vượng đã công bố, nhịp vận hành nghiêng về chủ động."),
        "recommendation": _block(
            "Ưu tiên hướng Dụng thần đã công bố: Hỏa.",
            "Hạn chế Kỵ thần đã công bố: Kim.",
            paths=("useful_god", "useful_god.unfavorable_display"),
        ),
        "summary": _block("Điểm lực đã công bố là 0.87. Ưu tiên hướng Dụng thần đã công bố: Hỏa."),
    }


def test_contract_surface_is_frozen() -> None:
    """Public contract lists seven sections and forbids calculation."""
    contract = commercial_composer_contract()
    assert contract["contract_id"] == CONTRACT_ID
    assert contract["framework_version"] == FRAMEWORK_VERSION
    assert contract["recalculates"] is False
    assert contract["llm"] is False
    assert contract["engine"] is False
    assert contract["input"] == "IntegratedNarrativeUnit"
    assert contract["output"] == "CommercialNarrativeUnit"
    assert contract["sections"] == list(COMMERCIAL_SECTIONS)
    assert contract["insufficient_copy"] == INSUFFICIENT_COPY


def test_commercial_section_order_and_titles() -> None:
    """Commercial reading follows the frozen consulting order."""
    assert COMMERCIAL_SECTIONS == (
        "executive_summary",
        "overall_reading",
        "current_situation",
        "strengths",
        "risks",
        "key_recommendation",
        "conclusion",
    )
    assert SECTION_IDS["current_situation"] == "sec-commercial-situation"
    assert SECTION_TITLES_VI["strengths"] == "Điểm mạnh"
    assert SECTION_TITLES_VI["risks"] == "Rủi ro chính"
    assert SECTION_TITLES_VI["key_recommendation"] == "Khuyến nghị trọng tâm"


def test_section_sources_read_only_integrated_blocks() -> None:
    """Every commercial section is filled from Integrated Narrative only."""
    assert SECTION_SOURCES["executive_summary"] == ("executive_summary",)
    assert SECTION_SOURCES["overall_reading"] == ("summary",)
    assert SECTION_SOURCES["current_situation"] == ("observation",)
    assert SECTION_SOURCES["strengths"] == ("impact",)
    assert SECTION_SOURCES["risks"] == ("reasoning", "recommendation")
    assert SECTION_SOURCES["key_recommendation"] == ("recommendation",)
    assert SECTION_SOURCES["conclusion"] == ("summary", "recommendation")


def test_allowed_and_forbidden_operations() -> None:
    """Composer may reshape published prose and must not invent truth."""
    assert ALLOWED_OPERATIONS == (
        "merge",
        "rewrite",
        "simplify",
        "reorder",
        "summarize",
    )
    assert FORBIDDEN_OPERATIONS == (
        "predict",
        "calculate",
        "infer",
        "invent",
        "expand",
    )
    assert COMPOSITION_STAGES[0] == "integrated_narrative"
    assert COMPOSITION_STAGES[-1] == "commercial_narrative_unit"


def test_compose_maps_integrated_blocks_without_new_facts() -> None:
    """Commercial sentences are Integrated sentences, reordered into consulting slots."""
    unit = compose_commercial_narrative(_integrated())
    assert unit.executive_summary.sentences[0].text == "Nhật chủ được đọc là Thân vượng."
    assert unit.current_situation.sentences[0].text == "Điểm lực đã công bố là 0.87."
    assert unit.strengths.sentences[0].text.startswith("Với thế Thân vượng")
    assert unit.key_recommendation.sentences[0].text.startswith("Ưu tiên hướng Dụng thần")
    published = [sentence.text for slot in COMMERCIAL_SECTIONS for sentence in getattr(unit, slot).sentences]
    source = {
        "Nhật chủ được đọc là Thân vượng.",
        "Điểm lực đã công bố là 0.87.",
        "Yếu tố hỗ trợ lực Nhật chủ: Tướng.",
        "Yếu tố suy giảm lực Nhật chủ: Quan Sát.",
        "Với thế Thân vượng đã công bố, nhịp vận hành nghiêng về chủ động.",
        "Ưu tiên hướng Dụng thần đã công bố: Hỏa.",
        "Hạn chế Kỵ thần đã công bố: Kim.",
        "Điểm lực đã công bố là 0.87. Ưu tiên hướng Dụng thần đã công bố: Hỏa.",
    }
    assert set(published) <= source
    for sentence in unit.current_situation.sentences:
        assert sentence.integrated_slots == ("observation",)


def test_risks_select_published_restraint_paths_only() -> None:
    """Risks copy Integrated negative/unfavorable lines; they do not infer new danger."""
    unit = compose_commercial_narrative(_integrated())
    texts = [sentence.text for sentence in unit.risks.sentences]
    assert "Yếu tố suy giảm lực Nhật chủ: Quan Sát." in texts
    assert "Hạn chế Kỵ thần đã công bố: Kim." in texts
    assert "Yếu tố hỗ trợ lực Nhật chủ: Tướng." not in texts
    assert not any(text.startswith("{") for text in texts)


def test_simplify_drops_machine_only_dumps() -> None:
    """JSON Integrated dumps are not commercial prose."""
    unit = compose_commercial_narrative(_integrated())
    joined = " ".join(
        sentence.text
        for slot in COMMERCIAL_SECTIONS
        for sentence in getattr(unit, slot).sentences
    )
    assert "five_layer_luck_runtime_summary" not in joined


def test_conclusion_summarizes_published_summary_and_recommendation() -> None:
    """Conclusion restates published summary; overlapping rec meaning is emitted once."""
    unit = compose_commercial_narrative(_integrated())
    texts = [sentence.text for sentence in unit.conclusion.sentences]
    assert texts[0].startswith("Điểm lực đã công bố là 0.87")
    assert unit.conclusion.sentences[0].integrated_slots == ("summary",)
    assert all("Ưu tiên hướng Dụng thần" in text or text.startswith("Điểm lực") for text in texts)
    assert len(texts) == 1


def test_missing_integrated_narrative_is_insufficient() -> None:
    """No rebuild from topic engines when Integrated Narrative is absent."""
    unit = compose_commercial_narrative(None)
    assert unit.status == "insufficient"
    payload = unit.to_dict()
    for slot in COMMERCIAL_SECTIONS:
        block = payload[slot]
        assert block["insufficient"] is True
        assert block["empty_copy"] == INSUFFICIENT_COPY
        assert block["sentences"] == []


def test_empty_unit_keeps_all_seven_sections() -> None:
    """Insufficient commercial units remain structurally complete."""
    unit = empty_commercial_unit()
    assert unit.status == "insufficient"
    for slot in COMMERCIAL_SECTIONS:
        block = getattr(unit, slot)
        assert block.slot == slot
        assert block.insufficient is True


def test_sentence_without_integrated_trace_is_rejected() -> None:
    """A commercial sentence that cannot cite Integrated Narrative is invalid."""
    orphan = CommercialSentence(
        text="Họ nghề hợp bạn.",
        slot="executive_summary",
        integrated_slots=(),
    )
    with pytest.raises(CommercialComposerError):
        CommercialNarrativeUnit(
            executive_summary=CommercialNarrativeBlock(
                slot="executive_summary",
                sentences=(orphan,),
                available=True,
                insufficient=False,
            ),
            overall_reading=CommercialNarrativeBlock(slot="overall_reading"),
            current_situation=CommercialNarrativeBlock(slot="current_situation"),
            strengths=CommercialNarrativeBlock(slot="strengths"),
            risks=CommercialNarrativeBlock(slot="risks"),
            key_recommendation=CommercialNarrativeBlock(slot="key_recommendation"),
            conclusion=CommercialNarrativeBlock(slot="conclusion"),
            status="partial",
        )


def test_package_does_not_import_engines_or_delivery() -> None:
    """INT-03A reads Integrated Narrative only. No Calendar, Identity, Workspace, or Report."""
    joined = "\n".join(path.read_text(encoding="utf-8") for path in COMPOSER_DIR.glob("*.py"))
    assert "from engines.calendar" not in joined
    assert "from engines.bazi" not in joined
    assert "from engines.strength" not in joined
    assert "from engines.pattern" not in joined
    assert "from engines.useful_god" not in joined
    assert "from engines.luck" not in joined
    assert "from engines.identity" not in joined
    assert "from engines.interpretation_engine" not in joined
    assert "from engines.report_engine" not in joined
    assert "from engines.narrative_engine" not in joined
    assert "customer_portal" not in joined
    assert "def calculate(" not in joined
    assert "openai" not in joined.lower()
    assert "compose_integrated_narrative" not in joined
    assert "compose_strength_narrative" not in joined
