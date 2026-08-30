"""ActionValidator — Decision-before-Action and customer-safety checks."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.action.action_errors import ActionValidationError
from engines.narrative_v2.action.action_model import (
    ALLOWED_STATUSES,
    MAX_ACTIONS,
    ActionItem,
    ActionPlanNarrative,
)
from engines.narrative_v2.action.decision_model import DecisionItem
from engines.narrative_v2.rewrite.rewrite_context import CommercialRewriteContext

FORBIDDEN_CONTEXT_ATTRS: tuple[str, ...] = (
    "canonical_analysis",
    "presentation",
    "action_plan",
)

UNSUPPORTED_ACTIONS: tuple[str, ...] = (
    "hãy mở rộng mạnh hơn",
    "hãy học thêm",
    "dùng màu đỏ",
    "hướng Nam",
    "hãy kết hôn",
    "hãy mở rộng kinh doanh",
    "nên dùng màu đỏ",
    "nên đi hướng Nam",
)

FEAR_LANGUAGE: tuple[str, ...] = (
    "Nguy hiểm",
    "Đại hung",
    "Tai họa",
    "rất nguy hiểm",
)

PREDICTION_MARKERS: tuple[str, ...] = (
    "chắc chắn",
    "nhất định",
    "You will",
)

SHORTHAND: tuple[str, ...] = (
    "chỗ dưỡng",
    "nền học/dưỡng",
    "kênh thoát",
    "Dựng khung vừa đủ",
)

EXPAND_TOKENS: tuple[str, ...] = ("mở rộng", "expand")
CONSOLIDATE_TOKENS: tuple[str, ...] = ("giữ nền", "không nhận thêm", "trước khi ôm")


@dataclass(slots=True)
class ActionValidationOutcome:
    """Action contract result."""

    passed: bool
    reason: str = ""

    @property
    def status(self) -> str:
        """PASS or FAIL."""
        return "PASS" if self.passed else "FAIL"


class ActionValidator:
    """Validate ActionPlanNarrative against N-IMP-08 contract rules."""

    def validate(
        self,
        plan: ActionPlanNarrative,
        rewrite: CommercialRewriteContext,
        decisions: tuple[DecisionItem, ...],
    ) -> ActionValidationOutcome:
        """PASS unless the action contract is violated."""
        try:
            self.assert_valid(plan, rewrite, decisions)
        except ActionValidationError as exc:
            return ActionValidationOutcome(passed=False, reason=exc.message)
        return ActionValidationOutcome(passed=True)

    def assert_valid(
        self,
        plan: ActionPlanNarrative,
        rewrite: CommercialRewriteContext,
        decisions: tuple[DecisionItem, ...],
    ) -> None:
        """Raise if the plan violates the action contract."""
        for attr in FORBIDDEN_CONTEXT_ATTRS:
            if hasattr(plan, attr) and attr != "status":
                if attr in {"canonical_analysis", "presentation", "action_plan"}:
                    raise ActionValidationError(f"Action must not expose {attr}")
        if plan.status not in ALLOWED_STATUSES:
            raise ActionValidationError(f"Invalid action status: {plan.status}")
        if plan.status == "insufficient":
            if plan.actions:
                raise ActionValidationError("Insufficient plan must not publish actions")
            return
        self._check_decisions(plan, decisions)
        self._check_actions(plan, rewrite, decisions)
        self._check_language(plan)
        self._check_conflicts(plan)
        if len(plan.actions) > MAX_ACTIONS:
            raise ActionValidationError("Too many actions")
        expected = tuple(sorted(plan.actions, key=lambda item: (-item.priority, item.action_id)))
        if plan.actions != expected:
            raise ActionValidationError("Actions are not deterministically ordered")


    def _check_decisions(
        self,
        plan: ActionPlanNarrative,
        decisions: tuple[DecisionItem, ...],
    ) -> None:
        if plan.actions and not decisions:
            raise ActionValidationError("Decision required before Action")
        if plan.top_priority is not None:
            decision_ids = {item.decision_id for item in decisions}
            if plan.top_priority.decision_id not in decision_ids:
                raise ActionValidationError("Top Priority missing Decision")
            if len({item.decision_id for item in decisions}) >= 1:
                expected = sorted(decisions, key=lambda item: (-item.priority, item.decision_id))[0]
                if plan.top_priority.decision_id != expected.decision_id:
                    raise ActionValidationError("Top Priority is not the selected Decision")

    def _check_actions(
        self,
        plan: ActionPlanNarrative,
        rewrite: CommercialRewriteContext,
        decisions: tuple[DecisionItem, ...],
    ) -> None:
        decision_ids = {item.decision_id for item in decisions}
        knowledge_ok = {kid for item in rewrite.items for kid in item.source_knowledge_ids}
        seen: set[str] = set()
        texts: set[str] = set()
        for action in plan.actions:
            if not action.decision_id:
                raise ActionValidationError("Action missing decision_id")
            if action.decision_id not in decision_ids:
                raise ActionValidationError("Action does not reference a Decision")
            if not action.source_knowledge_ids:
                raise ActionValidationError("Action missing knowledge trace")
            for knowledge_id in action.source_knowledge_ids:
                if knowledge_id not in knowledge_ok:
                    raise ActionValidationError(f"Unknown knowledge_id: {knowledge_id}")
            if action.action_id in seen:
                raise ActionValidationError(f"Duplicate action_id: {action.action_id}")
            seen.add(action.action_id)
            folded = action.description.casefold()
            if folded in texts:
                raise ActionValidationError("Duplicate Action")
            texts.add(folded)

    def _check_language(self, plan: ActionPlanNarrative) -> None:
        blob = _blob(plan)
        for token in UNSUPPORTED_ACTIONS:
            if token in blob:
                raise ActionValidationError("Unsupported Action")
        for token in FEAR_LANGUAGE:
            if token in blob:
                raise ActionValidationError("Fear language in Action Plan")
        for token in PREDICTION_MARKERS:
            if token in blob:
                raise ActionValidationError("Prediction in Action Plan")
        for token in SHORTHAND:
            if token in blob:
                raise ActionValidationError("Consultant shorthand in Action Plan")
        if "{" in blob or "}" in blob:
            raise ActionValidationError("JSON/debug leak in Action Plan")
        if "Engine" in blob or "NR-REL" in blob:
            raise ActionValidationError("Technical leak in Action Plan")

    def _check_conflicts(self, plan: ActionPlanNarrative) -> None:
        blob = _blob(plan).casefold()
        has_expand = any(token in blob for token in EXPAND_TOKENS)
        has_consolidate = any(token in blob for token in CONSOLIDATE_TOKENS)
        if has_expand and has_consolidate:
            raise ActionValidationError("Contradictory Actions")


def _blob(plan: ActionPlanNarrative) -> str:
    parts: list[str] = []
    if plan.top_priority is not None:
        parts.append(plan.top_priority.title)
        parts.append(plan.top_priority.description)
    for action in plan.actions:
        parts.append(action.title)
        parts.append(action.description)
    for warning in plan.warnings:
        parts.append(warning.title)
        parts.append(warning.description)
    return " ".join(parts)
