"""AI response validation models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


VALIDATION_CHECKS: tuple[str, ...] = (
    "contradiction",
    "unsupported_claims",
    "missing_evidence",
    "hallucination_risk",
    "confidence_mismatch",
)

WarningSeverity = Literal["low", "medium", "high"]


@dataclass(slots=True)
class ValidationWarning:
    """One validation warning raised against an AI response."""

    code: str
    severity: WarningSeverity
    message: str
    paragraph_index: int | None = None
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize warning."""
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "paragraph_index": self.paragraph_index,
            "detail": dict(self.detail),
        }


@dataclass(slots=True)
class ParagraphValidation:
    """Per-paragraph reference and warning summary."""

    index: int
    text: str
    references_evidence: bool
    references_knowledge: bool
    references_reasoning: bool
    warnings: list[ValidationWarning] = field(default_factory=list)

    @property
    def references_all(self) -> bool:
        """True when paragraph cites Evidence, Knowledge, and Reasoning."""
        return (
            self.references_evidence
            and self.references_knowledge
            and self.references_reasoning
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize paragraph validation."""
        return {
            "index": self.index,
            "text": self.text,
            "references_evidence": self.references_evidence,
            "references_knowledge": self.references_knowledge,
            "references_reasoning": self.references_reasoning,
            "references_all": self.references_all,
            "warnings": [row.to_dict() for row in self.warnings],
        }


@dataclass(slots=True)
class ValidationReport:
    """Result of validating an AI response against evidence, knowledge, and reasoning."""

    confidence: float
    warnings: list[ValidationWarning]
    paragraphs: list[ParagraphValidation] = field(default_factory=list)
    checks: dict[str, dict[str, Any]] = field(default_factory=dict)
    passed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def warnings_for(self, code: str) -> list[ValidationWarning]:
        """Return warnings matching a validation check code."""
        key = str(code or "").strip().lower()
        return [row for row in self.warnings if row.code == key]

    def to_dict(self) -> dict[str, Any]:
        """Serialize validation report."""
        return {
            "confidence": self.confidence,
            "warnings": [row.to_dict() for row in self.warnings],
            "paragraphs": [row.to_dict() for row in self.paragraphs],
            "checks": dict(self.checks),
            "passed": self.passed,
            "metadata": dict(self.metadata),
        }
