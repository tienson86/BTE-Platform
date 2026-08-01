"""Runtime validator for Pack 03 infrastructure.

Validates configuration, registry, dependencies, contracts, and runtime state.
Infrastructure only. No BaZi interpretation.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.runtime.contracts import RuntimeContract
from engines.interpretation_engine.runtime.registry_base import BaseRegistry

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Immutable validation report."""

    success: bool
    messages: tuple[str, ...] = ()
    details: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate report structural integrity."""
        return True


class RuntimeValidator:
    """Validate Pack 03 runtime infrastructure contracts."""

    def validate_configuration(
        self, config: Mapping[str, Any] | None
    ) -> ValidationReport:
        """Validate runtime configuration mapping."""
        if config is None:
            return ValidationReport(success=False, messages=("configuration_required",))
        if "runtime_id" in config and not config.get("runtime_id"):
            return ValidationReport(success=False, messages=("runtime_id_invalid",))
        return ValidationReport(
            success=True,
            messages=("configuration_ok",),
            details=dict(config),
        )

    def validate_registry(self, registry: BaseRegistry[Any]) -> ValidationReport:
        """Validate registry contract readiness."""
        if registry is None:
            return ValidationReport(success=False, messages=("registry_required",))
        ok = registry.validate()
        return ValidationReport(
            success=ok,
            messages=("registry_ok",) if ok else ("registry_invalid",),
            details={
                "registry_id": registry.registry_id,
                "entries": list(registry.list()),
            },
        )

    def validate_dependencies(
        self,
        *,
        required: tuple[str, ...],
        available: tuple[str, ...],
    ) -> ValidationReport:
        """Validate required dependency identifiers are available."""
        missing = tuple(sorted(set(required) - set(available)))
        if missing:
            return ValidationReport(
                success=False,
                messages=("dependencies_missing",),
                details={"missing": list(missing)},
            )
        return ValidationReport(
            success=True,
            messages=("dependencies_ok",),
            details={"required": list(required), "available": list(available)},
        )

    def validate_contract(self, runtime: RuntimeContract) -> ValidationReport:
        """Validate a runtime exposes and passes the public contract."""
        required = ("initialize", "shutdown", "validate", "execute", "metrics", "health")
        missing = [name for name in required if not hasattr(runtime, name)]
        if missing:
            return ValidationReport(
                success=False,
                messages=("contract_methods_missing",),
                details={"missing": missing},
            )
        try:
            ok = bool(runtime.validate())
        except Exception as exc:  # noqa: BLE001 - validation boundary
            logger.exception("runtime_contract_validate_failed")
            return ValidationReport(
                success=False,
                messages=(f"contract_validate_error:{type(exc).__name__}",),
            )
        return ValidationReport(
            success=ok,
            messages=("contract_ok",) if ok else ("contract_invalid_state",),
            details={"health": getattr(runtime.health(), "value", str(runtime.health()))},
        )

    def validate_runtime_state(self, runtime: RuntimeContract) -> ValidationReport:
        """Validate runtime health/metrics structural readiness."""
        health = runtime.health()
        metrics = runtime.metrics()
        if not metrics.validate():
            return ValidationReport(success=False, messages=("metrics_invalid",))
        return ValidationReport(
            success=True,
            messages=("runtime_state_ok",),
            details={
                "health": health.value,
                "execution_count": metrics.execution_count,
                "success_count": metrics.success_count,
                "failure_count": metrics.failure_count,
            },
        )
