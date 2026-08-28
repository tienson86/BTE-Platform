"""INT-02A Narrative Framework contract tests. No engine execution."""

from __future__ import annotations

from pathlib import Path

import pytest

from engines.narrative_framework import (
    ANALYTICAL_TOPICS,
    BLOCK_IDS,
    BLOCK_TITLES_VI,
    COMPOSITION_STAGES,
    CONTRACT_ID,
    FRAMEWORK_VERSION,
    INSUFFICIENT_COPY,
    NARRATIVE_BLOCKS,
    SENTENCE_OWNERS,
    TEMPLATE_HIERARCHY,
    WORKSPACE_BLOCK_ALIASES,
    NarrativeBlock,
    NarrativeFrameworkError,
    NarrativeSentence,
    TopicNarrativeUnit,
    narrative_framework_contract,
)
from engines.narrative_framework.contracts import FORBIDDEN_EMPTY_TOKENS
from engines.narrative_framework.models import empty_topic_unit

ROOT = Path(__file__).resolve().parents[2]
FRAMEWORK_DIR = ROOT / "engines" / "narrative_framework"


def test_contract_surface_is_frozen() -> None:
    """Public contract lists five blocks, topics, and no runtime flags."""
    contract = narrative_framework_contract()
    assert contract["contract_id"] == CONTRACT_ID
    assert contract["framework_version"] == FRAMEWORK_VERSION
    assert contract["runtime"] is False
    assert contract["recalculates"] is False
    assert contract["llm"] is False
    assert contract["frontend"] is False
    assert contract["blocks"] == [
        "observation",
        "reasoning",
        "impact",
        "recommendation",
        "conclusion",
    ]
    assert contract["insufficient_copy"] == "Chưa có dữ liệu"


def test_block_ids_and_vietnamese_titles() -> None:
    """Section ids and titles stay aligned with existing identity / workspace names."""
    assert NARRATIVE_BLOCKS == (
        "observation",
        "reasoning",
        "impact",
        "recommendation",
        "conclusion",
    )
    assert BLOCK_IDS["observation"] == "sec-observation"
    assert BLOCK_IDS["reasoning"] == "sec-reasoning"
    assert BLOCK_IDS["impact"] == "sec-impact"
    assert BLOCK_IDS["recommendation"] == "sec-recommendation"
    assert BLOCK_IDS["conclusion"] == "sec-conclusion"
    assert BLOCK_TITLES_VI["observation"] == "Quan sát"
    assert BLOCK_TITLES_VI["reasoning"] == "Lý do"
    assert BLOCK_TITLES_VI["impact"] == "Tác động"
    assert BLOCK_TITLES_VI["recommendation"] == "Khuyến nghị"
    assert BLOCK_TITLES_VI["conclusion"] == "Kết luận"


def test_workspace_aliases_do_not_invent_a_second_contract() -> None:
    """Frozen workspace names map onto framework slots."""
    assert WORKSPACE_BLOCK_ALIASES["observe"] == "observation"
    assert WORKSPACE_BLOCK_ALIASES["reason"] == "reasoning"
    assert WORKSPACE_BLOCK_ALIASES["advice"] == "recommendation"


def test_template_hierarchy_and_sentence_ownership() -> None:
    """Templates nest; engines own facts, knowledge owns wording, framework owns order."""
    assert TEMPLATE_HIERARCHY == (
        "topic_template",
        "block_template",
        "sentence_template",
        "slot",
    )
    assert SENTENCE_OWNERS["fact"] == "engine_result"
    assert SENTENCE_OWNERS["template"] == "sentence_library"
    assert SENTENCE_OWNERS["composition"] == "narrative_framework"
    assert SENTENCE_OWNERS["selection"] == "interpretation_engine"
    assert SENTENCE_OWNERS["delivery"] == "report_or_portal"


def test_composition_pipeline_order() -> None:
    """Composition consumes engine output; it does not calculate."""
    assert COMPOSITION_STAGES == (
        "engine_result",
        "topic_evidence_pack",
        "block_fill",
        "topic_narrative_unit",
    )


def test_analytical_topics_cover_every_narratable_engine() -> None:
    """Required topic catalog is frozen for later application sprints."""
    assert ANALYTICAL_TOPICS == (
        "strength",
        "pattern",
        "useful_god",
        "five_elements",
        "ten_gods",
        "shensha",
        "temperature",
        "luck",
    )
    assert "calendar" not in ANALYTICAL_TOPICS
    assert "bazi" not in ANALYTICAL_TOPICS


def test_insufficient_copy_is_the_only_empty_token() -> None:
    """Empty blocks use Chưa có dữ liệu, never N/A or Không."""
    assert INSUFFICIENT_COPY == "Chưa có dữ liệu"
    assert INSUFFICIENT_COPY not in FORBIDDEN_EMPTY_TOKENS
    for token in FORBIDDEN_EMPTY_TOKENS:
        assert token != INSUFFICIENT_COPY


def test_empty_topic_unit_keeps_all_five_blocks() -> None:
    """Insufficient topics remain structurally complete."""
    unit = empty_topic_unit("strength", "analysis.strength")
    assert tuple(unit.blocks.keys()) == NARRATIVE_BLOCKS
    assert unit.status == "insufficient"
    payload = unit.to_dict()
    assert payload["schema_version"] == FRAMEWORK_VERSION
    for slot in NARRATIVE_BLOCKS:
        block = payload["blocks"][slot]
        assert block["insufficient"] is True
        assert block["empty_copy"] == INSUFFICIENT_COPY
        assert block["section_id"] == BLOCK_IDS[slot]


def test_unit_rejects_missing_or_reordered_blocks() -> None:
    """A dropped conclusion is a contract violation, not a shorter card."""
    incomplete = {
        slot: NarrativeBlock(slot=slot)
        for slot in NARRATIVE_BLOCKS
        if slot != "conclusion"
    }
    with pytest.raises(NarrativeFrameworkError):
        TopicNarrativeUnit(
            topic_id="pattern",
            source_path="analysis.pattern",
            blocks=incomplete,
            status="partial",
        )


def test_sentence_role_must_match_block() -> None:
    """Recommendation prose cannot be stored on the observation block."""
    bad = NarrativeSentence(
        sentence_id="SEN-000001",
        role="recommendation",
        text="Giữ nhịp.",
        source_path="identity.interpretation.action",
        owner="sentence_library",
    )
    blocks = {slot: NarrativeBlock(slot=slot) for slot in NARRATIVE_BLOCKS}
    blocks["observation"] = NarrativeBlock(
        slot="observation",
        sentences=(bad,),
        available=True,
        insufficient=False,
    )
    with pytest.raises(NarrativeFrameworkError):
        TopicNarrativeUnit(
            topic_id="useful_god",
            source_path="analysis.useful_god",
            blocks=blocks,
            status="partial",
        )


def test_framework_package_does_not_import_engines_or_ui() -> None:
    """INT-02A is architecture-only: no Calendar, Bazi, Identity, Workspace, or Report."""
    joined = "\n".join(path.read_text(encoding="utf-8") for path in FRAMEWORK_DIR.glob("*.py"))
    assert "from engines.calendar" not in joined
    assert "from engines.bazi" not in joined
    assert "from engines.strength" not in joined
    assert "from engines.pattern" not in joined
    assert "from engines.identity" not in joined
    assert "from engines.interpretation_engine" not in joined
    assert "from engines.report_engine" not in joined
    assert "customer_portal" not in joined
    assert "def calculate(" not in joined
    assert "class NarrativeEngine" not in joined
