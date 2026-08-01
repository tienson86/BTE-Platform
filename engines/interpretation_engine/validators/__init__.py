"""Validation architecture package."""

from __future__ import annotations

from engines.interpretation_engine.validators.input_validator_interface import (
    InputValidatorInterface,
)
from engines.interpretation_engine.validators.output_validator_interface import (
    OutputValidatorInterface,
)

__all__ = [
    "InputValidatorInterface",
    "OutputValidatorInterface",
]
