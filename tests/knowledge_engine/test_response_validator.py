"""Unit tests for AI Response Validator (Epic 03 Milestone 07)."""

from __future__ import annotations

from engines.knowledge_engine import (
    VALIDATION_CHECKS,
    AIResponseValidator,
    EvidenceItem,
    EvidencePackage,
    KnowledgeHit,
    KnowledgeRecord,
    KnowledgeResult,
    ReasoningEdge,
    ReasoningGraph,
    ReasoningNode,
    ValidationReport,
)


def _support_packages() -> tuple[EvidencePackage, KnowledgeResult, ReasoningGraph]:
    evidence = EvidencePackage(
        items=[
            EvidenceItem(
                category="strength",
                rule="level=strong",
                reason="Day Master is strong and rooted",
                confidence=0.9,
                source="rule_context:strength.level",
            ),
            EvidenceItem(
                category="ten_gods",
                rule="present=Chính Quan",
                reason="Officer star is present",
                confidence=0.88,
                source="rule_context:ten_gods.items",
            ),
        ],
        categories={},
        metadata={},
    )
    knowledge = KnowledgeResult(
        entries=[
            KnowledgeHit(
                record=KnowledgeRecord(
                    id="TG-1",
                    topic="Ten Gods",
                    keyword="Chính Quan; Officer",
                    condition="",
                    classical_text="Chính Quan chủ quyền uy và trách nhiệm.",
                    modern_interpretation="Officer indicates authority and duty.",
                    priority=90,
                    confidence=0.9,
                    reference="Cổ thư",
                    source_file="03_ten_gods.csv",
                ),
                keyword_score=1.0,
                condition_score=1.0,
                relevance_score=0.95,
            )
        ],
        metadata={},
    )
    reasoning = ReasoningGraph(
        nodes=[
            ReasoningNode("ev:1", "Strong Officer", "evidence", "career"),
            ReasoningNode("cn:1", "Suitable Career", "conclusion", "career"),
        ],
        edges=[
            ReasoningEdge(
                "edge:1",
                "ev:1",
                "cn:1",
                "Officer star supports management potential",
                80,
                0.86,
                "rule:x",
            )
        ],
        conclusions=["Suitable Career"],
        metadata={},
    )
    return evidence, knowledge, reasoning


def _grounded_paragraph() -> str:
    return (
        "[Evidence] Day Master is strong with Chính Quan present. "
        "[Knowledge] Classical texts link Officer to authority and duty. "
        "[Reasoning] Therefore Suitable Career in management is favored."
    )


