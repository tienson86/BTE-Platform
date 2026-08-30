"""SummaryValidator — executive-summary contract checks."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.rewrite.rewrite_context import CommercialRewriteContext
from engines.narrative_v2.summary.summary_errors import SummaryValidationError
from engines.narrative_v2.summary.summary_formula import split_sentences, word_count
from engines.narrative_v2.summary.summary_model import (
    ALLOWED_STATUSES,
    CONCLUSION_SENTENCE_MAX,
    HEADLINE_WORD_LIMIT,
    SUMMARY_SENTENCE_MAX,
    OverviewSummary,
)

FORBIDDEN_CONTEXT_ATTRS: tuple[str, ...] = (
    "canonical_analysis",
    "action_plan",
    "presentation",
    "interpretation",
)

FORBIDDEN_CLAIMS: tuple[str, ...] = (
    "Bạn chắc chắn thành công.",
    "Bạn rất may mắn.",
    "Đây là giai đoạn tốt.",
    "Bạn nên bổ Hỏa.",
    "Bạn nên mở rộng kinh doanh.",
)

ACTION_MARKERS: tuple[str, ...] = (
    "Bạn nên",
    "hãy bổ",
    "màu đỏ",
    "hướng Nam",
)

PREDICTION_MARKERS: tuple[str, ...] = (
    "chắc chắn",
    "nhất định",
    "đại cát",
    "sẽ ly hôn",
)

TECHNICAL_LEAK: tuple[str, ...] = (
    "Engine",
    "NR-REL",
    "CanonicalAnalysis",
    "{{",
    "}}",
    "JSON",
)


@dataclass(slots=True)
class SummaryValidationOutcome:
    """Summary contract result."""

    passed: bool
    reason: str = ""

    @property
    def status(self) -> str:
        """PASS or FAIL."""
        return "PASS" if self.passed else "FAIL"


class SummaryValidator:
    """Validate OverviewSummary against N-IMP-06 contract rules."""

    def validate(
        self,
        summary: OverviewSummary,
        rewrite: CommercialRewriteContext,
    ) -> SummaryValidationOutcome:
        """PASS unless the summary contract is violated."""
        try:
            self.assert_valid(summary, rewrite)
        except SummaryValidationError as exc:
            return SummaryValidationOutcome(passed=False, reason=exc.message)
        return SummaryValidationOutcome(passed=True)

    def assert_valid(
        self,
        summary: OverviewSummary,
        rewrite: CommercialRewriteContext,
    ) -> None:
        """Raise if the overview violates the summary contract."""
        self._reject_forbidden_fields(summary)
        if summary.status not in ALLOWED_STATUSES:
            raise SummaryValidationError(f"Invalid summary status: {summary.status}")
        rewrite_ids = {item.rewrite_id for item in rewrite.items}
        self._check_insight_count(summary)
        self._check_populated_fields(summary, rewrite_ids)
        self._check_language(summary)
        self._check_lengths(summary)
        self._check_duplicates(summary)

    def _reject_forbidden_fields(self, summary: OverviewSummary) -> None:
        for attr in FORBIDDEN_CONTEXT_ATTRS:
            if hasattr(summary, attr):
                raise SummaryValidationError(f"Summary must not expose {attr}")

    def _check_insight_count(self, summary: OverviewSummary) -> None:
        meta = dict(summary.metadata)
        primary = meta.get("primary_rewrite_id")
        if summary.status == "insufficient":
            if primary:
                raise SummaryValidationError("Insufficient summary must not claim a primary insight")
            return
        if not primary:
            raise SummaryValidationError("Summary missing primary insight")

    def _check_populated_fields(
        self,
        summary: OverviewSummary,
        rewrite_ids: set[str],
    ) -> None:
        populated = _populated_map(summary)
        referenced = {ref.field for ref in summary.references}
        for field, text in populated.items():
            if field not in referenced:
                raise SummaryValidationError(f"Populated field missing trace: {field}")
            del text
        for ref in summary.references:
            if not ref.rewrite_ids:
                raise SummaryValidationError(f"Trace missing rewrite_id: {ref.field}")
            for rewrite_id in ref.rewrite_ids:
                if rewrite_id not in rewrite_ids:
                    raise SummaryValidationError(f"Unknown rewrite_id: {rewrite_id}")

    def _check_language(self, summary: OverviewSummary) -> None:
        blob = _blob(summary)
        for claim in FORBIDDEN_CLAIMS:
            if claim in blob:
                raise SummaryValidationError("Forbidden generated claim in summary")
        for token in ACTION_MARKERS:
            if token in blob:
                raise SummaryValidationError("Action generated in summary")
        for token in PREDICTION_MARKERS:
            if token in blob:
                raise SummaryValidationError("Prediction generated in summary")
        for token in TECHNICAL_LEAK:
            if token in blob:
                raise SummaryValidationError("Raw technical id in summary")
        if "{" in blob or "}" in blob:
            raise SummaryValidationError("JSON/debug leak in summary")

    def _check_lengths(self, summary: OverviewSummary) -> None:
        if summary.headline is not None:
            if word_count(summary.headline) > HEADLINE_WORD_LIMIT:
                raise SummaryValidationError("Headline exceeds word limit")
            if len(split_sentences(summary.headline)) != 1:
                raise SummaryValidationError("Headline must be one sentence")
        if summary.summary is not None:
            count = len(split_sentences(summary.summary))
            if count > SUMMARY_SENTENCE_MAX:
                raise SummaryValidationError("Summary exceeds sentence limit")
        if summary.conclusion is not None:
            if len(split_sentences(summary.conclusion)) > CONCLUSION_SENTENCE_MAX:
                raise SummaryValidationError("Conclusion exceeds sentence limit")

    def _check_duplicates(self, summary: OverviewSummary) -> None:
        texts = [
            text
            for text in (
                summary.headline,
                summary.summary,
                summary.identity,
                summary.balance,
                summary.conclusion,
            )
            if text
        ]
        if len(texts) != len(set(texts)):
            raise SummaryValidationError("Overview fields repeat identical wording")


def _populated_map(summary: OverviewSummary) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for name in ("headline", "summary", "identity", "balance", "conclusion"):
        value = getattr(summary, name)
        if isinstance(value, str) and value.strip():
            mapping[name] = value
    return mapping


def _blob(summary: OverviewSummary) -> str:
    parts = [
        summary.headline or "",
        summary.summary or "",
        summary.identity or "",
        summary.balance or "",
        summary.conclusion or "",
    ]
    return " ".join(parts)
