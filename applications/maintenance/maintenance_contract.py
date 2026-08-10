"""Maintenance mode contracts. No runtime enforcement."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

MaintenanceModeName = Literal[
    "normal",
    "maintenance",
    "read_only",
    "drain",
    "startup",
    "shutdown",
]


@dataclass(slots=True, frozen=True)
class MaintenanceState:
    """Declared maintenance state. Not applied to the process."""

    mode: MaintenanceModeName
    accepts_traffic: bool
    accepts_writes: bool
    draining: bool
    message: str
    implemented: bool = False
