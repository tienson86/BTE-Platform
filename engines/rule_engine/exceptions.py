"""Rule Engine exceptions."""

from __future__ import annotations


class RuleEngineError(Exception):
    """Base Rule Engine error."""


class RuleLoadError(RuleEngineError):
    """Unrecoverable rule loading failure."""


class RuleValidationError(RuleEngineError):
    """Unrecoverable rule validation failure."""
