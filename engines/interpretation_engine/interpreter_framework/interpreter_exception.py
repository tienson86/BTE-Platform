"""Standard exceptions for the Pack 03 Interpreter Framework."""

from __future__ import annotations


class InterpreterError(Exception):
    """Base exception for interpreter framework failures."""

    def __init__(self, message: str, *, code: str = "interpreter_error") -> None:
        """Initialize with message and stable error code."""
        super().__init__(message)
        self.message = message
        self.code = code


class ValidationError(InterpreterError):
    """Raised when interpreter input/result/contract validation fails."""

    def __init__(self, message: str, *, code: str = "validation_error") -> None:
        """Initialize validation error."""
        super().__init__(message, code=code)


class DependencyError(InterpreterError):
    """Raised when interpreter dependency resolution fails."""

    def __init__(self, message: str, *, code: str = "dependency_error") -> None:
        """Initialize dependency error."""
        super().__init__(message, code=code)


class ExecutionError(InterpreterError):
    """Raised when interpreter business execution fails."""

    def __init__(self, message: str, *, code: str = "execution_error") -> None:
        """Initialize execution error."""
        super().__init__(message, code=code)


class ConfigurationError(InterpreterError):
    """Raised when interpreter configuration/capability setup is invalid."""

    def __init__(self, message: str, *, code: str = "configuration_error") -> None:
        """Initialize configuration error."""
        super().__init__(message, code=code)
