"""Fixtures for ShenSha Engine tests."""

from __future__ import annotations

import pytest

from engines.analysis_engine.runtime.models import AnalysisContext, StageResult
from engines.analysis_engine.shensha_engine import (
    ShenShaEngine,
    create_default_knowledge_session,
)


def publish_upstream(
    context: AnalysisContext,
    *,
    strength_class: str = "strong",
    clashes: list | None = None,
) -> None:
    """Publish deterministic upstream StageResults required by ShenSha."""
    context.publish_stage_result(
        StageResult(
            stage_id="strength",
            payload={"classification": strength_class, "score": 0.8},
        )
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
                ]
            },
        )
    )
    context.publish_stage_result(
        StageResult(
            stage_id="combination",
            payload={
                "clashes": clashes
                if clashes is not None
                else [
                    {
                        "relation_type": "clash",
                        "relation_id": "clash_zi_wu",
                        "members": ["Tý", "Ngọ"],
                        "pillars": ["year", "day"],
                        "status": "active",
                    }
                ],
                "summary": {"active_count": 1},
            },
        )
    )


@pytest.fixture
def knowledge_session():
    return create_default_knowledge_session()


@pytest.fixture
def context(knowledge_session) -> AnalysisContext:
    # Giáp: TianYi at Sửu/Mùi, YangRen at Mão
    # Year Tý: TaoHua at Dậu, YiMa at Dần
    ctx = AnalysisContext(
        request_id="ss-req-001",
        chart={
            "day_master": "Giáp",
            "stems": {
                "year": "Canh",
                "month": "Bính",
                "day": "Giáp",
                "hour": "Mậu",
            },
            "branches": {
                "year": "Tý",
                "month": "Sửu",
                "day": "Dậu",
                "hour": "Mão",
            },
        },
        knowledge_session=knowledge_session,
        knowledge_version="1.0.0",
    )
    publish_upstream(ctx)
    return ctx


@pytest.fixture
def engine() -> ShenShaEngine:
    return ShenShaEngine()
