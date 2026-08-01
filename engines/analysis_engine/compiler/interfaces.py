"""Analysis Engine compiler public interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from engines.analysis_engine.compiler.build_context import BuildContext
from engines.analysis_engine.compiler.build_result import BuildResult
from engines.analysis_engine.compiler.manifest import CompilerManifest


class CompilerInterface(ABC):
    """Public interface for the Analysis Engine compiler."""

    @abstractmethod
    def compile(self, context: BuildContext) -> BuildResult:
        """Compile analysis artifacts for the provided build context."""

    @abstractmethod
    def validate(self, context: BuildContext) -> bool:
        """Validate that a build context is ready for compilation."""


class LoaderInterface(ABC):
    """Public interface for loading compiler inputs."""

    @abstractmethod
    def load(self, path: Path) -> BuildContext:
        """Load a build context from a filesystem path."""


class NormalizerInterface(ABC):
    """Public interface for normalizing compiler inputs."""

    @abstractmethod
    def normalize(self, context: BuildContext) -> BuildContext:
        """Return a normalized build context."""


class TransformerInterface(ABC):
    """Public interface for transforming normalized compiler inputs."""

    @abstractmethod
    def transform(self, context: BuildContext) -> BuildContext:
        """Return a transformed build context."""


class PackageBuilderInterface(ABC):
    """Public interface for packaging compiler outputs."""

    @abstractmethod
    def build(self, context: BuildContext, manifest: CompilerManifest) -> BuildResult:
        """Build a package from context and manifest."""
