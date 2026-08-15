"""Quality gates and duplicate-content detection for knowledge entities."""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, Mapping

from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntity
from engines.interpretation_engine.foundation.knowledge.status import KnowledgeStatus

_TOKEN_RE = re.compile(
    r"thực thần|thương quan|tỷ kiên|kiếp tài|chính tài|thiên tài|"
    r"chính quan|thất sát|chính ấn|thiên ấn|"
    r"giáp|ất|bính|đinh|mậu|kỷ|canh|tân|nhâm|quý|"
    r"thân vượng|thân nhược|trung hòa|rất vượng|rất nhược|"
    r"\bvery_strong\b|\bvery_weak\b|\bstrong\b|\bbalanced\b|\bweak\b",
    re.IGNORECASE,
)
_WS_RE = re.compile(r"\s+")

APPROVED_MIN_APPLICATIONS = 3
APPROVED_MIN_RECOMMENDATIONS = 2
APPROVED_MIN_WARNINGS = 1
APPROVED_MIN_CONCEPTS = 1
DUPLICATE_APPLICATION_ENTITY_FLOOR = 3


@dataclass(frozen=True, slots=True)
class QualityIssue:
    """One quality or duplication issue."""

    code: str
    message: str
    entity_id: str = ""

    def to_dict(self) -> dict[str, str]:
        """Serialize issue."""
        return {
            "code": self.code,
            "message": self.message,
            "entity_id": self.entity_id,
        }


