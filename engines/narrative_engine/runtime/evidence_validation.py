"""Evidence validation for Narrative Runtime (Sprint D1)."""

from __future__ import annotations

import logging

from .models import EvidenceKind, RuntimeEvidenceUnit, RuntimeInput

logger = logging.getLogger(__name__)

_MIN_CONFIDENCE = 0.0
_MAX_CONFIDENCE = 1.0


class EvidenceValidator:
    """
    Validate and normalize evidence units.

    Does not invent evidence. Does not generate prose.
    """

    def validate(self, runtime_input: RuntimeInput) -> tuple[RuntimeEvidenceUnit, ...]:
        """
        Return cleaned evidence tuple.

        Drops empty ids, clamps confidence, keeps commercial_ok flag.
        """
        cleaned: list[RuntimeEvidenceUnit] = []
        seen: set[str] = set()
        for unit in runtime_input.evidence:
            evidence_id = (unit.id or "").strip()
            if not evidence_id:
                logger.debug("evidence_validation.skip_empty_id")
                continue
            if evidence_id in seen:
                logger.debug("evidence_validation.skip_duplicate id=%s", evidence_id)
                continue
            seen.add(evidence_id)
            kind = unit.kind if isinstance(unit.kind, EvidenceKind) else EvidenceKind.OTHER
            confidence = _clamp_confidence(unit.confidence)
            cleaned.append(
                RuntimeEvidenceUnit(
                    id=evidence_id,
                    kind=kind,
                    confidence=confidence,
                    source_path=(unit.source_path or "").strip(),
                    commercial_ok=bool(unit.commercial_ok),
                )
            )
        logger.info("evidence_validation.count=%s", len(cleaned))
        return tuple(cleaned)


def _clamp_confidence(value: float) -> float:
    """Clamp confidence into [0, 1]."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return _MIN_CONFIDENCE
    if number < _MIN_CONFIDENCE:
        return _MIN_CONFIDENCE
    if number > _MAX_CONFIDENCE:
        return _MAX_CONFIDENCE
    return number
