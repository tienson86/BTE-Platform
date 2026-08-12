"""Production End-to-End Orchestrator — generic composition pipeline."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from engines.interpretation_engine_v2 import StrengthInterpretationService
from engines.report_engine.adapters.report_input_v1_adapter import build_report_input_v1
from engines.report_engine.contracts.report_input_v1 import (
    ReportInterpretationSectionV1,
    ReportInterpretationV1,
)
from engines.report_engine.services.report_export_service_v1 import ReportExportServiceV1

from applications.production.customer_projection import assert_no_internal_keys
from applications.production.engine_runner import EnginePipelineOutput, ProductionEngineRunner
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.interpretation.contracts import DomainStatus
from applications.production.interpretation.service import MultiDomainInterpretationService
from applications.production.knowledge_diagnostics import build_knowledge_diagnostics
from applications.production.luck_internal import extract_internal_dayun_sequence
from applications.production.models import (
    CustomerDeliverable,
    EXECUTIVE_CONSULTING_NOT_AVAILABLE,
    ProductionPipelineResult,
    ProductionRequest,
    SectionAvailability,
    SectionStatus,
)

logger = logging.getLogger(__name__)


def _map_domain_status(status: DomainStatus) -> SectionStatus:
    if status == DomainStatus.AVAILABLE:
        return SectionStatus.AVAILABLE
    if status == DomainStatus.PARTIAL:
        return SectionStatus.PARTIAL
    return SectionStatus.NOT_AVAILABLE


class ProductionEndToEndOrchestrator:
    """One orchestrator: engines → multi-domain composition → report → PDF."""

    def __init__(
        self,
        *,
        engine_runner: ProductionEngineRunner | None = None,
        strength_service: StrengthInterpretationService | None = None,
        composition_service: MultiDomainInterpretationService | None = None,
        export_service: ReportExportServiceV1 | None = None,
    ) -> None:
        self._engines = engine_runner or ProductionEngineRunner()
        self._strength = strength_service or StrengthInterpretationService()
        self._composition = composition_service or MultiDomainInterpretationService(
            strength_service=self._strength,
        )
        self._export = export_service or ReportExportServiceV1()

    def run(self, request: ProductionRequest) -> ProductionPipelineResult:
        """Execute full customer pipeline for one birth request."""
        stages: list[str] = []
        errors: list[str] = []
        request_key = request.request_key

        try:
            engine_output = self._engines.run(request)
            stages.extend(engine_output.stages)

            composition = self._composition.compose(
                case_id=request.case_id or request_key,
                engine_output=engine_output,
            )
            stages.append("interpretation_v2_strength")
            stages.append("interpretation_ten_gods")
            stages.append("interpretation_pattern")
            stages.append("interpretation_useful_god")
            stages.append("cross_domain_integration")
            stages.append("executive_consulting")

            report_input = build_report_input_v1(engine_output.report_source)
            report_input = self._enrich_report_with_composition(
                report_input,
                composition=composition,
            )
            stages.append("report_input_v1")

            pdf_path: Path | None = None
            report_status = SectionStatus.AVAILABLE
            if request.export_pdf:
                export_root = request.export_dir or Path(
                    "knowledge/report_v1_validation/exports"
                )
                export_result = self._export.export_pdf(
                    report_input,
                    export_root / f"BTE_{request_key}_Production_E2E.pdf",
                )
                pdf_path = Path(export_result.file_path)
                stages.append("pdf_export")

            domains = composition.customer_domain_payloads()
            executive = composition.executive
            executive_body = (
                executive.body
                if executive.status != DomainStatus.NOT_AVAILABLE
                else EXECUTIVE_CONSULTING_NOT_AVAILABLE
            )
            section_status = SectionAvailability(
                strength_interpretation=_map_domain_status(
                    composition.domains["strength"].status
                ),
                ten_gods_interpretation=_map_domain_status(
                    composition.domains["ten_gods"].status
                ),
                pattern_interpretation=_map_domain_status(
                    composition.domains["pattern"].status
                ),
                useful_god_interpretation=_map_domain_status(
                    composition.domains["useful_god"].status
                ),
                executive_consulting=_map_domain_status(executive.status),
                master_interpretation=SectionStatus.NOT_AVAILABLE,
                report=report_status,
            )
            customer = CustomerDeliverable(
                case_id=request.case_id or request_key,
                profile_name=request.full_name,
                executive_consulting=executive_body,
                section_status=section_status,
                master_interpretation_parts={},
                strength_interpretation=domains.get("strength", {}),
                ten_gods_interpretation=domains.get("ten_gods", {}),
                pattern_interpretation=domains.get("pattern", {}),
                useful_god_interpretation=domains.get("useful_god", {}),
                report_summary=executive.sections[5].paragraphs[0]
                if len(executive.sections) > 5
                else (executive_body[:500] if executive_body else ""),
                recommendations=list(executive.recommendations),
                pipeline_stages=stages,
            )
            customer_payload = customer.to_dict()
            assert_no_internal_keys(customer_payload)

            diagnostics = self._build_diagnostics(
                request,
                engine_output,
                composition.diagnostics,
            )

            return ProductionPipelineResult(
                success=True,
                case_id=request.case_id or request_key,
                customer=customer,
                pdf_path=pdf_path,
                stages_completed=stages,
                diagnostics=diagnostics,
            )
        except Exception as exc:
            logger.exception("production_pipeline_failed request=%s", request_key)
            errors.append(str(exc))
            return ProductionPipelineResult(
                success=False,
                case_id=request.case_id or request_key,
                customer=CustomerDeliverable(
                    case_id=request.case_id or request_key,
                    profile_name=request.full_name,
                    executive_consulting=EXECUTIVE_CONSULTING_NOT_AVAILABLE,
                ),
                stages_completed=stages,
                errors=errors,
            )

    def run_case_0001(
        self,
        *,
        export_dir: Path | None = None,
    ) -> ProductionPipelineResult:
        """Run canonical CASE-0001 through the generic pipeline."""
        request = ProductionRequest(
            case_id=CASE_0001_REQUEST.case_id,
            year=CASE_0001_REQUEST.year,
            month=CASE_0001_REQUEST.month,
            day=CASE_0001_REQUEST.day,
            hour=CASE_0001_REQUEST.hour,
            minute=CASE_0001_REQUEST.minute,
            gender=CASE_0001_REQUEST.gender,
            timezone=CASE_0001_REQUEST.timezone,
            full_name=CASE_0001_REQUEST.full_name,
            birth_place=CASE_0001_REQUEST.birth_place,
            export_pdf=True,
            export_dir=export_dir,
        )
        return self.run(request)

    def _enrich_report_with_composition(self, report_input, *, composition) -> Any:
        """Attach generic domain + executive sections to ReportInputV1."""
        sections = list(report_input.interpretation.sections)
        for domain_name, result in composition.domains.items():
            if result.status in {DomainStatus.NOT_AVAILABLE, DomainStatus.INSUFFICIENT}:
                continue
            body = result.conclusion
            for section in result.sections:
                body += "\n\n" + "\n\n".join(section.paragraphs)
            sections.append(
                ReportInterpretationSectionV1(
                    id=f"domain_{domain_name}",
                    title=f"Luận giải {domain_name}",
                    content=body[:4000],
                    priority=10,
                )
            )
        executive = composition.executive
        if executive.status != DomainStatus.NOT_AVAILABLE:
            sections.append(
                ReportInterpretationSectionV1(
                    id="executive_consulting",
                    title="Báo cáo tư vấn tổng hợp",
                    content=executive.body[:8000],
                    priority=0,
                )
            )
        insight = ""
        if executive.sections:
            for section in executive.sections:
                if section.section_id == "INSIGHT" and section.paragraphs:
                    insight = section.paragraphs[0]
                    break
        report_input.interpretation = ReportInterpretationV1(
            executive_summary=insight or report_input.interpretation.executive_summary,
            sections=sections,
            conclusion=report_input.interpretation.conclusion,
            recommendations=list(executive.recommendations)
            or list(report_input.interpretation.recommendations),
            warnings=list(report_input.interpretation.warnings),
            confidence=report_input.interpretation.confidence,
        )
        return report_input

    def _build_diagnostics(
        self,
        request: ProductionRequest,
        engine_output: EnginePipelineOutput,
        composition_diagnostics: dict[str, Any],
    ) -> dict[str, Any]:
        sequence = extract_internal_dayun_sequence(engine_output.luck)
        knowledge = build_knowledge_diagnostics(self._strength)
        bazi = engine_output.analysis.bazi
        pillars = {
            "year": f"{bazi.year_pillar.stem} {bazi.year_pillar.branch}",
            "month": f"{bazi.month_pillar.stem} {bazi.month_pillar.branch}",
            "day": f"{bazi.day_pillar.stem} {bazi.day_pillar.branch}",
            "hour": f"{bazi.hour_pillar.stem} {bazi.hour_pillar.branch}",
        }
        return {
            "knowledge": knowledge,
            "luck_internal": {
                "dayun_sequence_count": len(sequence),
                "dayun_sequence": sequence,
            },
            "master_interpretation_policy": "GOLDEN_REFERENCE_ONLY",
            "composition": composition_diagnostics,
            "engine_analysis": {
                "request_key": request.request_key,
                "pillars": pillars,
                "strength": {
                    "strength_level": engine_output.strength_result.strength_level,
                    "strength_score": engine_output.strength_result.strength_score,
                },
                "pattern": engine_output.analysis.pattern.to_dict()
                if engine_output.analysis.pattern
                else {},
                "useful_god": engine_output.analysis.useful_god.to_dict()
                if engine_output.analysis.useful_god
                else {},
                "ten_gods": engine_output.ten_gods.to_dict(),
            },
        }
