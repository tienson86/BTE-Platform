"""Unit tests for Report Generator components."""

from __future__ import annotations

import json

import pytest

from engines.analysis_engine.report_generator import (
    CATALOG_THEME_IDS,
    ChartRenderer,
    ComponentRenderer,
    FormatProfile,
    ReportAssemblyContext,
    ReportBindingError,
    ReportBuilder,
    ReportFormatProfileError,
    ReportGenerator,
    ReportPrerequisiteError,
    ReportValidationError,
    SectionBuilder,
    SectionRenderer,
    StructuredDataBlock,
    TableRenderer,
    TemplateLoader,
    ThemeManager,
    ThemeRegistry,
)


class TestValidation:
    def test_missing_interpretation_fails(self, generator: ReportGenerator) -> None:
        with pytest.raises(ReportValidationError):
            generator.assemble(
                ReportAssemblyContext(
                    interpretation_result=None,  # type: ignore[arg-type]
                    format_profile=FormatProfile(),
                )
            )

    def test_missing_analysis_when_required(
        self,
        generator: ReportGenerator,
        interpretation_result,
    ) -> None:
        profile = FormatProfile.full_publication(require_analysis_result=True)
        with pytest.raises(ReportPrerequisiteError):
            generator.assemble(
                ReportAssemblyContext(
                    interpretation_result=interpretation_result,
                    analysis_result=None,
                    format_profile=profile,
                )
            )

    def test_illegal_format_rejected(
        self,
        generator: ReportGenerator,
        interpretation_result,
    ) -> None:
        with pytest.raises(ReportFormatProfileError):
            generator.assemble(
                ReportAssemblyContext(
                    interpretation_result=interpretation_result,
                    format_profile=FormatProfile(formats=("xml",)),  # type: ignore[arg-type]
                )
            )


class TestThemeAndTemplate:
    def test_theme_registry_default(self) -> None:
        theme = ThemeRegistry().get("default")
        assert theme.theme_id == "default"
        assert "--accent" in theme.css_variables

    def test_unknown_theme_fails(self) -> None:
        with pytest.raises(ReportFormatProfileError):
            ThemeRegistry().get("missing")

    def test_template_loader_default(self) -> None:
        template = TemplateLoader().load("default")
        assert "{title}" in template.html_shell
        assert "{sections}" in template.markdown_shell

    def test_catalog_themes_available(self) -> None:
        manager = ThemeManager()
        for theme_id in CATALOG_THEME_IDS:
            theme = manager.get(theme_id)
            assert theme.theme_id == theme_id
            assert theme.css_variables["--bg"]
            assert manager.print_css(theme_id)
        catalog = manager.list_catalog()
        assert [item.theme_id for item in catalog] == list(CATALOG_THEME_IDS)

    def test_template_loader_catalog_and_print(self) -> None:
        loader = TemplateLoader()
        for template_id in ("classic", "modern", "professional", "dark", "print"):
            template = loader.load(template_id)
            assert template.template_id == template_id
            assert "{sections}" in template.html_shell


class TestRenderers:
    def test_section_renderer_html_and_markdown(self, interpretation_result) -> None:
        sections = SectionBuilder().build(
            interpretation_result,
            profile=FormatProfile(mandatory_sections=("overview",)),
        )
        html = SectionRenderer().render_html(sections[0])
        md = SectionRenderer().render_markdown(sections[0])
        assert 'class="report-section"' in html
        assert sections[0].title in md

    def test_table_and_chart_renderers(self) -> None:
        block = StructuredDataBlock(
            block_id="data:strength",
            stage_id="strength",
            title="Strength",
            payload={"classification": "strong", "score": 0.82, "support": 12},
            order=0,
        )
        table_html = TableRenderer().render_html(block)
        chart_html = ChartRenderer().render_html(block)
        table_md = TableRenderer().render_markdown(block)
        chart_md = ChartRenderer().render_markdown(block)
        assert "report-table" in table_html
        assert "chart-bar-fill" in chart_html
        assert "| Field | Value |" in table_md
        assert "Strength Chart" in chart_md

    def test_component_renderer_composes_blocks(self) -> None:
        block = StructuredDataBlock(
            block_id="data:luck",
            stage_id="luck",
            title="Luck",
            payload={
                "summary": {"active_count": 4, "current_da_yun_index": 2},
            },
            order=0,
        )
        html = ComponentRenderer().render_data_blocks_html((block,))
        md = ComponentRenderer().render_data_blocks_markdown((block,))
        assert "Analytical Data" in html
        assert "Analytical Data" in md


