"""Report Builder — assemble StructuredReport from bound inputs."""

from __future__ import annotations

from engines.analysis_engine.report_generator.models import (
    FormatHints,
    FormatProfile,
    ReportAssemblyContext,
    ReportMetadata,
    ReportSection,
    ReportTheme,
    StructuredDataBlock,
    StructuredReport,
    canonical_stage_order,
    default_stage_titles,
)
from engines.analysis_engine.report_generator.section_builder import SectionBuilder
from engines.analysis_engine.runtime.models import AnalysisResult


class ReportBuilder:
    """Build the canonical StructuredReport assembly model."""

    def __init__(self, *, section_builder: SectionBuilder | None = None) -> None:
        self._section_builder = section_builder or SectionBuilder()

    def build(
        self,
        context: ReportAssemblyContext,
        *,
        theme: ReportTheme,
        module_version: str,
    ) -> StructuredReport:
        """Assemble StructuredReport from context without reinterpretation."""
        profile = context.format_profile
        sections = self._section_builder.build(
            context.interpretation_result,
            profile=profile,
        )
        data_blocks = self._bind_data_blocks(context.analysis_result, profile)
        metadata = ReportMetadata(
            report_id=f"report:{context.request_id}",
            request_id=context.request_id,
            title=profile.title,
            module_version=module_version,
            theme_id=theme.theme_id,
            template_id=profile.template_id,
            formats=tuple(profile.formats),
            extras=dict(profile.metadata),
        )
        format_hints = FormatHints(
            theme_id=theme.theme_id,
            template_id=profile.template_id,
            css_variables=dict(theme.css_variables),
            details={"font_family": theme.font_family},
        )
        source_trace = {
            "interpretation_request_id": context.interpretation_result.request_id,
            "interpretation_module_version": (
                context.interpretation_result.module_version
            ),
            "interpretation_knowledge_version": (
                context.interpretation_result.knowledge_version
            ),
            "analysis_request_id": (
                None
                if context.analysis_result is None
                else context.analysis_result.request_id
            ),
            "analysis_runtime_version": (
                None
                if context.analysis_result is None
                else context.analysis_result.runtime_version
            ),
            "section_ids": [section.section_id for section in sections],
            "data_block_ids": [block.block_id for block in data_blocks],
        }
        overview = context.interpretation_result.overview.strip()
        if not overview and sections:
            overview = sections[0].body
        return StructuredReport(
            metadata=metadata,
            sections=sections,
            data_blocks=data_blocks,
            format_hints=format_hints,
            source_trace=source_trace,
            overview=overview,
        )

    def _bind_data_blocks(
        self,
        analysis: AnalysisResult | None,
        profile: FormatProfile,
    ) -> tuple[StructuredDataBlock, ...]:
        if not profile.include_structured_data or analysis is None:
            return ()
        titles = default_stage_titles()
        blocks: list[StructuredDataBlock] = []
        for order, stage_id in enumerate(canonical_stage_order()):
            stage = analysis.get_stage_result(stage_id)
            if stage is None:
                continue
            blocks.append(
                StructuredDataBlock(
                    block_id=f"data:{stage_id}",
                    stage_id=stage_id,
                    title=titles.get(stage_id, stage_id),
                    payload=dict(stage.payload),
                    order=order,
                    trace={
                        "module_version": stage.module_version,
                        "status": stage.status,
                    },
                )
            )
        return tuple(blocks)
