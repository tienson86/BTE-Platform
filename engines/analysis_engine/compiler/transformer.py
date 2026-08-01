"""Analysis Engine compiler transformer interface."""

from __future__ import annotations

from engines.analysis_engine.compiler.build_context import BuildContext
from engines.analysis_engine.compiler.interfaces import TransformerInterface


class Transformer(TransformerInterface):
    """Architecture skeleton for transforming compiler inputs.

    Public interface only. No transformation logic.
    """

    def transform(self, context: BuildContext) -> BuildContext:
        """Return a transformed build context."""
        raise NotImplementedError
