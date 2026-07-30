"""Luck Engine package.

Importable implementation of Analysis Engine stage 08 (Luck).

Architecture documentation lives in:
``engines/analysis_engine/08_luck_engine/``

Note: Distinct from legacy ``engines.luck_engine``.
"""

from __future__ import annotations

from engines.analysis_engine.luck_engine.default_knowledge import (
    create_default_knowledge_session,
)
from engines.analysis_engine.luck_engine.engine import LuckEngine
from engines.analysis_engine.luck_engine.exceptions import (
    LuckConflictResolutionError,
    LuckEngineError,
    LuckExecutionError,
    LuckKnowledgeError,
    LuckPrerequisiteError,
    LuckValidationError,
)
from engines.analysis_engine.luck_engine.knowledge_access import (
    AssetView,
    InMemoryKnowledgeSession,
    KnowledgeSession,
    ModuleView,
)
from engines.analysis_engine.luck_engine.models import (
    LuckInteractionOutcome,
    LuckLayerOutcome,
    LuckPillar,
    LuckResult,
    RejectedAlternative,
)

__all__ = [
    "AssetView",
    "InMemoryKnowledgeSession",
    "KnowledgeSession",
    "LuckConflictResolutionError",
    "LuckEngine",
    "LuckEngineError",
    "LuckExecutionError",
    "LuckInteractionOutcome",
    "LuckKnowledgeError",
    "LuckLayerOutcome",
    "LuckPillar",
    "LuckPrerequisiteError",
    "LuckResult",
    "LuckValidationError",
    "ModuleView",
    "RejectedAlternative",
    "create_default_knowledge_session",
]

__version__ = "1.0.0"
