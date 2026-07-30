"""Golden Dataset Manager service layer."""

from __future__ import annotations

import uuid
from typing import Any

from applications.validation_console.api.compare import compare_outputs
from applications.validation_console.api.coverage import (
    compute_coverage,
    compute_statistics,
)
from applications.validation_console.api.models import (
    CaseCompareResult,
    DatasetStatus,
    GoldenCase,
    GoldenDataset,
    HistoryEntry,
    RegressionReport,
    utc_now,
)
from applications.validation_console.api.store import DatasetStore, get_store
from applications.validation_console.api.validators import (
    ValidationIssue,
    validate_case_payload,
    validate_cases,
    validate_dataset_payload,
)


class ValidationConsoleError(Exception):
    """Base Validation Console error."""

    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class NotFoundError(ValidationConsoleError):
    """Dataset or case not found."""


class ValidationError(ValidationConsoleError):
    """Payload validation failed."""

    def __init__(
        self,
        message: str,
        *,
        issues: list[ValidationIssue],
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, details=details)
        self.issues = issues


class WorkflowError(ValidationConsoleError):
    """Illegal lifecycle transition."""


_TRANSITIONS: dict[str, set[DatasetStatus]] = {
    "submit": {"draft", "rejected"},
    "approve": {"review"},
    "reject": {"review"},
    "release": {"approved"},
}

_NEXT_STATUS: dict[str, DatasetStatus] = {
    "submit": "review",
    "approve": "approved",
    "reject": "rejected",
    "release": "released",
}


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def _bump_patch(version: str) -> str:
    parts = version.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        return "0.1.1"
    major, minor, patch = (int(part) for part in parts)
    return f"{major}.{minor}.{patch + 1}"


def _case_from_payload(payload: dict[str, Any]) -> GoldenCase:
    return GoldenCase.from_dict(
        {
            "case_id": payload["case_id"],
            "description": payload.get("description") or "",
            "input_fixture": payload.get("input_fixture") or {},
            "expected_output": payload.get("expected_output") or {},
            "actual_output": payload.get("actual_output"),
            "tags": payload.get("tags") or [],
            "coverage_goal": payload.get("coverage_goal") or "",
            "tolerance_policy": payload.get("tolerance_policy") or "exact",
            "metadata": payload.get("metadata") or {},
        }
    )


