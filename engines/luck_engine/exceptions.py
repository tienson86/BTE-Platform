"""Luck Engine exceptions."""


class LuckEngineError(Exception):
    """Base error for Luck Engine failures."""


class LuckContextError(LuckEngineError):
    """Raised when Luck Engine inputs are unusable."""
