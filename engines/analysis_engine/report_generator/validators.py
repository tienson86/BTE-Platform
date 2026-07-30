"""Input / output validators for Report Generator."""

from __future__ import annotations

from engines.analysis_engine.interpretation_engine.models import InterpretationResult
from engines.analysis_engine.report_generator.exceptions import (
    ReportFormatProfileError,
    ReportPrerequisiteError,
    ReportSchemaError,
    ReportValidationError,
)
from engines.analysis_engine.report_generator.models import (
    SUPPORTED_FORMATS,
    FormatProfile,
    ReportAssemblyContext,
    ReportGeneratorResult,
    StructuredReport,
)
from engines.analysis_engine.runtime.models import AnalysisResult


def validate_context(context: ReportAssemblyContext) -> None:
    """Validate ReportAssemblyContext admission requirements."""
    if not isinstance(context, ReportAssemblyContext):
        raise ReportValidationError(
            "ReportAssemblyContext is required",
            details={"type": type(context).__name__},
        )
    if not context.request_id:
        raise ReportValidationError("request_id is required")
    if context.interpretation_result is None:
        raise ReportPrerequisiteError("interpretation_result is required")
    if not isinstance(context.interpretation_result, InterpretationResult):
        raise ReportValidationError(
            "interpretation_result must be InterpretationResult",
            details={"type": type(context.interpretation_result).__name__},
        )
    if context.format_profile is None:
        raise ReportValidationError("format_profile is required")
    if not isinstance(context.format_profile, FormatProfile):
        raise ReportValidationError(
            "format_profile must be FormatProfile",
            details={"type": type(context.format_profile).__name__},
        )


def validate_format_profile(profile: FormatProfile) -> None:
    """Validate format profile legality."""
    if not profile.formats:
        raise ReportFormatProfileError(
            "format_profile must declare at least one output format",
        )
    illegal = [fmt for fmt in profile.formats if fmt not in SUPPORTED_FORMATS]
    if illegal:
        raise ReportFormatProfileError(
            "Unsupported output format(s) in format_profile",
            details={"illegal": illegal, "supported": list(SUPPORTED_FORMATS)},
        )
    if not profile.theme_id:
        raise ReportFormatProfileError("format_profile.theme_id is required")
    if not profile.template_id:
        raise ReportFormatProfileError("format_profile.template_id is required")


def validate_prerequisites(context: ReportAssemblyContext) -> None:
    """Validate upstream prerequisites for the declared profile."""
    interpretation = context.interpretation_result
    if not interpretation.sections:
        raise ReportPrerequisiteError(
            "InterpretationResult.sections is empty",
        )
    if not interpretation.overview.strip() and not any(
        section.body.strip() for section in interpretation.sections
    ):
        raise ReportPrerequisiteError(
            "InterpretationResult has no narrative content",
        )

    profile = context.format_profile
    if profile.require_analysis_result or profile.include_structured_data:
        if context.analysis_result is None:
            raise ReportPrerequisiteError(
                "AnalysisResult is required by format_profile",
                details={
                    "require_analysis_result": profile.require_analysis_result,
                    "include_structured_data": profile.include_structured_data,
                },
            )
        if not isinstance(context.analysis_result, AnalysisResult):
            raise ReportValidationError(
                "analysis_result must be AnalysisResult",
                details={"type": type(context.analysis_result).__name__},
            )


def validate_structured_report(report: StructuredReport) -> None:
    """Validate StructuredReport schema invariants."""
    if not report.metadata.report_id:
        raise ReportSchemaError("StructuredReport.metadata.report_id is required")
    if not report.sections:
        raise ReportSchemaError("StructuredReport.sections must not be empty")
    seen: set[str] = set()
    for section in report.sections:
        if section.section_id in seen:
            raise ReportSchemaError(
                "Duplicate section_id in StructuredReport",
                details={"section_id": section.section_id},
            )
        seen.add(section.section_id)
        if not section.body.strip():
            raise ReportSchemaError(
                "Report section body must not be empty",
                details={"section_id": section.section_id},
            )


def validate_result(
    result: ReportGeneratorResult,
    *,
    profile: FormatProfile,
) -> None:
    """Validate published ReportGeneratorResult against profile."""
    validate_structured_report(result.structured_report)
    required = set(profile.formats)
    artifacts = {
        "html": result.html,
        "pdf": result.pdf,
        "json": result.json,
        "markdown": result.markdown,
    }
    missing = [fmt for fmt in required if artifacts.get(fmt) is None]
    if missing:
        raise ReportSchemaError(
            "ReportGeneratorResult missing mandatory format artifacts",
            details={"missing": missing},
        )
    if result.html is not None and not result.html.content.strip():
        raise ReportSchemaError("HTML artifact content is empty")
    if result.markdown is not None and not result.markdown.content.strip():
        raise ReportSchemaError("Markdown artifact content is empty")
    if result.json is not None and not result.json.content.strip():
        raise ReportSchemaError("JSON artifact content is empty")
    if result.pdf is not None:
        if not result.pdf.content.startswith(b"%PDF"):
            raise ReportSchemaError("PDF artifact is not a valid PDF")
