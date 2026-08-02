"""Unit tests for Prompt Builder (Epic 03 Milestone 06)."""

from __future__ import annotations

import re

from engines.knowledge_engine import (
    PROMPT_SECTION_KEYS,
    EvidenceItem,
    EvidencePackage,
    KnowledgeHit,
    KnowledgeRecord,
    KnowledgeResult,
    PromptBuilder,
    ReasoningEdge,
    ReasoningGraph,
    ReasoningNode,
    StructuredPrompt,
)


def _sample_chart() -> dict:
    return {
        "day_master": "Bính",
        "day_master_element": "Hỏa",
        "gender": "male",
        "year_pillar": {"stem": "Canh", "branch": "Ngọ"},
        "month_pillar": {"stem": "Ất", "branch": "Tỵ"},
        "day_pillar": {"stem": "Bính", "branch": "Ngọ"},
        "hour_pillar": {"stem": "Quý", "branch": "Tỵ"},
        "birth_season": "summer",
    }


def _sample_evidence() -> EvidencePackage:
    return EvidencePackage(
        items=[
            EvidenceItem(
                category="ten_gods",
                rule="present=Chính Quan",
                reason="Officer star is visible in the chart",
                confidence=0.9,
                source="rule_context:ten_gods.items",
            ),
            EvidenceItem(
                category="strength",
                rule="level=strong",
                reason="Day Master is supported",
                confidence=0.85,
                source="rule_context:strength.level",
            ),
        ],
        categories={
            "ten_gods": [],
            "strength": [],
        },
        metadata={"item_count": 2},
    )


def _sample_knowledge() -> KnowledgeResult:
    record = KnowledgeRecord(
        id="TG-001-OFFICER",
        topic="Ten Gods",
        keyword="Chính Quan; Officer",
        condition="ten_gods contains chính quan",
        classical_text="Chính Quan chủ quyền uy và trách nhiệm.",
        modern_interpretation="Officer indicates structured authority and duty.",
        priority=90,
        confidence=0.92,
        reference="Đế Thiên Tùy Bút",
        source_file="03_ten_gods.csv",
    )
    return KnowledgeResult(
        entries=[
            KnowledgeHit(
                record=record,
                keyword_score=1.0,
                condition_score=1.0,
                relevance_score=0.95,
                matched_keywords=("chính quan",),
                matched_conditions=("ten_gods",),
            )
        ],
        metadata={"trace": []},
    )


def _sample_reasoning() -> ReasoningGraph:
    nodes = [
        ReasoningNode("ev:career_officer_strong", "Strong Officer", "evidence", "career"),
        ReasoningNode(
            "ir:career_officer_strong",
            "Career Leadership",
            "intermediate_rule",
            "career",
            {"template_id": "career_officer_strong"},
        ),
        ReasoningNode(
            "rs:career_officer_strong",
            "Management Potential",
            "reasoning",
            "career",
        ),
        ReasoningNode(
            "cn:career_officer_strong",
            "Suitable Career",
            "conclusion",
            "career",
        ),
    ]
    edges = [
        ReasoningEdge(
            "edge:1",
            "ev:career_officer_strong",
            "ir:career_officer_strong",
            "Officer star supports authority and organizational role.",
            90,
            0.9,
            "rule:career_officer_strong",
        ),
        ReasoningEdge(
            "edge:2",
            "ir:career_officer_strong",
            "rs:career_officer_strong",
            "Leadership signal implies capacity to manage people and process.",
            80,
            0.86,
            "rule:career_officer_strong",
        ),
        ReasoningEdge(
            "edge:3",
            "rs:career_officer_strong",
            "cn:career_officer_strong",
            "Management roles are favored.",
            70,
            0.84,
            "rule:career_officer_strong",
        ),
    ]
    return ReasoningGraph(
        nodes=nodes,
        edges=edges,
        conclusions=["Suitable Career"],
        metadata={"trace": [{"template_id": "career_officer_strong", "accepted": True}]},
    )


