"""Unit tests for Analysis Luck Engine."""

from __future__ import annotations

import pytest

from engines.analysis_engine.luck_engine import (
    LuckEngine,
    LuckKnowledgeError,
    LuckPrerequisiteError,
    LuckResult,
    LuckValidationError,
    create_default_knowledge_session,
)
from engines.analysis_engine.runtime.models import AnalysisContext
from tests.analysis_luck_engine.conftest import publish_upstream, sample_luck_block


class TestLuckValidation:
    def test_missing_luck_block_fails(self, engine: LuckEngine) -> None:
        ctx = AnalysisContext(
            request_id="x",
            chart={"day_master": "Giáp"},
            knowledge_session=create_default_knowledge_session(),
        )
        with pytest.raises(LuckValidationError):
            engine.evaluate(ctx)

    def test_missing_upstream_fails(
        self,
        engine: LuckEngine,
        knowledge_session,
    ) -> None:
        ctx = AnalysisContext(
            request_id="x",
            chart={"day_master": "Giáp", "luck": sample_luck_block()},
            knowledge_session=knowledge_session,
        )
        with pytest.raises(LuckPrerequisiteError) as exc_info:
            engine.evaluate(ctx)
        assert "shensha" in str(exc_info.value.details.get("missing"))

    def test_missing_knowledge_session_fails(self, engine: LuckEngine) -> None:
        ctx = AnalysisContext(
            request_id="x",
            chart={"day_master": "Giáp", "luck": sample_luck_block()},
        )
        publish_upstream(ctx)
        with pytest.raises(LuckKnowledgeError):
            engine.evaluate(ctx)


class TestLuckLayers:
    def test_evaluates_all_five_layers(
        self,
        engine: LuckEngine,
        context: AnalysisContext,
    ) -> None:
        result = engine.evaluate_luck(context)
        assert len(result.da_yun) == 4
        assert len(result.liu_nian) == 1
        assert len(result.liu_yue) == 1
        assert len(result.liu_ri) == 1
        assert len(result.liu_shi) == 1
        assert result.summary["current_da_yun_index"] == 3
        assert any(item.status == "active" for item in result.da_yun)
        assert all(item.status == "active" for item in result.liu_nian)
        assert result.confidence.score is not None
        assert result.evidence

    def test_inactive_parent_blocks_children(
        self,
        engine: LuckEngine,
        knowledge_session,
    ) -> None:
        luck = sample_luck_block()
        luck["current_age"] = 99  # outside all da yun ranges
        ctx = AnalysisContext(
            request_id="blocked",
            chart={"day_master": "Giáp", "luck": luck},
            knowledge_session=knowledge_session,
        )
        publish_upstream(ctx)
        result = engine.evaluate_luck(ctx)
        assert all(item.status == "inactive" for item in result.da_yun)
        assert all(item.status == "blocked" for item in result.liu_nian)
        assert all(item.status == "blocked" for item in result.liu_shi)

    def test_useful_god_overlap_marks_favorable(
        self,
        engine: LuckEngine,
        context: AnalysisContext,
    ) -> None:
        result = engine.evaluate_luck(context)
        active_dy = next(item for item in result.da_yun if item.status == "active")
        assert active_dy.pillar.stem == "Kỷ"
        assert active_dy.favorability == "favorable"
        assert "useful_god_overlap" in active_dy.reason_codes

    def test_stage_result_roundtrip(
        self,
        engine: LuckEngine,
        context: AnalysisContext,
    ) -> None:
        stage = engine.evaluate(context)
        assert stage.stage_id == "luck"
        rebuilt = LuckResult.from_stage_result(stage)
        assert rebuilt.to_dict() == stage.payload


class TestLuckDeterminism:
    def test_identical_inputs_identical_outputs(
        self,
        engine: LuckEngine,
        context: AnalysisContext,
    ) -> None:
        assert (
            engine.evaluate_luck(context).to_dict()
            == engine.evaluate_luck(context).to_dict()
        )
