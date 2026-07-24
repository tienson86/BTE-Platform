"""Execution planning for matched priority rules."""

from __future__ import annotations

from collections.abc import Iterable

from .models import ConditionMatch, ExecutionPlan, ExecutionStep, PriorityData


class ExecutionPlanner:
    """Build an ordered execution plan using ``priority_order.json``."""

    def __init__(self, data: PriorityData) -> None:
        self.data = data

    def plan(
        self,
        matched_conditions: Iterable[ConditionMatch],
        *,
        completed_dependencies: set[str] | None = None,
    ) -> ExecutionPlan:
        """Create an execution plan for matched conditions.

        ``depends_on`` entries may point to either priority rule IDs (``PR...``)
        or priority order IDs (``PO...``). This keeps the planner tolerant of
        both styles used in early BTE data drafts.
        """

        matched_by_rule = {
            item.priority_rule: item for item in matched_conditions if item.matched
        }
        return self.plan_rule_ids(
            set(matched_by_rule),
            completed_dependencies=completed_dependencies,
            matched_by_rule=matched_by_rule,
        )

    def plan_rule_ids(
        self,
        rule_ids: Iterable[str],
        *,
        completed_dependencies: set[str] | None = None,
        matched_by_rule: dict[str, ConditionMatch] | None = None,
    ) -> ExecutionPlan:
        """Create an execution plan from already matched priority rule IDs."""

        completed = set(completed_dependencies or set())
        matched_by_rule = matched_by_rule or {}
        available_rule_ids = set(rule_ids)
        orders_by_rule = self.data.orders_by_rule_id
        rules_by_id = self.data.rules_by_id

        skipped: list[str] = []
        steps: list[ExecutionStep] = []
        executed_rule_ids: set[str] = set()
        executed_order_ids: set[str] = set()

        for rule_id in sorted(
            available_rule_ids,
            key=lambda item: orders_by_rule[item].stage
            if item in orders_by_rule
            else rules_by_id[item].execution_order,
        ):
            rule = rules_by_id.get(rule_id)
            order = orders_by_rule.get(rule_id)
            if rule is None or order is None or not rule.enabled or not order.enabled:
                skipped.append(rule_id)
                continue

            if not self._dependencies_satisfied(
                order.depends_on,
                completed | executed_rule_ids | executed_order_ids | available_rule_ids,
            ):
                skipped.append(rule_id)
                continue

            step = ExecutionStep(
                order=order,
                rule=rule,
                condition=None
                if rule_id not in matched_by_rule
                else matched_by_rule[rule_id].condition,
            )
            steps.append(step)
            executed_rule_ids.add(rule.id)
            executed_order_ids.add(order.id)

            if order.terminate_pipeline or rule.stop_processing:
                break

        return ExecutionPlan(steps=tuple(steps), skipped=tuple(skipped))

    @staticmethod
    def _dependencies_satisfied(
        dependencies: Iterable[str], available_ids: set[str]
    ) -> bool:
        return all(item in available_ids for item in dependencies)
