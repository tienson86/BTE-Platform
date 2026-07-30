"""Fixtures for Ten Gods Engine tests."""

from __future__ import annotations

import pytest

from engines.analysis_engine.runtime.models import AnalysisContext, StageResult
from engines.analysis_engine.ten_gods_engine import (
    TenGodsEngine,
    create_default_knowledge_session,
)


def publish_upstream(context: AnalysisContext) -> None:
    """Publish deterministic upstream StageResults required by Ten Gods."""
    context.publish_stage_result(
        StageResult(
            stage_id="strength",
            payload={"classification": "strong", "score": 0.82},
        )
    )
    context.publish_stage_result(
        StageResult(
            stage_id="temperature",
            payload={"classification": "cold", "balance": "need_warm"},
        )
    )
    context.publish_stage_result(
        StageResult(
            stage_id="pattern",
            payload={"pattern_id": "zheng_guan_ge", "name": "Zheng Guan Ge"},
        )
    )
    context.publish_stage_result(
        StageResult(
            stage_id="useful_god",
            payload={
                "useful_gods": ["zheng_guan", "shi_shen"],
                "favorable": ["zheng_guan", "shi_shen"],
                "unfavorable": ["shang_guan"],
            },
        )
    )


@pytest.fixture
def knowledge_session():
    return create_default_knowledge_session()


@pytest.fixture
def context(knowledge_session) -> AnalysisContext:
    ctx = AnalysisContext(
        request_id="tg-req-001",
        chart={
            "day_master": "Giáp",
            "stems": {
                "year": "Canh",
                "month": "Bính",
                "day": "Giáp",
                "hour": "Mậu",
            },
        },
        calendar={"solar_term": "立春"},
        metadata={"source": "ten-gods-test"},
        knowledge_session=knowledge_session,
        knowledge_version="1.0.0",
    )
    publish_upstream(ctx)
    return ctx


@pytest.fixture
def engine() -> TenGodsEngine:
    return TenGodsEngine()
