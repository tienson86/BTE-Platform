"""ConsultingStyleValidator — meaning-preserving style contract."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.communication.communication_context import (
    ALLOWED_STATUSES,
    ConsultingNarrative,
)
from engines.narrative_v2.communication.communication_errors import ConsultingStyleValidationError
from engines.narrative_v2.communication.consulting_style import semantic_fingerprint
from engines.narrative_v2.communication.consulting_style_profile import DEFAULT_PROFILE_ID
from engines.narrative_v2.communication.consulting_style_registry import ESCALATION_TERMS
from engines.narrative_v2.conversation.conversation_context import ConversationNarrative
from engines.narrative_v2.conversation.conversation_flow import join_sentences
from engines.narrative_v2.conversation.conversation_registry import FLOW_STAGES

ACTION_MARKERS: tuple[str, ...] = (
    "You should",
    "Bạn nên",
    "Action Plan",
    "Priority:",
    "màu đỏ",
    "hướng Nam",
)

PREDICTION_MARKERS: tuple[str, ...] = (
    "You will",
    "Definitely",
    "chắc chắn",
    "nhất định",
    "sẽ luôn",
)

TECHNICAL_LEAK: tuple[str, ...] = (
    "Engine",
    "NR-REL",
    "CanonicalAnalysis",
    "JSON",
    "{{",
)


@dataclass(slots=True)
class ConsultingStyleValidationOutcome:
    """Consulting Style contract result."""

    passed: bool
    reason: str = ""

    @property
    def status(self) -> str:
        """PASS or FAIL."""
        return "PASS" if self.passed else "FAIL"


class ConsultingStyleValidator:
    """Validate ConsultingNarrative against N-IMP-07B rules."""

    def validate(
        self,
        consulting: ConsultingNarrative,
        conversation: ConversationNarrative,
    ) -> ConsultingStyleValidationOutcome:
        """PASS unless meaning or safety is violated."""
        try:
            self.assert_valid(consulting, conversation)
        except ConsultingStyleValidationError as exc:
            return ConsultingStyleValidationOutcome(passed=False, reason=exc.message)
        return ConsultingStyleValidationOutcome(passed=True)

    def assert_valid(
        self,
        consulting: ConsultingNarrative,
        conversation: ConversationNarrative,
    ) -> None:
        """Raise if consulting style violates the contract."""
        if consulting.status not in ALLOWED_STATUSES:
            raise ConsultingStyleValidationError(
                f"Invalid consulting status: {consulting.status}"
            )
        if consulting.style_profile != DEFAULT_PROFILE_ID:
            raise ConsultingStyleValidationError("Invalid consulting profile")
        before = _conversation_fingerprint(conversation)
        after = semantic_fingerprint(consulting.flow)
        if after != before:
            raise ConsultingStyleValidationError("Meaning fingerprint mismatch")
        self._check_language(consulting.flow)
        self._check_capitalization(consulting.flow)


    def _check_language(self, flow: str) -> None:
        blob = flow
        for token in ACTION_MARKERS:
            if token in blob:
                raise ConsultingStyleValidationError("Action generated in consulting style")
        for token in PREDICTION_MARKERS:
            if token in blob:
                raise ConsultingStyleValidationError("Prediction generated in consulting style")
        for token in ESCALATION_TERMS:
            if token in blob:
                raise ConsultingStyleValidationError("Semantic escalation in consulting style")
        for token in TECHNICAL_LEAK:
            if token in blob:
                raise ConsultingStyleValidationError("Raw technical id in consulting style")
        if "{" in blob or "}" in blob:
            raise ConsultingStyleValidationError("JSON/debug leak in consulting style")

    def _check_capitalization(self, flow: str) -> None:
        if ", Bạn" in flow:
            raise ConsultingStyleValidationError(
                "Vietnamese capitalization after comma is incorrect"
            )


def _conversation_fingerprint(conversation: ConversationNarrative) -> str:
    texts = tuple(getattr(conversation, stage) for stage in FLOW_STAGES)
    return semantic_fingerprint(join_sentences(tuple(text for text in texts if text)))
