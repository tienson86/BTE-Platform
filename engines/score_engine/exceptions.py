"""Score Engine exceptions."""


class ScoreEngineError(Exception):
    """Base error for Score Engine failures."""


class ScoreContextError(ScoreEngineError):
    """Raised when Score Engine input is not a usable RuleContext."""
