"""KnowledgeValidator — approval and trace checks. No rewrite."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.evidence.evidence_context import NarrativeEvidenceContext
from engines.narrative_v2.knowledge.knowledge_context import NarrativeKnowledgeContext
from engines.narrative_v2.knowledge.knowledge_errors import KnowledgeValidationError
from engines.narrative_v2.knowledge.knowledge_item import KnowledgeItem
from engines.narrative_v2.knowledge.knowledge_status import (
    ALLOWED_KNOWLEDGE_TYPES,
    ELIGIBLE_SOURCE_STATUSES,
)
from engines.narrative_v2.reasoning.reasoning_context import NarrativeReasoningContext

CUSTOMER_REWRITE_MARKERS: tuple[str, ...] = (
    "Bạn có nội lực tốt",
    "Bạn làm việc có hệ thống",
    "Tình duyên thuận lợi",
    "Giai đoạn thuận lợi để mở rộng",
    "Nên dùng màu đỏ",
)

FORBIDDEN_CONTEXT_ATTRS: tuple[str, ...] = (
    "final_summary",
    "final_interpretation",
    "final_action_plan",
    "presentation",
    "canonical_analysis",
    "action_plan",
)


@dataclass(slots=True)
class KnowledgeValidationOutcome:
    """Knowledge contract result."""

    passed: bool
    reason: str = ""

    @property
    def status(self) -> str:
        """PASS or FAIL."""
        return "PASS" if self.passed else "FAIL"


class KnowledgeValidator:
    """Validate KnowledgeContext against N-IMP-04 contract rules."""

    def validate(
        self,
        context: NarrativeKnowledgeContext,
        reasoning: NarrativeReasoningContext,
        evidence: NarrativeEvidenceContext,
    ) -> KnowledgeValidationOutcome:
        """PASS unless the knowledge contract is violated."""
        try:
            self.assert_valid(context, reasoning, evidence)
        except KnowledgeValidationError as exc:
            return KnowledgeValidationOutcome(passed=False, reason=exc.message)
        return KnowledgeValidationOutcome(passed=True)

    def assert_valid(
        self,
        context: NarrativeKnowledgeContext,
        reasoning: NarrativeReasoningContext,
        evidence: NarrativeEvidenceContext,
    ) -> None:
        """Raise if the context violates the knowledge contract."""
        self._reject_forbidden_fields(context)
        reasoning_ids = {node.reasoning_id for node in reasoning.nodes}
        evidence_ids = {item.evidence_id for item in evidence.items}
        seen_ids: set[str] = set()
        seen_matches: set[tuple[str, str]] = set()
        for item in context.items:
            self._check_item(item, reasoning_ids, evidence_ids, seen_ids)
        for match in context.matches:
            pair = (match.semantic_key, match.knowledge_id)
            if pair in seen_matches:
                raise KnowledgeValidationError(
                    f"Duplicate knowledge match: {match.knowledge_id}"
                )
            seen_matches.add(pair)
            self._check_trace(match.reasoning_ids, reasoning_ids, match.evidence_ids, evidence_ids)

    def _reject_forbidden_fields(self, context: NarrativeKnowledgeContext) -> None:
        for attr in FORBIDDEN_CONTEXT_ATTRS:
            if hasattr(context, attr):
                raise KnowledgeValidationError(f"Knowledge must not expose {attr}")

    def _check_item(
        self,
        item: KnowledgeItem,
        reasoning_ids: set[str],
        evidence_ids: set[str],
        seen_ids: set[str],
    ) -> None:
        if not item.knowledge_id:
            raise KnowledgeValidationError("Knowledge id is missing")
        if item.knowledge_id in seen_ids:
            raise KnowledgeValidationError(f"Duplicate knowledge_id: {item.knowledge_id}")
        seen_ids.add(item.knowledge_id)
        if item.status not in ELIGIBLE_SOURCE_STATUSES:
            raise KnowledgeValidationError(
                f"Source is not approved: {item.knowledge_id}"
            )
        if item.knowledge_type not in ALLOWED_KNOWLEDGE_TYPES:
            raise KnowledgeValidationError(
                f"Unsupported knowledge type: {item.knowledge_type}"
            )
        if not item.source_path:
            raise KnowledgeValidationError(
                f"Knowledge source_path missing: {item.knowledge_id}"
            )
        if not item.semantic_key:
            raise KnowledgeValidationError(
                f"Knowledge semantic_key missing: {item.knowledge_id}"
            )
        self._reject_debug(item.technical_meaning)
        self._reject_debug(item.customer_meaning_candidate)
        self._reject_rewrite(item)
        if not item.references:
            raise KnowledgeValidationError(
                f"Knowledge is not traceable: {item.knowledge_id}"
            )
        ref = item.references[0]
        self._check_trace(ref.reasoning_ids, reasoning_ids, ref.evidence_ids, evidence_ids)

    def _check_trace(
        self,
        node_ids: tuple[str, ...],
        reasoning_ids: set[str],
        ev_ids: tuple[str, ...],
        evidence_ids: set[str],
    ) -> None:
        for reasoning_id in node_ids:
            if reasoning_id not in reasoning_ids:
                raise KnowledgeValidationError(f"Unknown reasoning_id: {reasoning_id}")
        for evidence_id in ev_ids:
            if evidence_id not in evidence_ids:
                raise KnowledgeValidationError(f"Unknown evidence_id: {evidence_id}")

    def _reject_debug(self, value: object) -> None:
        if value is None or isinstance(value, str):
            return
        raise KnowledgeValidationError("Raw runtime/debug objects are rejected")

    def _reject_rewrite(self, item: KnowledgeItem) -> None:
        blob = " ".join(
            part
            for part in (item.technical_meaning, item.customer_meaning_candidate)
            if part
        )
        for marker in CUSTOMER_REWRITE_MARKERS:
            if marker in blob:
                raise KnowledgeValidationError(
                    f"Customer rewrite is not knowledge resolution: {item.knowledge_id}"
                )
