"""Pack 03 shared runtime contracts and base types."""

from __future__ import annotations

from engines.interpretation_engine.runtime.base import BaseRuntime
from engines.interpretation_engine.runtime.contracts import (
    HealthStatus,
    RuntimeContract,
    RuntimeExecuteResult,
    RuntimeMetricsSnapshot,
)
from engines.interpretation_engine.runtime.legacy_adapter import LegacyContextAdapter
from engines.interpretation_engine.runtime.registry_base import BaseRegistry

__all__ = [
    "BaseRegistry",
    "BaseRuntime",
    "HealthStatus",
    "LegacyContextAdapter",
    "RuntimeContract",
    "RuntimeExecuteResult",
    "RuntimeMetricsSnapshot",
]
