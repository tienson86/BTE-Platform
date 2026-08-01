"""Interpretation Engine models (legacy + Pack 03 architecture/output)."""

from __future__ import annotations

from engines.interpretation_engine.models.context import InterpretationContext
from engines.interpretation_engine.models.final_analysis_input import FinalAnalysisInput
from engines.interpretation_engine.models.interpretation_context_model import (
    InterpretationContextModel,
)
from engines.interpretation_engine.models.interpretation_result import InterpretationResult
from engines.interpretation_engine.models.interpretation_result_model import (
    InterpretationResultModel,
)
from engines.interpretation_engine.models.interpretation_section_model import (
    InterpretationSectionModel,
)
from engines.interpretation_engine.models.metadata import Metadata
from engines.interpretation_engine.models.paragraph_result import ParagraphResult
from engines.interpretation_engine.models.report import (
    InterpretationReport,
    ReportParagraph,
    ReportSection,
)
from engines.interpretation_engine.models.rule import Rule
from engines.interpretation_engine.models.rule_result import RuleResult
from engines.interpretation_engine.models.section_result import SectionResult
from engines.interpretation_engine.models.sentence_result import SentenceResult
from engines.interpretation_engine.models.trace_information import TraceInformation
from engines.interpretation_engine.models.version_info import VersionInfo

__all__ = [
    # Legacy
    "InterpretationContext",
    "InterpretationReport",
    "ReportParagraph",
    "ReportSection",
    "Rule",
    "RuleResult",
    # Pack 03 architecture shells
    "FinalAnalysisInput",
    "InterpretationContextModel",
    "InterpretationResultModel",
    "InterpretationSectionModel",
    # Pack 03 interpretation output models
    "InterpretationResult",
    "Metadata",
    "ParagraphResult",
    "SectionResult",
    "SentenceResult",
    "TraceInformation",
    "VersionInfo",
]
