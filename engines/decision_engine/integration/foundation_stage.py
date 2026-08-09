"""Useful God Foundation decision-package integration stage."""

from __future__ import annotations

from typing import Any, Mapping

from engines.decision_engine.integration.base_stage import (
    bind_decision_payload,
    merge_declared_values,
    snapshot_subset,
)
from engines.decision_engine.pipeline.decision_context import DecisionExecutionContext
from engines.decision_engine.pipeline.package_loader import LoadedPackage
from engines.decision_engine.pipeline.stage_registry import (
    FOUNDATION_INPUTS,
    FOUNDATION_OUTPUTS,
)


class UsefulGodFoundationStage:
    """Bind Useful God Foundation. Does not identify Yong Shen."""

    stage_id: str = "useful_god_foundation"
    package_id: str = "bz_06_useful_god_foundation"

    def dependencies(self) -> tuple[str, ...]:
        """Foundation is the decision pipeline root."""
        return ()

    def execute(
        self,
        context: DecisionExecutionContext,
        package: LoadedPackage,
    ) -> Mapping[str, Any]:
        """Publish Foundation binding and passthrough declared snapshot fields."""
        published = merge_declared_values(
            declared=FOUNDATION_OUTPUTS,
            snapshot=context.snapshot,
            upstream={},
            defaults={
                "useful_god": context.snapshot.get("useful_god", "withheld"),
                "favorable_gods": context.snapshot.get("favorable_gods", []),
                "unfavorable_gods": context.snapshot.get("unfavorable_gods", []),
                "decision_confidence": context.snapshot.get("decision_confidence", "none"),
                "decision_score": context.snapshot.get("decision_score", 0),
                "decision_reasoning": context.snapshot.get("decision_reasoning", ""),
                "decision_diagnostics": context.snapshot.get("decision_diagnostics", []),
            },
        )
        payload = bind_decision_payload(
            stage_id=self.stage_id,
            package=package,
            produced_signals=FOUNDATION_OUTPUTS,
            consumed_signals=FOUNDATION_INPUTS,
            upstream_stages=self.dependencies(),
            snapshot_facts=snapshot_subset(context.snapshot, FOUNDATION_INPUTS),
            published_values=published,
        )
        context.publish(
            self.stage_id,
            payload,
            declared_outputs=FOUNDATION_OUTPUTS,
        )
        return payload
