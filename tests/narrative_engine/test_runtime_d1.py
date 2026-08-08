"""Tests for PACK_05 Narrative Runtime (Sprint D1) — NarrativeTree only."""

from __future__ import annotations

import pytest

from engines.narrative_engine import NarrativeEngine
from engines.narrative_engine.runtime import (
    ComponentType,
    EvidenceKind,
    NarrativeRuntime,
    NarrativeRuntimeValidationError,
    NarrativeTree,
    NodeStatus,
    RuntimeEvidenceUnit,
    RuntimeInput,
    RuntimeInterpretationRef,
    TreeStatus,
    build_runtime_input,
)


def _rich_input() -> RuntimeInput:
    return RuntimeInput(
        evidence=(
            RuntimeEvidenceUnit("e1", EvidenceKind.IDENTITY, 0.9, "bazi.day_master"),
            RuntimeEvidenceUnit("e2", EvidenceKind.STRENGTH, 0.8, "strength"),
            RuntimeEvidenceUnit("e3", EvidenceKind.EXPLANATION, 0.7, "strength.reasoning"),
            RuntimeEvidenceUnit("e4", EvidenceKind.IMPLICATION, 0.6, "impact"),
            RuntimeEvidenceUnit("e5", EvidenceKind.ACTION, 0.85, "useful_god"),
            RuntimeEvidenceUnit("e6", EvidenceKind.RISK, 0.75, "ky_than"),
            RuntimeEvidenceUnit("e7", EvidenceKind.WEAKNESS, 0.7, "weakness"),
            RuntimeEvidenceUnit("e8", EvidenceKind.GRADE, 0.65, "score.grade"),
        ),
        interpretation_refs=(
            RuntimeInterpretationRef("i1", "summary", "Tổng quan", True, ("tổng quan",)),
            RuntimeInterpretationRef("i2", "reason", "Lý giải", True, ("lý giải",)),
            RuntimeInterpretationRef("i3", "action", "Dụng thần", True, ("dụng thần",)),
            RuntimeInterpretationRef("i4", "warn", "Điểm cần lưu ý", True, ("lưu ý",)),
            RuntimeInterpretationRef("i5", "close", "Kết luận", True, ("kết luận",)),
        ),
        analysis_valid=True,
        interpretation_valid=True,
        run_id="test-rich",
    )


def test_compose_tree_official_order_and_no_prose_fields() -> None:
    tree = NarrativeRuntime().compose_tree(_rich_input())
    assert isinstance(tree, NarrativeTree)
    assert len(tree.nodes) == 7
    assert [node.component_type for node in tree.nodes] == list(ComponentType)
    assert [node.priority for node in tree.nodes] == list(range(7))
    for node in tree.nodes:
        assert not hasattr(node, "text")
        assert not hasattr(node, "paragraphs")
        assert "text" not in node.to_dict()
        assert set(node.to_dict()) == {
            "component_type",
            "evidence_refs",
            "interpretation_refs",
            "confidence",
            "priority",
            "dependencies",
            "status",
        }


def test_rich_input_ready_statuses() -> None:
    tree = NarrativeRuntime().compose_tree(_rich_input())
    assert tree.status in {TreeStatus.COMPLETE, TreeStatus.PARTIAL_INSUFFICIENT}
    assert tree.validation_issues == ()
    observation = tree.node_map()[ComponentType.OBSERVATION]
    assert observation.status == NodeStatus.READY
    assert "e1" in observation.evidence_refs or "e2" in observation.evidence_refs
    recommendation = tree.node_map()[ComponentType.RECOMMENDATION]
    assert recommendation.status == NodeStatus.READY
    assert "e5" in recommendation.evidence_refs


