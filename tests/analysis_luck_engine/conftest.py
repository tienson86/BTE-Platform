"""Fixtures for Analysis Luck Engine tests."""

from __future__ import annotations

import pytest

from engines.analysis_engine.luck_engine import (
    LuckEngine,
    create_default_knowledge_session,
)
from engines.analysis_engine.runtime.models import AnalysisContext, StageResult


def sample_luck_block() -> dict:
    """Deterministic luck timeline for tests."""
    return {
        "current_age": 35,
        "da_yun_sequence": [
            {
                "index": 0,
                "stem": "Bính",
                "branch": "Dần",
                "start_age": 4,
                "end_age": 13,
                "label": "dy0",
            },
            {
                "index": 1,
                "stem": "Đinh",
                "branch": "Mão",
                "start_age": 14,
                "end_age": 23,
                "label": "dy1",
            },
            {
                "index": 2,
                "stem": "Mậu",
                "branch": "Thìn",
                "start_age": 24,
                "end_age": 33,
                "label": "dy2",
            },
            {
                "index": 3,
                "stem": "Kỷ",
                "branch": "Tỵ",
                "start_age": 34,
                "end_age": 43,
                "label": "dy3",
            },
        ],
        "liu_nian": {"stem": "Giáp", "branch": "Thìn", "year": 2024, "label": "ln"},
        "liu_yue": {"stem": "Bính", "branch": "Dần", "month": 2, "label": "ly"},
        "liu_ri": {"stem": "Mậu", "branch": "Ngọ", "day": 10, "label": "lr"},
        "liu_shi": {"stem": "Nhâm", "branch": "Tý", "hour": 1, "label": "ls"},
    }


def publish_upstream(context: AnalysisContext) -> None:
    """Publish deterministic upstream StageResults required by Luck."""
    context.publish_stage_result(
        StageResult(stage_id="strength", payload={"classification": "strong"})
    )
    context.publish_stage_result(
        StageResult(stage_id="temperature", payload={"classification": "balanced"})
    )
    context.publish_stage_result(
        StageResult(stage_id="pattern", payload={"pattern_id": "zheng_guan_ge"})
    )
    context.publish_stage_result(
        StageResult(
            stage_id="useful_god",
            payload={
                "useful_gods": ["Kỷ", "Tỵ", "Thổ"],
                "favorable": ["Kỷ", "Tỵ", "Thổ"],
            },
        )
    )
    context.publish_stage_result(
        StageResult(
            stage_id="ten_gods",
            payload={"presence": [{"god_id": "zheng_guan"}]},
        )
    )
    context.publish_stage_result(
        StageResult(
            stage_id="combination",
            payload={"clashes": [{"relation_id": "clash_zi_wu"}]},
        )
    )
    context.publish_stage_result(
        StageResult(
            stage_id="shensha",
            payload={
                "presence": [{"shensha_id": "yangren"}],
                "inauspicious": [{"shensha_id": "yangren"}],
            },
        )
    )


@pytest.fixture
def knowledge_session():
    return create_default_knowledge_session()


@pytest.fixture
def context(knowledge_session) -> AnalysisContext:
    ctx = AnalysisContext(
        request_id="luck-req-001",
        chart={
            "day_master": "Giáp",
            "stems": {"day": "Giáp"},
            "branches": {"year": "Tý", "day": "Ngọ"},
            "luck": sample_luck_block(),
        },
        knowledge_session=knowledge_session,
        knowledge_version="1.0.0",
    )
    publish_upstream(ctx)
    return ctx


@pytest.fixture
def engine() -> LuckEngine:
    return LuckEngine()
