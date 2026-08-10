"""Operational context contract. No runtime control plane."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

EnvironmentName = Literal["development", "beta", "production"]
NodeRole = Literal["api", "portal", "nginx", "worker", "ops"]


@dataclass(slots=True)
class OperationsContext:
    """Describes where an operator is acting. Not a live process state."""

    environment: EnvironmentName
    node_role: NodeRole
    region: str = "unspecified"
    deployment_id: str = "local"
    read_only: bool = False
    maintenance: bool = False
    draining: bool = False
