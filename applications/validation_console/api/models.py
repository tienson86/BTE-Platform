"""Domain models for Validation Console Golden Dataset Manager."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

DatasetStatus = Literal["draft", "review", "approved", "released", "rejected"]
CaseResultStatus = Literal["pass", "fail", "skip", "error"]

DATASET_STATUSES: tuple[DatasetStatus, ...] = (
    "draft",
    "review",
    "approved",
    "released",
    "rejected",
)


def utc_now() -> str:
    """Return ISO-8601 UTC timestamp."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(slots=True)
class GoldenCase:
    """One golden case inside a managed dataset."""

    case_id: str
    description: str
    input_fixture: dict[str, Any]
    expected_output: dict[str, Any]
    actual_output: dict[str, Any] | None = None
    tags: list[str] = field(default_factory=list)
    coverage_goal: str = ""
    tolerance_policy: str = "exact"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize case."""
        return {
            "case_id": self.case_id,
            "description": self.description,
            "input_fixture": dict(self.input_fixture),
            "expected_output": dict(self.expected_output),
            "actual_output": (
                None if self.actual_output is None else dict(self.actual_output)
            ),
            "tags": list(self.tags),
            "coverage_goal": self.coverage_goal,
            "tolerance_policy": self.tolerance_policy,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> GoldenCase:
        """Rebuild case from payload."""
        actual = payload.get("actual_output")
        return cls(
            case_id=str(payload["case_id"]),
            description=str(payload.get("description") or ""),
            input_fixture=dict(payload.get("input_fixture") or {}),
            expected_output=dict(payload.get("expected_output") or {}),
            actual_output=None if actual is None else dict(actual),
            tags=[str(tag) for tag in payload.get("tags") or []],
            coverage_goal=str(payload.get("coverage_goal") or ""),
            tolerance_policy=str(payload.get("tolerance_policy") or "exact"),
            metadata=dict(payload.get("metadata") or {}),
        )


@dataclass(slots=True)
class DiffItem:
    """One field-level difference."""

    field: str
    expected: Any
    actual: Any

    def to_dict(self) -> dict[str, Any]:
        """Serialize diff item."""
        return asdict(self)


@dataclass(slots=True)
class CaseCompareResult:
    """Compare result for one case."""

    case_id: str
    status: CaseResultStatus
    differences: list[DiffItem] = field(default_factory=list)
    message: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize case compare result."""
        return {
            "case_id": self.case_id,
            "status": self.status,
            "differences": [item.to_dict() for item in self.differences],
            "message": self.message,
        }


@dataclass(slots=True)
class RegressionReport:
    """Regression run summary for a dataset."""

    report_id: str
    dataset_id: str
    ran_at: str
    actor: str
    total: int
    passed: int
    failed: int
    skipped: int
    errors: int
    case_results: list[CaseCompareResult] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize regression report."""
        return {
            "report_id": self.report_id,
            "dataset_id": self.dataset_id,
            "ran_at": self.ran_at,
            "actor": self.actor,
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "skipped": self.skipped,
            "errors": self.errors,
            "case_results": [item.to_dict() for item in self.case_results],
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> RegressionReport:
        """Rebuild report."""
        results = []
        for item in payload.get("case_results") or []:
            results.append(
                CaseCompareResult(
                    case_id=str(item["case_id"]),
                    status=item.get("status") or "error",
                    differences=[
                        DiffItem(**diff) for diff in item.get("differences") or []
                    ],
                    message=str(item.get("message") or ""),
                )
            )
        return cls(
            report_id=str(payload["report_id"]),
            dataset_id=str(payload["dataset_id"]),
            ran_at=str(payload.get("ran_at") or utc_now()),
            actor=str(payload.get("actor") or "system"),
            total=int(payload.get("total") or 0),
            passed=int(payload.get("passed") or 0),
            failed=int(payload.get("failed") or 0),
            skipped=int(payload.get("skipped") or 0),
            errors=int(payload.get("errors") or 0),
            case_results=results,
        )


@dataclass(slots=True)
class HistoryEntry:
    """Dataset history event."""

    event_id: str
    action: str
    actor: str
    at: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize history entry."""
        return asdict(self)


@dataclass(slots=True)
class GoldenDataset:
    """Managed golden dataset in Validation Console workspace."""

    dataset_id: str
    name: str
    description: str = ""
    version: str = "0.1.0"
    status: DatasetStatus = "draft"
    module: str = "general"
    cases: list[GoldenCase] = field(default_factory=list)
    reports: list[RegressionReport] = field(default_factory=list)
    history: list[HistoryEntry] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    created_by: str = "editor"
    updated_by: str = "editor"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize dataset."""
        return {
            "dataset_id": self.dataset_id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "status": self.status,
            "module": self.module,
            "cases": [case.to_dict() for case in self.cases],
            "reports": [report.to_dict() for report in self.reports],
            "history": [item.to_dict() for item in self.history],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "metadata": dict(self.metadata),
            "case_count": len(self.cases),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> GoldenDataset:
        """Rebuild dataset."""
        return cls(
            dataset_id=str(payload["dataset_id"]),
            name=str(payload.get("name") or ""),
            description=str(payload.get("description") or ""),
            version=str(payload.get("version") or "0.1.0"),
            status=payload.get("status") or "draft",
            module=str(payload.get("module") or "general"),
            cases=[GoldenCase.from_dict(item) for item in payload.get("cases") or []],
            reports=[
                RegressionReport.from_dict(item)
                for item in payload.get("reports") or []
            ],
            history=[
                HistoryEntry(**item) for item in payload.get("history") or []
            ],
            created_at=str(payload.get("created_at") or utc_now()),
            updated_at=str(payload.get("updated_at") or utc_now()),
            created_by=str(payload.get("created_by") or "editor"),
            updated_by=str(payload.get("updated_by") or "editor"),
            metadata=dict(payload.get("metadata") or {}),
        )