class TestAIResponseValidator:
    def test_grounded_response_passes(self) -> None:
        evidence, knowledge, reasoning = _support_packages()
        report = AIResponseValidator().validate(
            _grounded_paragraph(),
            evidence=evidence,
            knowledge=knowledge,
            reasoning=reasoning,
            claimed_confidence=0.88,
        )
        assert isinstance(report, ValidationReport)
        assert report.passed is True
        assert report.confidence >= 0.7
        assert report.paragraphs[0].references_all is True
        for code in VALIDATION_CHECKS:
            assert code in report.checks
            assert report.checks[code]["passed"] is True

    def test_missing_evidence_references(self) -> None:
        evidence, knowledge, reasoning = _support_packages()
        report = AIResponseValidator().validate(
            "Day Master looks strong and career is good.",
            evidence=evidence,
            knowledge=knowledge,
            reasoning=reasoning,
        )
        assert report.checks["missing_evidence"]["passed"] is False
        assert report.warnings_for("missing_evidence")
        assert report.paragraphs[0].references_all is False
        assert report.passed is False

    def test_each_paragraph_requires_all_three_refs(self) -> None:
        evidence, knowledge, reasoning = _support_packages()
        text = (
            _grounded_paragraph()
            + "\n\n"
            + "[Evidence] Officer is present but knowledge and reasoning missing."
        )
        report = AIResponseValidator().validate(
            text,
            evidence=evidence,
            knowledge=knowledge,
            reasoning=reasoning,
        )
        assert len(report.paragraphs) == 2
        assert report.paragraphs[0].references_all is True
        assert report.paragraphs[1].references_all is False
        assert any(
            row.paragraph_index == 1 for row in report.warnings_for("missing_evidence")
        )

    def test_contradiction_strong_vs_weak(self) -> None:
        evidence, knowledge, reasoning = _support_packages()
        text = (
            "[Evidence] Chart is weak. "
            "[Knowledge] Officer texts still apply. "
            "[Reasoning] Career path remains Suitable Career."
        )
        report = AIResponseValidator().validate(
            text,
            evidence=evidence,
            knowledge=knowledge,
            reasoning=reasoning,
        )
        assert report.checks["contradiction"]["passed"] is False
        assert report.warnings_for("contradiction")

    def test_contradicted_conclusion(self) -> None:
        evidence, knowledge, reasoning = _support_packages()
        text = (
            "[Evidence] Officer is present and Day Master is strong. "
            "[Knowledge] Classical Officer meaning is authority. "
            "[Reasoning] This is not Suitable Career for management."
        )
        report = AIResponseValidator().validate(
            text,
            evidence=evidence,
            knowledge=knowledge,
            reasoning=reasoning,
        )
        messages = " ".join(row.message for row in report.warnings_for("contradiction"))
        assert "Suitable Career" in messages

    def test_unsupported_claims(self) -> None:
        evidence, knowledge, reasoning = _support_packages()
        text = (
            "[Evidence] [Knowledge] [Reasoning] "
            "Quantum tarot jupiter zodiac predicts lottery wealth forever."
        )
        report = AIResponseValidator(min_support_overlap=0.3).validate(
            text,
            evidence=evidence,
            knowledge=knowledge,
            reasoning=reasoning,
        )
        assert report.checks["unsupported_claims"]["passed"] is False
        assert report.warnings_for("unsupported_claims")

    def test_unsupported_without_corpus(self) -> None:
        report = AIResponseValidator().validate(
            "[Evidence] [Knowledge] [Reasoning] Day Master is strong."
        )
        assert report.warnings_for("unsupported_claims")

    def test_hallucination_risk_absolute_without_support(self) -> None:
        report = AIResponseValidator().validate(
            "[Evidence] [Knowledge] [Reasoning] This is definitely always true."
        )
        assert report.checks["hallucination_risk"]["passed"] is False
        assert report.warnings_for("hallucination_risk")

    def test_hallucination_risk_foreign_terms(self) -> None:
        evidence, knowledge, reasoning = _support_packages()
        text = (
            "[Evidence] [Knowledge] [Reasoning] "
            "Definitely quantum-tarot and jupiter-mars guarantee Suitable Career."
        )
        report = AIResponseValidator().validate(
            text,
            evidence=evidence,
            knowledge=knowledge,
            reasoning=reasoning,
        )
        assert report.warnings_for("hallucination_risk")

    def test_confidence_mismatch(self) -> None:
        evidence, knowledge, reasoning = _support_packages()
        report = AIResponseValidator(confidence_tolerance=0.1).validate(
            _grounded_paragraph() + " confidence: 0.20",
            evidence=evidence,
            knowledge=knowledge,
            reasoning=reasoning,
        )
        assert report.checks["confidence_mismatch"]["passed"] is False
        mismatch = report.warnings_for("confidence_mismatch")
        assert mismatch
        assert "claimed_confidence" in mismatch[0].detail

    def test_claimed_confidence_argument(self) -> None:
        evidence, knowledge, reasoning = _support_packages()
        report = AIResponseValidator(confidence_tolerance=0.05).validate(
            _grounded_paragraph(),
            evidence=evidence,
            knowledge=knowledge,
            reasoning=reasoning,
            claimed_confidence=0.1,
        )
        assert report.warnings_for("confidence_mismatch")

    def test_empty_response(self) -> None:
        report = AIResponseValidator().validate("")
        assert report.paragraphs == []
        assert report.confidence < 0.7
        assert report.passed is False

    def test_mapping_inputs_and_to_dict(self) -> None:
        report = AIResponseValidator().validate(
            _grounded_paragraph(),
            evidence={
                "items": [
                    {
                        "category": "strength",
                        "rule": "level=strong",
                        "reason": "Day Master strong",
                        "confidence": 0.9,
                        "source": "x",
                    }
                ]
            },
            knowledge={
                "entries": [
                    {
                        "id": "TG-1",
                        "topic": "Ten Gods",
                        "keyword": "Chính Quan Officer",
                        "condition": "",
                        "classical_text": "Chính Quan chủ quyền uy",
                        "modern_interpretation": "authority duty",
                        "priority": 1,
                        "confidence": 0.9,
                        "reference": "book",
                        "source_file": "x.csv",
                    }
                ]
            },
            reasoning={
                "nodes": [
                    {"id": "ev:1", "label": "Strong Officer", "kind": "evidence"},
                    {"id": "cn:1", "label": "Suitable Career", "kind": "conclusion"},
                ],
                "edges": [
                    {
                        "id": "e1",
                        "source_id": "ev:1",
                        "target_id": "cn:1",
                        "reason": "Officer supports management",
                        "priority": 1,
                        "confidence": 0.8,
                        "source": "x",
                    }
                ],
                "conclusions": ["Suitable Career"],
                "metadata": {},
            },
            claimed_confidence=0.85,
        )
        payload = report.to_dict()
        assert payload["confidence"] == report.confidence
        assert "warnings" in payload
        assert payload["paragraphs"][0]["references_all"] is True

    def test_vietnamese_reference_markers(self) -> None:
        evidence, knowledge, reasoning = _support_packages()
        text = (
            "Theo bằng chứng Day Master strong với Chính Quan. "
            "Theo tri thức cổ điển Officer chỉ authority. "
            "Theo lập luận Suitable Career là hướng phù hợp."
        )
        report = AIResponseValidator().validate(
            text,
            evidence=evidence,
            knowledge=knowledge,
            reasoning=reasoning,
            claimed_confidence=0.85,
        )
        assert report.paragraphs[0].references_all is True
