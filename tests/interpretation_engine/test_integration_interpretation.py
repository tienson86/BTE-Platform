"""Integration tests: Interpretation Engine consumes Analysis Runtime output."""

from __future__ import annotations

from engines.analysis_engine.interpretation_engine import (
    InterpretationContext,
    InterpretationEngine,
    InterpretationResult,
    create_default_knowledge_session,
)
from engines.analysis_engine.runtime import AnalysisContext, AnalysisRuntime, StageResult
from engines.analysis_engine.runtime.base_module import BaseAnalysisModule
from engines.analysis_engine.runtime.models import ConfidenceEvaluation, RuleEvidence
from engines.analysis_engine.summary_engine import SummaryEngine


class UpstreamStub(BaseAnalysisModule):
    """Deterministic upstream analytical stub."""

    def __init__(
        self,
        stage_id: str,
        payload: dict,
        *,
        confidence: float = 0.8,
        dependencies: tuple[str, ...] = (),
    ) -> None:
        super().__init__(stage_id=stage_id, dependencies=dependencies)
        self._payload = payload
        self._confidence = confidence

    def evaluate(self, context: AnalysisContext) -> StageResult:
        return StageResult(
            stage_id=self.stage_id,
            module_version=self.version,
            payload=dict(self._payload),
            confidence=ConfidenceEvaluation(
                score=self._confidence,
                level="high",
            ),
            evidence=[
                RuleEvidence(
                    rule_id=f"{self.stage_id}:stub",
                    category=self.stage_id,
                    priority=10,
                    reference="stub",
                )
            ],
        )


def _build_analysis_runtime() -> AnalysisRuntime:
    runtime = AnalysisRuntime(require_all_canonical_stages=False)
    specs: list[tuple[str, dict, float, tuple[str, ...]]] = [
        ("strength", {"classification": "strong"}, 0.9, ()),
        ("temperature", {"classification": "balanced"}, 0.8, ("strength",)),
        ("pattern", {"pattern_id": "zheng_guan_ge"}, 0.85, ("strength", "temperature")),
        (
            "useful_god",
            {"useful_gods": ["zheng_guan"]},
            0.7,
            ("strength", "temperature", "pattern"),
        ),
        (
            "ten_gods",
            {"presence": [{"god_id": "zheng_guan"}]},
            0.88,
            ("strength", "temperature", "pattern", "useful_god"),
        ),
        (
            "combination",
            {"clashes": []},
            0.72,
            ("strength", "temperature", "pattern", "useful_god", "ten_gods"),
        ),
        (
            "shensha",
            {"presence": [{"shensha_id": "tianyi_guiren"}], "auspicious": []},
            0.77,
            (
                "strength",
                "temperature",
                "pattern",
                "useful_god",
                "ten_gods",
                "combination",
            ),
        ),
        (
            "luck",
            {"summary": {"active_count": 4, "current_da_yun_index": 2}},
            0.75,
            (
                "strength",
                "temperature",
                "pattern",
                "useful_god",
                "ten_gods",
                "combination",
                "shensha",
            ),
        ),
    ]
    for stage_id, payload, confidence, deps in specs:
        runtime.register(
            UpstreamStub(
                stage_id,
                payload,
                confidence=confidence,
                dependencies=deps,
            )
        )
    runtime.register(SummaryEngine())
    return runtime


def test_runtime_analysis_then_interpretation() -> None:
    runtime = _build_analysis_runtime()
    analysis_context = AnalysisContext(
        request_id="interp-int-001",
        chart={"day_master": "Giáp"},
    )
    analysis_result = runtime.run(analysis_context)
    assert analysis_result.summary_result is not None

    engine = InterpretationEngine()
    interpretation = engine.interpret(
        InterpretationContext(
            analysis_result=analysis_result,
            chart={"day_master": "Giáp"},
            knowledge_session=create_default_knowledge_session(),
            knowledge_version="1.0.0",
        )
    )
    assert isinstance(interpretation, InterpretationResult)
    assert interpretation.request_id == "interp-int-001"
    assert interpretation.overview
    assert "Giáp" in interpretation.overview
    section_ids = [section.section_id for section in interpretation.sections]
    assert section_ids[0] == "overview"
    assert "strength" in section_ids
    assert "luck" in section_ids


def test_interpretation_deterministic_across_runs() -> None:
    runtime = _build_analysis_runtime()
    engine = InterpretationEngine()
    session = create_default_knowledge_session()

    def once(request_id: str) -> dict:
        analysis = runtime.run(
            AnalysisContext(
                request_id=request_id,
                chart={"day_master": "Giáp"},
            )
        )
        result = engine.interpret(
            InterpretationContext(
                analysis_result=analysis,
                chart={"day_master": "Giáp"},
                knowledge_session=session,
            )
        )
        payload = result.to_dict()
        payload.pop("request_id", None)
        return payload

    assert once("a") == once("b")


def test_interpretation_evidence_traces_sentences() -> None:
    runtime = _build_analysis_runtime()
    analysis = runtime.run(
        AnalysisContext(request_id="interp-int-003", chart={"day_master": "Giáp"})
    )
    result = InterpretationEngine().interpret(
        InterpretationContext(
            analysis_result=analysis,
            chart={"day_master": "Giáp"},
            knowledge_session=create_default_knowledge_session(),
        )
    )
    assert result.evidence
    rule_ids = {item.rule_id for item in result.evidence}
    assert "overview_intro" in rule_ids
    assert "strength_strong" in rule_ids
