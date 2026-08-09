"""Shared helpers for Decision Package integration stages."""

from __future__ import annotations

from typing import Any, Mapping

from engines.decision_engine.exceptions import DependencyViolationError
from engines.decision_engine.pipeline.decision_context import DecisionExecutionContext
from engines.decision_engine.pipeline.package_loader import LoadedPackage


def require_upstream(
    context: DecisionExecutionContext,
    stage_id: str,
    required_stages: tuple[str, ...],
) -> None:
    """Reject execution when required upstream stage outputs are absent."""
    missing = [item for item in required_stages if not context.has_result(item)]
    if missing:
        raise DependencyViolationError(
            f"missing_inputs:{stage_id}:{','.join(missing)}"
        )


def snapshot_subset(snapshot: Mapping[str, Any], keys: tuple[str, ...]) -> dict[str, Any]:
    """Copy selected published snapshot facts without transforming them."""
    return {key: snapshot[key] for key in keys if key in snapshot}


def merge_declared_values(
    *,
    declared: tuple[str, ...],
    snapshot: Mapping[str, Any],
    upstream: Mapping[str, Any],
    defaults: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Resolve declared outputs from snapshot, then upstream, then defaults."""
    values: dict[str, Any] = {}
    fallback = dict(defaults or {})
    for name in declared:
        if name in snapshot:
            values[name] = snapshot[name]
        elif name in upstream:
            values[name] = upstream[name]
        elif name in fallback:
            values[name] = fallback[name]
    return values


def bind_decision_payload(
    *,
    stage_id: str,
    package: LoadedPackage,
    produced_signals: tuple[str, ...],
    consumed_signals: tuple[str, ...],
    upstream_stages: tuple[str, ...],
    snapshot_facts: Mapping[str, Any],
    published_values: Mapping[str, Any],
) -> dict[str, Any]:
    """Build a binding payload. Does not evaluate package rules."""
    payload: dict[str, Any] = {
        "stage_id": stage_id,
        "package_id": package.package_id,
        "package_version": package.package_version,
        "schema_version": package.schema_version,
        "knowledge_version": package.knowledge_version,
        "compatibility_version": package.compatibility_version,
        "status": "bound",
        "rule_count": package.rule_count,
        "rule_ids": package.rule_ids[:8],
        "produced_signals": produced_signals,
        "consumed_signals": consumed_signals,
        "upstream_stages": upstream_stages,
        "snapshot_facts": dict(snapshot_facts),
    }
    payload.update(dict(published_values))
    return payload
