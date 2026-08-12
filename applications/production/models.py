"""Production pipeline result models."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class SectionStatus(str, Enum):
    """Customer section availability."""

    AVAILABLE = "AVAILABLE"
    PARTIAL = "PARTIAL"
    NOT_AVAILABLE = "NOT_AVAILABLE"


EXECUTIVE_CONSULTING_NOT_AVAILABLE = "EXECUTIVE_CONSULTING_NOT_AVAILABLE"


@dataclass(slots=True)
class ProductionRequest:
    """Birth input for production end-to-end pipeline."""

    year: int
    month: int
    day: int
    hour: int
    minute: int
    gender: str
    timezone: str = "Asia/Bangkok"
    full_name: str = ""
    birth_place: str = ""
    case_id: str = ""
    export_pdf: bool = True
    export_dir: Path | None = None
    options: dict[str, Any] = field(default_factory=dict)

    @property
    def birth_date(self) -> str:
        """ISO birth date string."""
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"

    @property
    def birth_time(self) -> str:
        """HH:MM birth time string."""
        return f"{self.hour:02d}:{self.minute:02d}"

    @property
    def request_key(self) -> str:
        """Stable key for exports when case_id is absent."""
        if self.case_id:
            return self.case_id
        return (
            f"{self.birth_date}_{self.birth_time}_{self.gender}_{self.timezone}"
        ).replace(":", "").replace("-", "")


@dataclass(slots=True)
class SectionAvailability:
    """Per-section availability for customer deliverable."""

    strength_interpretation: SectionStatus = SectionStatus.NOT_AVAILABLE
    ten_gods_interpretation: SectionStatus = SectionStatus.NOT_AVAILABLE
    pattern_interpretation: SectionStatus = SectionStatus.NOT_AVAILABLE
    useful_god_interpretation: SectionStatus = SectionStatus.NOT_AVAILABLE
    executive_consulting: SectionStatus = SectionStatus.NOT_AVAILABLE
    identity_report: SectionStatus = SectionStatus.NOT_AVAILABLE
    career_report: SectionStatus = SectionStatus.NOT_AVAILABLE
    master_interpretation: SectionStatus = SectionStatus.NOT_AVAILABLE
    report: SectionStatus = SectionStatus.NOT_AVAILABLE

    def to_dict(self) -> dict[str, str]:
        """Serialize section statuses."""
        return {
            "strength_interpretation": self.strength_interpretation.value,
            "ten_gods_interpretation": self.ten_gods_interpretation.value,
            "pattern_interpretation": self.pattern_interpretation.value,
            "useful_god_interpretation": self.useful_god_interpretation.value,
            "executive_consulting": self.executive_consulting.value,
            "identity_report": self.identity_report.value,
            "career_report": self.career_report.value,
            "master_interpretation": self.master_interpretation.value,
            "report": self.report.value,
        }


@dataclass(slots=True)
class CustomerDeliverable:
    """Customer Mode output — no validation, evidence, or internal runtime."""

    case_id: str
    profile_name: str
    executive_consulting: str
    section_status: SectionAvailability = field(default_factory=SectionAvailability)
    master_interpretation_parts: dict[str, str] = field(default_factory=dict)
    strength_interpretation: dict[str, Any] = field(default_factory=dict)
    ten_gods_interpretation: dict[str, Any] = field(default_factory=dict)
    pattern_interpretation: dict[str, Any] = field(default_factory=dict)
    useful_god_interpretation: dict[str, Any] = field(default_factory=dict)
    identity_report: str = ""
    career_report: str = ""
    report_summary: str = ""
    recommendations: list[str] = field(default_factory=list)
    pipeline_stages: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize customer-safe payload."""
        return {
            "case_id": self.case_id,
            "profile_name": self.profile_name,
            "executive_consulting": self.executive_consulting,
            "section_status": self.section_status.to_dict(),
            "master_interpretation_parts": dict(self.master_interpretation_parts),
            "strength_interpretation": dict(self.strength_interpretation),
            "ten_gods_interpretation": dict(self.ten_gods_interpretation),
            "pattern_interpretation": dict(self.pattern_interpretation),
            "useful_god_interpretation": dict(self.useful_god_interpretation),
            "identity_report": self.identity_report,
            "career_report": self.career_report,
            "report_summary": self.report_summary,
            "recommendations": list(self.recommendations),
            "pipeline_stages": list(self.pipeline_stages),
        }


@dataclass(slots=True)
class ProductionPipelineResult:
    """Full production pipeline outcome."""

    success: bool
    case_id: str
    customer: CustomerDeliverable
    pdf_path: Path | None = None
    report_input_version: str = "1.0"
    stages_completed: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    diagnostics: dict[str, Any] = field(default_factory=dict)

    def to_customer_dict(self) -> dict[str, Any]:
        """Return customer-visible payload only."""
        payload = self.customer.to_dict()
        if self.pdf_path is not None:
            payload["pdf_path"] = str(self.pdf_path)
        payload["success"] = self.success
        payload["stages_completed"] = list(self.stages_completed)
        return payload
