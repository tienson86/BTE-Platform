"""ConversationValidator — flow-only contract. Meaning must not change."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.conversation.conversation_errors import ConversationValidationError
from engines.narrative_v2.conversation.conversation_flow import (
    meaning_hash,
    sentence_set_hash,
    split_sentences,
)
from engines.narrative_v2.conversation.conversation_registry import ALLOWED_TRANSITIONS, FLOW_STAGES
from engines.narrative_v2.conversation.conversation_transition import leading_connector
from engines.narrative_v2.conversation.conversation_context import (
    ALLOWED_STATUSES,
    ConversationNarrative,
)
from engines.narrative_v2.interpretation.interpretation_model import InterpretationNarrative
from engines.narrative_v2.rewrite.rewrite_context import CommercialRewriteContext

ACTION_MARKERS: tuple[str, ...] = (
    "You should",
    "Bạn nên",
    "Action Plan",
    "Priority:",
)

PREDICTION_MARKERS: tuple[str, ...] = (
    "You will",
    "Definitely",
    "Surely",
    "Guaranteed",
    "chắc chắn",
    "nhất định",
)


@dataclass(slots=True)
class ConversationValidationOutcome:
    """Conversation contract result."""

    passed: bool
    reason: str = ""

    @property
    def status(self) -> str:
        """PASS or FAIL."""
        return "PASS" if self.passed else "FAIL"


class ConversationValidator:
    """Validate ConversationNarrative against N-IMP-07A rules."""

    def validate(
        self,
        conversation: ConversationNarrative,
        interpretation: InterpretationNarrative,
        rewrite: CommercialRewriteContext,
    ) -> ConversationValidationOutcome:
        """PASS unless flow or meaning-preservation is violated."""
        try:
            self.assert_valid(conversation, interpretation, rewrite)
        except ConversationValidationError as exc:
            return ConversationValidationOutcome(passed=False, reason=exc.message)
        return ConversationValidationOutcome(passed=True)

    def assert_valid(
        self,
        conversation: ConversationNarrative,
        interpretation: InterpretationNarrative,
        rewrite: CommercialRewriteContext,
    ) -> None:
        """Raise if conversation violates the flow contract."""
        del rewrite
        if conversation.status not in ALLOWED_STATUSES:
            raise ConversationValidationError(
                f"Invalid conversation status: {conversation.status}"
            )
        if conversation.meaning != interpretation.meaning:
            raise ConversationValidationError("Meaning must not change")
        if conversation.recommendation != interpretation.recommendation:
            raise ConversationValidationError("Recommendation must not change")
        if meaning_hash(conversation.meaning) != meaning_hash(interpretation.meaning):
            raise ConversationValidationError("Meaning hash mismatch")
        self._check_sentence_set(conversation, interpretation)
        self._check_transitions(conversation.flow)
        self._check_language(conversation.flow)

    def _check_sentence_set(
        self,
        conversation: ConversationNarrative,
        interpretation: InterpretationNarrative,
    ) -> None:
        before = sentence_set_hash(tuple(getattr(interpretation, stage) for stage in FLOW_STAGES))
        after_fields = sentence_set_hash(
            tuple(getattr(conversation, stage) for stage in FLOW_STAGES)
        )
        if after_fields != before:
            raise ConversationValidationError("Conversation dropped or added meaning sentences")
        flow_hash = sentence_set_hash((conversation.flow,))
        if flow_hash != before:
            raise ConversationValidationError("Flow dropped or added meaning sentences")

    def _check_transitions(self, flow: str) -> None:
        for sentence in split_sentences(flow):
            connector = leading_connector(sentence)
            if connector is None:
                continue
            if connector not in ALLOWED_TRANSITIONS:
                raise ConversationValidationError("Unregistered transition in flow")

    def _check_language(self, flow: str) -> None:
        for token in ACTION_MARKERS:
            if token in flow:
                raise ConversationValidationError("Action generated in conversation")
        for token in PREDICTION_MARKERS:
            if token in flow:
                raise ConversationValidationError("Prediction generated in conversation")
        if "{" in flow or "}" in flow:
            raise ConversationValidationError("JSON/debug leak in conversation")
