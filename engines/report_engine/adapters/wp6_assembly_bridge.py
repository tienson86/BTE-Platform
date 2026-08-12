"""Compatibility layer: ReportInputV1 → WP6 ReportBuilder."""

from __future__ import annotations

from typing import Any

from engines.report_engine.contracts.report_input_v1 import ReportInputV1
from engines.report_engine.report import ReportModel
from engines.report_engine.service import ReportService


def report_input_to_interpretation_dict(report_input: ReportInputV1) -> dict[str, Any]:
    """Convert ReportInputV1 into the dict shape expected by WP6 ReportBuilder."""
    sections: dict[str, Any] = {}
    for section in report_input.interpretation.sections:
        sections[section.id or section.title] = {
            "name": section.title,
            "title": section.title,
            "content": section.content,
            "body": section.content,
            "rules": [],
            "score": 0,
        }
    strengths = [
        {"title": item, "description": item}
        for item in report_input.interpretation.recommendations
    ]
    weaknesses = [
        {"title": item, "description": item}
        for item in report_input.interpretation.warnings
    ]
    return {
        "summary": report_input.interpretation.executive_summary,
        "sections": sections,
        "confidence": report_input.interpretation.confidence or 0.0,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "warnings": weaknesses,
        "score": {
            "overall": report_input.strength.score or 0.0,
            "rating": report_input.strength.level,
        },
        "metadata": {
            "subject_name": report_input.profile.full_name,
            "case_id": report_input.metadata.case_id,
        },
    }


def build_report_model_from_input(
    report_input: ReportInputV1,
    *,
    service: ReportService | None = None,
) -> ReportModel:
    """Feed ReportInputV1 into WP6 Report Assembly via compatibility adapter."""
    payload = report_input_to_interpretation_dict(report_input)
    builder_service = service or ReportService()
    return builder_service.build(payload)
