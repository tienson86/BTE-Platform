"""Integration tests: Interpretation → Report Generator pipeline."""

from __future__ import annotations

from engines.analysis_engine.interpretation_engine import (
    InterpretationContext,
    InterpretationEngine,
    create_default_knowledge_session,
)
from engines.analysis_engine.report_generator import (
    FormatProfile,
    ReportAssemblyContext,
    ReportEngine,
    ReportGenerator,
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
            confidence=ConfidenceEvaluation(score=self._confidence, level="high"),
            evidence=[
                RuleEvidence(
                    rule_id=f"{self.stage_id}:stub",
                    category=self.stage_id,
                    priority=10,
                    reference="stub",
                )
            ],
        )


def _build_runtime() -> AnalysisRuntime:
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
            UpstreamStub(stage_id, payload, confidence=confidence, dependencies=deps)
        )
    runtime.register(SummaryEngine())
    return runtime


def test_end_to_end_analysis_interpretation_report() -> None:
    runtime = _build_runtime()
    analysis = runtime.run(
        AnalysisContext(
            request_id="rpt-int-001",
            chart={"day_master": "Giáp"},
        )
    )
    interpretation = InterpretationEngine().interpret(
        InterpretationContext(
            analysis_result=analysis,
            chart={"day_master": "Giáp"},
            knowledge_session=create_default_knowledge_session(),
        )
    )
    result = ReportGenerator().assemble(
        ReportAssemblyContext(
            interpretation_result=interpretation,
            analysis_result=analysis,
            format_profile=FormatProfile.full_publication(title="E2E Report"),
            request_id="rpt-int-001",
        )
    )
    assert result.html is not None and "Giáp" in result.html.content
    assert result.markdown is not None and "## " in result.markdown.content
    assert result.json is not None and result.json.payload["report"]["overview"]
    assert result.pdf is not None and result.pdf.content.startswith(b"%PDF")
    assert result.structured_report.data_blocks
    assert result.summary["section_count"] >= 1


def test_report_engine_alias() -> None:
    assert ReportEngine is ReportGenerator


def test_report_deterministic_across_pipeline_runs() -> None:
    runtime = _build_runtime()
    report_engine = ReportGenerator()
    interp_engine = InterpretationEngine()
    session = create_default_knowledge_session()

    def once(request_id: str) -> dict:
        analysis = runtime.run(
            AnalysisContext(request_id=request_id, chart={"day_master": "Giáp"})
        )
        interpretation = interp_engine.interpret(
            InterpretationContext(
                analysis_result=analysis,
                chart={"day_master": "Giáp"},
                knowledge_session=session,
            )
        )
        result = report_engine.assemble(
            ReportAssemblyContext(
                interpretation_result=interpretation,
                analysis_result=analysis,
                format_profile=FormatProfile.full_publication(),
            )
        )
        return {
            "html": result.html.content if result.html else None,
            "markdown": result.markdown.content if result.markdown else None,
            "pdf_size": result.pdf.size if result.pdf else None,
            "section_ids": [
                section.section_id for section in result.structured_report.sections
            ],
            "data_block_ids": [
                block.block_id for block in result.structured_report.data_blocks
            ],
            "overview": result.structured_report.overview,
        }

    assert once("a") == once("b")