_FORBIDDEN = re.compile(
    r"(?i)(\.csv\b|knowledge_engine|score_engine|bazi_engine|\w+Engine|"
    r"rule:career_officer_strong|TG-001|template_id|03_ten_gods|"
    r"ev:career_officer_strong|edge:1)"
)


class TestPromptBuilder:
    def test_sections_are_separated(self) -> None:
        prompt = PromptBuilder().build(
            chart=_sample_chart(),
            evidence=_sample_evidence(),
            knowledge=_sample_knowledge(),
            reasoning=_sample_reasoning(),
        )
        assert isinstance(prompt, StructuredPrompt)
        for key in PROMPT_SECTION_KEYS:
            section = prompt.section(key)
            assert section is not None
            assert section.title
            assert key in prompt.sections
            assert f"## {section.title}" in prompt.text

        # Section order in assembled text.
        positions = [
            prompt.text.index(f"## {prompt.sections[key].title}")
            for key in PROMPT_SECTION_KEYS
        ]
        assert positions == sorted(positions)

    def test_facts_from_chart(self) -> None:
        prompt = PromptBuilder().build(chart=_sample_chart())
        facts = prompt.section("facts")
        assert facts is not None
        body = facts.content
        assert "Day Master: Bính" in body
        assert "Year Pillar: Canh Ngọ" in body
        assert "Season: summer" in body

    def test_evidence_and_knowledge_content(self) -> None:
        prompt = PromptBuilder().build(
            evidence=_sample_evidence(),
            knowledge=_sample_knowledge(),
        )
        evidence = prompt.section("evidence")
        knowledge = prompt.section("knowledge")
        assert evidence is not None and "present=Chính Quan" in evidence.content
        assert "Chart context" in evidence.content
        assert knowledge is not None
        assert "Classical:" in knowledge.content
        assert "Modern:" in knowledge.content
        assert "Reference:" not in knowledge.content
        assert "Đế Thiên Tùy Bút" not in knowledge.content
        assert "## Internal Sources" in prompt.text
        assert "Đế Thiên Tùy Bút" in prompt.text or "Other classical" in prompt.text

    def test_reasoning_chains_without_ids(self) -> None:
        prompt = PromptBuilder().build(reasoning=_sample_reasoning())
        reasoning = prompt.section("reasoning")
        assert reasoning is not None
        assert (
            "Strong Officer → Career Leadership → Management Potential → Suitable Career"
            in reasoning.content
        )
        assert "Suitable Career" in reasoning.content
        assert "ev:" not in reasoning.content
        assert "rule:" not in reasoning.content

    def test_never_expose_rule_ids_csv_engine_names(self) -> None:
        # Poison inputs with forbidden tokens that must be redacted.
        poisoned_knowledge = KnowledgeResult(
            entries=[
                KnowledgeHit(
                    record=KnowledgeRecord(
                        id="TG-001-OFFICER",
                        topic="Ten Gods from knowledge_engine",
                        keyword="Officer",
                        condition="",
                        classical_text="Loaded from 03_ten_gods.csv via KnowledgeLoader",
                        modern_interpretation="Do not cite score_engine or BaziEngine.",
                        priority=1,
                        confidence=0.5,
                        reference="see database/20_knowledge/03_ten_gods.csv",
                        source_file="03_ten_gods.csv",
                    ),
                    keyword_score=1.0,
                    condition_score=1.0,
                    relevance_score=1.0,
                )
            ],
            metadata={},
        )
        poisoned_evidence = EvidencePackage(
            items=[
                EvidenceItem(
                    category="pattern",
                    rule="main=chinh_quan rule:career_officer_strong",
                    reason="Matched by pattern_engine template_id=career_officer_strong",
                    confidence=0.7,
                    source="rule:career_officer_strong",
                )
            ],
            categories={},
            metadata={},
        )
        prompt = PromptBuilder().build(
            chart=_sample_chart(),
            evidence=poisoned_evidence,
            knowledge=poisoned_knowledge,
            reasoning=_sample_reasoning(),
        )
        full = prompt.text
        assert "TG-001" not in full
        assert "03_ten_gods.csv" not in full
        assert "knowledge_engine" not in full.lower()
        assert "score_engine" not in full.lower()
        assert "BaziEngine" not in full
        assert "pattern_engine" not in full.lower()
        assert "rule:career_officer_strong" not in full
        assert "template_id" not in full.lower()
        assert not _FORBIDDEN.search(full)

    def test_writing_style_present(self) -> None:
        prompt = PromptBuilder().build()
        style = prompt.section("writing_style")
        assert style is not None
        assert style.content
        assert "Do not mention internal identifiers" in style.content

    def test_empty_inputs(self) -> None:
        prompt = PromptBuilder().build()
        assert prompt.section("facts") is not None
        assert prompt.section("facts").content == ""
        assert "(none)" in prompt.text
        assert prompt.metadata["fact_count"] == 0

    def test_mapping_inputs_supported(self) -> None:
        prompt = PromptBuilder().build(
            chart={"day_master": "Giáp"},
            evidence={
                "items": [
                    {
                        "category": "bazi",
                        "rule": "day_master=Giáp",
                        "reason": "Stem present",
                        "confidence": 1.0,
                        "source": "rule_context:bazi.day_master",
                    }
                ]
            },
            knowledge={
                "entries": [
                    {
                        "id": "FE-99",
                        "topic": "Wood",
                        "keyword": "Giáp",
                        "condition": "",
                        "classical_text": "Giáp thuộc Mộc.",
                        "modern_interpretation": "Jia is Wood.",
                        "priority": 1,
                        "confidence": 0.8,
                        "reference": "Ngũ Hành",
                        "source_file": "01_five_elements.csv",
                    }
                ]
            },
            reasoning={
                "nodes": [
                    {"id": "ev:x", "label": "Wood Day Master", "kind": "evidence"},
                    {"id": "cn:x", "label": "Growth Theme", "kind": "conclusion"},
                ],
                "edges": [
                    {
                        "id": "edge:x",
                        "source_id": "ev:x",
                        "target_id": "cn:x",
                        "reason": "Wood implies growth.",
                        "priority": 1,
                        "confidence": 0.7,
                        "source": "rule:hidden",
                    }
                ],
                "conclusions": ["Growth Theme"],
                "metadata": {},
            },
        )
        assert "Day Master: Giáp" in prompt.text
        assert "day_master=Giáp" in prompt.text
        assert "Giáp thuộc Mộc." in prompt.text
        assert "01_five_elements.csv" not in prompt.text
        assert "FE-99" not in prompt.text
        assert "rule:hidden" not in prompt.text

    def test_to_dict(self) -> None:
        prompt = PromptBuilder().build(chart=_sample_chart())
        payload = prompt.to_dict()
        assert "sections" in payload
        assert "text" in payload
        assert payload["sections"]["facts"]["title"] == "Facts"

    def test_four_pillars_chart_shape(self) -> None:
        prompt = PromptBuilder().build(
            chart={
                "day_master": "Ất",
                "four_pillars": {
                    "year": {"stem": "Giáp", "branch": "Tý"},
                    "month_pillar": "Ất Sửu",
                    "day": {"can": "Ất", "chi": "Mão"},
                    "hour": {"stem": "Bính"},
                },
            }
        )
        facts = prompt.section("facts").content
        assert "Year Pillar: Giáp Tý" in facts
        assert "Month Pillar: Ất Sửu" in facts
        assert "Day Pillar: Ất Mão" in facts
        assert "Hour Pillar: Bính" in facts

    def test_chart_object_to_dict_and_attributes(self) -> None:
        class ChartDict:
            def to_dict(self) -> dict:
                return {"day_master": "Nhâm", "gender": "female"}

        class ChartAttrs:
            day_master = "Quý"
            day_master_element = "Thủy"
            gender = "male"
            year_pillar = None
            month_pillar = None
            day_pillar = None
            hour_pillar = None
            birth_season = "winter"
            season = None
            four_pillars = None
            bazi = None
            wuxing = None

        prompt_a = PromptBuilder().build(chart=ChartDict())
        prompt_b = PromptBuilder().build(chart=ChartAttrs())
        assert "Day Master: Nhâm" in prompt_a.text
        assert "Day Master: Quý" in prompt_b.text
        assert "Season: winter" in prompt_b.text

    def test_knowledge_list_and_nested_record(self) -> None:
        record = KnowledgeRecord(
            id="YY-1",
            topic="",
            keyword="",
            condition="",
            classical_text="Âm Dương tương sinh.",
            modern_interpretation="",
            priority=1,
            confidence=0.6,
            reference="",
            source_file="",
        )
        hit = KnowledgeHit(
            record=record,
            keyword_score=1.0,
            condition_score=1.0,
            relevance_score=1.0,
        )
        prompt = PromptBuilder().build(
            knowledge=[
                hit,
                record,
                {
                    "record": {
                        "topic": "Yin Yang",
                        "classical_text": "Cân bằng.",
                        "confidence": 0.5,
                    }
                },
                "ignore",
            ]
        )
        body = prompt.section("knowledge").content
        assert "Âm Dương tương sinh." in body
        assert "Knowledge entry" in body
        assert "Yin Yang" in body
        assert "YY-1" not in prompt.text

    def test_evidence_mixed_rows_and_public_sources(self) -> None:
        item = EvidenceItem(
            category="custom_cat",
            rule="flag=true",
            reason="",
            confidence=1.1,
            source="manual_review",
        )
        prompt = PromptBuilder().build(
            evidence={
                "items": [
                    item,
                    {
                        "category": "bazi",
                        "rule": "x=1",
                        "reason": "r",
                        "confidence": 0.2,
                        "source": "",
                    },
                    {
                        "category": "bazi",
                        "rule": "y=2",
                        "reason": "r",
                        "confidence": 0.2,
                        "source": "leak.csv",
                    },
                    {
                        "category": "bazi",
                        "rule": "z=3",
                        "reason": "r",
                        "confidence": 0.2,
                        "source": "score_engine",
                    },
                    "bad-row",
                ]
            }
        )
        body = prompt.section("evidence").content
        assert "Source: manual_review" in body
        assert "leak.csv" not in body
        assert "score_engine" not in body

    def test_reasoning_object_rows_and_empty_reason(self) -> None:
        node_a = ReasoningNode("ev:a", "Evidence A", "evidence")
        node_b = ReasoningNode("cn:a", "Conclusion A", "conclusion")
        edge_ok = ReasoningEdge(
            "edge:a", "ev:a", "cn:a", "Valid reason", 1, 0.5, "public"
        )
        edge_blank = ReasoningEdge("edge:b", "ev:a", "cn:a", "", 1, 0.5, "public")
        prompt = PromptBuilder().build(
            reasoning={
                "nodes": [
                    node_a,
                    node_b,
                    {"id": "ev:b", "label": "Evidence B", "kind": "evidence"},
                ],
                "edges": [
                    edge_ok,
                    edge_blank,
                    {
                        "id": "edge:c",
                        "source_id": "ev:b",
                        "target_id": "cn:a",
                        "reason": "Another",
                        "priority": 1,
                        "confidence": 0.4,
                        "source": "x",
                    },
                ],
                "conclusions": ["Conclusion A"],
                "metadata": {},
            }
        )
        body = prompt.section("reasoning").content
        assert "Valid reason" in body
        assert "Another" in body
        assert body.count("Evidence A → Conclusion A") == 1

    def test_pillar_object_and_custom_style(self) -> None:
        class Pillar:
            stem = "Mậu"
            branch = "Thìn"

        prompt = PromptBuilder(writing_style=["Keep tone neutral."]).build(
            chart={"year_pillar": Pillar(), "day_pillar": 12}
        )
        assert "Year Pillar: Mậu Thìn" in prompt.text
        assert "Keep tone neutral." in prompt.section("writing_style").content

    def test_structured_prompt_skips_missing_section(self) -> None:
        from engines.knowledge_engine.prompt_models import PromptSection

        prompt = StructuredPrompt(
            sections={"facts": PromptSection("facts", "Facts", ["Day Master: Giáp"])}
        )
        assert "## Facts" in prompt.text
        assert "## Evidence" not in prompt.text
        assert prompt.section("missing") is None
