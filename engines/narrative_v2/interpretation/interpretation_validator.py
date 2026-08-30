"""InterpretationValidator — conversation-formula contract checks."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.rewrite.rewrite_context import CommercialRewriteContext
from engines.narrative_v2.interpretation.interpretation_errors import (
    InterpretationValidationError,
)
from engines.narrative_v2.interpretation.interpretation_formula import split_sentences
from engines.narrative_v2.interpretation.interpretation_model import (
    ALLOWED_STATUSES,
    CLOSING_SENTENCE_MAX,
    CONTENT_FIELDS,
    FORMULA_STAGES,
    OVERVIEW_SENTENCE_MAX,
    InterpretationNarrative,
)

FORBIDDEN_CONTEXT_ATTRS: tuple[str, ...] = (
    "canonical_analysis",
    "action_plan",
    "presentation",
    "action",
)

FORBIDDEN_CLAIMS: tuple[str, ...] = (
    "You should",
    "You will",
    "Definitely",
    "Surely",
    "Guaranteed",
    "Bạn chắc chắn thành công.",
    "Bạn rất may mắn.",
    "Đây là giai đoạn tốt.",
    "Bạn nên bổ Hỏa.",
    "Bạn nên mở rộng kinh doanh.",
)

ACTION_MARKERS: tuple[str, ...] = (
    "You should",
    "Bạn nên",
    "hãy bổ",
    "màu đỏ",
    "hướng Nam",
    "Action Plan",
    "Priority:",
)

PREDICTION_MARKERS: tuple[str, ...] = (
    "You will",
    "Definitely",
    "Surely",
    "Guaranteed",
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
class InterpretationValidationOutcome:
    """Interpretation contract result."""

    passed: bool
    reason: str = ""

    @property
    def status(self) -> str:
        """PASS or FAIL."""
        return "PASS" if self.passed else "FAIL"


class InterpretationValidator:
    """Validate InterpretationNarrative against N-IMP-07 contract rules."""

    def validate(
        self,
        narrative: InterpretationNarrative,
        rewrite: CommercialRewriteContext,
    ) -> InterpretationValidationOutcome:
        """PASS unless the interpretation contract is violated."""
        try:
            self.assert_valid(narrative, rewrite)
        except InterpretationValidationError as exc:
            return InterpretationValidationOutcome(passed=False, reason=exc.message)
        return InterpretationValidationOutcome(passed=True)

    def assert_valid(
        self,
        narrative: InterpretationNarrative,
        rewrite: CommercialRewriteContext,
    ) -> None:
        """Raise if the narrative violates the interpretation contract."""
        self._reject_forbidden_fields(narrative)
        if narrative.status not in ALLOWED_STATUSES:
            raise InterpretationValidationError(
                f"Invalid interpretation status: {narrative.status}"
            )
        self._check_formula_metadata(narrative)
        rewrite_ids = {item.rewrite_id for item in rewrite.items}
        self._check_populated_fields(narrative, rewrite_ids)
        self._check_language(narrative)
        self._check_lengths(narrative)
        self._check_duplicates(narrative)

    def _reject_forbidden_fields(self, narrative: InterpretationNarrative) -> None:
        for attr in FORBIDDEN_CONTEXT_ATTRS:
            if hasattr(narrative, attr):
                raise InterpretationValidationError(
                    f"Interpretation must not expose {attr}"
                )

    def _check_formula_metadata(self, narrative: InterpretationNarrative) -> None:
        meta = dict(narrative.metadata)
        recorded = meta.get("formula_stages")
        expected = ",".join(FORMULA_STAGES)
        if recorded != expected:
            raise InterpretationValidationError("Interpretation formula stages missing")
        if narrative.status == "insufficient":
            return
        if not meta.get("primary_rewrite_id"):
            raise InterpretationValidationError("Interpretation missing primary insight")

    def _check_populated_fields(
        self,
        narrative: InterpretationNarrative,
        rewrite_ids: set[str],
    ) -> None:
        referenced = {ref.field for ref in narrative.references}
        for field in CONTENT_FIELDS:
            value = getattr(narrative, field)
            if isinstance(value, str) and value.strip():
                if field not in referenced:
                    raise InterpretationValidationError(
                        f"Populated field missing trace: {field}"
                    )
        for ref in narrative.references:
            if not ref.rewrite_ids:
                raise InterpretationValidationError(f"Trace missing rewrite_id: {ref.field}")
            for rewrite_id in ref.rewrite_ids:
                if rewrite_id not in rewrite_ids:
                    raise InterpretationValidationError(f"Unknown rewrite_id: {rewrite_id}")

    def _check_language(self, narrative: InterpretationNarrative) -> None:
        blob = _blob(narrative)
        for claim in FORBIDDEN_CLAIMS:
            if claim in blob:
                raise InterpretationValidationError("Forbidden generated claim")
        for token in ACTION_MARKERS:
            if token in blob:
                raise InterpretationValidationError("Action generated in interpretation")
        for token in PREDICTION_MARKERS:
            if token in blob:
                raise InterpretationValidationError("Prediction generated in interpretation")
        for token in TECHNICAL_LEAK:
            if token in blob:
                raise InterpretationValidationError("Raw technical id in interpretation")
        if "{" in blob or "}" in blob:
            raise InterpretationValidationError("JSON/debug leak in interpretation")

    def _check_lengths(self, narrative: InterpretationNarrative) -> None:
        if narrative.overview is not None:
            count = len(split_sentences(narrative.overview))
            if count > OVERVIEW_SENTENCE_MAX:
                raise InterpretationValidationError("Overview exceeds sentence limit")
        if narrative.closing is not None:
            if len(split_sentences(narrative.closing)) > CLOSING_SENTENCE_MAX:
                raise InterpretationValidationError("Closing exceeds sentence limit")
        if narrative.recommendation is not None:
            lowered = narrative.recommendation
            if "Start " in lowered or lowered.startswith("Do "):
                raise InterpretationValidationError("Action generated in recommendation")

    def _check_duplicates(self, narrative: InterpretationNarrative) -> None:
        texts: list[str] = []
        for field in CONTENT_FIELDS:
            if field == "closing":
                continue
            value = getattr(narrative, field)
            if isinstance(value, str) and value.strip():
                texts.append(value)
        if len(texts) != len(set(texts)):
            raise InterpretationValidationError(
                "Interpretation fields repeat identical wording"
            )
        if (
            narrative.overview
            and narrative.closing
            and narrative.overview == narrative.closing
        ):
            raise InterpretationValidationError("Closing must not copy overview")


def _blob(narrative: InterpretationNarrative) -> str:
    parts = [getattr(narrative, field) or "" for field in CONTENT_FIELDS]
    return " ".join(parts)