def test_observation_insufficient_cascades_to_reasoning_and_impact() -> None:
    runtime_input = RuntimeInput(
        evidence=(
            RuntimeEvidenceUnit("e5", EvidenceKind.ACTION, 0.9, "action"),
            RuntimeEvidenceUnit("e6", EvidenceKind.RISK, 0.8, "risk"),
        ),
        interpretation_refs=(),
        run_id="cascade",
    )
    tree = NarrativeRuntime().compose_tree(runtime_input)
    nodes = tree.node_map()
    assert nodes[ComponentType.OBSERVATION].status == NodeStatus.INSUFFICIENT_EVIDENCE
    assert nodes[ComponentType.REASONING].status == NodeStatus.INSUFFICIENT_EVIDENCE
    assert nodes[ComponentType.IMPACT].status == NodeStatus.INSUFFICIENT_EVIDENCE
    assert nodes[ComponentType.RECOMMENDATION].status == NodeStatus.READY
    assert nodes[ComponentType.WARNING].status == NodeStatus.READY
    assert tree.status == TreeStatus.PARTIAL_INSUFFICIENT


def test_invalid_analysis_raises() -> None:
    runtime_input = RuntimeInput(analysis_valid=False, run_id="bad")
    with pytest.raises(NarrativeRuntimeValidationError):
        NarrativeRuntime().compose_tree(runtime_input)


def test_invalid_interpretation_raises() -> None:
    runtime_input = RuntimeInput(interpretation_valid=False, run_id="bad-interp")
    with pytest.raises(NarrativeRuntimeValidationError):
        NarrativeRuntime().compose_tree(runtime_input)


def test_empty_evidence_marks_all_insufficient() -> None:
    tree = NarrativeRuntime().compose_tree(RuntimeInput(run_id="empty"))
    assert tree.status == TreeStatus.PARTIAL_INSUFFICIENT
    assert all(node.status == NodeStatus.INSUFFICIENT_EVIDENCE for node in tree.nodes)


def test_build_runtime_input_from_dict_and_engine_wrapper() -> None:
    analysis = {
        "bazi": {"day_master": "Canh"},
        "strength": {"strength_score": 45, "confidence": 0.8, "reasoning": "Nhật chủ được sinh trợ."},
        "pattern": {"cach_cuc": "Chính Ấn", "ky_than": "Thổ"},
        "useful_god": {"useful_god": "Thực Thần", "confidence": 0.77},
        "score": {"grade": "D+", "recommendation": "Nhiều điểm cần cải thiện"},
    }
    interpretation = {
        "sections": [
            {"id": "summary", "title": "Tổng quan", "body": "Bạn có tố chất ổn định."},
            {
                "id": "tech",
                "title": "Rule",
                "body": "Kích hoạt khi Nhật Chủ ở trạng thái cân bằng.",
            },
            {"id": "note", "title": "Điểm cần lưu ý", "body": "Cần lưu ý yếu tố hao."},
        ]
    }
    runtime_input = build_runtime_input(
        analysis=analysis,
        interpretation=interpretation,
        run_id="from-dict",
    )
    assert any(unit.kind == EvidenceKind.IDENTITY for unit in runtime_input.evidence)
    tech = next(ref for ref in runtime_input.interpretation_refs if ref.section_id == "tech")
    assert tech.commercial_ok is False

    tree = NarrativeEngine().compose_tree(
        analysis=analysis,
        interpretation=interpretation,
        run_id="engine-d1",
    )
    assert tree.run_id == "engine-d1"
    assert len(tree.nodes) == 7
    assert tree.status != TreeStatus.INVALID


def test_duplicate_and_empty_evidence_filtered() -> None:
    runtime_input = RuntimeInput(
        evidence=(
            RuntimeEvidenceUnit("", EvidenceKind.IDENTITY, 0.9),
            RuntimeEvidenceUnit("e1", EvidenceKind.IDENTITY, 1.5),
            RuntimeEvidenceUnit("e1", EvidenceKind.IDENTITY, 0.2),
            RuntimeEvidenceUnit("e2", EvidenceKind.ACTION, 0.8),
        ),
        run_id="dedupe",
    )
    tree = NarrativeRuntime().compose_tree(runtime_input)
    observation = tree.node_map()[ComponentType.OBSERVATION]
    assert observation.evidence_refs.count("e1") <= 1
    assert observation.confidence <= 1.0
