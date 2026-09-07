"""Semantic report models. Document structure only. No renderer data."""

from __future__ import annotations

from dataclasses import dataclass, field

from consulting.marriage.models.enums import MarriageDomain


@dataclass(slots=True)
class ReportMetadata:
    """Report identity and version references. Correlation ids are not Canonical-native."""

    consultation_id: str
    module_version: str
    policy_version: str
    recommendation_version: str
    narrative_version: str
    report_profile_version: str
    report_model_version: str
    language: str
    audience: str
    created_at: str
    person_a_correlation_id: str
    person_b_correlation_id: str


@dataclass(slots=True)
class ReportBlock:
    """Smallest semantic report unit. No CSS or layout coordinates."""

    block_id: str
    kind: str
    title: str | None = None
    body: str | None = None
    semantic_key: str | None = None
    domain: MarriageDomain | None = None
    state: str | None = None
    visibility: str = "customer"
    source_finding_ids: list[str] = field(default_factory=list)
    source_recommendation_ids: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ReportSection:
    """One report section in the customer story order."""

    section_id: str
    title: str
    summary: str | None = None
    blocks: list[ReportBlock] = field(default_factory=list)
    visibility: str = "customer"


@dataclass(slots=True)
class MarriageReportModel:
    """Semantic marriage report. Not PDF, DOCX, or HTML."""

    metadata: ReportMetadata
    sections: list[ReportSection] = field(default_factory=list)
