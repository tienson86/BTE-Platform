"""Confidence resolution for Narrative Runtime (Sprint D1)."""

from __future__ import annotations

import logging
from statistics import fmean

from .models import (
    ComponentType,
    NodeStatus,
    RuntimeEvidenceUnit,
)

logger = logging.getLogger(__name__)


class ConfidenceResolver:
    """
    Resolve per-component confidence from bound evidence.

    Structural metric only — not narrative wording.
    """

    def resolve(
        self,
        evidence_by_id: dict[str, RuntimeEvidenceUnit],
        bindings: dict[ComponentType, tuple[tuple[str, ...], tuple[str, ...]]],
        statuses: dict[ComponentType, NodeStatus],
    ) -> dict[ComponentType, float]:
        """Return confidence in [0, 1] per component."""
        scores: dict[ComponentType, float] = {}
        for component, (evidence_ids, _interp_ids) in bindings.items():
            status = statuses.get(component, NodeStatus.INSUFFICIENT_EVIDENCE)
            if status in {NodeStatus.INSUFFICIENT_EVIDENCE, NodeStatus.BLOCKED, NodeStatus.INVALID}:
                scores[component] = 0.0
                continue
            confidences = [
                evidence_by_id[evidence_id].confidence
                for evidence_id in evidence_ids
                if evidence_id in evidence_by_id
            ]
            if not confidences:
                # Interpretation-only binding: modest structural confidence.
                scores[component] = 0.5 if bindings[component][1] else 0.0
            else:
                scores[component] = round(fmean(confidences), 4)
            logger.debug(
                "confidence_resolver.%s value=%s",
                component.value,
                scores[component],
            )
        return scores
