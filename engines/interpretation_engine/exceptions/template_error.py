"""Template Engine exception."""

from __future__ import annotations

from engines.interpretation_engine.exceptions.interpretation_error import (
    InterpretationArchitectureError,
)


class TemplateEngineError(InterpretationArchitectureError):
    """Raised for template engine infrastructure failures.

    Pack 03 template engine has no template library and does not render prose.
    """
