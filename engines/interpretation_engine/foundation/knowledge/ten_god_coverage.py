"""Coverage index and quality report for Ten Gods knowledge V1."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from engines.interpretation_engine.foundation.concepts.registry import ConceptRegistry
from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntity
from engines.interpretation_engine.foundation.knowledge.entity_types import TEN_GOD_KEYS
from engines.interpretation_engine.foundation.knowledge.quality import (
    DuplicateContentDetector,
    KnowledgeQualityGate,
)
from engines.interpretation_engine.foundation.knowledge.registry import (
    DEFAULT_KNOWLEDGE_ROOT,
    KnowledgeRegistry,
)
from engines.interpretation_engine.foundation.knowledge.status import KnowledgeStatus
from engines.interpretation_engine.foundation.knowledge.validator import KnowledgeValidator

TEN_GOD_ORDER: tuple[str, ...] = TEN_GOD_KEYS


@dataclass(frozen=True, slots=True)
class TenGodQualityReport:
    """Machine-readable Ten Gods knowledge quality report."""

    entity_count: int
    approved_count: int
    draft_count: int
    concept_count: int
    broken_references: tuple[str, ...]
    missing_required_content: tuple[str, ...]
    duplicate_content_warnings: tuple[dict[str, Any], ...]
    application_coverage: dict[str, int]
    recommendation_coverage: int
    warning_coverage: int
    ten_god_status: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        """Serialize report."""
        return {
            "entity_count": self.entity_count,
            "approved_count": self.approved_count,
            "draft_count": self.draft_count,
            "concept_count": self.concept_count,
            "broken_references": list(self.broken_references),
            "missing_required_content": list(self.missing_required_content),
            "duplicate_content_warnings": list(self.duplicate_content_warnings),
            "application_coverage": dict(self.application_coverage),
            "recommendation_coverage": self.recommendation_coverage,
            "warning_coverage": self.warning_coverage,
            "ten_god_status": dict(self.ten_god_status),
        }

    def to_markdown(self) -> str:
        """Render coverage index."""
        lines = ["# Ten Gods Knowledge V1", "", "## Ten Gods", ""]
        for key in TEN_GOD_ORDER:
            status = self.ten_god_status.get(key, "MISSING")
            lines.append(f"{key:<16} {status}")
        lines.extend(
            [
                "",
                "## Coverage",
                "",
                f"- entity count: {self.entity_count}",
                f"- approved: {self.approved_count}",
                f"- draft: {self.draft_count}",
                f"- concept count: {self.concept_count}",
                f"- entities with recommendations: {self.recommendation_coverage}",
                f"- entities with warnings: {self.warning_coverage}",
                f"- broken references: {len(self.broken_references)}",
                f"- missing required content: {len(self.missing_required_content)}",
                f"- duplicate-content warnings: {len(self.duplicate_content_warnings)}",
                "",
                "### Application coverage",
                "",
            ]
        )
        for domain, count in sorted(self.application_coverage.items()):
            lines.append(f"- {domain}: {count}/{self.entity_count}")
        lines.append("")
        return "\n".join(lines)


def build_ten_god_quality_report(
    *,
    knowledge_registry: KnowledgeRegistry | None = None,
    concept_registry: ConceptRegistry | None = None,
) -> TenGodQualityReport:
    """Build Ten Gods coverage/quality report from loaded registries."""
    knowledge = knowledge_registry or KnowledgeRegistry.default()
    concepts = concept_registry or ConceptRegistry.default()
    entities = list(knowledge.list("TenGods"))
    validation = KnowledgeValidator().validate(
        entities,
        known_concept_ids=concepts.known_ids(),
    )
    broken = tuple(
        f"{issue.code}: {issue.message}"
        for issue in validation.issues
        if issue.code in {"broken_reference", "broken_concept_reference"}
    )
    quality = KnowledgeQualityGate().evaluate_approved(entities)
    missing_required = tuple(
        f"{issue.entity_id}: {issue.code}" for issue in quality.issues
    )
    duplicates = DuplicateContentDetector().detect(entities)
    application_counts: Counter[str] = Counter()
    recommendation_entities = 0
    warning_entities = 0
    for entity in entities:
        for domain, text in entity.applications.items():
            if str(text).strip():
                application_counts[domain] += 1
        if any(str(item.get("action") or "").strip() for item in entity.recommendations):
            recommendation_entities += 1
        if any(
            str(item.get("risk") or item.get("condition") or "").strip()
            for item in entity.warnings
        ):
            warning_entities += 1
    by_key = {entity.key: entity for entity in entities}
    ten_god_status = {key: _status(by_key.get(key)) for key in TEN_GOD_ORDER}
    return TenGodQualityReport(
        entity_count=len(entities),
        approved_count=sum(
            1 for entity in entities if entity.metadata.status == KnowledgeStatus.APPROVED
        ),
        draft_count=sum(
            1 for entity in entities if entity.metadata.status == KnowledgeStatus.DRAFT
        ),
        concept_count=len(
            {concept_id for entity in entities for concept_id in entity.concept_ids}
        ),
        broken_references=broken,
        missing_required_content=missing_required,
        duplicate_content_warnings=tuple(item.to_dict() for item in duplicates),
        application_coverage=dict(application_counts),
        recommendation_coverage=recommendation_entities,
        warning_coverage=warning_entities,
        ten_god_status=ten_god_status,
    )


def write_ten_god_reports(
    *,
    knowledge_root: Path | None = None,
    report: TenGodQualityReport | None = None,
) -> tuple[Path, Path]:
    """Write coverage markdown and machine-readable quality JSON."""
    payload = report or build_ten_god_quality_report()
    root = knowledge_root or DEFAULT_KNOWLEDGE_ROOT
    coverage_path = root / "domains" / "ten_gods" / "COVERAGE.md"
    quality_path = root / "reports" / "ten_gods_k5_quality.json"
    quality_path.parent.mkdir(parents=True, exist_ok=True)
    coverage_path.parent.mkdir(parents=True, exist_ok=True)
    coverage_path.write_text(payload.to_markdown(), encoding="utf-8")
    quality_path.write_text(
        json.dumps(payload.to_dict(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return coverage_path, quality_path


def _status(entity: KnowledgeEntity | None) -> str:
    """Return coverage status label for one Ten God."""
    if entity is None:
        return "MISSING"
    return entity.metadata.status.value.upper()