class TestTemplateSystemAssemble:
    @pytest.mark.parametrize("theme_id", list(CATALOG_THEME_IDS))
    def test_assemble_with_catalog_theme(
        self,
        generator: ReportGenerator,
        interpretation_result,
        analysis_result,
        theme_id: str,
    ) -> None:
        result = generator.assemble(
            ReportAssemblyContext(
                interpretation_result=interpretation_result,
                analysis_result=analysis_result,
                format_profile=FormatProfile(
                    formats=("html", "markdown"),
                    theme_id=theme_id,
                    template_id=theme_id,
                    include_structured_data=True,
                    mandatory_sections=("overview",),
                ),
            )
        )
        assert result.html is not None
        assert f"--accent" in result.html.content or ":root" in result.html.content
        assert result.summary["theme_id"] == theme_id
        assert "report-table" in result.html.content
        assert result.markdown is not None

    def test_print_format_artifact(
        self,
        generator: ReportGenerator,
        interpretation_result,
        analysis_result,
    ) -> None:
        result = generator.assemble(
            ReportAssemblyContext(
                interpretation_result=interpretation_result,
                analysis_result=analysis_result,
                format_profile=FormatProfile(
                    formats=("print", "html", "pdf", "markdown"),
                    theme_id="professional",
                    template_id="professional",
                    include_structured_data=True,
                    mandatory_sections=("overview",),
                ),
            )
        )
        assert result.print is not None
        assert "print-document" in result.print.content or "@media print" in result.print.content
        assert result.html is not None
        assert result.pdf is not None
        assert result.markdown is not None


class TestSectionAndReportBuilder:
    def test_section_builder_preserves_body(self, interpretation_result) -> None:
        sections = SectionBuilder().build(
            interpretation_result,
            profile=FormatProfile(mandatory_sections=("overview",)),
        )
        assert sections[0].section_id == "overview"
        assert "Giáp" in sections[0].body

    def test_missing_mandatory_section_fails(self, interpretation_result) -> None:
        with pytest.raises(ReportBindingError):
            SectionBuilder().build(
                interpretation_result,
                profile=FormatProfile(mandatory_sections=("career",)),
            )

    def test_report_builder_binds_data_blocks(
        self,
        assembly_context: ReportAssemblyContext,
    ) -> None:
        theme = ThemeRegistry().get("default")
        report = ReportBuilder().build(
            assembly_context,
            theme=theme,
            module_version="1.0.0",
        )
        assert report.sections
        assert report.data_blocks
        stage_ids = [block.stage_id for block in report.data_blocks]
        assert stage_ids[0] == "strength"
        assert "summary" in stage_ids


class TestSerializersViaAssemble:
    def test_full_publication_artifacts(
        self,
        generator: ReportGenerator,
        assembly_context: ReportAssemblyContext,
    ) -> None:
        result = generator.assemble(assembly_context)
        assert result.html is not None
        assert "<html" in result.html.content.lower()
        assert "Giáp" in result.html.content
        assert result.markdown is not None
        assert result.markdown.content.startswith("# ")
        assert result.json is not None
        payload = json.loads(result.json.content)
        assert payload["format"] == "json"
        assert payload["report"]["metadata"]["request_id"] == "rpt-req-001"
        assert result.pdf is not None
        assert result.pdf.content.startswith(b"%PDF")
        assert result.structured_report.overview

    def test_interpretation_only_profile(
        self,
        generator: ReportGenerator,
        interpretation_result,
    ) -> None:
        profile = FormatProfile(
            formats=("html", "markdown"),
            require_analysis_result=False,
            include_structured_data=False,
            mandatory_sections=("overview",),
        )
        result = generator.assemble(
            ReportAssemblyContext(
                interpretation_result=interpretation_result,
                format_profile=profile,
            )
        )
        assert result.html is not None
        assert result.markdown is not None
        assert result.pdf is None
        assert result.json is None
        assert result.structured_report.data_blocks == ()

    def test_does_not_mutate_upstream(
        self,
        generator: ReportGenerator,
        assembly_context: ReportAssemblyContext,
    ) -> None:
        before_interp = assembly_context.interpretation_result.to_dict()
        before_analysis = {
            stage_id: dict(stage.payload)
            for stage_id, stage in assembly_context.analysis_result.stage_results.items()  # type: ignore[union-attr]
        }
        generator.assemble(assembly_context)
        assert assembly_context.interpretation_result.to_dict() == before_interp
        after_analysis = {
            stage_id: dict(stage.payload)
            for stage_id, stage in assembly_context.analysis_result.stage_results.items()  # type: ignore[union-attr]
        }
        assert before_analysis == after_analysis

    def test_deterministic(
        self,
        generator: ReportGenerator,
        assembly_context: ReportAssemblyContext,
    ) -> None:
        first = generator.assemble(assembly_context).to_dict()
        second = generator.assemble(assembly_context).to_dict()
        # Drop timing metadata differences if any nested duration appears.
        first.pop("diagnostics", None)
        second.pop("diagnostics", None)
        assert first["html"] == second["html"]
        assert first["markdown"] == second["markdown"]
        assert first["json"] == second["json"]
        assert first["pdf_size"] == second["pdf_size"]

    def test_generate_alias(
        self,
        generator: ReportGenerator,
        assembly_context: ReportAssemblyContext,
    ) -> None:
        a = generator.assemble(assembly_context)
        b = generator.generate(assembly_context)
        assert a.structured_report.to_dict() == b.structured_report.to_dict()
        assert a.html is not None and b.html is not None
        assert a.html.content == b.html.content
