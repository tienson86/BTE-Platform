"""Analysis Engine compiler loader interface."""

from __future__ import annotations

from pathlib import Path

from engines.analysis_engine.compiler.build_context import BuildContext
from engines.analysis_engine.compiler.interfaces import LoaderInterface


class Loader(LoaderInterface):
    """Architecture skeleton for loading compiler inputs.

    Public interface only. No loading logic.
    """

    def load(self, path: Path) -> BuildContext:
        """Load a build context from a filesystem path."""
        raise NotImplementedError
