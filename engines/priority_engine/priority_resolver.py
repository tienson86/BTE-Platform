"""Resolve conflicts between planned priority rules."""

from __future__ import annotations

from .models import ExecutionPlan, PriorityData, PriorityRule, ResolutionResult


class PriorityResolver:
    """Select accepted rules and the winning rule from an execution plan."""

    ACCEPTED_LABEL = "PL031"
    IGNORED_LABEL = "PL033"
    CONTINUE_LABEL = "PL035"
    REVIEW_LABEL = "PL037"
    FINISHED_LABEL = "PL040"

    COMPLETED_STATUS = "PL025"
    SKIPPED_STATUS = "PL024"
    CONFLICT_STATUS = "PL027"

    def __init__(self, data: PriorityData) -> None:
        self.data = data

    def resolve(self, plan: ExecutionPlan) -> ResolutionResult:
        """Resolve a planned set of rules by priority and execution order."""

        rules = tuple(step.rule for step in plan.steps)
        if not rules:
            return ResolutionResult(
                accepted_rules=(),
                rejected_rules=(),
                conflict_rules=(),
                winner=None,
                decision_label=self.IGNORED_LABEL,
                pipeline_status=self.SKIPPED_STATUS,
                reason="No priority rule matched.",
            )

        sorted_rules = tuple(sorted(rules, key=self._sort_key))
        winner = sorted_rules[0]
        top_priority_rules = tuple(
            rule for rule in sorted_rules if rule.priority == winner.priority
        )
        conflict_rules = top_priority_rules if len(top_priority_rules) > 1 else ()

        accepted_rules = self._accepted_rules(sorted_rules, winner)
        rejected_rules = tuple(rule for rule in sorted_rules if rule not in accepted_rules)
        terminate = winner.stop_processing or any(
            step.order.terminate_pipeline for step in plan.steps if step.rule.id == winner.id
        )

        if conflict_rules:
            decision_label = self.REVIEW_LABEL
            pipeline_status = self.CONFLICT_STATUS
            reason = "Multiple rules share the highest priority."
        elif terminate:
            decision_label = self.FINISHED_LABEL
            pipeline_status = self.COMPLETED_STATUS
            reason = "Winning rule terminates the priority pipeline."
        elif len(accepted_rules) > 1:
            decision_label = self.CONTINUE_LABEL
            pipeline_status = self.COMPLETED_STATUS
            reason = "Multiple compatible rules remain accepted."
        else:
            decision_label = self.ACCEPTED_LABEL
            pipeline_status = self.COMPLETED_STATUS
            reason = "Highest priority rule accepted."

        return ResolutionResult(
            accepted_rules=accepted_rules,
            rejected_rules=rejected_rules,
            conflict_rules=conflict_rules,
            winner=winner,
            decision_label=decision_label,
            pipeline_status=pipeline_status,
            terminate_pipeline=terminate,
            reason=reason,
        )

    @staticmethod
    def _sort_key(rule: PriorityRule) -> tuple[int, int]:
        return (-rule.priority, rule.execution_order)

    @staticmethod
    def _accepted_rules(
        sorted_rules: tuple[PriorityRule, ...], winner: PriorityRule
    ) -> tuple[PriorityRule, ...]:
        if winner.override_lower_rules or winner.stop_processing:
            return (winner,)

        accepted: list[PriorityRule] = []
        for rule in sorted_rules:
            if rule.priority == winner.priority or not winner.override_lower_rules:
                accepted.append(rule)
        return tuple(accepted)
