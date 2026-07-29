"""
BTE Platform
Interpretation Engine Exceptions
"""

from __future__ import annotations


class InterpretationError(Exception):
    """Base Exception."""
    pass


# ==========================================================
# Validation
# ==========================================================

class InterpretationValidationError(InterpretationError):
    pass


class InvalidContextError(InterpretationValidationError):
    pass


class InvalidTemplateError(InterpretationValidationError):
    pass


class InvalidRendererError(InterpretationValidationError):
    pass


# ==========================================================
# Template
# ==========================================================

class TemplateError(InterpretationError):
    pass


class TemplateNotFoundError(TemplateError):
    pass


class TemplateParseError(TemplateError):
    pass


class RuleMatchError(TemplateError):
    pass


# ==========================================================
# Rendering
# ==========================================================

class RenderError(InterpretationError):
    pass


class MarkdownRenderError(RenderError):
    pass


class HtmlRenderError(RenderError):
    pass


class PdfRenderError(RenderError):
    pass


class JsonRenderError(RenderError):
    pass


# ==========================================================
# Engine
# ==========================================================

class InterpretationEngineError(InterpretationError):
    pass


class EngineInitializeError(InterpretationEngineError):
    pass


class EngineExecutionError(InterpretationEngineError):
    pass
