"""Interpretation Engine exception hierarchy (architecture + legacy re-exports)."""

from __future__ import annotations

from engines.interpretation_engine.exceptions.context_error import InterpretationContextError
from engines.interpretation_engine.exceptions.interpretation_error import (
    InterpretationArchitectureError,
)
from engines.interpretation_engine.exceptions.pipeline_error import InterpretationPipelineError
from engines.interpretation_engine.exceptions.placeholder_error import PlaceholderEngineError
from engines.interpretation_engine.exceptions.registry_error import InterpretationRegistryError
from engines.interpretation_engine.exceptions.sentence_error import SentenceEngineError
from engines.interpretation_engine.exceptions.template_error import TemplateEngineError
from engines.interpretation_engine.exceptions.validator_error import InterpretationValidatorError
from engines.interpretation_engine.legacy_runtime.exceptions import (
    InterpretationError,
    InterpretationValidationError,
    InvalidContextError,
    InvalidRendererError,
    InvalidTemplateError,
    TemplateError,
)

__all__ = [
    "InterpretationArchitectureError",
    "InterpretationContextError",
    "InterpretationError",
    "InterpretationPipelineError",
    "InterpretationRegistryError",
    "InterpretationValidationError",
    "InterpretationValidatorError",
    "InvalidContextError",
    "InvalidRendererError",
    "InvalidTemplateError",
    "PlaceholderEngineError",
    "SentenceEngineError",
    "TemplateEngineError",
    "TemplateError",
]
