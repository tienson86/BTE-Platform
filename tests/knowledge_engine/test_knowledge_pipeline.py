"""Unit tests for Knowledge Pipeline integration (Epic 03 Milestone 10)."""

from __future__ import annotations

from engines.knowledge_engine import (
    PIPELINE_STAGES,
    KnowledgeHit,
    KnowledgePipeline,
    KnowledgeRecord,
    KnowledgeResult,
)


def _context() -> dict:
    return {
        "ten_gods": {"items": ["chính quan"], "status": "ok"},
        "pattern": {"main_pattern": "chinh_quan", "name": "chính quan"},
        "useful_god": {"element": "kim", "status": "ok"},
        "strength": {"level": "strong"},
        "shensha": {"stars": ["hoa cái"], "status": "ok"},
        "day_master": "Bính",
        "bazi": {
            "day_master": "Bính",
            "year_pillar": {"stem": "Canh", "branch": "Ngọ"},
            "day_pillar": {"stem": "Bính", "branch": "Ngọ"},
        },
    }


def _knowledge() -> KnowledgeResult:
    record = KnowledgeRecord(
        id="KNW-TG-001",
        topic="Ten Gods",
        keyword="chính quan",
        condition="",
        classical_text="Chính Quan chủ quyền uy.",
        modern_interpretation="Officer means authority.",
        priority=90,
        confidence=0.9,
        reference="Uyên Hải Tử Bình|chương 1|trang 1",
    )
    return KnowledgeResult(
        entries=[
            KnowledgeHit(
                record=record,
                keyword_score=1.0,
                condition_score=1.0,
                relevance_score=1.0,
            )
        ],
        metadata={},
    )


class TestKnowledgePipeline:
    def test_pipeline_stage_order(self) -> None:
        assert PIPELINE_STAGES == (
            "knowledge",
            "retriever",
            "reasoning_graph",
            "evidence_builder",
            "prompt_builder",
            "llm",
            "response_validator",
            "portal",
        )

    def test_full_pipeline_grounded(self) -> None:
        result = KnowledgePipeline().run(
            rule_context=_context(),
            question="Why is Suitable Career favored?",
            knowledge=_knowledge(),
        )
        assert result.evidence.items
        assert result.knowledge.entries
        assert result.reasoning.nodes
        assert result.prompt.sections
        assert result.llm_output
        assert result.validation is not None
        assert result.discussion is not None
        assert result.discussion.grounded is True
        assert result.portal_payload["replaces_narrative"] is False
        assert "[Evidence]" in result.llm_output
        assert result.metadata["stages"] == list(PIPELINE_STAGES)

    def test_portal_status_additive(self) -> None:
        status = KnowledgePipeline.portal_status()
        assert status["alters_public_pipeline"] is False
        assert status["alters_narrative"] is False
        assert status["endpoint"] == "/api/v1/discussion"

    def test_never_raw_chart_alone_via_discussion(self) -> None:
        result = KnowledgePipeline().run(
            rule_context={
                "day_master": "Bính",
                "year_pillar": {"stem": "Canh", "branch": "Ngọ"},
            },
            question="Why?",
            knowledge=_knowledge(),
        )
        # Bare pillars produce little/no reasoning; incomplete grounding refused.
        assert result.discussion is not None
        assert result.portal_payload["replaces_narrative"] is False
