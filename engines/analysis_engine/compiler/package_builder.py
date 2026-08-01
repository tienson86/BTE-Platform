"""Analysis Engine compiler package builder interface."""

from __future__ import annotations

from engines.analysis_engine.compiler.build_context import BuildContext
from engines.analysis_engine.compiler.build_result import BuildResult
from engines.analysis_engine.compiler.interfaces import PackageBuilderInterface
from engines.analysis_engine.compiler.manifest import CompilerManifest


class PackageBuilder(PackageBuilderInterface):
    """Architecture skeleton for packaging compiler outputs.

    Public interface only. No packaging logic.
    """

    def build(self, context: BuildContext, manifest: CompilerManifest) -> BuildResult:
        """Build a package from context and manifest."""
        raise NotImplementedError
