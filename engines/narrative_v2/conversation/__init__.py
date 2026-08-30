"""Narrative V2 Conversation Composer public surface."""

from __future__ import annotations

from engines.narrative_v2.conversation.conversation_composer import ConversationComposer
from engines.narrative_v2.conversation.conversation_context import (
    ConversationNarrative,
    ConversationReference,
)
from engines.narrative_v2.conversation.conversation_errors import (
    ConversationError,
    ConversationValidationError,
)
from engines.narrative_v2.conversation.conversation_flow import meaning_hash
from engines.narrative_v2.conversation.conversation_registry import (
    ALLOWED_TRANSITIONS,
    FLOW_STAGES,
    ConversationRegistry,
)
from engines.narrative_v2.conversation.conversation_validator import (
    ConversationValidationOutcome,
    ConversationValidator,
)

__all__ = [
    "ALLOWED_TRANSITIONS",
    "FLOW_STAGES",
    "ConversationComposer",
    "ConversationError",
    "ConversationNarrative",
    "ConversationReference",
    "ConversationRegistry",
    "ConversationValidationError",
    "ConversationValidationOutcome",
    "ConversationValidator",
    "meaning_hash",
]
