"""Production End-to-End Orchestrator — Sprint 2 single customer pipeline."""

from __future__ import annotations

import logging
import re
from pathlib import Path

from engines.interpretation_engine_v2 import StrengthInterpretationService
from engines.report_engine.adapters.report_input_v1_adapter import (
    ReportInputV1Adapter,
    build_report_input_v1,
)
from engines.report_engine.contracts.report_input_v1 import (
    ReportInterpretationSectionV1,
    ReportInterpretationV1,
)
from engines.report_engine.services.report_export_service_v1 import ReportExportServiceV1

from applications.production.customer_projection import (
    assert_no_internal_keys,
    project_strength_interpretation,
)
from applications.production.engine_runner import ProductionEngineRunner
from applications.production.master_interpretation_loader import (
    extract_executive_summary,
    load_all_master_parts,
    load_executive_consulting,
)
from applications.production.models import (
    CustomerDeliverable,
    ProductionPipelineResult,
    ProductionRequest,
)

logger = logging.getLogger(__name__)

CASE_0001_REQUEST = ProductionRequest(
    case_id="CASE-0001",
    year=1987,
    month=1,
    day=21,
    hour=4,
    minute=30,
    gender="male",
    timezone="Asia/Bangkok",
    full_name="Nguyễn Tiến Sơn",
    birth_place="Hà Tây, Việt Nam",
)


class ProductionEndToEndOrchestrator:
    """One orchestrator: engines → interpretation → consulting → PDF."""

    def __init__(
        self,
        *,
        engine_runner: ProductionEngineRunner | None = None,
        strength_service: StrengthInterpretationService | None = None,
        report_adapter: ReportInputV1Adapter | None = None,
        export_service: ReportExportServiceV1 | None = None,
    ) -> None:
        self._engines = engine_runner or ProductionEngineRunner()
        self._strength = strength_service or StrengthInterpretationService()
        self._adapter = report_adapter or ReportInputV1Adapter()
        self._export = export_service or ReportExportServiceV1()

    def run(self, request: ProductionRequest) -> ProductionPipelineResult:
        """Execute full customer pipeline for one birth request."""
        stages: list[str] = []
        errors: list[str] = []

        try:
            engine_output = self._engines.run(request)
            stages.extend(engine_output.stages)

            strength_interp = self._run_strength_interpretation(request.case_id)
            stages.append("interpretation_v2_strength")

            master_parts = load_all_master_parts(request.case_id)
            stages.append("master_interpretation")

            executive = load_executive_consulting(request.case_id)
            stages.append("executive_consulting")

            report_input = build_report_input_v1(engine_output.report_source)
            report_input = self._enrich_report_with_consulting(
                report_input,
                executive=executive,
                master_parts=master_parts,
            )
            stages.append("report_input_v1")

            pdf_path: Path | None = None
            if request.export_pdf:
                export_root = request.export_dir or Path(
                    "knowledge/report_v1_validation/exports"
                )
                export_result = self._export.export_pdf(
                    report_input,
                    export_root
                    / f"BTE_{request.case_id}_Production_E2E.pdf",
                )
                pdf_path = Path(export_result.file_path)
                stages.append("pdf_export")

            strength_customer = project_strength_interpretation(strength_interp)
            recommendations = self._extract_recommendations(executive)
            customer = CustomerDeliverable(
                case_id=request.case_id,
                profile_name=request.full_name,
                executive_consulting=executive,
                master_interpretation_parts=master_parts,
                strength_interpretation=strength_customer,
                report_summary=extract_executive_summary(executive),
                recommendations=recommendations,
                pipeline_stages=stages,
            )
            customer_payload = customer.to_dict()
            assert_no_internal_keys(customer_payload)

            return ProductionPipelineResult(
                success=True,
                case_id=request.case_id,
                customer=customer,
                pdf_path=pdf_path,
                stages_completed=stages,
            )
        except Exception as exc:
            logger.exception("production_pipeline_failed case_id=%s", request.case_id)
            errors.append(str(exc))
            return ProductionPipelineResult(
                success=False,
                case_id=request.case_id,
                customer=CustomerDeliverable(
                    case_id=request.case_id,
                    profile_name=request.full_name,
                    executive_consulting="",
                ),
                stages_completed=stages,
                errors=errors,
            )

    def run_case_0001(
        self,
        *,
        export_dir: Path | None = None,
    ) -> ProductionPipelineResult:
        """Run canonical CASE-0001 acceptance path."""
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

    def _run_strength_interpretation(self, case_id: str):
        if case_id.upper() == "CASE-0001":
            return self._strength.run_case_0001()
        raise ValueError(
            f"Strength Interpretation V2 not configured for case_id={case_id}"
        )

    def _enrich_report_with_consulting(
        self,
        report_input,
        *,
        executive: str,
        master_parts: dict[str, str],
    ):
        summary = extract_executive_summary(executive)
        sections = list(report_input.interpretation.sections)
        sections.append(
            ReportInterpretationSectionV1(
                id="executive_consulting",
                title="Báo cáo tư vấn tổng hợp",
                content=executive[:8000],
                priority=0,
            )
        )
        for part_id, body in master_parts.items():
            sections.append(
                ReportInterpretationSectionV1(
                    id=f"master_part_{part_id}",
                    title=f"Phần {part_id}",
                    content=body[:4000],
                    priority=int(part_id),
                )
            )
        report_input.interpretation = ReportInterpretationV1(
            executive_summary=summary or report_input.interpretation.executive_summary,
            sections=sections,
            conclusion=report_input.interpretation.conclusion,
            recommendations=self._extract_recommendations(executive)
            or list(report_input.interpretation.recommendations),
            warnings=list(report_input.interpretation.warnings),
            confidence=report_input.interpretation.confidence,
        )
        return report_input

    @staticmethod
    def _extract_recommendations(executive: str) -> list[str]:
        items: list[str] = []
        for match in re.finditer(
            r"## (?:Khuyến nghị|Ưu tiên|Tránh) \d+[^\n]*\n+(.*?)(?=\n## |\n# |\Z)",
            executive,
            re.DOTALL,
        ):
            block = match.group(1).strip()
            action = re.search(r"\*\*Action:\*\* (.+)", block)
            if action:
                items.append(action.group(1).strip())
        return items[:6]
