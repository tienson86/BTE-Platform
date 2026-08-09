"""Machine-readable Decision Audit for every Decision Pipeline run."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class DecisionAudit:
    """Legality and isolation audit. Always JSON-serializable."""

    contract_validation: str
    dependency_validation: str
    priority_legality: str
    override_legality: str
    upstream_preserved: bool
    new_outputs_only: bool
    deterministic_execution: bool
    version_compatibility: str
    reason_codes: tuple[str, ...] = ()
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the decision audit."""
        return {
            "contract_validation": self.contract_validation,
            "dependency_validation": self.dependency_validation,
            "priority_legality": self.priority_legality,
            "override_legality": self.override_legality,
            "upstream_preserved": self.upstream_preserved,
            "new_outputs_only": self.new_outputs_only,
            "deterministic_execution": self.deterministic_execution,
            "version_compatibility": self.version_compatibility,
            "reason_codes": list(self.reason_codes),
            "details": dict(self.details),
        }


def passing_audit(*, reason_codes: tuple[str, ...] = ()) -> DecisionAudit:
    """Return an audit for a fully legal successful run."""
    return DecisionAudit(
        contract_validation="pass",
        dependency_validation="pass",
        priority_legality="pass",
        override_legality="pass",
        upstream_preserved=True,
        new_outputs_only=True,
        deterministic_execution=True,
        version_compatibility="pass",
        reason_codes=reason_codes,
    )


def failing_audit(reason: str, *, reason_codes: tuple[str, ...] = ()) -> DecisionAudit:
    """Return an audit for a stopped run. Upstream remains preserved."""
    codes = reason_codes or (reason,)
    failed = "fail" if reason else "fail"
    return DecisionAudit(
        contract_validation=failed if "version" in reason or "contract" in reason or "schema" in reason else "pass",
        dependency_validation="fail" if "prerequisite" in reason or "missing_inputs" in reason or "unknown_stages" in reason else "pass",
        priority_legality="not_run" if "fail" in failed else "pass",
        override_legality="not_run",
        upstream_preserved=True,
        new_outputs_only=True,
        deterministic_execution=True,
        version_compatibility="fail" if "version" in reason else "pass",
        reason_codes=codes,
        details={"stop_reason": reason},
    )
