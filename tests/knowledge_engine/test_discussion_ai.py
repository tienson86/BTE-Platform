"""Conversation tests for Discussion AI (Epic 03 Milestone 09)."""

from __future__ import annotations

from engines.knowledge_engine import (
    SUPPORTED_QUESTION_TYPES,
    AIResponseValidator,
    DiscussionAI,
    EvidenceBuilder,
    KnowledgeHit,
    KnowledgeRecord,
    KnowledgeResult,
    ReasoningGraphEngine,
)


def _officer_context() -> dict:
    return {
        "ten_gods": {"items": ["chính quan", "thực thần"], "status": "ok"},
        "pattern": {"main_pattern": "chinh_quan", "name": "chính quan"},
        "shensha": {"stars": ["hoa cái"], "status": "ok"},
        "useful_god": {"element": "kim", "name": "Kim", "status": "ok"},
        "strength": {"level": "strong"},
        "temperature": {"status": "warm"},
        "day_master": "Bính",
        "bazi": {
            "day_master": "Bính",
            "year_pillar": {"stem": "Canh", "branch": "Ngọ"},
            "month_pillar": {"stem": "Ất", "branch": "Tỵ"},
            "day_pillar": {"stem": "Bính", "branch": "Ngọ"},
            "hour_pillar": {"stem": "Quý", "branch": "Tỵ"},
        },
    }


def _knowledge() -> KnowledgeResult:
    records = [
        KnowledgeRecord(
            id="KNW-TG-001",
            topic="Ten Gods",
            keyword="chính quan;officer",
            condition="ten_gods contains chính quan",
            classical_text="Chính Quan chủ quyền uy và trách nhiệm.",
            modern_interpretation="Officer indicates authority and structured duty.",
            priority=90,
            confidence=0.92,
            reference="Uyên Hải Tử Bình|chương 3|trang 12",
        ),
        KnowledgeRecord(
            id="KNW-UG-001",
            topic="Useful God",
            keyword="dụng thần;useful god;kim",
            condition="useful_god.element exists",
            classical_text="Dụng thần là then chốt điều hòa cục diện.",
            modern_interpretation="Useful God balances the chart dynamics.",
            priority=85,
            confidence=0.9,
            reference="Tử Bình Chân Thuyên|chương 2|trang 8",
        ),
    ]
    return KnowledgeResult(
        entries=[
            KnowledgeHit(
                record=record,
                keyword_score=1.0,
                condition_score=1.0,
                relevance_score=0.95,
            )
            for record in records
        ],
        metadata={},
    )


def _ai() -> DiscussionAI:
    return DiscussionAI(reasoning_engine=ReasoningGraphEngine())


class TestDiscussionClassification:
    def test_supported_question_types(self) -> None:
        ai = _ai()
        assert ai.classify("Why is Officer strong?") == "why"
        assert ai.classify("How does the conclusion form?") == "how"
        assert ai.classify("What evidence supports this?") == "evidence"
        assert ai.classify("Is there an alternative interpretation?") == (
            "alternative_interpretation"
        )
        assert ai.classify("What if birth time changes?") == "what_if_birth_time"
        assert ai.classify("What if Useful God changes?") == "what_if_useful_god"
        assert ai.classify("Tell me a joke") == "unsupported"
        assert set(SUPPORTED_QUESTION_TYPES) == {
            "why",
            "how",
            "evidence",
            "alternative_interpretation",
            "what_if_birth_time",
            "what_if_useful_god",
        }


class TestDiscussionGrounding:
    def test_never_answers_from_raw_chart_alone(self) -> None:
        ai = _ai()
        chart_only = {
            "day_master": "Bính",
            "year_pillar": {"stem": "Canh", "branch": "Ngọ"},
            "day_pillar": {"stem": "Bính", "branch": "Ngọ"},
        }
        refused = ai.ask("Why is this chart strong?", chart=chart_only)
        assert refused.refused is True
        assert refused.refuse_reason == "raw_chart_only"
        assert refused.grounded is False

        refused_context = ai.ask(
            "Why is this chart strong?",
            rule_context=chart_only,
        )
        assert refused_context.refused is True
        assert refused_context.refuse_reason == "raw_chart_only"

    def test_requires_evidence_knowledge_and_reasoning(self) -> None:
        ai = _ai()
        incomplete = ai.ask(
            "Why is Officer favored?",
            rule_context=_officer_context(),
            knowledge=KnowledgeResult(entries=[], metadata={}),
        )
        assert incomplete.refused is True
        assert incomplete.refuse_reason == "incomplete_grounding"
        assert "Knowledge" in incomplete.answer

    def test_grounded_answer_uses_all_three(self) -> None:
        ai = _ai()
        answer = ai.ask(
            "Why is Suitable Career favored?",
            rule_context=_officer_context(),
            knowledge=_knowledge(),
        )
        assert answer.refused is False
        assert answer.grounded is True
        assert answer.used_evidence is True
        assert answer.used_knowledge is True
        assert answer.used_reasoning is True
        assert "[Evidence]" in answer.answer
        assert "[Knowledge]" in answer.answer
        assert "[Reasoning]" in answer.answer
        assert answer.confidence > 0.0


