"""Report architecture package."""

from __future__ import annotations

from engines.interpretation_engine.report.report_builder_interface import ReportBuilderInterface
from engines.interpretation_engine.report.report_model import InterpretationReportModel

__all__ = [
    "InterpretationReportModel",
    "ReportBuilderInterface",
]
