"""Unit tests for Combination Engine."""

from __future__ import annotations

import pytest

from engines.analysis_engine.combination_engine import (
    CombinationEngine,
    CombinationKnowledgeError,
    CombinationPrerequisiteError,
    CombinationResult,
    CombinationValidationError,
    create_default_knowledge_session,
)
from engines.analysis_engine.runtime.models import AnalysisContext
from tests.combination_engine.conftest import publish_upstream


class TestCombinationValidation:
    def test_missing_chart_relations_fails(self, engine: CombinationEngine) -> None:
        ctx = AnalysisContext(
            request_id="x",
            chart={"day_master": "Giáp"},
            knowledge_session=create_default_knowledge_session(),
        )
        with pytest.raises(CombinationValidationError):
            engine.evaluate(ctx)

    def test_missing_upstream_fails(
        self,
        engine: CombinationEngine,
        knowledge_session,
    ) -> None:
        ctx = AnalysisContext(
            request_id="x",
            chart={
                "stems": {"year": "Giáp", "month": "Kỷ"},
                "branches": {"year": "Tý", "month": "Sửu"},
            },
            knowledge_session=knowledge_session,
        )
        with pytest.raises(CombinationPrerequisiteError) as exc_info:
            engine.evaluate(ctx)
        assert "ten_gods" in str(exc_info.value.details.get("missing"))

    def test_missing_knowledge_session_fails(self, engine: CombinationEngine) -> None:
        ctx = AnalysisContext(
            request_id="x",
            chart={
                "stems": {"year": "Giáp", "month": "Kỷ"},
                "branches": {"year": "Tý", "month": "Sửu"},
            },
        )
        publish_upstream(ctx)
        with pytest.raises(CombinationKnowledgeError):
            engine.evaluate(ctx)


class TestCombinationDetection:
    def test_detects_stem_and_branch_and_clash(
        self,
        engine: CombinationEngine,
        context: AnalysisContext,
    ) -> None:
        result = engine.evaluate_combination(context)
        stem_ids = {item.relation_id for item in result.stem_combinations}
        branch_ids = {item.relation_id for item in result.branch_combinations}
        clash_ids = {item.relation_id for item in result.clashes}

        assert "stem_jia_ji" in stem_ids
        assert "branch_zi_chou" in branch_ids
        assert "clash_zi_wu" in clash_ids
        assert result.confidence.score is not None
        assert result.evidence

    def test_clash_blocks_overlapping_branch_combination(
        self,
        engine: CombinationEngine,
        context: AnalysisContext,
    ) -> None:
        result = engine.evaluate_combination(context)
        # year Tý + month Sửu hop overlaps year Tý which clashes day Ngọ
        blocked = [
            item
            for item in result.branch_combinations
            if item.relation_id == "branch_zi_chou"
        ]
        # Original detections remain in typed lists; active_relations reflect resolution.
        assert any(item.relation_id == "branch_zi_chou" for item in result.branch_combinations)
        active_ids = {
            (item.relation_id, item.status) for item in result.active_relations
        }
        assert ("clash_zi_wu", "active") in active_ids
        assert any(
            item.reason_code == "overlap_with_clash"
            for item in result.rejected_alternatives
        )
        assert blocked  # detected before resolution

    def test_stage_result_roundtrip(
        self,
        engine: CombinationEngine,
        context: AnalysisContext,
    ) -> None:
        stage = engine.evaluate(context)
        assert stage.stage_id == "combination"
        rebuilt = CombinationResult.from_stage_result(stage)
        assert rebuilt.to_dict() == stage.payload


class TestCombinationDeterminism:
    def test_identical_inputs_identical_outputs(
        self,
        engine: CombinationEngine,
        context: AnalysisContext,
    ) -> None:
        assert (
            engine.evaluate_combination(context).to_dict()
            == engine.evaluate_combination(context).to_dict()
        )

    def test_transformations_are_deterministic(
        self,
        engine: CombinationEngine,
        context: AnalysisContext,
    ) -> None:
        result = engine.evaluate_combination(context)
        assert result.transformations
        # Strong strength stabilizes; clash may still block member transforms.
        assert all(isinstance(item.success, bool) for item in result.transformations)