class TestDiscussionConversation:
    def test_full_supported_conversation(self) -> None:
        ai = _ai()
        questions = [
            "Why is the Officer pattern important?",
            "How is the career conclusion formed?",
            "What evidence supports this reading?",
            "Is there an alternative interpretation?",
            "What if birth time changes?",
            "What if Useful God changes?",
        ]
        conversation = ai.converse(
            questions,
            rule_context=_officer_context(),
            knowledge=_knowledge(),
        )
        assert len(conversation.turns) == 6
        assert conversation.all_grounded is True
        assert conversation.metadata["refused_turns"] == 0

        types = [turn.question_type for turn in conversation.turns]
        assert types == [
            "why",
            "how",
            "evidence",
            "alternative_interpretation",
            "what_if_birth_time",
            "what_if_useful_god",
        ]
        for turn in conversation.turns:
            assert turn.used_evidence and turn.used_knowledge and turn.used_reasoning
            assert "[Evidence]" in turn.answer
            assert "[Knowledge]" in turn.answer
            assert "[Reasoning]" in turn.answer

        payload = conversation.to_dict()
        assert payload["all_grounded"] is True
        assert len(payload["turns"]) == 6

    def test_vietnamese_conversation_flow(self) -> None:
        ai = _ai()
        conversation = ai.converse(
            [
                "Tại sao Cách Cục Chính Quan được ưu tiên?",
                "Như thế nào mà ra kết luận sự nghiệp?",
                "Bằng chứng nào đang hỗ trợ?",
                "Có diễn giải khác không?",
                "Nếu giờ sinh thay đổi thì sao?",
                "Nếu Dụng thần thay đổi thì sao?",
            ],
            rule_context=_officer_context(),
            knowledge=_knowledge(),
        )
        assert conversation.all_grounded is True
        assert [turn.question_type for turn in conversation.turns] == list(
            SUPPORTED_QUESTION_TYPES
        )

    def test_mixed_conversation_refuses_unsupported_and_chart_only(self) -> None:
        ai = _ai()
        conversation = ai.converse(
            [
                "Why is Officer strong?",
                "What is the weather today?",
            ],
            rule_context=_officer_context(),
            knowledge=_knowledge(),
        )
        assert conversation.turns[0].grounded is True
        assert conversation.turns[1].refused is True
        assert conversation.turns[1].refuse_reason == "unsupported_question_type"
        assert conversation.all_grounded is True

    def test_answers_pass_response_validator_markers(self) -> None:
        ai = _ai()
        evidence = EvidenceBuilder().build(_officer_context())
        reasoning = ReasoningGraphEngine().build(
            _officer_context(),
            knowledge_result=_knowledge(),
        )
        answer = ai.ask(
            "What evidence supports Suitable Career?",
            rule_context=_officer_context(),
            knowledge=_knowledge(),
            evidence=evidence,
            reasoning=reasoning,
        )
        report = AIResponseValidator().validate(
            answer.answer,
            evidence=evidence,
            knowledge=_knowledge(),
            reasoning=reasoning,
            claimed_confidence=answer.confidence,
        )
        assert report.paragraphs[0].references_all is True
        assert report.checks["missing_evidence"]["passed"] is True

    def test_missing_rule_context_and_empty_question(self) -> None:
        ai = _ai()
        assert ai.classify("") == "unsupported"
        refused = ai.ask("Why is this favored?")
        assert refused.refused is True
        assert refused.refuse_reason == "missing_rule_context"

    def test_alternative_uses_secondary_conclusion(self) -> None:
        from engines.knowledge_engine import ReasoningEdge, ReasoningGraph, ReasoningNode

        ai = _ai()
        evidence = EvidenceBuilder().build(_officer_context())
        reasoning = ReasoningGraph(
            nodes=[
                ReasoningNode("ev:1", "Strong Officer", "evidence"),
                ReasoningNode("cn:1", "Suitable Career", "conclusion"),
                ReasoningNode("cn:2", "Academic Path", "conclusion"),
            ],
            edges=[
                ReasoningEdge("e1", "ev:1", "cn:1", "primary", 80, 0.9, "x"),
                ReasoningEdge("e2", "ev:1", "cn:2", "secondary", 60, 0.7, "x"),
            ],
            conclusions=["Suitable Career", "Academic Path"],
            metadata={},
        )
        answer = ai.ask(
            "Is there an alternative interpretation?",
            rule_context=_officer_context(),
            knowledge=_knowledge(),
            evidence=evidence,
            reasoning=reasoning,
        )
        assert answer.grounded is True
        assert "Academic Path" in answer.answer
        assert answer.to_dict()["question_type"] == "alternative_interpretation"
