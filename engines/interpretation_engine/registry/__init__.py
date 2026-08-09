"""Interpretation registry architecture and runtime package."""

from __future__ import annotations

from engines.interpretation_engine.registry.dependency_graph import DependencyGraph
from engines.interpretation_engine.registry.module_registry import (
    InterpretationModuleRecord,
    InterpretationModuleRegistry,
)
from engines.interpretation_engine.registry.loader import Loader
from engines.interpretation_engine.registry.metadata import (
    InterpreterRegistryEntry,
    InterpreterRegistrySnapshot,
    Metadata,
)
from engines.interpretation_engine.registry.pack_reader import PackReaderInterface
from engines.interpretation_engine.registry.registry import Registry
from engines.interpretation_engine.registry.registry_interface import (
    InterpretationRegistryInterface,
)
from engines.interpretation_engine.registry.resolver import Resolver
from engines.interpretation_engine.registry.version_manager import VersionManager

__all__ = [
    "DependencyGraph",
    "InterpretationModuleRecord",
    "InterpretationModuleRegistry",
    "InterpretationRegistryInterface",
    "InterpreterRegistryEntry",
    "InterpreterRegistrySnapshot",
    "Loader",
    "Metadata",
    "PackReaderInterface",
    "Registry",
    "Resolver",
    "VersionManager",
]
