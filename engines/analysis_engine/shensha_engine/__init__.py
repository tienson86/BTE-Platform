"""ShenSha Engine package.

Importable implementation of Analysis Engine stage 07 (ShenSha).

Architecture documentation lives in:
``engines/analysis_engine/07_shensha_engine/``
"""

from __future__ import annotations

from engines.analysis_engine.shensha_engine.default_knowledge import (
    create_default_knowledge_session,
)
from engines.analysis_engine.shensha_engine.engine import ShenShaEngine
from engines.analysis_engine.shensha_engine.exceptions import (
    ShenShaConflictResolutionError,
    ShenShaEngineError,
    ShenShaExecutionError,
    ShenShaKnowledgeError,
    ShenShaPrerequisiteError,
    ShenShaValidationError,
)
from engines.analysis_engine.shensha_engine.knowledge_access import (
    AssetView,
    InMemoryKnowledgeSession,
    KnowledgeSession,
    ModuleView,
)
from engines.analysis_engine.shensha_engine.models import (
    CompatibilityOutcome,
    ExceptionOutcome,
    InteractionOutcome,
    RejectedAlternative,
    ShenShaPresence,
    ShenShaResult,
)

__all__ = [
    "AssetView",
    "CompatibilityOutcome",
    "ExceptionOutcome",
    "InMemoryKnowledgeSession",
    "InteractionOutcome",
    "KnowledgeSession",
    "ModuleView",
    "RejectedAlternative",
    "ShenShaConflictResolutionError",
    "ShenShaEngine",
    "ShenShaEngineError",
    "ShenShaExecutionError",
    "ShenShaKnowledgeError",
    "ShenShaPresence",
    "ShenShaPrerequisiteError",
    "ShenShaResult",
    "ShenShaValidationError",
    "create_default_knowledge_session",
]

__version__ = "1.0.0"
