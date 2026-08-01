"""Analysis Engine compiler normalizer interface."""

from __future__ import annotations

from engines.analysis_engine.compiler.build_context import BuildContext
from engines.analysis_engine.compiler.interfaces import NormalizerInterface


class Normalizer(NormalizerInterface):
    """Architecture skeleton for normalizing compiler inputs.

    Public interface only. No normalization logic.
    """

    def normalize(self, context: BuildContext) -> BuildContext:
        """Return a normalized build context."""
        raise NotImplementedError
