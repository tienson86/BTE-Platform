"""Priority engine orchestration pipeline."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from .condition_matcher import ConditionMatcher
from .execution_planner import ExecutionPlanner
from .models import ConditionMatch, PriorityData, PriorityPipelineResult
from .priority_resolver import PriorityResolver


class PriorityPipeline:
    """Orchestrate condition matching, execution planning, and resolution."""

    def __init__(self, data: PriorityData) -> None:
        self.data = data
        self.matcher = ConditionMatcher(data)
        self.planner = ExecutionPlanner(data)
        self.resolver = PriorityResolver(data)

    def run(
        self,
        context: Mapping[str, Any],
        *,
        include_unmatched: bool = False,
        completed_dependencies: set[str] | None = None,
    ) -> PriorityPipelineResult:
        """Run the full priority pipeline from raw context."""

        condition_results = self.matcher.match(
            context,
            include_unmatched=include_unmatched,
        )
        matched = tuple(item for item in condition_results if item.matched)
        plan = self.planner.plan(
            matched,
            completed_dependencies=completed_dependencies,
        )
        resolution = self.resolver.resolve(plan)
        return PriorityPipelineResult(
            matched_conditions=condition_results,
            execution_plan=plan,
            resolution=resolution,
        )

    def run_matched_rules(
        self,
        rule_ids: Iterable[str],
        *,
        completed_dependencies: set[str] | None = None,
    ) -> PriorityPipelineResult:
        """Run priority planning and resolution for already matched rule IDs."""

        normalized_rule_ids = tuple(dict.fromkeys(rule_ids))
        condition_by_rule = {
            condition.priority_rule: condition
            for condition in self.data.conditions
            if condition.priority_rule in normalized_rule_ids
        }
        condition_results = tuple(
            ConditionMatch(condition=condition_by_rule[rule_id], matched=True)
            for rule_id in normalized_rule_ids
            if rule_id in condition_by_rule
        )
        plan = self.planner.plan_rule_ids(
            normalized_rule_ids,
            completed_dependencies=completed_dependencies,
        )
        resolution = self.resolver.resolve(plan)
        return PriorityPipelineResult(
            matched_conditions=condition_results,
            execution_plan=plan,
            resolution=resolution,
        )
