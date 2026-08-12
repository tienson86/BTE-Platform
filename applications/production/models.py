"""Production pipeline result models."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ProductionRequest:
    """Birth input for production end-to-end pipeline."""

    case_id: str
    year: int
    month: int
    day: int
    hour: int
    minute: int
    gender: str
    timezone: str = "Asia/Bangkok"
    full_name: str = ""
    birth_place: str = ""
    export_pdf: bool = True
    export_dir: Path | None = None


@dataclass(slots=True)
class CustomerDeliverable:
    """Customer Mode output — no validation, evidence, or internal runtime."""

    case_id: str
    profile_name: str
    executive_consulting: str
    master_interpretation_parts: dict[str, str] = field(default_factory=dict)
    strength_interpretation: dict[str, Any] = field(default_factory=dict)
    report_summary: str = ""
    recommendations: list[str] = field(default_factory=list)
    pipeline_stages: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize customer-safe payload."""
        return {
            "case_id": self.case_id,
            "profile_name": self.profile_name,
            "executive_consulting": self.executive_consulting,
            "master_interpretation_parts": dict(self.master_interpretation_parts),
            "strength_interpretation": dict(self.strength_interpretation),
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

    def to_customer_dict(self) -> dict[str, Any]:
        """Return customer-visible payload only."""
        payload = self.customer.to_dict()
        if self.pdf_path is not None:
            payload["pdf_path"] = str(self.pdf_path)
        payload["success"] = self.success
        payload["stages_completed"] = list(self.stages_completed)
        return payload
