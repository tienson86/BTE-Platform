"""Interpretation Engine package.

Importable implementation that consumes AnalysisResult and produces
InterpretationResult for Report Generator.

Does not belong to Analysis Runtime stage modules (01–09).
"""

from __future__ import annotations

from engines.analysis_engine.interpretation_engine.default_knowledge import (
    create_default_knowledge_session,
)
from engines.analysis_engine.interpretation_engine.engine import InterpretationEngine
from engines.analysis_engine.interpretation_engine.exceptions import (
    InterpretationBindingError,
    InterpretationEngineError,
    InterpretationExecutionError,
    InterpretationKnowledgeError,
    InterpretationPrerequisiteError,
    InterpretationValidationError,
)
from engines.analysis_engine.interpretation_engine.knowledge_access import (
    AssetView,
    InMemoryKnowledgeSession,
    KnowledgeSession,
    ModuleView,
)
from engines.analysis_engine.interpretation_engine.models import (
    CANONICAL_SECTIONS,
    REQUIRED_ANALYSIS_STAGES,
    BoundSentence,
    BoundTemplate,
    InterpretationContext,
    InterpretationParagraph,
    InterpretationResult,
    InterpretationSection,
    SelectedSentence,
)
from engines.analysis_engine.interpretation_engine.pipeline import (
    InterpretationPipeline,
)

__all__ = [
    "CANONICAL_SECTIONS",
    "REQUIRED_ANALYSIS_STAGES",
    "AssetView",
    "BoundSentence",
    "BoundTemplate",
    "InMemoryKnowledgeSession",
    "InterpretationBindingError",
    "InterpretationContext",
    "InterpretationEngine",
    "InterpretationEngineError",
    "InterpretationExecutionError",
    "InterpretationKnowledgeError",
    "InterpretationParagraph",
    "InterpretationPipeline",
    "InterpretationPrerequisiteError",
    "InterpretationResult",
    "InterpretationSection",
    "InterpretationValidationError",
    "KnowledgeSession",
    "ModuleView",
    "SelectedSentence",
    "create_default_knowledge_session",
]

__version__ = "1.0.0"
