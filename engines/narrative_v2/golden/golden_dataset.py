"""Narrative V2 Golden Dataset. Certified baselines only."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Mapping

from engines.narrative_v2.golden.golden_case import GOLDEN_SCHEMA_VERSION, STATUS_FROZEN, GoldenCase
from engines.narrative_v2.golden.golden_errors import GoldenEligibilityError
from engines.narrative_v2.golden.golden_history import GoldenHistory
from engines.narrative_v2.golden.golden_registry import GoldenRegistryEntry
from engines.narrative_v2.golden.golden_serializer import (
    canonical_payload_hash,
    certification_hash,
    freeze_mapping,
    narrative_hash,
    presentation_hash,
    review_hash,
    thaw_mapping,
)
from engines.narrative_v2.golden.golden_validator import GoldenValidator
from engines.narrative_v2.presentation.presentation_status import NARRATIVE_VERSION, PRESENTATION_VERSION

logger = logging.getLogger(__name__)


class GoldenDataset:
    """Promote CERTIFIED cases into an append-only Golden Dataset."""

    def __init__(
        self,
        *,
        history: GoldenHistory | None = None,
        validator: GoldenValidator | None = None,
    ) -> None:
        self._history = history or GoldenHistory()
        self._validator = validator or GoldenValidator()

    def eligible(self, certification: Mapping[str, Any]) -> bool:
        """True only when Certification status is CERTIFIED."""
        try:
            self._validator.require_eligible(certification)
        except GoldenEligibilityError:
            return False
        return True

    def promote(
        self,
        *,
        case_id: str,
        presentation: Mapping[str, Any],
        certification: Mapping[str, Any],
        canonical: Mapping[str, Any] | None = None,
        created: str | None = None,
    ) -> GoldenCase:
        """Freeze a CERTIFIED Presentation as a new Golden version. Never overwrites."""
        self._validator.require_eligible(certification)
        self._validator.require_presentation(presentation)
        snapshot = dict(presentation)
        certified = dict(certification)
        stamped = created or str(certified.get("review_time") or "") or _now()
        reviewer = str(certified.get("reviewer") or "").strip()
        version = self._history.next_version(case_id)
        case = _build_case(
            case_id=case_id,
            snapshot=snapshot,
            certified=certified,
            canonical=canonical,
            version=version,
            stamped=stamped,
            reviewer=reviewer,
        )
        entry = GoldenRegistryEntry(
            case_id=case_id,
            version=version,
            status=STATUS_FROZEN,
            created=stamped,
            reviewer=reviewer,
        )
        self._history.append(case, entry)
        logger.info(
            "golden.promoted case=%s version=%s reviewer=%s",
            case_id,
            version,
            reviewer,
        )
        return case

    def get(self, case_id: str, version: int | None = None) -> GoldenCase | None:
        """Return a frozen Golden Case. Latest version when version is omitted."""
        if version is None:
            return self._history.latest(case_id)
        return self._history.load_case(case_id, version)

    def registry(self) -> list[dict[str, Any]]:
        """Return append-only registry rows."""
        return self._history.registry_records()

    def compare(
        self,
        *,
        case_id: str,
        presentation: Mapping[str, Any],
        version: int | None = None,
    ) -> dict[str, Any]:
        """Regression compare a current Presentation against a Golden Case."""
        golden = self.get(case_id, version)
        if golden is None:
            return {
                "case_id": case_id,
                "matched": False,
                "reason": "missing_golden",
                "diffs": [{"path": "", "kind": "missing_golden", "current": "", "golden": ""}],
                "hashes": {},
            }
        current = dict(presentation)
        baseline = thaw_mapping(golden.presentation)
        if not isinstance(baseline, dict):
            baseline = {}
        diffs = self._validator.diff_presentations(current, baseline)
        current_hash = presentation_hash(current)
        return {
            "case_id": case_id,
            "version": golden.version,
            "matched": not diffs and current_hash == golden.presentation_hash,
            "reason": "" if not diffs else "presentation_drift",
            "diffs": diffs,
            "hashes": {
                "current_presentation_hash": current_hash,
                "golden_presentation_hash": golden.presentation_hash,
                "golden_canonical_hash": golden.canonical_hash,
                "golden_review_hash": golden.review_hash,
                "golden_certification_hash": golden.certification_hash,
                "golden_narrative_hash": golden.narrative_hash,
            },
        }


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _build_case(
    *,
    case_id: str,
    snapshot: dict[str, Any],
    certified: dict[str, Any],
    canonical: Mapping[str, Any] | None,
    version: int,
    stamped: str,
    reviewer: str,
) -> GoldenCase:
    """Assemble an immutable Golden Case from certified inputs."""
    return GoldenCase(
        case_id=case_id,
        presentation=freeze_mapping(snapshot),  # type: ignore[arg-type]
        certification=freeze_mapping(certified),  # type: ignore[arg-type]
        canonical_hash=canonical_payload_hash(canonical, case_id),
        presentation_hash=presentation_hash(snapshot),
        review_hash=review_hash(certified),
        certification_hash=certification_hash(certified),
        narrative_hash=narrative_hash(snapshot),
        status=STATUS_FROZEN,
        version=version,
        created=stamped,
        reviewer=reviewer,
        metadata=freeze_mapping(  # type: ignore[arg-type]
            {
                "schema": GOLDEN_SCHEMA_VERSION,
                "shadow_mode": True,
                "replaces_pack05": False,
                "presentation_version": PRESENTATION_VERSION,
                "narrative_version": NARRATIVE_VERSION,
                "certification_version": str(certified.get("certification_version") or ""),
                "source_status": str(certified.get("status") or ""),
            }
        ),
    )
