"""Golden Dataset eligibility and regression compare."""

from __future__ import annotations

import json
from typing import Any, Mapping

from engines.narrative_v2.certification.certification_result import STATUS_CERTIFIED
from engines.narrative_v2.golden.golden_errors import GoldenEligibilityError, GoldenValidationError
from engines.narrative_v2.golden.golden_serializer import (
    canonical_payload_hash,
    certification_hash,
    narrative_hash,
    presentation_hash,
    review_hash,
)
from engines.narrative_v2.presentation.presentation_status import PRESENTATION_VERSION


class GoldenValidator:
    """Reject anything that is not a CERTIFIED Presentation baseline."""

    def require_eligible(self, certification: Mapping[str, Any]) -> None:
        """Raise when the case is not allowed into Golden Dataset."""
        status = str(certification.get("status") or "").upper()
        if status != STATUS_CERTIFIED:
            raise GoldenEligibilityError(f"not_certified:{status or 'missing'}")
        if certification.get("golden_eligible") is False:
            raise GoldenEligibilityError("golden_eligible_false")
        if not str(certification.get("reviewer") or "").strip():
            raise GoldenEligibilityError("reviewer_required")

    def require_presentation(self, presentation: Mapping[str, Any]) -> None:
        """Raise when Presentation is missing or not the frozen contract."""
        if not presentation:
            raise GoldenValidationError("presentation_required")
        metadata = presentation.get("metadata")
        if not isinstance(metadata, Mapping):
            raise GoldenValidationError("presentation_metadata_required")
        version = str(metadata.get("version") or "")
        if version != PRESENTATION_VERSION:
            raise GoldenValidationError(f"incompatible_presentation:{version}")

    def verify_hashes(
        self,
        *,
        presentation: Mapping[str, Any],
        certification: Mapping[str, Any],
        canonical: Mapping[str, Any] | None,
        expected: Mapping[str, str],
    ) -> None:
        """Raise when stored hashes no longer match the frozen payloads."""
        case_id = str(certification.get("case_id") or expected.get("case_id") or "")
        actual = {
            "canonical_hash": canonical_payload_hash(canonical, case_id),
            "presentation_hash": presentation_hash(presentation),
            "review_hash": review_hash(certification),
            "certification_hash": certification_hash(certification),
            "narrative_hash": narrative_hash(presentation),
        }
        for key, value in actual.items():
            if str(expected.get(key) or "") != value:
                raise GoldenValidationError(f"hash_mismatch:{key}")

    def diff_presentations(
        self,
        current: Mapping[str, Any],
        golden: Mapping[str, Any],
    ) -> list[dict[str, str]]:
        """Leaf diffs for Narrative regression. Does not mutate either payload."""
        rows: list[dict[str, str]] = []
        _walk("", dict(current), dict(golden), rows)
        return rows


def _walk(prefix: str, current: object, golden: object, rows: list[dict[str, str]]) -> None:
    if isinstance(current, dict) and isinstance(golden, dict):
        keys = sorted(set(current) | set(golden))
        for key in keys:
            path = f"{prefix}.{key}" if prefix else str(key)
            if key not in current:
                rows.append({"path": path, "kind": "missing_current", "current": "", "golden": _fmt(golden[key])})
            elif key not in golden:
                rows.append({"path": path, "kind": "extra_current", "current": _fmt(current[key]), "golden": ""})
            else:
                _walk(path, current[key], golden[key], rows)
        return
    if isinstance(current, list) and isinstance(golden, list):
        length = max(len(current), len(golden))
        for index in range(length):
            path = f"{prefix}[{index}]"
            if index >= len(current):
                rows.append({"path": path, "kind": "missing_current", "current": "", "golden": _fmt(golden[index])})
            elif index >= len(golden):
                rows.append({"path": path, "kind": "extra_current", "current": _fmt(current[index]), "golden": ""})
            else:
                _walk(path, current[index], golden[index], rows)
        return
    if current != golden:
        rows.append(
            {
                "path": prefix or "/",
                "kind": "changed",
                "current": _fmt(current),
                "golden": _fmt(golden),
            }
        )


def _fmt(value: object) -> str:
    if value is None:
        return "null"
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    if len(text) > 240:
        return text[:237] + "..."
    return text
