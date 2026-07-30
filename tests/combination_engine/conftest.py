"""Fixtures for Combination Engine tests."""

from __future__ import annotations

import pytest

from engines.analysis_engine.combination_engine import (
    CombinationEngine,
    create_default_knowledge_session,
)
from engines.analysis_engine.runtime.models import AnalysisContext, StageResult


def publish_upstream(context: AnalysisContext) -> None:
    """Publish deterministic upstream StageResults required by Combination."""
    context.publish_stage_result(
        StageResult(
            stage_id="strength",
            payload={"classification": "strong", "score": 0.8},
        )
    )
    context.publish_stage_result(
        StageResult(
            stage_id="temperature",
            payload={"classification": "balanced"},
        )
    )
    context.publish_stage_result(
        StageResult(
            stage_id="pattern",
            payload={"pattern_id": "zheng_guan_ge"},
        )
    )
    context.publish_stage_result(
        StageResult(
            stage_id="useful_god",
            payload={"useful_gods": ["zheng_guan"], "favorable": ["zheng_guan"]},
        )
    )
    context.publish_stage_result(
        StageResult(
            stage_id="ten_gods",
            payload={
                "presence": [
                    {
                        "god_id": "zheng_guan",
                        "label": "Zheng Guan",
                        "source_pillar": "year",
                        "source_stem": "Canh",
                        "polarity_class": "officer",
                        "count": 1,
                    }
                ],
                "summary": {"presence_count": 1},
            },
        )
    )


@pytest.fixture
def knowledge_session():
    return create_default_knowledge_session()


@pytest.fixture
def context(knowledge_session) -> AnalysisContext:
    # Giáp-Kỷ stem hop; Tý-Sửu branch hop; Tý-Ngọ clash on year/day.
    ctx = AnalysisContext(
        request_id="comb-req-001",
        chart={
            "day_master": "Giáp",
            "stems": {
                "year": "Giáp",
                "month": "Kỷ",
                "day": "Giáp",
                "hour": "Bính",
            },
            "branches": {
                "year": "Tý",
                "month": "Sửu",
                "day": "Ngọ",
                "hour": "Tuất",
            },
        },
        knowledge_session=knowledge_session,
        knowledge_version="1.0.0",
    )
    publish_upstream(ctx)
    return ctx


@pytest.fixture
def engine() -> CombinationEngine:
    return CombinationEngine()
