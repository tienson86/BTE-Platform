"""Optional native engine sources for foundation builders."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class EngineSources:
    """Native engine outputs — avoids recalculating analytical truth."""

    useful_god_result: Any | None = None
    strength_result: Any | None = None
    temperature_result: Any | None = None
    ten_gods_result: Any | None = None
    pattern_context: Any | None = None
    rule_context: Mapping[str, Any] | None = None
