"""Unit tests for Ten Gods Engine."""

from __future__ import annotations

import pytest

from engines.analysis_engine.runtime.models import AnalysisContext, StageResult
from engines.analysis_engine.ten_gods_engine import (
    TenGodsEngine,
    TenGodsKnowledgeError,
    TenGodsPrerequisiteError,
    TenGodsResult,
    TenGodsValidationError,
    create_default_knowledge_session,
)
from tests.ten_gods_engine.conftest import publish_upstream


class TestTenGodsValidation:
    def test_missing_day_master_fails(self, engine: TenGodsEngine) -> None:
        ctx = AnalysisContext(
            request_id="x",
            chart={"stems": {}},
            knowledge_session=create_default_knowledge_session(),
        )
        with pytest.raises(TenGodsValidationError):
            engine.evaluate(ctx)

    def test_missing_upstream_fails(
        self,
        engine: TenGodsEngine,
        knowledge_session,
    ) -> None:
        ctx = AnalysisContext(
            request_id="x",
            chart={"day_master": "Giáp", "stems": {"day": "Giáp", "year": "Canh"}},
            knowledge_session=knowledge_session,
        )
        with pytest.raises(TenGodsPrerequisiteError):
            engine.evaluate(ctx)

    def test_missing_knowledge_session_fails(self, engine: TenGodsEngine) -> None:
        ctx = AnalysisContext(
            request_id="x",
            chart={"day_master": "Giáp", "stems": {"day": "Giáp", "year": "Canh"}},
        )
        publish_upstream(ctx)
        with pytest.raises(TenGodsKnowledgeError):
            engine.evaluate(ctx)


class TestTenGodsPresence:
    def test_presence_from_stems(
        self,
        engine: TenGodsEngine,
        context: AnalysisContext,
    ) -> None:
        result = engine.evaluate_ten_gods(context)
        god_ids = {item.god_id for item in result.presence}
        # Giáp day master:
        # year Canh -> controls Mộc? Canh=Kim controls Mộc -> officer class
        # month Bính -> Giáp generates Hỏa -> output class
        # hour Mậu -> Giáp controls Thổ -> wealth class
        assert "zheng_guan" in god_ids or "qi_sha" in god_ids
        assert "shi_shen" in god_ids or "shang_guan" in god_ids
        assert "zheng_cai" in god_ids or "pian_cai" in god_ids
        assert all(item.source_pillar != "day" for item in result.presence)

    def test_stage_result_roundtrip(
        self,
        engine: TenGodsEngine,
        context: AnalysisContext,
    ) -> None:
        stage = engine.evaluate(context)
        assert stage.stage_id == "ten_gods"
        assert stage.status == "success"
        rebuilt = TenGodsResult.from_stage_result(stage)
        assert rebuilt.to_dict() == stage.payload


class TestTenGodsDeterminism:
    def test_identical_inputs_identical_outputs(
        self,
        engine: TenGodsEngine,
        context: AnalysisContext,
    ) -> None:
        first = engine.evaluate_ten_gods(context).to_dict()
        second = engine.evaluate_ten_gods(context).to_dict()
        assert first == second

    def test_fresh_context_same_semantics(
        self,
        engine: TenGodsEngine,
        knowledge_session,
    ) -> None:
        def build() -> AnalysisContext:
            ctx = AnalysisContext(
                request_id="det",
                chart={
                    "day_master": "Giáp",
                    "stems": {
                        "year": "Canh",
                        "month": "Bính",
                        "day": "Giáp",
                        "hour": "Mậu",
                    },
                },
                knowledge_session=knowledge_session,
                knowledge_version="1.0.0",
            )
            publish_upstream(ctx)
            return ctx

        left = engine.evaluate_ten_gods(build()).to_dict()
        right = engine.evaluate_ten_gods(build()).to_dict()
        # Strip request-correlated diagnostics noise if any — payload must match.
        assert left["presence"] == right["presence"]
        assert left["favorability"] == right["favorability"]
        assert left["confidence"] == right["confidence"]
        assert left["relationships"] == right["relationships"]
        assert left["interactions"] == right["interactions"]
        assert left["life_areas"] == right["life_areas"]


class TestTenGodsInteractions:
    def test_strength_and_pattern_interactions_present(
        self,
        engine: TenGodsEngine,
        context: AnalysisContext,
    ) -> None:
        result = engine.evaluate_ten_gods(context)
        dimensions = {item.dimension for item in result.interactions}
        assert "strength" in dimensions
        assert "pattern" in dimensions
        assert "temperature" in dimensions
        assert result.confidence.score is not None
        assert 0.0 <= float(result.confidence.score) <= 1.0
        assert result.evidence
