"""RewriteValidator — meaning preservation and language-standard checks."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.knowledge.knowledge_context import NarrativeKnowledgeContext
from engines.narrative_v2.rewrite.rewrite_context import CommercialRewriteContext
from engines.narrative_v2.rewrite.rewrite_errors import RewriteValidationError
from engines.narrative_v2.rewrite.rewrite_item import RewriteItem
from engines.narrative_v2.rewrite.rewrite_strategy import (
    ALLOWED_STATUSES,
    ALLOWED_STRATEGIES,
    ENGINE_LEAK,
    ESCALATION_ADDED,
    FEAR_LANGUAGE,
    FORBIDDEN_ADDRESS,
    FORTUNE_ABSOLUTES,
)

FORBIDDEN_CONTEXT_ATTRS: tuple[str, ...] = (
    "overview",
    "interpretation",
    "action_plan",
    "presentation",
    "canonical_analysis",
    "final_summary",
)

NEGATIVE_GENERATED: tuple[str, ...] = (
    "Bạn chắc chắn thành công.",
    "Bạn nhất định giàu.",
    "Bạn sẽ ly hôn.",
    "Đây là vận đại cát.",
    "Bạn nên dùng màu đỏ vì Hỏa là Dụng thần.",
)


@dataclass(slots=True)
class RewriteValidationOutcome:
    """Rewrite contract result."""

    passed: bool
    reason: str = ""

    @property
    def status(self) -> str:
        """PASS or FAIL."""
        return "PASS" if self.passed else "FAIL"


class RewriteValidator:
    """Validate CommercialRewriteContext against N-IMP-05 contract rules."""

    def validate(
        self,
        context: CommercialRewriteContext,
        knowledge: NarrativeKnowledgeContext,
    ) -> RewriteValidationOutcome:
        """PASS unless the rewrite contract is violated."""
        try:
            self.assert_valid(context, knowledge)
        except RewriteValidationError as exc:
            return RewriteValidationOutcome(passed=False, reason=exc.message)
        return RewriteValidationOutcome(passed=True)

    def assert_valid(
        self,
        context: CommercialRewriteContext,
        knowledge: NarrativeKnowledgeContext,
    ) -> None:
        """Raise if the context violates the rewrite contract."""
        self._reject_forbidden_fields(context)
        knowledge_ids = {item.knowledge_id for item in knowledge.items}
        seen: set[str] = set()
        ordered = tuple(
            sorted(context.items, key=lambda item: item.rewrite_id)
        )
        if context.items != ordered:
            raise RewriteValidationError("Rewrite items are not deterministically ordered")
        for item in context.items:
            self._check_item(item, knowledge_ids, seen)

    def _reject_forbidden_fields(self, context: CommercialRewriteContext) -> None:
        for attr in FORBIDDEN_CONTEXT_ATTRS:
            if hasattr(context, attr):
                raise RewriteValidationError(f"Rewrite must not expose {attr}")

    def _check_item(
        self,
        item: RewriteItem,
        knowledge_ids: set[str],
        seen: set[str],
    ) -> None:
        if not item.rewrite_id.startswith("rewrite."):
            raise RewriteValidationError(f"Rewrite id is not deterministic: {item.rewrite_id}")
        if item.rewrite_id in seen:
            raise RewriteValidationError(f"Duplicate rewrite_id: {item.rewrite_id}")
        seen.add(item.rewrite_id)
        if item.strategy not in ALLOWED_STRATEGIES:
            raise RewriteValidationError(f"Unknown rewrite strategy: {item.strategy}")
        if item.status not in ALLOWED_STATUSES:
            raise RewriteValidationError(f"Invalid rewrite status: {item.status}")
        if not item.source_knowledge_ids:
            raise RewriteValidationError(f"Rewrite missing knowledge trace: {item.rewrite_id}")
        for knowledge_id in item.source_knowledge_ids:
            if knowledge_id not in knowledge_ids:
                raise RewriteValidationError(f"Unknown knowledge_id: {knowledge_id}")
        self._reject_debug(item.customer_language)
        self._reject_debug(item.source_meaning)
        self._check_language(item)
        self._check_escalation(item)
        self._check_preservation(item)

    def _reject_debug(self, value: object) -> None:
        if not isinstance(value, str):
            raise RewriteValidationError("Raw runtime/debug objects are rejected")
        if "{" in value or "}" in value:
            raise RewriteValidationError("Raw JSON/debug leak in rewrite")

    def _check_language(self, item: RewriteItem) -> None:
        blob = item.customer_language
        for marker in NEGATIVE_GENERATED:
            if marker in blob:
                raise RewriteValidationError("Forbidden generated customer sentence")
        for token in FORBIDDEN_ADDRESS:
            if token in blob:
                raise RewriteValidationError("Forbidden address term in rewrite")
        for token in FORTUNE_ABSOLUTES:
            if token in blob and token not in item.source_meaning:
                raise RewriteValidationError("Unsupported certainty in rewrite")
        for token in FEAR_LANGUAGE:
            if token in blob:
                raise RewriteValidationError("Fear language in rewrite")
        for token in ENGINE_LEAK:
            if token in blob:
                raise RewriteValidationError("Raw technical/runtime leak in rewrite")

    def _check_escalation(self, item: RewriteItem) -> None:
        for token in ESCALATION_ADDED:
            if token in item.customer_language and token not in item.source_meaning:
                raise RewriteValidationError("Semantic escalation in rewrite")

    def _check_preservation(self, item: RewriteItem) -> None:
        if not item.source_meaning.strip():
            raise RewriteValidationError("Rewrite missing source meaning")
        if item.normalized_meaning.strip() == "":
            raise RewriteValidationError("Rewrite missing normalized meaning")
        source_core = _core_text(item.source_meaning)
        customer_core = _core_text(item.customer_language)
        if source_core not in customer_core and customer_core not in source_core:
            if not customer_core.endswith(source_core) and not _address_wraps(source_core, customer_core):
                raise RewriteValidationError("Rewrite does not preserve source meaning")


def _core_text(text: str) -> str:
    return " ".join(text.strip().rstrip(".").split())


def _address_wraps(source: str, customer: str) -> bool:
    if customer.startswith("Bạn "):
        rest = customer[len("Bạn "):]
        return _core_text(rest).casefold() == source.casefold() or source.casefold() in rest.casefold()
    return False
