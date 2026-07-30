"""Unit tests for ShenSha Engine."""

from __future__ import annotations

import pytest

from engines.analysis_engine.runtime.models import AnalysisContext
from engines.analysis_engine.shensha_engine import (
    ShenShaEngine,
    ShenShaKnowledgeError,
    ShenShaPrerequisiteError,
    ShenShaResult,
    ShenShaValidationError,
    create_default_knowledge_session,
)
from tests.shensha_engine.conftest import publish_upstream


class TestShenShaValidation:
    def test_missing_branches_fails(self, engine: ShenShaEngine) -> None:
        ctx = AnalysisContext(
            request_id="x",
            chart={"day_master": "Giáp", "stems": {"day": "Giáp"}},
            knowledge_session=create_default_knowledge_session(),
        )
        with pytest.raises(ShenShaValidationError):
            engine.evaluate(ctx)

    def test_missing_upstream_fails(
        self,
        engine: ShenShaEngine,
        knowledge_session,
    ) -> None:
        ctx = AnalysisContext(
            request_id="x",
            chart={
                "day_master": "Giáp",
                "stems": {"day": "Giáp"},
                "branches": {"year": "Tý", "month": "Sửu"},
            },
            knowledge_session=knowledge_session,
        )
        with pytest.raises(ShenShaPrerequisiteError) as exc_info:
            engine.evaluate(ctx)
        assert "combination" in str(exc_info.value.details.get("missing"))

    def test_missing_knowledge_session_fails(self, engine: ShenShaEngine) -> None:
        ctx = AnalysisContext(
            request_id="x",
            chart={
                "day_master": "Giáp",
                "stems": {"day": "Giáp"},
                "branches": {"year": "Tý", "month": "Sửu", "day": "Dậu", "hour": "Mão"},
            },
        )
        publish_upstream(ctx)
        with pytest.raises(ShenShaKnowledgeError):
            engine.evaluate(ctx)


class TestShenShaDetection:
    def test_detects_core_shensha(
        self,
        engine: ShenShaEngine,
        context: AnalysisContext,
    ) -> None:
        result = engine.evaluate_shensha(context)
        ids = {item.shensha_id for item in result.presence}
        assert "tianyi_guiren" in ids
        assert "yangren" in ids
        assert "taohua" in ids
        assert any(item.polarity == "auspicious" for item in result.auspicious)
        assert result.confidence.score is not None
        assert result.evidence

    def test_yima_when_branch_present(
        self,
        engine: ShenShaEngine,
        knowledge_session,
    ) -> None:
        ctx = AnalysisContext(
            request_id="yima",
            chart={
                "day_master": "Giáp",
                "stems": {"day": "Giáp"},
                "branches": {
                    "year": "Tý",
                    "month": "Sửu",
                    "day": "Dậu",
                    "hour": "Dần",
                },
            },
            knowledge_session=knowledge_session,
        )
        publish_upstream(ctx)
        result = engine.evaluate_shensha(ctx)
        assert any(item.shensha_id == "yima" for item in result.presence)

    def test_exception_qualifies_taohua_on_clash(
        self,
        engine: ShenShaEngine,
        context: AnalysisContext,
    ) -> None:
        result = engine.evaluate_shensha(context)
        assert any(
            item.shensha_id == "taohua" and item.action == "qualify"
            for item in result.exceptions
        )
        assert any(
            item.shensha_id == "taohua" and item.status == "qualified"
            for item in result.presence
        )

    def test_weak_strength_suppresses_yangren(
        self,
        engine: ShenShaEngine,
        knowledge_session,
    ) -> None:
        ctx = AnalysisContext(
            request_id="weak",
            chart={
                "day_master": "Giáp",
                "stems": {"day": "Giáp"},
                "branches": {
                    "year": "Tý",
                    "month": "Sửu",
                    "day": "Dậu",
                    "hour": "Mão",
                },
            },
            knowledge_session=knowledge_session,
        )
        publish_upstream(ctx, strength_class="weak", clashes=[])
        result = engine.evaluate_shensha(ctx)
        assert any(
            item.shensha_id == "yangren" and item.status == "suppressed"
            for item in result.presence
        )
        assert not any(item.shensha_id == "yangren" for item in result.inauspicious)

    def test_stage_result_roundtrip(
        self,
        engine: ShenShaEngine,
        context: AnalysisContext,
    ) -> None:
        stage = engine.evaluate(context)
        assert stage.stage_id == "shensha"
        rebuilt = ShenShaResult.from_stage_result(stage)
        assert rebuilt.to_dict() == stage.payload


class TestShenShaDeterminism:
    def test_identical_inputs_identical_outputs(
        self,
        engine: ShenShaEngine,
        context: AnalysisContext,
    ) -> None:
        assert (
            engine.evaluate_shensha(context).to_dict()
            == engine.evaluate_shensha(context).to_dict()
        )
