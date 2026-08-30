"""Action Builder — Decision → Priority → ActionPlanNarrative.

Does not invent astrology. Does not explain Meaning.
"""

from __future__ import annotations

import logging

from engines.narrative_v2.action.action_errors import ActionError
from engines.narrative_v2.action.action_model import (
    ACTION_VERSION,
    MIN_ACTIONS_FOR_COMPLETE,
    ActionPlanNarrative,
    ActionReference,
    STATUS_INSUFFICIENT,
    STATUS_PARTIAL,
)
from engines.narrative_v2.action.action_selector import ActionSelector
from engines.narrative_v2.action.action_validator import ActionValidator
from engines.narrative_v2.action.decision_builder import DecisionBuilder
from engines.narrative_v2.action.decision_model import DecisionItem
from engines.narrative_v2.action.priority_selector import PrioritySelector
from engines.narrative_v2.interpretation.interpretation_model import InterpretationNarrative
from engines.narrative_v2.rewrite.rewrite_context import CommercialRewriteContext

logger = logging.getLogger(__name__)

_CONTEXT_METADATA: tuple[tuple[str, str], ...] = (
    ("shadow_mode", "true"),
    ("replaces_pack05", "false"),
    ("portal_connected", "false"),
    ("layer", "action"),
    ("action_version", ACTION_VERSION),
    ("ck01_mapped", "false"),
    ("current_period_source", "none"),
)


class ActionBuilder:
    """Assemble ActionPlanNarrative after Meaning is available."""

    def __init__(
        self,
        *,
        decisions: DecisionBuilder | None = None,
        priorities: PrioritySelector | None = None,
        actions: ActionSelector | None = None,
        validator: ActionValidator | None = None,
    ) -> None:
        self._decisions = decisions or DecisionBuilder()
        self._priorities = priorities or PrioritySelector()
        self._actions = actions or ActionSelector()
        self._validator = validator or ActionValidator()

    def build(
        self,
        rewrite_context: object,
        interpretation: object,
        consulting: object | None = None,
    ) -> ActionPlanNarrative:
        """Build an Action Plan from rewrite + interpretation. Consulting is optional."""
        del consulting
        rewrite = _require_rewrite(rewrite_context)
        narrative = _require_interpretation(interpretation)
        if narrative.status == "insufficient" or not narrative.meaning:
            plan = _insufficient(_CONTEXT_METADATA)
            self._validator.assert_valid(plan, rewrite, ())
            return plan
        context = self._decisions.build(rewrite, narrative)
        if not context.items:
            plan = _insufficient(
                _CONTEXT_METADATA + (("status_reason", "no_approved_decision_asset"),)
            )
            self._validator.assert_valid(plan, rewrite, ())
            return plan
        top = self._priorities.select(context.items)
        actions = self._actions.select_actions(context.items, rewrite)
        warnings = self._actions.select_warnings(context.items, rewrite)
        if actions and top is None:
            raise ActionError("Decision required before Action")
        plan = _assemble(rewrite, context.items, top, actions, warnings)
        logger.info(
            "action.assembled",
            extra={"status": plan.status, "actions": len(plan.actions)},
        )
        self._validator.assert_valid(plan, rewrite, context.items)
        return plan


def _require_rewrite(value: object) -> CommercialRewriteContext:
    if isinstance(value, CommercialRewriteContext):
        return value
    raise ActionError("Action Builder accepts CommercialRewriteContext only")


def _require_interpretation(value: object) -> InterpretationNarrative:
    if isinstance(value, InterpretationNarrative):
        return value
    raise ActionError("Action Builder accepts InterpretationNarrative only")


def _insufficient(base_meta: tuple[tuple[str, str], ...]) -> ActionPlanNarrative:
    return ActionPlanNarrative(
        top_priority=None,
        actions=(),
        warnings=(),
        current_period=None,
        references=(),
        metadata=base_meta + (("status_reason", "no_action_capable_content"),),
        status=STATUS_INSUFFICIENT,
    )


def _assemble(
    rewrite: CommercialRewriteContext,
    decisions: tuple[DecisionItem, ...],
    top: object,
    actions: tuple[object, ...],
    warnings: tuple[object, ...],
) -> ActionPlanNarrative:
    unresolved = tuple(entry.semantic_key for entry in rewrite.unresolved)
    enough = len(actions) >= MIN_ACTIONS_FOR_COMPLETE and top is not None
    status = STATUS_PARTIAL
    if enough and not unresolved:
        status = "complete"
    refs: list[ActionReference] = []
    if top is not None:
        chosen = next(item for item in decisions if item.decision_id == getattr(top, "decision_id"))
        refs.append(
            ActionReference(
                field="top_priority",
                rewrite_ids=chosen.source_rewrite_ids,
                knowledge_ids=chosen.source_knowledge_ids,
                reasoning_ids=chosen.source_reasoning_ids,
                evidence_ids=chosen.source_evidence_ids,
                decision_ids=(chosen.decision_id,),
            )
        )
    for action in actions:
        refs.extend(action.references)
    for warning in warnings:
        refs.extend(warning.references)
    meta = _CONTEXT_METADATA + (
        ("decision_count", str(len(decisions))),
        ("action_count", str(len(actions))),
        ("warning_count", str(len(warnings))),
    )
    if unresolved:
        meta = meta + (("rewrite_unresolved", ",".join(unresolved)),)
    return ActionPlanNarrative(
        top_priority=top,
        actions=actions,
        warnings=warnings,
        current_period=None,
        references=tuple(refs),
        metadata=meta,
        status=status,
    )