@dataclass(frozen=True, slots=True)
class KnowledgeQualityResult:
    """Outcome of content-quality evaluation."""

    passed: bool
    issues: tuple[QualityIssue, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize quality result."""
        return {
            "passed": self.passed,
            "issues": [item.to_dict() for item in self.issues],
        }


@dataclass(frozen=True, slots=True)
class DuplicateContentWarning:
    """Normalized exact/near-exact duplication across entities."""

    code: str
    message: str
    entity_ids: tuple[str, ...]
    fingerprint: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize duplication warning."""
        return {
            "code": self.code,
            "message": self.message,
            "entity_ids": list(self.entity_ids),
            "fingerprint": self.fingerprint,
        }


class KnowledgeQualityGate:
    """Minimum content requirements for approved knowledge entities."""

    def evaluate(self, entity: KnowledgeEntity) -> KnowledgeQualityResult:
        """Evaluate one entity against K2 approved-content requirements."""
        issues: list[QualityIssue] = []
        if not entity.meaning.strip():
            issues.append(_issue("missing_meaning", "missing meaning", entity.id))
        if not entity.positive_meaning.strip():
            issues.append(
                _issue("missing_positive_meaning", "missing positive_meaning", entity.id)
            )
        if not entity.negative_meaning.strip():
            issues.append(
                _issue("missing_negative_meaning", "missing negative_meaning", entity.id)
            )
        if len(_meaningful_applications(entity.applications)) < APPROVED_MIN_APPLICATIONS:
            issues.append(
                _issue(
                    "insufficient_applications",
                    "approved entity requires >= 3 meaningful applications",
                    entity.id,
                )
            )
        if len(_meaningful_recommendations(entity.recommendations)) < APPROVED_MIN_RECOMMENDATIONS:
            issues.append(
                _issue(
                    "insufficient_recommendations",
                    "approved entity requires >= 2 recommendations",
                    entity.id,
                )
            )
        if len(_meaningful_warnings(entity.warnings)) < APPROVED_MIN_WARNINGS:
            issues.append(
                _issue(
                    "insufficient_warnings",
                    "approved entity requires >= 1 warning",
                    entity.id,
                )
            )
        if len(entity.concept_ids) < APPROVED_MIN_CONCEPTS:
            issues.append(
                _issue(
                    "missing_concept_reference",
                    "approved entity requires >= 1 concept_id",
                    entity.id,
                )
            )
        if not entity.evidence_notes.strip():
            issues.append(
                _issue("missing_evidence_notes", "missing evidence_notes", entity.id)
            )
        if not entity.metadata.author or not entity.metadata.version:
            issues.append(_issue("invalid_metadata", "metadata incomplete", entity.id))
        return KnowledgeQualityResult(passed=not issues, issues=tuple(issues))

    def evaluate_approved(self, entities: list[KnowledgeEntity]) -> KnowledgeQualityResult:
        """Evaluate all approved entities; drafts are not quality-gated."""
        issues: list[QualityIssue] = []
        for entity in entities:
            if entity.metadata.status != KnowledgeStatus.APPROVED:
                continue
            result = self.evaluate(entity)
            issues.extend(result.issues)
        return KnowledgeQualityResult(passed=not issues, issues=tuple(issues))


class DuplicateContentDetector:
    """Lightweight normalized exact/near-exact duplication detector."""

    def detect(self, entities: list[KnowledgeEntity]) -> tuple[DuplicateContentWarning, ...]:
        """Find identical meaning, recommendations, or widely copied applications."""
        warnings: list[DuplicateContentWarning] = []
        warnings.extend(self._group_field(entities, "meaning", lambda item: item.meaning))
        warnings.extend(self._identical_recommendations(entities))
        warnings.extend(self._copied_applications(entities))
        return tuple(warnings)

    def _group_field(
        self,
        entities: list[KnowledgeEntity],
        field_name: str,
        getter: Callable[[KnowledgeEntity], str],
    ) -> list[DuplicateContentWarning]:
        """Group entities that share a stem-invariant field fingerprint."""
        buckets: dict[str, list[str]] = defaultdict(list)
        for entity in entities:
            fingerprint = _fingerprint(str(getter(entity)))
            if not fingerprint:
                continue
            buckets[fingerprint].append(entity.id)
        warnings: list[DuplicateContentWarning] = []
        for fingerprint, entity_ids in buckets.items():
            unique_ids = tuple(dict.fromkeys(entity_ids))
            if len(unique_ids) < 2:
                continue
            warnings.append(
                DuplicateContentWarning(
                    code=f"duplicate_{field_name}",
                    message=f"identical {field_name} across {len(unique_ids)} entities",
                    entity_ids=unique_ids,
                    fingerprint=fingerprint[:120],
                )
            )
        return warnings

    def _identical_recommendations(
        self,
        entities: list[KnowledgeEntity],
    ) -> list[DuplicateContentWarning]:
        """Detect identical recommendation action text reused across stems."""
        buckets: dict[str, list[str]] = defaultdict(list)
        for entity in entities:
            for item in entity.recommendations:
                action = str(item.get("action") or "")
                fingerprint = _fingerprint(action)
                if not fingerprint:
                    continue
                buckets[fingerprint].append(entity.id)
        warnings: list[DuplicateContentWarning] = []
        for fingerprint, entity_ids in buckets.items():
            unique_ids = tuple(dict.fromkeys(entity_ids))
            if len(unique_ids) < 2:
                continue
            warnings.append(
                DuplicateContentWarning(
                    code="duplicate_recommendation",
                    message=(
                        "identical recommendation action across "
                        f"{len(unique_ids)} entities"
                    ),
                    entity_ids=unique_ids,
                    fingerprint=fingerprint[:120],
                )
            )
        return warnings

    def _copied_applications(
        self,
        entities: list[KnowledgeEntity],
    ) -> list[DuplicateContentWarning]:
        """Detect application text copied across most entities."""
        buckets: dict[tuple[str, str], list[str]] = defaultdict(list)
        for entity in entities:
            for domain, text in entity.applications.items():
                fingerprint = _fingerprint(str(text))
                if not fingerprint:
                    continue
                buckets[(domain, fingerprint)].append(entity.id)
        warnings: list[DuplicateContentWarning] = []
        for (domain, fingerprint), entity_ids in buckets.items():
            unique_ids = tuple(dict.fromkeys(entity_ids))
            if len(unique_ids) < DUPLICATE_APPLICATION_ENTITY_FLOOR:
                continue
            warnings.append(
                DuplicateContentWarning(
                    code="duplicate_application",
                    message=(
                        f"application '{domain}' copied across "
                        f"{len(unique_ids)} entities"
                    ),
                    entity_ids=unique_ids,
                    fingerprint=fingerprint[:120],
                )
            )
        return warnings


def _meaningful_applications(applications: Mapping[str, str]) -> dict[str, str]:
    """Return applications with non-empty values."""
    return {
        key: value
        for key, value in applications.items()
        if str(key).strip() and str(value).strip()
    }


def _meaningful_recommendations(items: tuple[Mapping[str, Any], ...]) -> list[str]:
    """Return recommendation actions that contain substance."""
    results: list[str] = []
    for item in items:
        action = str(item.get("action") or "").strip()
        if action:
            results.append(action)
    return results


def _meaningful_warnings(items: tuple[Mapping[str, Any], ...]) -> list[str]:
    """Return warnings that contain a risk or condition."""
    results: list[str] = []
    for item in items:
        text = str(item.get("risk") or item.get("condition") or "").strip()
        if text:
            results.append(text)
    return results


def _fingerprint(text: str) -> str:
    """Normalize text for exact/near-exact comparison."""
    lowered = text.strip().lower()
    if not lowered:
        return ""
    replaced = _TOKEN_RE.sub("{token}", lowered)
    return _WS_RE.sub(" ", replaced)


def _issue(code: str, message: str, entity_id: str) -> QualityIssue:
    """Build one quality issue."""
    return QualityIssue(code=code, message=message, entity_id=entity_id)
