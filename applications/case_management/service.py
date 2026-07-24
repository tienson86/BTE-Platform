"""Case management service + customer analyze orchestration."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Callable

from applications.case_management.exporter import CaseExporter, ExportFormat
from applications.case_management.history import list_customer_history
from applications.case_management.models import CaseModel
from applications.case_management.repository import CaseRepository
from applications.customer.models import CustomerModel
from applications.customer.service import CustomerNotFoundError, CustomerService


class CaseNotFoundError(LookupError):
    """Case id not found."""


class CaseServiceError(ValueError):
    """Invalid case operation."""


AnalyzeFn = Callable[..., dict[str, Any]]


def parse_birth_parts(
    birth_datetime: str | None,
) -> tuple[int, int, int, int, int]:
    """Parse ISO birth_datetime into year/month/day/hour/minute."""
    if not birth_datetime:
        raise CaseServiceError("Customer birth_datetime is required for analyze")
    try:
        value = datetime.fromisoformat(birth_datetime.replace("Z", "+00:00"))
    except ValueError as exc:
        raise CaseServiceError("Invalid customer birth_datetime") from exc
    return value.year, value.month, value.day, value.hour, value.minute


class CaseService:
    """CRUD cases, history, export, and analyze-by-customer."""

    def __init__(
        self,
        repository: CaseRepository,
        customer_service: CustomerService,
        *,
        analyze_fn: AnalyzeFn | None = None,
        engine_version: str = "1.0.0",
        exporter: CaseExporter | None = None,
    ) -> None:
        self.repository = repository
        self.customer_service = customer_service
        self.analyze_fn = analyze_fn
        self.engine_version = engine_version
        self.exporter = exporter or CaseExporter()

    def create(self, case: CaseModel) -> CaseModel:
        """Persist a case (customer must exist)."""
        self.customer_service.get(case.customer_id)
        return self.repository.create(case)

    def get(self, case_id: str) -> CaseModel:
        """Get case or raise."""
        case = self.repository.get(case_id)
        if case is None:
            raise CaseNotFoundError(case_id)
        return case

    def list(self, *, customer_id: str | None = None) -> list[CaseModel]:
        """List cases; optionally filter by customer."""
        if customer_id:
            return self.repository.list_by_customer(customer_id)
        return self.repository.list()

    def delete(self, case_id: str) -> bool:
        """Delete a case."""
        return self.repository.delete(case_id)

    def history(self, customer_id: str) -> list[dict[str, Any]]:
        """Interpretation history for a customer."""
        self.customer_service.get(customer_id)
        return list_customer_history(self.repository, customer_id)

    def export(self, case_id: str, fmt: ExportFormat = "json") -> str:
        """Export a case in json/markdown/html."""
        return self.exporter.export(self.get(case_id), fmt)

    def analyze_customer(
        self,
        customer_id: str,
        *,
        overrides: dict[str, Any] | None = None,
    ) -> tuple[CustomerModel, CaseModel, dict[str, Any]]:
        """
        Run full pipeline for a customer and store a Case.

        ``overrides`` may supply year/month/day/hour/minute/gender/timezone.
        """
        if self.analyze_fn is None:
            raise CaseServiceError("analyze_fn is not configured")

        customer = self.customer_service.get(customer_id)
        year, month, day, hour, minute = parse_birth_parts(customer.birth_datetime)
        gender = customer.gender
        timezone = customer.timezone

        if overrides:
            year = int(overrides.get("year", year))
            month = int(overrides.get("month", month))
            day = int(overrides.get("day", day))
            hour = int(overrides.get("hour", hour))
            minute = int(overrides.get("minute", minute))
            if "gender" in overrides:
                gender = overrides.get("gender")
            if overrides.get("timezone"):
                timezone = str(overrides["timezone"])

        input_snapshot = {
            "customer_id": customer.customer_id,
            "full_name": customer.full_name,
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "gender": gender,
            "timezone": timezone,
            "birth_datetime": customer.birth_datetime,
        }

        result = self.analyze_fn(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            gender=gender,
            timezone=timezone,
        )

        case = CaseModel.create(
            customer_id=customer.customer_id,
            engine_version=self.engine_version,
            input_snapshot=input_snapshot,
            calendar_result=dict(result.get("calendar") or {}),
            bazi_result=dict(result.get("bazi") or {}),
            pattern_result=dict(result.get("pattern") or {}),
            score_result=dict(result.get("score") or {}),
            interpretation_result=dict(result.get("interpretation") or {}),
            report_result=dict(result.get("report") or {}),
            narrative_result=dict(result.get("narrative") or {}),
        )
        self.repository.create(case)
        return customer, case, result


__all__ = [
    "CaseNotFoundError",
    "CaseService",
    "CaseServiceError",
    "parse_birth_parts",
]
