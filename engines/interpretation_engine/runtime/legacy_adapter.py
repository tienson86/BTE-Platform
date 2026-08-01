"""Legacy compatibility adapters for Pack 03 runtime infrastructure.

Adapters bridge legacy InterpretationContext consumers to Pack 03
PackInterpretationContext without deleting legacy packages.
No BaZi interpretation logic.
"""

from __future__ import annotations

import logging
from typing import Any

from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.legacy_runtime.context import (
    InterpretationContext as LegacyInterpretationContext,
)

logger = logging.getLogger(__name__)

# Marker for audits / greps: this module is a LEGACY compatibility adapter.
LEGACY_COMPATIBILITY_ADAPTER = True


class LegacyContextAdapter:
    """Adapter between legacy InterpretationContext and PackInterpretationContext.

    Does not convert BaZi fields into Pack 03 context.
    Pack 03 runtime requires PackInterpretationContext built from Pack 02 FinalResult.
    """

    def is_legacy(self, context: Any) -> bool:
        """Return True when object is the legacy InterpretationContext type."""
        return isinstance(context, LegacyInterpretationContext) and not isinstance(
            context, PackInterpretationContext
        )

    def is_pack03(self, context: Any) -> bool:
        """Return True when object is PackInterpretationContext."""
        return isinstance(context, PackInterpretationContext)

    def require_pack03(self, context: Any) -> PackInterpretationContext:
        """Accept PackInterpretationContext only; reject legacy contexts."""
        if isinstance(context, PackInterpretationContext):
            return context
        if self.is_legacy(context):
            logger.warning(
                "legacy_context_rejected",
                extra={"adapter": "LegacyContextAdapter"},
            )
            raise TypeError("pack_interpretation_context_required_legacy_rejected")
        raise TypeError("pack_interpretation_context_required")

    def describe(self, context: Any) -> dict[str, str]:
        """Return structural description of context type for diagnostics."""
        if self.is_pack03(context):
            return {
                "kind": "pack03",
                "type": "PackInterpretationContext",
                "id": getattr(context, "id", ""),
            }
        if self.is_legacy(context):
            return {
                "kind": "legacy",
                "type": "LegacyInterpretationContext",
                "id": "",
            }
        return {"kind": "unknown", "type": type(context).__name__, "id": ""}
