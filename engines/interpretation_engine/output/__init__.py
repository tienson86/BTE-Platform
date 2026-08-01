"""Output architecture package."""

from __future__ import annotations

from engines.interpretation_engine.output.output_artifact import OutputArtifact
from engines.interpretation_engine.output.output_formatter_interface import (
    OutputFormatterInterface,
)

__all__ = [
    "OutputArtifact",
    "OutputFormatterInterface",
]
