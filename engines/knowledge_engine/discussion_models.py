"""Discussion AI models for grounded conversational answers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


QuestionType = Literal[
    "why",
    "how",
    "evidence",
    "alternative_interpretation",
    "what_if_birth_time",
    "what_if_useful_god",
    "unsupported",
]

SUPPORTED_QUESTION_TYPES: tuple[str, ...] = (
    "why",
    "how",
    "evidence",
    "alternative_interpretation",
    "what_if_birth_time",
    "what_if_useful_god",
)


@dataclass(slots=True)
class DiscussionAnswer:
    """One grounded Discussion AI reply."""

    question: str
    question_type: QuestionType
    answer: str
    grounded: bool
    used_evidence: bool
    used_knowledge: bool
    used_reasoning: bool
    refused: bool = False
    refuse_reason: str = ""
    confidence: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize answer."""
        return {
            "question": self.question,
            "question_type": self.question_type,
            "answer": self.answer,
            "grounded": self.grounded,
            "used_evidence": self.used_evidence,
            "used_knowledge": self.used_knowledge,
            "used_reasoning": self.used_reasoning,
            "refused": self.refused,
            "refuse_reason": self.refuse_reason,
            "confidence": self.confidence,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class ConversationResult:
    """Multi-turn Discussion AI conversation result."""

    turns: list[DiscussionAnswer]
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def all_grounded(self) -> bool:
        """True when every non-refused turn is grounded on E/K/R."""
        answered = [turn for turn in self.turns if not turn.refused]
        return bool(answered) and all(turn.grounded for turn in answered)

    def to_dict(self) -> dict[str, Any]:
        """Serialize conversation."""
        return {
            "turns": [turn.to_dict() for turn in self.turns],
            "all_grounded": self.all_grounded,
            "metadata": dict(self.metadata),
        }
