"""Startup and graceful shutdown sequence contracts. No process control."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(slots=True, frozen=True)
class LifecycleStep:
    """One ordered lifecycle step."""

    order: int
    name: str
    description: str


STARTUP_SEQUENCE: Final[tuple[LifecycleStep, ...]] = (
    LifecycleStep(1, "load_config", "Load env from secret store. No secrets in git."),
    LifecycleStep(2, "bind_ports", "Listen on configured host/port."),
    LifecycleStep(3, "health_live", "Expose /live when the process can answer."),
    LifecycleStep(4, "health_ready", "Expose /ready when dependencies are acceptable."),
    LifecycleStep(5, "accept_traffic", "Edge may route to this instance."),
)

SHUTDOWN_SEQUENCE: Final[tuple[LifecycleStep, ...]] = (
    LifecycleStep(1, "enter_drain", "Mark instance draining. Edge stops new requests."),
    LifecycleStep(2, "complete_inflight", "Wait for in-flight requests up to drain timeout."),
    LifecycleStep(3, "stop_ready", "Fail readiness. Keep /live until exit."),
    LifecycleStep(4, "release_resources", "Close files, storage handles, log handlers."),
    LifecycleStep(5, "exit", "Process exits 0 after drain timeout or completion."),
)

DRAIN_TIMEOUT_SECONDS: Final[int] = 30


def describe_startup() -> tuple[LifecycleStep, ...]:
    """Return the startup sequence contract."""
    return STARTUP_SEQUENCE


def describe_shutdown() -> tuple[LifecycleStep, ...]:
    """Return the graceful shutdown sequence contract."""
    return SHUTDOWN_SEQUENCE