class GoldenDatasetService:
    """Create, import, compare, regress, approve, stats, coverage."""

    def __init__(self, store: DatasetStore | None = None) -> None:
        self._store = store or get_store()

    def list_datasets(
        self,
        *,
        status: str | None = None,
        module: str | None = None,
    ) -> list[dict[str, Any]]:
        """List managed datasets."""
        return [
            dataset.to_dict()
            for dataset in self._store.list_datasets(status=status, module=module)
        ]

    def get_dataset(self, dataset_id: str) -> dict[str, Any]:
        """Return one dataset."""
        return self._require(dataset_id).to_dict()

    def create_dataset(
        self,
        *,
        name: str,
        description: str = "",
        module: str = "general",
        cases: list[dict[str, Any]] | None = None,
        actor: str = "editor",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Create a draft dataset (optionally with cases)."""
        issues = validate_dataset_payload(name=name, cases=cases)
        errors = [issue for issue in issues if issue.severity == "error"]
        if errors:
            raise ValidationError("Dataset validation failed", issues=issues)

        now = utc_now()
        parsed_cases = [_case_from_payload(item) for item in cases or []]
        dataset = GoldenDataset(
            dataset_id=_new_id("ds"),
            name=name.strip(),
            description=description.strip(),
            module=module.strip() or "general",
            status="draft",
            version="0.1.0",
            cases=parsed_cases,
            history=[
                HistoryEntry(
                    event_id=_new_id("evt"),
                    action="created",
                    actor=actor,
                    at=now,
                    message="Dataset created as draft",
                    details={"case_count": len(parsed_cases)},
                )
            ],
            created_at=now,
            updated_at=now,
            created_by=actor,
            updated_by=actor,
            metadata=dict(metadata or {}),
        )
        return self._store.upsert(dataset).to_dict()

    def import_dataset(
        self,
        *,
        name: str,
        cases: list[dict[str, Any]],
        description: str = "",
        module: str = "general",
        actor: str = "editor",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Import a dataset bundle into the workspace."""
        if not cases:
            raise ValidationError(
                "Import requires at least one case",
                issues=[
                    ValidationIssue(
                        code="empty_import",
                        severity="error",
                        message="cases must not be empty",
                        path="cases",
                    )
                ],
            )
        return self.create_dataset(
            name=name,
            description=description or f"Imported dataset ({len(cases)} cases)",
            module=module,
            cases=cases,
            actor=actor,
            metadata={**(metadata or {}), "imported": True},
        )

    def add_case(
        self,
        dataset_id: str,
        *,
        case: dict[str, Any],
        actor: str = "editor",
    ) -> dict[str, Any]:
        """Add a case to a draft/rejected dataset."""
        dataset = self._require_editable(dataset_id)
        issues = validate_case_payload(case)
        errors = [issue for issue in issues if issue.severity == "error"]
        if errors:
            raise ValidationError("Case validation failed", issues=issues)
        case_id = str(case["case_id"])
        if any(existing.case_id == case_id for existing in dataset.cases):
            raise ValidationError(
                f"Duplicate case_id: {case_id}",
                issues=[
                    ValidationIssue(
                        code="duplicate_case_id",
                        severity="error",
                        message=f"Duplicate case_id: {case_id}",
                        path="case_id",
                    )
                ],
            )
        now = utc_now()
        dataset.cases.append(_case_from_payload(case))
        dataset.updated_at = now
        dataset.updated_by = actor
        if dataset.status == "rejected":
            dataset.status = "draft"
        dataset.history.insert(
            0,
            HistoryEntry(
                event_id=_new_id("evt"),
                action="case_added",
                actor=actor,
                at=now,
                message=f"Added case {case_id}",
            ),
        )
        return self._store.upsert(dataset).to_dict()

    def set_actual(
        self,
        dataset_id: str,
        case_id: str,
        *,
        actual_output: dict[str, Any],
        actor: str = "editor",
    ) -> dict[str, Any]:
        """Attach actual output for a case (used by compare/regression)."""
        dataset = self._require(dataset_id)
        case = self._require_case(dataset, case_id)
        case.actual_output = dict(actual_output)
        now = utc_now()
        dataset.updated_at = now
        dataset.updated_by = actor
        dataset.history.insert(
            0,
            HistoryEntry(
                event_id=_new_id("evt"),
                action="actual_set",
                actor=actor,
                at=now,
                message=f"Set actual for {case_id}",
            ),
        )
        return self._store.upsert(dataset).to_dict()

    def compare(
        self,
        dataset_id: str,
        *,
        case_id: str | None = None,
    ) -> dict[str, Any]:
        """Compare expected vs actual for one or all cases."""
        dataset = self._require(dataset_id)
        targets = dataset.cases
        if case_id:
            targets = [self._require_case(dataset, case_id)]
        results = [self._compare_case(case) for case in targets]
        return {
            "dataset_id": dataset_id,
            "results": [item.to_dict() for item in results],
            "summary": _summarize(results),
        }

    def run_regression(
        self,
        dataset_id: str,
        *,
        actor: str = "validator",
    ) -> dict[str, Any]:
        """Run regression across all cases and store a report."""
        dataset = self._require(dataset_id)
        results = [self._compare_case(case) for case in dataset.cases]
        summary = _summarize(results)
        now = utc_now()
        report = RegressionReport(
            report_id=_new_id("rpt"),
            dataset_id=dataset_id,
            ran_at=now,
            actor=actor,
            total=summary["total"],
            passed=summary["passed"],
            failed=summary["failed"],
            skipped=summary["skipped"],
            errors=summary["errors"],
            case_results=results,
        )
        dataset.reports.insert(0, report)
        dataset.updated_at = now
        dataset.updated_by = actor
        dataset.history.insert(
            0,
            HistoryEntry(
                event_id=_new_id("evt"),
                action="regression",
                actor=actor,
                at=now,
                message=(
                    f"Regression: {report.passed}/{report.total} passed, "
                    f"{report.failed} failed"
                ),
                details=summary,
            ),
        )
        self._store.upsert(dataset)
        return report.to_dict()

    def statistics(self, dataset_id: str) -> dict[str, Any]:
        """Return dataset statistics."""
        return compute_statistics(self._require(dataset_id))

    def coverage(self, dataset_id: str) -> dict[str, Any]:
        """Return coverage report."""
        return compute_coverage(self._require(dataset_id))

    def approval_queue(self) -> list[dict[str, Any]]:
        """Datasets awaiting review."""
        return self.list_datasets(status="review")

    def transition(
        self,
        dataset_id: str,
        *,
        action: str,
        actor: str = "reviewer",
        message: str = "",
    ) -> dict[str, Any]:
        """Apply approval workflow transition."""
        if action not in _TRANSITIONS:
            raise WorkflowError(
                f"Unknown workflow action: {action}",
                details={"action": action},
            )
        dataset = self._require(dataset_id)
        if dataset.status not in _TRANSITIONS[action]:
            raise WorkflowError(
                f"Cannot {action} from status '{dataset.status}'",
                details={
                    "status": dataset.status,
                    "allowed_from": sorted(_TRANSITIONS[action]),
                },
            )
        issues = validate_cases(dataset.cases)
        if action in {"submit", "approve", "release"}:
            errors = [issue for issue in issues if issue.severity == "error"]
            if errors:
                raise ValidationError(
                    f"Cannot {action}: dataset has validation errors",
                    issues=issues,
                )
            if action in {"approve", "release"} and not dataset.cases:
                raise ValidationError(
                    f"Cannot {action}: dataset has no cases",
                    issues=[
                        ValidationIssue(
                            code="empty_dataset",
                            severity="error",
                            message="dataset must contain at least one case",
                            path="cases",
                        )
                    ],
                )

        now = utc_now()
        dataset.status = _NEXT_STATUS[action]
        dataset.updated_at = now
        dataset.updated_by = actor
        if action in {"approve", "release"}:
            dataset.version = _bump_patch(dataset.version)
        dataset.history.insert(
            0,
            HistoryEntry(
                event_id=_new_id("evt"),
                action=action,
                actor=actor,
                at=now,
                message=message or f"Workflow action: {action}",
                details={"status": dataset.status, "version": dataset.version},
            ),
        )
        return self._store.upsert(dataset).to_dict()

    def _compare_case(self, case: GoldenCase) -> CaseCompareResult:
        if case.actual_output is None:
            return CaseCompareResult(
                case_id=case.case_id,
                status="skip",
                message="No actual_output attached",
            )
        differences = compare_outputs(case.expected_output, case.actual_output)
        if differences:
            return CaseCompareResult(
                case_id=case.case_id,
                status="fail",
                differences=differences,
                message=f"{len(differences)} difference(s)",
            )
        return CaseCompareResult(
            case_id=case.case_id,
            status="pass",
            message="Exact match",
        )

    def _require(self, dataset_id: str) -> GoldenDataset:
        dataset = self._store.get(dataset_id)
        if dataset is None:
            raise NotFoundError(
                f"Dataset not found: {dataset_id}",
                details={"dataset_id": dataset_id},
            )
        return dataset

    def _require_editable(self, dataset_id: str) -> GoldenDataset:
        dataset = self._require(dataset_id)
        if dataset.status not in {"draft", "rejected"}:
            raise WorkflowError(
                "Only draft or rejected datasets can be edited",
                details={"status": dataset.status},
            )
        return dataset

    @staticmethod
    def _require_case(dataset: GoldenDataset, case_id: str) -> GoldenCase:
        for case in dataset.cases:
            if case.case_id == case_id:
                return case
        raise NotFoundError(
            f"Case not found: {case_id}",
            details={"dataset_id": dataset.dataset_id, "case_id": case_id},
        )


def _summarize(results: list[CaseCompareResult]) -> dict[str, int]:
    summary = {
        "total": len(results),
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "errors": 0,
    }
    for item in results:
        if item.status == "pass":
            summary["passed"] += 1
        elif item.status == "fail":
            summary["failed"] += 1
        elif item.status == "skip":
            summary["skipped"] += 1
        else:
            summary["errors"] += 1
    return summary


def seed_demo_datasets(service: GoldenDatasetService | None = None) -> None:
    """Seed a sample dataset when workspace is empty."""
    svc = service or GoldenDatasetService()
    if svc.list_datasets():
        return
    svc.create_dataset(
        name="Demo Strength Cases",
        description="Sample golden dataset for Validation Console",
        module="strength",
        actor="system",
        cases=[
            {
                "case_id": "case_0001",
                "description": "Strong day master sample",
                "input_fixture": {
                    "birth": {
                        "gender": "male",
                        "timezone": "Asia/Ho_Chi_Minh",
                        "location": "HCM",
                        "datetime": "1990-05-15T10:30:00",
                    }
                },
                "expected_output": {
                    "strength": "strong",
                    "score": 72,
                },
                "actual_output": {
                    "strength": "strong",
                    "score": 72,
                },
                "tags": ["strength", "canonical"],
                "coverage_goal": "canonical",
            },
            {
                "case_id": "case_0002",
                "description": "Boundary weak sample",
                "input_fixture": {
                    "birth": {
                        "gender": "female",
                        "timezone": "Asia/Ho_Chi_Minh",
                        "location": "HN",
                        "datetime": "1988-01-02T06:00:00",
                    }
                },
                "expected_output": {
                    "strength": "weak",
                    "score": 28,
                },
                "actual_output": {
                    "strength": "weak",
                    "score": 30,
                },
                "tags": ["strength", "boundary"],
                "coverage_goal": "boundary",
            },
            {
                "case_id": "case_0003",
                "description": "Conflict placeholder without actual",
                "input_fixture": {"note": "conflict fixture"},
                "expected_output": {"strength": "balanced"},
                "tags": ["conflict"],
                "coverage_goal": "conflict",
            },
        ],
    )
