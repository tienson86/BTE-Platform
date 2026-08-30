"""Apply and strip registered conversation transitions."""

from __future__ import annotations

from engines.narrative_v2.conversation.conversation_registry import ALLOWED_TRANSITIONS

TRANSITION_SUFFIX = ", "


def apply_transition(connector: str, text: str) -> str:
    """Prefix a registered connector. Does not edit the following sentence."""
    if connector not in ALLOWED_TRANSITIONS:
        raise ValueError(f"Unregistered transition: {connector}")
    body = text.strip()
    if not body:
        return ""
    return f"{connector}{TRANSITION_SUFFIX}{body}"


def strip_transition(text: str) -> str:
    """Remove a leading registered connector, if present."""
    stripped = text.strip()
    for connector in sorted(ALLOWED_TRANSITIONS, key=len, reverse=True):
        prefix = f"{connector}{TRANSITION_SUFFIX}"
        if stripped.startswith(prefix):
            return stripped[len(prefix) :].strip()
    return stripped


def leading_connector(text: str) -> str | None:
    """Return the leading registered connector, or None."""
    stripped = text.strip()
    for connector in sorted(ALLOWED_TRANSITIONS, key=len, reverse=True):
        prefix = f"{connector}{TRANSITION_SUFFIX}"
        if stripped.startswith(prefix):
            return connector
    return None
