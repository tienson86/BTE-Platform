"""Ten Gods Engine package.

Importable implementation of Analysis Engine stage 05 (Ten Gods).

Architecture documentation lives in:
``engines/analysis_engine/05_ten_gods_engine/``
"""

from __future__ import annotations

from engines.analysis_engine.ten_gods_engine.default_knowledge import (
    create_default_knowledge_session,
)
from engines.analysis_engine.ten_gods_engine.engine import TenGodsEngine
from engines.analysis_engine.ten_gods_engine.exceptions import (
    TenGodsConflictResolutionError,
    TenGodsEngineError,
    TenGodsExecutionError,
    TenGodsKnowledgeError,
    TenGodsPrerequisiteError,
    TenGodsValidationError,
)
from engines.analysis_engine.ten_gods_engine.knowledge_access import (
    AssetView,
    InMemoryKnowledgeSession,
    KnowledgeSession,
    ModuleView,
)
from engines.analysis_engine.ten_gods_engine.models import (
    FavorabilityOutcome,
    InteractionOutcome,
    LifeAreaConcept,
    RejectedAlternative,
    RelationshipOutcome,
    TenGodPresence,
    TenGodsResult,
)

__all__ = [
    "AssetView",
    "FavorabilityOutcome",
    "InMemoryKnowledgeSession",
    "InteractionOutcome",
    "KnowledgeSession",
    "LifeAreaConcept",
    "ModuleView",
    "RejectedAlternative",
    "RelationshipOutcome",
    "TenGodPresence",
    "TenGodsConflictResolutionError",
    "TenGodsEngine",
    "TenGodsEngineError",
    "TenGodsExecutionError",
    "TenGodsKnowledgeError",
    "TenGodsPrerequisiteError",
    "TenGodsResult",
    "TenGodsValidationError",
    "create_default_knowledge_session",
]

__version__ = "1.0.0"
