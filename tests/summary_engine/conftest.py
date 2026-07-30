"""Fixtures for Summary Engine tests."""

from __future__ import annotations

import pytest

from engines.analysis_engine.runtime.models import (
    AnalysisContext,
    ConfidenceEvaluation,
    RuleEvidence,
    StageResult,
)
from engines.analysis_engine.summary_engine import SummaryEngine
from engines.analysis_engine.summary_engine.models import UPSTREAM_STAGES


def make_upstream_result(
    stage_id: str,
    *,
    payload: dict | None = None,
    confidence: float = 0.8,
    with_evidence: bool = True,
) -> StageResult:
    """Build a deterministic upstream StageResult."""
    base_payload = payload or {"classification": stage_id, "summary": {"ok": True}}
    evidence = []
    if with_evidence:
        evidence = [
            RuleEvidence(
                rule_id=f"{stage_id}:rule",
                category=stage_id,
                priority=50,
                reference=f"{stage_id}_knowledge",
            )
        ]
    return StageResult(
        stage_id=stage_id,
        status="success",
        module_version="1.0.0",
        payload=base_payload,
        confidence=ConfidenceEvaluation(score=confidence, level="high"),
        evidence=evidence,
    )


def publish_all_upstream(context: AnalysisContext) -> None:
    """Publish all eight mandatory upstream results."""
    payloads = {
        "strength": {"classification": "strong"},
        "temperature": {"classification": "balanced"},
        "pattern": {"pattern_id": "zheng_guan_ge"},
        "useful_god": {"useful_gods": ["zheng_guan"], "favorable": ["zheng_guan"]},
        "ten_gods": {"presence": [{"god_id": "zheng_guan"}], "summary": {"n": 1}},
        "combination": {"clashes": [{"relation_id": "clash_zi_wu"}], "summary": {}},
        "shensha": {
            "auspicious": [{"shensha_id": "tianyi_guiren"}],
            "inauspicious": [],
            "presence": [{"shensha_id": "tianyi_guiren"}],
        },
        "luck": {
            "summary": {"active_count": 5, "current_da_yun_index": 3},
            "confidence": {"score": 0.75, "level": "medium"},
        },
    }
    scores = {
        "strength": 0.90,
        "temperature": 0.80,
        "pattern": 0.85,
        "useful_god": 0.70,
        "ten_gods": 0.88,
        "combination": 0.72,
        "shensha": 0.77,
        "luck": 0.75,
    }
    for stage_id in UPSTREAM_STAGES:
        context.publish_stage_result(
            make_upstream_result(
                stage_id,
                payload=payloads[stage_id],
                confidence=scores[stage_id],
            )
        )


@pytest.fixture
def context() -> AnalysisContext:
    ctx = AnalysisContext(
        request_id="sum-req-001",
        chart={"day_master": "Giáp"},
        metadata={"source": "summary-test"},
    )
    publish_all_upstream(ctx)
    return ctx


@pytest.fixture
def engine() -> SummaryEngine:
    return SummaryEngine()
