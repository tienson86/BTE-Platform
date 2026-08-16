"""Production End-to-End Orchestrator — generic composition pipeline."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from engines.interpretation_engine_v2 import StrengthInterpretationService
from engines.report_engine.adapters.report_input_v1_adapter import build_report_input_v1
from engines.report_engine.commercial.builder import CommercialReportBuilder
from engines.report_engine.commercial.models import (
    CommercialBuildRequest,
    CommercialFeatureInput,
)
from engines.report_engine.commercial.pdf_exporter import CommercialPdfExporter
from engines.report_engine.contracts.report_input_v1 import (
    ReportInterpretationSectionV1,
    ReportInterpretationV1,
)
from engines.report_engine.services.report_export_service_v1 import ReportExportServiceV1

from applications.api.services.narrative_result_truth import build_narrative_result_dict
from applications.production.customer_projection import assert_no_internal_keys
from applications.production.engine_runner import EnginePipelineOutput, ProductionEngineRunner
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.interpretation.contracts import (
    DomainStatus,
    ExecutiveConsultingResult,
)
from applications.production.interpretation.cross_domain.models import ThemeStatus
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
from applications.production.product_context.delivery import ContextDeliveryAdapter
from applications.production.product_context.engine import ProductContextEngine
from applications.production.product_context.input_builder import (
    build_product_context_input,
)
from applications.production.product_context.models import (
    LanguageProfile,
    LifeStage,
    PurchasePackage,
    ReaderRole,
)

logger = logging.getLogger(__name__)


def _map_domain_status(status: DomainStatus) -> SectionStatus:
    if status == DomainStatus.AVAILABLE:
        return SectionStatus.AVAILABLE
    if status == DomainStatus.PARTIAL:
        return SectionStatus.PARTIAL
    return SectionStatus.NOT_AVAILABLE


class ProductionEndToEndOrchestrator:
    """One orchestrator: engines → composition → product context → report → PDF."""

    def __init__(
        self,
        *,
        engine_runner: ProductionEngineRunner | None = None,
        strength_service: StrengthInterpretationService | None = None,
        composition_service: MultiDomainInterpretationService | None = None,
        export_service: ReportExportServiceV1 | None = None,
        product_context_engine: ProductContextEngine | None = None,
        context_delivery: ContextDeliveryAdapter | None = None,
        commercial_builder: CommercialReportBuilder | None = None,
        commercial_exporter: CommercialPdfExporter | None = None,
    ) -> None:
        self._engines = engine_runner or ProductionEngineRunner()
        self._strength = strength_service or StrengthInterpretationService()
        self._composition = composition_service or MultiDomainInterpretationService(
            strength_service=self._strength,
        )
        self._export = export_service or ReportExportServiceV1()
        self._product_context = product_context_engine or ProductContextEngine()
        self._context_delivery = context_delivery or ContextDeliveryAdapter()
        self._commercial_builder = commercial_builder or CommercialReportBuilder()
        self._commercial_export = commercial_exporter or CommercialPdfExporter()

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
            stages.append("cross_domain_reasoning")
            stages.append("identity_report")
            stages.append("career_report")
            stages.append("executive_consulting")

            context_input = build_product_context_input(request)
            product_context = self._product_context.resolve(context_input)
            delivery = self._context_delivery.apply(composition, product_context)
            stages.append("product_context")
            stages.append("context_delivery")

            report_input = build_report_input_v1(engine_output.report_source)
            stages.append("report_input_v1")

            narrative_result = self._compose_narrative_result(request, engine_output)
            stages.append("narrative_result")

            commercial_request = self._build_commercial_request(
                request,
                engine_output=engine_output,
                composition=composition,
                delivery=delivery,
                product_context=product_context,
                narrative_result=narrative_result,
            )
            commercial_report = self._commercial_builder.build(commercial_request)
            stages.append("commercial_theme_library")
            stages.append("commercial_language")
            stages.append("commercial_report_builder")

            pdf_path: Path | None = None
            report_status = SectionStatus.AVAILABLE
            if request.export_pdf:
                export_root = request.export_dir or Path(
                    "knowledge/report_v1_validation/exports"
                )
                export_result = self._commercial_export.export(
                    commercial_report,
                    export_root / f"BTE_{request_key}_Production_E2E.pdf",
                )
                pdf_path = Path(export_result.file_path)
                stages.append("pdf_export")

            domains = composition.customer_domain_payloads()
            executive = delivery.executive
            executive_body = (
                executive.body
                if executive.status != DomainStatus.NOT_AVAILABLE
                else EXECUTIVE_CONSULTING_NOT_AVAILABLE
            )
            identity_body = (
                delivery.identity.body
                if delivery.identity.status != DomainStatus.NOT_AVAILABLE
                else ""
            )
            # Keep explicit hide marker when context blocks Career (customer-visible policy signal).
            career_body = delivery.career.body or ""
            if (
                delivery.career.status == DomainStatus.NOT_AVAILABLE
                and not career_body
            ):
                career_body = "CAREER_REPORT_HIDDEN_BY_PRODUCT_CONTEXT"
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
                identity_report=_map_domain_status(delivery.identity.status),
                career_report=_map_domain_status(delivery.career.status),
                development_guidance=(
                    SectionStatus.AVAILABLE
                    if delivery.development_guidance
                    else SectionStatus.NOT_AVAILABLE
                ),
                parent_guidance=(
                    SectionStatus.AVAILABLE
                    if delivery.parent_guidance
                    else SectionStatus.NOT_AVAILABLE
                ),
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
                identity_report=identity_body,
                career_report=career_body,
                development_guidance=delivery.development_guidance,
                parent_guidance=delivery.parent_guidance,
                report_summary=executive.sections[0].paragraphs[0]
                if executive.sections and executive.sections[0].paragraphs
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
            diagnostics["product_context"] = product_context.to_dict()
            diagnostics["context_delivery"] = dict(delivery.diagnostics or {})
            diagnostics["commercial_report"] = dict(commercial_report.diagnostics)
            diagnostics["narrative_result_status"] = narrative_result.get("status")
            diagnostics["narrative_result_contract"] = narrative_result.get("contract")

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

    def _compose_narrative_result(
        self,
        request: ProductionRequest,
        engine_output: EnginePipelineOutput,
    ) -> dict[str, Any]:
        """Compose NarrativeResult V2 for the production PDF path."""
        analysis = engine_output.analysis
        return build_narrative_result_dict(
            analysis={
                "bazi": analysis.bazi_dict(),
                "pattern": analysis.pattern_dict(),
                "strength": analysis.strength_dict(),
                "useful_god": analysis.useful_god_dict(),
                "score": analysis.score_dict(),
            },
            interpretation=analysis.interpretation_dict(),
            run_id=request.case_id or request.request_key,
            engine_output=engine_output,
        )

    def _build_commercial_request(
        self,
        request: ProductionRequest,
        *,
        engine_output: EnginePipelineOutput,
        composition,
        delivery,
        product_context,
        narrative_result: dict[str, Any] | None = None,
    ) -> CommercialBuildRequest:
        """Map canonical narrative + product features into the commercial builder."""
        advisor_mode = self._is_advisor_mode(request, product_context)
        parent_context = product_context.language_profile == LanguageProfile.PARENT_SUPPORT or (
            product_context.life_stage in {LifeStage.CHILD, LifeStage.TEEN}
        )
        active_themes = [
            theme.theme_id
            for theme in composition.cross_domain.themes
            if theme.status != ThemeStatus.SUPPRESSED
        ]
        appendix_rows: list[tuple[str, str]] = []
        appendix_paragraphs: list[str] = []
        if advisor_mode:
            appendix_rows, appendix_paragraphs = self._advisor_appendix(
                engine_output,
                composition,
            )
        calendar = engine_output.calendar or {}
        luck = engine_output.luck or {}
        current = luck.get("current_cycle") or {}
        current_dayun = ""
        if current:
            gan = current.get("gan_zhi") or ""
            years = ""
            if current.get("year_start") and current.get("year_end"):
                years = f"{current['year_start']}–{current['year_end']}"
            current_dayun = " ".join(part for part in (gan, years) if part)
        dayun_cycles: list[tuple[str, str]] = []
        for item in luck.get("cycles") or []:
            if not isinstance(item, dict):
                continue
            gan_zhi = str(item.get("gan_zhi") or "").strip()
            year_start = item.get("year_start")
            year_end = item.get("year_end")
            years = ""
            if year_start and year_end:
                years = f"{year_start}–{year_end}"
            label = f"Đại vận {item.get('index', len(dayun_cycles)) + 1}"
            value = " ".join(part for part in (gan_zhi, years) if part)
            if value:
                dayun_cycles.append((label, value))
        five_summary = ""
        series = []
        if engine_output.analysis.score and engine_output.analysis.score.wuxing_series:
            series = list(engine_output.analysis.score.wuxing_series)
        if series:
            five_summary = ", ".join(
                f"{item.get('label')}:{item.get('value')}"
                for item in series
                if isinstance(item, dict)
            )
        ten_gods = list(engine_output.analysis.bazi.ten_gods or [])
        return CommercialBuildRequest(
            client_name=request.full_name,
            case_id=request.case_id or request.request_key,
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            birth_lunar=str(calendar.get("lunar_date") or ""),
            birth_place=request.birth_place,
            gender=request.gender,
            cung_phi=str(calendar.get("cung_phi") or ""),
            menh_quai=str(calendar.get("menh_quai") or ""),
            nhom_trach=str(calendar.get("nhom_trach") or ""),
            current_dayun=current_dayun,
            dayun_start_age=str(luck.get("start_age") or ""),
            dayun_cycles=dayun_cycles,
            five_elements_summary=five_summary,
            ten_gods_summary=", ".join(str(item) for item in ten_gods if item),
            identity=self._feature_input(
                "identity",
                "Danh tính",
                delivery.identity,
            ),
            career=self._feature_input(
                "career",
                "Sự nghiệp",
                delivery.career,
            ),
            executive=self._feature_input(
                "executive",
                "Tư vấn tổng hợp",
                delivery.executive,
            ),
            primary_theme=composition.cross_domain.primary_theme,
            active_theme_ids=active_themes,
            capacity_level=engine_output.strength_result.strength_level,
            has_conflicts=bool(composition.cross_domain.conflicts),
            parent_context=parent_context,
            purchase_package=product_context.purchase_package.value,
            reader_role=product_context.reader_role.value,
            advisor_mode=advisor_mode,
            writing_variant=str(request.options.get("writing_variant") or ""),
            appendix_rows=appendix_rows,
            appendix_paragraphs=appendix_paragraphs,
            narrative_result=narrative_result,
        )

    @staticmethod
    def _feature_input(
        feature_id: str,
        title: str,
        result: ExecutiveConsultingResult,
    ) -> CommercialFeatureInput:
        """Adapt a composed feature into commercial builder input."""
        sections = [
            (section.section_id, section.title, list(section.paragraphs))
            for section in result.sections
        ]
        return CommercialFeatureInput(
            feature_id=feature_id,
            title=title,
            status=result.status.value,
            sections=sections,
            body=result.body,
        )

    @staticmethod
    def _is_advisor_mode(request: ProductionRequest, product_context) -> bool:
        """Appendix is Advisor Mode only — never default customer PDF."""
        options = dict(request.options or {})
        if options.get("advisor_mode") in {True, "true", "1", 1}:
            return True
        if product_context.purchase_package == PurchasePackage.PACKAGE_D:
            return True
        return product_context.reader_role == ReaderRole.CONSULTANT

    @staticmethod
    def _advisor_appendix(
        engine_output: EnginePipelineOutput,
        composition,
    ) -> tuple[list[tuple[str, str]], list[str]]:
        """Technical rows for Advisor Mode appendix."""
        strength = engine_output.strength_result
        plan = composition.cross_domain.executive_claim_plan
        rows = [
            ("Mức thân", str(strength.strength_level or "")),
            ("Điểm thân", str(strength.strength_score or "")),
            ("Chủ đề chính", composition.cross_domain.primary_theme),
            ("Xung đột", ", ".join(composition.cross_domain.conflicts)),
        ]
        paragraphs = [
            f"identity_core: {plan.identity_core}",
            f"operating_style: {plan.operating_style}",
            f"primary_insight: {plan.primary_insight}",
        ]
        why = composition.cross_domain.diagnostics.get("why_primary") or {}
        if why:
            paragraphs.append(f"why_primary: {why}")
        return rows, paragraphs

    def _enrich_report_with_composition(
        self,
        report_input,
        *,
        composition,
        delivery=None,
    ) -> Any:
        """Attach generic domain + context-delivered feature sections to ReportInputV1."""
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
        identity = delivery.identity if delivery is not None else composition.identity
        career = delivery.career if delivery is not None else composition.career
        executive = delivery.executive if delivery is not None else composition.executive

        if executive.status != DomainStatus.NOT_AVAILABLE:
            sections.append(
                ReportInterpretationSectionV1(
                    id="executive_consulting",
                    title="Báo cáo tư vấn tổng hợp",
                    content=executive.body[:8000],
                    priority=0,
                )
            )
        if identity.status != DomainStatus.NOT_AVAILABLE:
            sections.append(
                ReportInterpretationSectionV1(
                    id="identity_report",
                    title="Báo cáo danh tính",
                    content=identity.body[:6000],
                    priority=1,
                )
            )
        if career.status != DomainStatus.NOT_AVAILABLE:
            sections.append(
                ReportInterpretationSectionV1(
                    id="career_report",
                    title="Báo cáo sự nghiệp",
                    content=career.body[:6000],
                    priority=2,
                )
            )
        if delivery is not None and delivery.parent_guidance:
            sections.append(
                ReportInterpretationSectionV1(
                    id="parent_guidance",
                    title="Hướng dẫn phụ huynh",
                    content=delivery.parent_guidance[:4000],
                    priority=3,
                )
            )
        if delivery is not None and delivery.development_guidance:
            sections.append(
                ReportInterpretationSectionV1(
                    id="development_guidance",
                    title="Định hướng phát triển",
                    content=delivery.development_guidance[:4000],
                    priority=4,
                )
            )
        insight = ""
        if executive.sections:
            for section in executive.sections:
                if section.section_id in {"INSIGHT", "CONCLUSION", "WHO"} and section.paragraphs:
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
