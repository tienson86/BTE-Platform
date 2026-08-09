"""Useful God Override decision-package integration stage."""

from __future__ import annotations

from typing import Any, Mapping

from engines.decision_engine.integration.base_stage import (
    bind_decision_payload,
    merge_declared_values,
    require_upstream,
    snapshot_subset,
)
from engines.decision_engine.pipeline.decision_context import DecisionExecutionContext
from engines.decision_engine.pipeline.package_loader import LoadedPackage
from engines.decision_engine.pipeline.stage_registry import OVERRIDE_INPUTS, OVERRIDE_OUTPUTS


class UsefulGodOverrideStage:
    """Bind Useful God Override. Does not recompute Foundation or Priority."""

    stage_id: str = "useful_god_override"
    package_id: str = "bz_08_useful_god_override"

    def dependencies(self) -> tuple[str, ...]:
        """Override consumes Foundation and Priority outputs."""
        return ("useful_god_foundation", "useful_god_priority")

    def execute(
        self,
        context: DecisionExecutionContext,
        package: LoadedPackage,
    ) -> Mapping[str, Any]:
        """Publish Override binding. Legal override only from published diagnostics."""
        require_upstream(context, self.stage_id, self.dependencies())
        priority = context.priority_result or {}
        diagnostics = list(
            context.snapshot.get("resolution_diagnostics")
            or priority.get("resolution_diagnostics")
            or []
        )
        applied = bool(context.snapshot.get("override_applied", False))
        reason = str(context.snapshot.get("override_reason", "none"))
        if not applied and any(
            marker in diagnostics
            for marker in ("contradiction", "follow_pattern", "transformation")
        ):
            applied = True
            reason = next(
                marker
                for marker in ("transformation", "follow_pattern", "contradiction")
                if marker in diagnostics
            )
        resolved = priority.get("resolved_useful_god")
        final_god = context.snapshot.get("final_useful_god")
        if final_god is None:
            final_god = "withheld" if (applied and reason == "contradiction") else resolved
        published = merge_declared_values(
            declared=OVERRIDE_OUTPUTS,
            snapshot=context.snapshot,
            upstream={
                "final_useful_god": final_god,
                "final_favorable_gods": priority.get("resolved_favorable_gods"),
                "final_unfavorable_gods": priority.get("resolved_unfavorable_gods"),
                "override_applied": applied,
                "override_reason": reason,
                "override_confidence": (
                    "low" if applied else priority.get("resolution_confidence")
                ),
                "decision_trace": {
                    "upstream_decision": resolved,
                    "override_applied": applied,
                    "override_reason": reason,
                },
                "decision_audit": {
                    "upstream_untouched": True,
                    "new_outputs_only": True,
                    "override_applied": applied,
                },
            },
        )
        payload = bind_decision_payload(
            stage_id=self.stage_id,
            package=package,
            produced_signals=OVERRIDE_OUTPUTS,
            consumed_signals=OVERRIDE_INPUTS,
            upstream_stages=self.dependencies(),
            snapshot_facts=snapshot_subset(context.snapshot, OVERRIDE_INPUTS),
            published_values=published,
        )
        context.publish(
            self.stage_id,
            payload,
            declared_outputs=OVERRIDE_OUTPUTS,
        )
        return payload
