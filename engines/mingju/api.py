"""Public MC-01 API. Downstream must import from here, not internal modules."""

from __future__ import annotations

from engines.mingju.adapters import build_mingju_context
from engines.mingju.composer import compose_mingju_decision
from engines.mingju.engine import MingJuDecisionEngine
from engines.mingju.models import MingJuComposedDecision, MingJuContext, MingJuDecisionResult
from engines.mingju.views import to_full_dict, to_pack07_snapshot, to_public_dict


def analyze_mingju(
    context: MingJuContext,
    *,
    ruleset_version: str | None = None,
) -> MingJuDecisionResult:
    """Canonical MC-01 calculation entry point."""
    return MingJuDecisionEngine().analyze(context, ruleset_version=ruleset_version)


__all__ = [
    "MingJuComposedDecision",
    "MingJuContext",
    "MingJuDecisionEngine",
    "MingJuDecisionResult",
    "analyze_mingju",
    "build_mingju_context",
    "compose_mingju_decision",
    "to_full_dict",
    "to_pack07_snapshot",
    "to_public_dict",
]
