"""
BTE Platform - Integration Layer.

Integration Layer chịu trách nhiệm điều phối toàn bộ Pipeline.

Canonical order (aligned with production OrchestratorService):

    Calendar Engine
            │
            ▼
      Bazi Engine
            │
            ▼
    Pattern Engine
            │
            ▼
    RuleContext (Stage 5)
            │
            ▼
     Score Engine
            │
            ▼
Interpretation Engine
            │
            ▼
     Report Engine

Production SSOT: applications.api.services.orchestrator.OrchestratorService

Module này chỉ điều phối luồng xử lý, không chứa thuật toán
luận giải Bát Tự.
"""

from .pipeline import Pipeline
from .orchestrator import IntegrationOrchestrator

from .context import IntegrationContext
from .result import IntegrationResult

from .validator import IntegrationValidator
from .exception_handler import ExceptionHandler

from .hooks import PipelineHooks
from .config import PipelineConfig

from .stage import PipelineStage
from .event_bus import EventBus
from .events import PipelineEvents

__version__ = "1.0.0"

__all__ = [

    # Core
    "Pipeline",
    "IntegrationOrchestrator",

    # Data
    "IntegrationContext",
    "IntegrationResult",

    # Support
    "IntegrationValidator",
    "ExceptionHandler",
    "PipelineHooks",
    "PipelineConfig",

    # Stage
    "PipelineStage",

    # Event
    "EventBus",
    "PipelineEvents",
]
