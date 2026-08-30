"""EvidenceValidator — contract checks only. No astrology interpretation."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.evidence.evidence_context import NarrativeEvidenceContext
from engines.narrative_v2.evidence.evidence_errors import EvidenceValidationError
from engines.narrative_v2.evidence.evidence_item import (
    ALLOWED_STATUSES,
    EvidenceItem,
    EvidenceValue,
)
from engines.narrative_v2.evidence.evidence_registry import (
    ALLOWED_DOMAINS,
    FORBIDDEN_KEY_TOKENS,
    FORBIDDEN_SOURCE_PREFIXES,
)

CUSTOMER_PROSE_MARKERS: tuple[str, ...] = (
    "Bạn có",
    "Bạn làm",
    "nên bổ",
    "tình duyên tốt",
    "vận thuận lợi",
    "nội lực tốt",
    "làm việc có hệ thống",
)


@dataclass(slots=True)
class EvidenceValidationOutcome:
    """Ordering-free evidence contract result."""

    passed: bool
    reason: str = ""

    @property
    def status(self) -> str:
        """PASS or FAIL."""
        return "PASS" if self.passed else "FAIL"


class EvidenceValidator:
    """Validate EvidenceContext against N-IMP-02 contract rules."""

    def validate(self, context: NarrativeEvidenceContext) -> EvidenceValidationOutcome:
        """PASS unless the evidence contract is violated."""
        try:
            self.assert_valid(context)
        except EvidenceValidationError as exc:
            return EvidenceValidationOutcome(passed=False, reason=exc.message)
        return EvidenceValidationOutcome(passed=True)

    def assert_valid(self, context: NarrativeEvidenceContext) -> None:
        """Raise if the context violates the evidence contract."""
        self._check_ids(context.items)
        for item in context.items:
            self._check_item(item)

    def _check_ids(self, items: tuple[EvidenceItem, ...]) -> None:
        seen: set[str] = set()
        for item in items:
            if not item.evidence_id.startswith("evidence."):
                raise EvidenceValidationError(
                    f"Evidence id is not deterministic: {item.evidence_id}"
                )
            if item.evidence_id in seen:
                raise EvidenceValidationError(
                    f"Duplicate evidence_id: {item.evidence_id}"
                )
            seen.add(item.evidence_id)

    def _check_item(self, item: EvidenceItem) -> None:
        if item.domain not in ALLOWED_DOMAINS:
            raise EvidenceValidationError(f"Domain not allowed: {item.domain}")
        if item.status not in ALLOWED_STATUSES:
            raise EvidenceValidationError(f"Invalid evidence status: {item.status}")
        if item.status == "available" and not item.source_path:
            raise EvidenceValidationError(
                f"Available evidence missing source_path: {item.evidence_id}"
            )
        self._reject_forbidden_path(item.source_path)
        self._reject_forbidden_tokens(item.key)
        self._reject_forbidden_tokens(item.evidence_id)
        self._reject_prose(item)
        self._reject_debug_value(item.value)

    def _reject_forbidden_path(self, source_path: str) -> None:
        root = source_path.split(".", 1)[0]
        if root in FORBIDDEN_SOURCE_PREFIXES:
            raise EvidenceValidationError(
                f"Source path is not canonical: {source_path}"
            )

    def _reject_forbidden_tokens(self, token: str) -> None:
        lowered = token.lower()
        for banned in FORBIDDEN_KEY_TOKENS:
            if banned in lowered:
                raise EvidenceValidationError(
                    f"Frontend or presentation token is forbidden: {token}"
                )

    def _reject_prose(self, item: EvidenceItem) -> None:
        texts = [item.label]
        if isinstance(item.value, str):
            texts.append(item.value)
        elif isinstance(item.value, tuple):
            texts.extend(str(part) for part in item.value)
        blob = " ".join(texts)
        for marker in CUSTOMER_PROSE_MARKERS:
            if marker in blob:
                raise EvidenceValidationError(
                    f"Customer prose is not evidence: {item.evidence_id}"
                )

    def _reject_debug_value(self, value: EvidenceValue) -> None:
        if value is None or isinstance(value, (str, int, float, bool)):
            return
        if isinstance(value, tuple):
            for part in value:
                if not isinstance(part, (str, int, float, bool)):
                    raise EvidenceValidationError(
                        "Raw runtime/debug objects are rejected"
                    )
            return
        raise EvidenceValidationError("Raw runtime/debug objects are rejected")
