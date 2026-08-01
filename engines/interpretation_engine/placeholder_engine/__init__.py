"""Placeholder Engine architecture and runtime package.

Infrastructure for placeholder reference resolution, binding, formatting,
and validation. No interpretation logic.
"""

from __future__ import annotations

from engines.interpretation_engine.placeholder_engine.binder import Binder
from engines.interpretation_engine.placeholder_engine.formatter import Formatter
from engines.interpretation_engine.placeholder_engine.interface import (
    PlaceholderEngine,
    PlaceholderEngineInterface,
)
from engines.interpretation_engine.placeholder_engine.metadata import (
    Metadata,
    PlaceholderBinding,
    PlaceholderRef,
    PlaceholderResolution,
    PlaceholderValue,
)
from engines.interpretation_engine.placeholder_engine.resolver import Resolver
from engines.interpretation_engine.placeholder_engine.validator import Validator

__all__ = [
    "Binder",
    "Formatter",
    "Metadata",
    "PlaceholderBinding",
    "PlaceholderEngine",
    "PlaceholderEngineInterface",
    "PlaceholderRef",
    "PlaceholderResolution",
    "PlaceholderValue",
    "Resolver",
    "Validator",
]
