"""Summary Engine package.

Importable implementation of Analysis Engine stage 09 (Summary).

Architecture documentation lives in:
``engines/analysis_engine/09_summary_engine/``
"""

from __future__ import annotations

from engines.analysis_engine.summary_engine.engine import SummaryEngine
from engines.analysis_engine.summary_engine.exceptions import (
    SummaryConsistencyError,
    SummaryEngineError,
    SummaryExecutionError,
    SummaryPrerequisiteError,
    SummaryValidationError,
)
from engines.analysis_engine.summary_engine.models import (
    UPSTREAM_STAGES,
    ConsistencyIssue,
    ConsolidatedConfidenceSummary,
    CrossStageConsistencyReport,
    DomainSummaryView,
    EvidenceIndexEntry,
    SummaryResult,
)

__all__ = [
    "UPSTREAM_STAGES",
    "ConsistencyIssue",
    "ConsolidatedConfidenceSummary",
    "CrossStageConsistencyReport",
    "DomainSummaryView",
    "EvidenceIndexEntry",
    "SummaryConsistencyError",
    "SummaryEngine",
    "SummaryEngineError",
    "SummaryExecutionError",
    "SummaryPrerequisiteError",
    "SummaryResult",
    "SummaryValidationError",
]

__version__ = "1.0.0"
