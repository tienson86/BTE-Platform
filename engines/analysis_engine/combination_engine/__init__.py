"""Combination Engine package.

Importable implementation of Analysis Engine stage 06 (Combination).

Architecture documentation lives in:
``engines/analysis_engine/06_combination_engine/``
"""

from __future__ import annotations

from engines.analysis_engine.combination_engine.default_knowledge import (
    create_default_knowledge_session,
)
from engines.analysis_engine.combination_engine.engine import CombinationEngine
from engines.analysis_engine.combination_engine.exceptions import (
    CombinationConflictResolutionError,
    CombinationEngineError,
    CombinationExecutionError,
    CombinationKnowledgeError,
    CombinationPrerequisiteError,
    CombinationValidationError,
)
from engines.analysis_engine.combination_engine.knowledge_access import (
    AssetView,
    InMemoryKnowledgeSession,
    KnowledgeSession,
    ModuleView,
)
from engines.analysis_engine.combination_engine.models import (
    CombinationResult,
    RejectedAlternative,
    RelationOutcome,
    TransformationOutcome,
)

__all__ = [
    "AssetView",
    "CombinationConflictResolutionError",
    "CombinationEngine",
    "CombinationEngineError",
    "CombinationExecutionError",
    "CombinationKnowledgeError",
    "CombinationPrerequisiteError",
    "CombinationResult",
    "CombinationValidationError",
    "InMemoryKnowledgeSession",
    "KnowledgeSession",
    "ModuleView",
    "RejectedAlternative",
    "RelationOutcome",
    "TransformationOutcome",
    "create_default_knowledge_session",
]

__version__ = "1.0.0"
