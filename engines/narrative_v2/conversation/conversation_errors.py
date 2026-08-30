"""Narrative V2 Conversation error model.

N-IMP-07A: flow assembly failures only. Does not rewrite Meaning.
"""

from __future__ import annotations


class ConversationError(Exception):
    """Base error for Conversation Composer."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ConversationValidationError(ConversationError):
    """Conversation contract validation failed."""
