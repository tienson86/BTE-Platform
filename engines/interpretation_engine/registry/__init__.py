"""Interpretation registry architecture package."""

from __future__ import annotations

from engines.interpretation_engine.registry.pack_reader import PackReaderInterface
from engines.interpretation_engine.registry.registry_interface import (
    InterpretationRegistryInterface,
)

__all__ = [
    "InterpretationRegistryInterface",
    "PackReaderInterface",
]
