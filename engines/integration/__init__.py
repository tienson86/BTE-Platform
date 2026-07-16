"""
BTE Platform - Integration Layer.

Integration Layer chịu trách nhiệm điều phối toàn bộ Pipeline:

    Calendar Engine
            │
            ▼
      Bazi Engine
            │
            ▼
     Score Engine
            │
            ▼
    Pattern Engine
            │
            ▼
Interpretation Engine
            │
            ▼
     Report Engine

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
