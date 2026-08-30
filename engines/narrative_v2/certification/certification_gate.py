"""Narrative Certification Gate. Records decisions. Never mutates Narrative."""

from __future__ import annotations

import copy
import uuid
from datetime import datetime, timezone
from typing import Any, Mapping

from engines.narrative_v2.certification.certification_context import CertificationContext
from engines.narrative_v2.certification.certification_errors import (
    CertificationRejectedError,
    CertificationTransitionError,
)
from engines.narrative_v2.certification.certification_history import CertificationHistory
from engines.narrative_v2.certification.certification_registry import can_transition
from engines.narrative_v2.certification.certification_result import (
    CERTIFICATION_VERSION,
    DECISIONS,
    STATUS_CERTIFIED,
    STATUS_DRAFT,
    CertificationResult,
)
from engines.narrative_v2.certification.certification_validator import CertificationValidator
from engines.narrative_v2.presentation.presentation_status import PRESENTATION_VERSION


class CertificationGate:
    """Final approval layer before Golden Dataset eligibility."""

    def __init__(
        self,
        *,
        history: CertificationHistory | None = None,
        validator: CertificationValidator | None = None,
    ) -> None:
        self._history = history or CertificationHistory()
        self._validator = validator or CertificationValidator()

    def inspect(
        self,
        *,
        case_id: str,
        presentation: Mapping[str, Any],
        studio_review: Mapping[str, Any] | None = None,
        validation_summary: Mapping[str, Any] | None = None,
        test_summary: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Evaluate gates without recording a decision."""
        context = CertificationContext(
            case_id=case_id,
            presentation=dict(presentation),
            studio_review=dict(studio_review or {}),
            validation_summary=dict(validation_summary or {"status": "PASS"}),
            test_summary=dict(test_summary or {"status": "PASS"}),
            reviewer="",
            review_comment="",
        )
        quality = self._validator.evaluate(context)
        status = self._history.current_status(case_id)
        return {
            "case_id": case_id,
            "status": status,
            "golden_eligible": status == STATUS_CERTIFIED,
            "quality_summary": quality,
            "history": self._history.list_for(case_id),
            "latest": self._history.latest(case_id),
        }

    def submit(
        self,
        *,
        case_id: str,
        presentation: Mapping[str, Any],
        decision: str,
        reviewer: str,
        review_comment: str = "",
        studio_review: Mapping[str, Any] | None = None,
        validation_summary: Mapping[str, Any] | None = None,
        test_summary: Mapping[str, Any] | None = None,
        review_time: str | None = None,
    ) -> CertificationResult:
        """Append a certification decision. Presentation is copied, never written back."""
        snapshot = copy.deepcopy(dict(presentation))
        token = decision.strip().upper()
        if token not in DECISIONS:
            raise CertificationTransitionError(f"unknown_decision:{decision}")
        name = reviewer.strip()
        if not name:
            raise CertificationRejectedError("reviewer_required")
        current = self._history.current_status(case_id)
        if not can_transition(current, token):
            raise CertificationTransitionError(f"illegal_transition:{current}->{token}")
        context = CertificationContext(
            case_id=case_id,
            presentation=snapshot,
            studio_review=dict(studio_review or {}),
            validation_summary=dict(validation_summary or {"status": "PASS"}),
            test_summary=dict(test_summary or {"status": "PASS"}),
            reviewer=name,
            review_comment=review_comment.strip(),
            review_time=review_time,
        )
        quality = self._validator.evaluate(context)
        if token == STATUS_CERTIFIED and not quality.get("all_passed"):
            raise CertificationRejectedError("quality_gates_failed")
        stamped = review_time or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        result = CertificationResult(
            review_id=str(uuid.uuid4()),
            case_id=case_id,
            status=token,
            decision=token,
            reviewer=name,
            review_time=stamped,
            review_comment=review_comment.strip(),
            quality_summary=quality,
            certification_version=CERTIFICATION_VERSION,
            references={
                "presentation_version": PRESENTATION_VERSION,
                "presentation_status": snapshot.get("status"),
            },
            metadata={
                "shadow_mode": True,
                "replaces_pack05": False,
                "previous_status": current,
                "from_draft": current == STATUS_DRAFT,
            },
            golden_eligible=token == STATUS_CERTIFIED,
        )
        self._history.append(result)
        return result

    def eligible_for_golden(self, case_id: str) -> bool:
        """True only when the latest status is CERTIFIED."""
        return self._history.current_status(case_id) == STATUS_CERTIFIED
