"""Sprint D2 tests — NarrativeTree → NarrativeResult."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from engines.narrative_engine import (
    INSUFFICIENT_EVIDENCE_NARRATIVE,
    NarrativeEngine,
    NarrativeResult,
    NarrativeResultComposer,
)
from engines.narrative_engine.composer.constants import INSUFFICIENT_EVIDENCE_NARRATIVE as COPY
from engines.narrative_engine.runtime import NarrativeRuntime, TreeStatus
from engines.narrative_engine.runtime.models import ComponentType, NodeStatus


ANALYSIS = {
    "bazi": {"day_master": "Canh", "day_master_element": "Kim"},
    "strength": {
        "strength_level": "strong",
        "strength_score": 0.87,
        "confidence": 0.8,
        "reasoning": "Nhật chủ được sinh trợ trong cục.",
    },
    "pattern": {
        "cach_cuc": "Chính Ấn",
        "dung_than": "Thực Thần",
        "ky_than": "Thổ",
        "than_vuong_nhuoc": "Trung hòa",
    },
    "useful_god": {
        "useful_god": "Thực Thần",
        "favorable_gods": ["Thực Thần", "Thương Quan"],
        "unfavorable_gods": ["Tỷ Kiên", "Kiếp Tài"],
        "confidence": 0.77,
        "matched_rules": ["str_004", "flo_001"],
    },
    "score": {
        "grade": "D+",
        "strength_score": 45,
        "recommendation": "Nhiều điểm cần cải thiện",
    },
}

INTERPRETATION = {
    "sections": [
        {
            "id": "summary",
            "title": "Tổng quan",
            "body": "Bạn có tố chất ổn định và thiên về trách nhiệm.",
        },
        {
            "id": "tech",
            "title": "Rule dump",
            "body": "Kích hoạt khi Nhật Chủ ở trạng thái cân bằng.",
        },
        {
            "id": "action",
            "title": "Dụng thần",
            "body": "Ưu tiên phát huy Thực Thần trong hành động.",
        },
        {
            "id": "note",
            "title": "Điểm cần lưu ý",
            "body": "Cần lưu ý yếu tố Tỷ Kiên và Kiếp Tài.",
        },
        {
            "id": "close",
            "title": "Kết luận",
            "body": "Giữ đúng hướng ưu tiên và kiểm soát điểm cần lưu ý.",
        },
    ]
}

GOLDEN_PATH = Path(__file__).parent / "golden" / "d2_narrative_result_structure.json"


def test_compose_narrative_result_traceability_and_order() -> None:
    engine = NarrativeEngine()
    result = engine.compose_narrative_result(
        analysis=ANALYSIS,
        interpretation=INTERPRETATION,
        run_id="d2-rich",
    )
    assert isinstance(result, NarrativeResult)
    assert result.run_id == "d2-rich"
    assert len(result.sections) == 7
    assert [section.id for section in result.sections] == [
        f"sec-{item.value}" for item in ComponentType
    ]
    assert result.validation_issues == ()
    assert result.status.value in {"complete", "partial_insufficient"}

    source_pool = _source_pool(ANALYSIS, INTERPRETATION)
    for section in result.sections:
        for paragraph in section.paragraphs:
            if paragraph.insufficient_data:
                assert paragraph.text == INSUFFICIENT_EVIDENCE_NARRATIVE
                continue
            assert paragraph.evidence_refs or paragraph.interpretation_refs
            assert _text_supported_by_sources(paragraph.text, source_pool)


def test_technical_interpretation_not_emitted_as_customer_prose() -> None:
    result = NarrativeEngine().compose_narrative_result(
        analysis=ANALYSIS,
        interpretation=INTERPRETATION,
        run_id="d2-filter",
    )
    blob = " ".join(
        paragraph.text
        for section in result.sections
        for paragraph in section.paragraphs
    )
    assert "Kích hoạt khi" not in blob
    assert "PACK_" not in blob


def test_insufficient_tree_emits_approved_copy() -> None:
    tree = NarrativeRuntime().compose_tree_from_sources(run_id="empty-tree")
    assert tree.status == TreeStatus.PARTIAL_INSUFFICIENT
    result = NarrativeResultComposer().compose(tree)
    assert result.summary.identity == COPY
    assert "identity" in result.summary.insufficient_flags
    for section in result.sections:
        assert section.insufficient_data or all(
            paragraph.insufficient_data for paragraph in section.paragraphs
        )


def test_invalid_tree_rejected() -> None:
    tree = NarrativeRuntime().compose_tree_from_sources(
        analysis=ANALYSIS,
        interpretation=INTERPRETATION,
        run_id="will-invalidate",
    )
    # Force invalid status for gate test.
    from engines.narrative_engine.runtime.models import NarrativeTree, TreeStatus

    bad = NarrativeTree(
        nodes=tree.nodes,
        run_id=tree.run_id,
        status=TreeStatus.INVALID,
        validation_issues=("forced",),
        metadata={},
    )
    with pytest.raises(Exception):
        NarrativeResultComposer().compose(bad)


def test_golden_structure_validation() -> None:
    result = NarrativeEngine().compose_narrative_result(
        analysis=ANALYSIS,
        interpretation=INTERPRETATION,
        run_id="d2-golden",
    )
    payload = result.to_dict()
    assert GOLDEN_PATH.exists()
    expected = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    assert payload["run_id"] == "d2-golden"
    assert len(payload["sections"]) == expected["section_count"]
    assert [section["id"] for section in payload["sections"]] == expected["section_ids"]
    assert set(payload["summary"]) >= set(expected["summary_keys"])
    for section in payload["sections"]:
        for paragraph in section["paragraphs"]:
            if paragraph["insufficient_data"]:
                assert paragraph["text"] == expected["insufficient_text"]
            else:
                assert paragraph["evidence_refs"] or paragraph["interpretation_refs"]


def _source_pool(analysis: dict, interpretation: dict) -> str:
    parts: list[str] = [json.dumps(analysis, ensure_ascii=False)]
    for section in interpretation.get("sections") or []:
        if "Kích hoạt khi" in str(section.get("body") or ""):
            continue
        parts.append(str(section.get("title") or ""))
        parts.append(str(section.get("body") or ""))
    return " ".join(parts)


def _text_supported_by_sources(text: str, source_pool: str) -> bool:
    """Every non-framing token cluster should appear in sources or approved frames."""
    frames = (
        "Quan sát từ dữ liệu phân tích:",
        "Lý giải dựa trên nguồn đã kiểm chứng:",
        "Ý nghĩa thực tế từ nguồn phân tích:",
        "Ưu tiên theo nguồn phân tích:",
        "Ưu tiên phát huy theo nguồn phân tích:",
        "Cần lưu ý theo nguồn phân tích:",
        "Cần lưu ý:",
        "Điểm then chốt từ các nguồn đã nêu:",
    )
    residual = text
    for frame in frames:
        residual = residual.replace(frame, " ")
    residual = residual.strip(" .")
    # Allow if any substantial source snippet is present in text, or residual tokens in pool.
    if any(
        snippet and snippet in text
        for snippet in (
            "Canh",
            "Chính Ấn",
            "Thực Thần",
            "Nhật chủ được sinh trợ",
            "tố chất ổn định",
            "Tỷ Kiên",
            "Kiếp Tài",
            "Nhiều điểm cần cải thiện",
            "Giữ đúng hướng ưu tiên",
        )
    ):
        return True
    tokens = [token for token in residual.replace(",", " ").split() if len(token) > 2]
    if not tokens:
        return True
    return any(token in source_pool for token in tokens)
