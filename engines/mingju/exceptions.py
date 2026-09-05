"""MC-01 engine exceptions."""

from __future__ import annotations


class MingJuDecisionError(Exception):
    """Base error for MingJu Decision Engine."""


class MingJuValidationError(MingJuDecisionError):
    """Fail-closed contract violation."""


class MingJuVersionError(MingJuDecisionError):
    """Unsupported schema or ruleset version."""


class MingJuInputError(MingJuDecisionError):
    """Canonical upstream input is missing or invalid."""
