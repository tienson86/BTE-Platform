"""Unit tests for Interpretation Engine pipeline components."""

from __future__ import annotations

import pytest

from engines.analysis_engine.interpretation_engine import (
    InterpretationBindingError,
    InterpretationContext,
    InterpretationEngine,
    InterpretationPrerequisiteError,
    InterpretationResult,
    InterpretationValidationError,
    create_default_knowledge_session,
)
from engines.analysis_engine.interpretation_engine.paragraph_builder import (
    ParagraphBuilder,
)
from engines.analysis_engine.interpretation_engine.placeholder_binding import (
    PlaceholderBinder,
    build_placeholder_values,
)
from engines.analysis_engine.interpretation_engine.sentence_selection import (
    SentenceSelector,
)
from engines.analysis_engine.interpretation_engine.template_binding import (
    TemplateBinder,
)
from engines.analysis_engine.runtime.models import (
    AnalysisContext,
    AnalysisResult,
    ExecutionMetadata,
    ExecutionTrace,
    PerformanceMetrics,
)
from tests.interpretation_engine.conftest import build_analysis_result


class TestInterpretationValidation:
    def test_missing_stages_fail(self, engine: InterpretationEngine) -> None:
        ctx = AnalysisContext(request_id="x", chart={"day_master": "Giáp"})
        analysis = AnalysisResult.from_context(
            ctx,
            execution_metadata=ExecutionMetadata(request_id="x", status="success"),
            performance_metrics=PerformanceMetrics(),
            execution_trace=ExecutionTrace(request_id="x"),
        )
        with pytest.raises(InterpretationPrerequisiteError) as exc_info:
            engine.interpret(
                InterpretationContext(
                    analysis_result=analysis,
                    chart={"day_master": "Giáp"},
                    knowledge_session=create_default_knowledge_session(),
                )
            )
        assert "strength" in exc_info.value.details.get("missing", [])

    def test_request_id_required(self, engine: InterpretationEngine) -> None:
        analysis = build_analysis_result(request_id="keep")
        # Force empty request_id after construction.
        context = InterpretationContext(
            analysis_result=analysis,
            chart={"day_master": "Giáp"},
            knowledge_session=create_default_knowledge_session(),
            request_id="keep",
        )
        context.request_id = ""
        with pytest.raises(InterpretationValidationError):
            engine.interpret(context)


class TestSentenceSelection:
    def test_selects_matching_strength_sentence(
        self,
        context: InterpretationContext,
    ) -> None:
        session = context.knowledge_session
        selected = SentenceSelector().select(context, session=session)
        ids = {item.sentence_id for item in selected}
        assert "strength_strong" in ids
        assert "strength_weak" not in ids

    def test_selects_overview_and_recommendations(
        self,
        context: InterpretationContext,
    ) -> None:
        selected = SentenceSelector().select(
            context,
            session=context.knowledge_session,
        )
        sections = {item.section_id for item in selected}
        assert "overview" in sections
        assert "recommendations" in sections


class TestTemplateAndPlaceholderBinding:
    def test_template_binding_resolves_text(
        self,
        context: InterpretationContext,
    ) -> None:
        session = context.knowledge_session
        selected = SentenceSelector().select(context, session=session)
        templates = TemplateBinder().bind(selected, session=session)
        assert all(item.template_text for item in templates)

    def test_placeholder_binding_fills_day_master(
        self,
        context: InterpretationContext,
    ) -> None:
        session = context.knowledge_session
        selected = SentenceSelector().select(context, session=session)
        templates = TemplateBinder().bind(selected, session=session)
        sentences = PlaceholderBinder().bind(templates, context)
        overview = next(s for s in sentences if s.sentence_id == "overview_intro")
        assert "Giáp" in overview.text
        assert "{" not in overview.text

    def test_missing_required_placeholder_fails(
        self,
        engine: InterpretationEngine,
        knowledge_session,
    ) -> None:
        analysis = build_analysis_result()
        context = InterpretationContext(
            analysis_result=analysis,
            chart={},  # missing day_master
            knowledge_session=knowledge_session,
        )
        with pytest.raises(InterpretationBindingError):
            engine.interpret(context)

    def test_build_placeholder_values_includes_luck_summary(
        self,
        context: InterpretationContext,
    ) -> None:
        values = build_placeholder_values(context)
        assert values["active_count"] == "4"
        assert values["current_da_yun_index"] == "2"


class TestParagraphBuilder:
    def test_groups_by_section(self, context: InterpretationContext) -> None:
        session = context.knowledge_session
        selected = SentenceSelector().select(context, session=session)
        templates = TemplateBinder().bind(selected, session=session)
        sentences = PlaceholderBinder().bind(templates, context)
        order = tuple(session.get_asset("interpretation.sections").data["order"])
        paragraphs = ParagraphBuilder().build(sentences, section_order=order)
        assert paragraphs
        assert all(p.text for p in paragraphs)


class TestInterpretationResult:
    def test_interpret_produces_sections(
        self,
        engine: InterpretationEngine,
        context: InterpretationContext,
    ) -> None:
        result = engine.interpret(context)
        assert isinstance(result, InterpretationResult)
        assert result.overview
        section_ids = {s.section_id for s in result.sections}
        assert "overview" in section_ids
        assert "strength" in section_ids
        assert "pattern" in section_ids
        assert "luck" in section_ids
        assert result.confidence.score is not None
        assert result.evidence

    def test_roundtrip_dict(
        self,
        engine: InterpretationEngine,
        context: InterpretationContext,
    ) -> None:
        result = engine.interpret(context)
        rebuilt = InterpretationResult.from_dict(result.to_dict())
        assert rebuilt.to_dict() == result.to_dict()

    def test_does_not_mutate_analysis_result(
        self,
        engine: InterpretationEngine,
        context: InterpretationContext,
    ) -> None:
        before = {
            stage_id: dict(stage.payload)
            for stage_id, stage in context.analysis_result.stage_results.items()
        }
        engine.interpret(context)
        after = {
            stage_id: dict(stage.payload)
            for stage_id, stage in context.analysis_result.stage_results.items()
        }
        assert before == after

    def test_deterministic(
        self,
        engine: InterpretationEngine,
        context: InterpretationContext,
    ) -> None:
        first = engine.interpret(context).to_dict()
        second = engine.interpret(context).to_dict()
        assert first == second

    def test_run_alias(
        self,
        engine: InterpretationEngine,
        context: InterpretationContext,
    ) -> None:
        assert engine.run(context).to_dict() == engine.interpret(context).to_dict()
