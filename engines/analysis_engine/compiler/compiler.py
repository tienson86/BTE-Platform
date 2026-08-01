"""Analysis Engine compiler core interface."""

from __future__ import annotations

from engines.analysis_engine.compiler.build_context import BuildContext
from engines.analysis_engine.compiler.build_result import BuildResult
from engines.analysis_engine.compiler.interfaces import CompilerInterface


class Compiler(CompilerInterface):
    """Architecture skeleton for the Analysis Engine compiler.

    Public interface only. No compilation logic.
    """

    def compile(self, context: BuildContext) -> BuildResult:
        """Compile analysis artifacts for the provided build context."""
        raise NotImplementedError

    def validate(self, context: BuildContext) -> bool:
        """Validate that a build context is ready for compilation."""
        raise NotImplementedError
