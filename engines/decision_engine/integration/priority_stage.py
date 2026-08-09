"""Useful God Priority decision-package integration stage."""

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
from engines.decision_engine.pipeline.stage_registry import PRIORITY_INPUTS, PRIORITY_OUTPUTS


class UsefulGodPriorityStage:
    """Bind Useful God Priority. Does not recompute Foundation."""

    stage_id: str = "useful_god_priority"
    package_id: str = "bz_07_useful_god_priority"

    def dependencies(self) -> tuple[str, ...]:
        """Priority consumes Foundation outputs."""
        return ("useful_god_foundation",)

    def execute(
        self,
        context: DecisionExecutionContext,
        package: LoadedPackage,
    ) -> Mapping[str, Any]:
        """Publish Priority binding. Conflict markers pass through published diagnostics."""
        require_upstream(context, self.stage_id, self.dependencies())
        foundation = context.foundation_result or {}
        diagnostics = list(
            context.snapshot.get("decision_diagnostics")
            or foundation.get("decision_diagnostics")
            or []
        )
        conflict = context.snapshot.get("conflict_resolution")
        if conflict is None:
            conflict = (
                "applied"
                if any(
                    marker in diagnostics
                    for marker in ("multiple_candidates", "tie_candidates", "useful_in_unfavorable")
                )
                else "none"
            )
        published = merge_declared_values(
            declared=PRIORITY_OUTPUTS,
            snapshot=context.snapshot,
            upstream={
                "resolved_useful_god": foundation.get("useful_god"),
                "resolved_favorable_gods": foundation.get("favorable_gods"),
                "resolved_unfavorable_gods": foundation.get("unfavorable_gods"),
                "decision_priority": "primary",
                "conflict_resolution": conflict,
                "resolution_confidence": foundation.get("decision_confidence"),
                "resolution_reasoning": foundation.get("decision_reasoning"),
                "resolution_diagnostics": diagnostics,
            },
        )
        payload = bind_decision_payload(
            stage_id=self.stage_id,
            package=package,
            produced_signals=PRIORITY_OUTPUTS,
            consumed_signals=PRIORITY_INPUTS,
            upstream_stages=self.dependencies(),
            snapshot_facts=snapshot_subset(context.snapshot, PRIORITY_INPUTS),
            published_values=published,
        )
        context.publish(
            self.stage_id,
            payload,
            declared_outputs=PRIORITY_OUTPUTS,
        )
        return payload
