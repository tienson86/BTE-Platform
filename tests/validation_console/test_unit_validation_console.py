"""Unit tests for Validation Console Golden Dataset Manager."""

from __future__ import annotations

from pathlib import Path

import pytest

from applications.validation_console.api.compare import compare_outputs
from applications.validation_console.api.coverage import (
    compute_coverage,
    compute_statistics,
)
from applications.validation_console.api.services import (
    GoldenDatasetService,
    ValidationError,
    WorkflowError,
)
from applications.validation_console.api.store import DatasetStore
from applications.validation_console.api.validators import validate_dataset_payload


def test_compare_outputs_detects_field_diff() -> None:
    diffs = compare_outputs({"score": 10, "label": "a"}, {"score": 11, "label": "a"})
    assert len(diffs) == 1
    assert diffs[0].field == "score"
    assert diffs[0].expected == 10
    assert diffs[0].actual == 11


def test_validate_dataset_requires_name() -> None:
    issues = validate_dataset_payload(name="", cases=[])
    assert any(issue.code == "missing_name" for issue in issues)


def test_create_import_compare_regression(tmp_path: Path) -> None:
    service = GoldenDatasetService(DatasetStore(tmp_path / "data"))
    created = service.create_dataset(
        name="Unit Pack",
        module="strength",
        cases=[
            {
                "case_id": "case_u001",
                "description": "match",
                "input_fixture": {"x": 1},
                "expected_output": {"v": 1},
                "actual_output": {"v": 1},
                "tags": ["canonical"],
                "coverage_goal": "canonical",
            },
            {
                "case_id": "case_u002",
                "description": "mismatch",
                "input_fixture": {"x": 2},
                "expected_output": {"v": 2},
                "actual_output": {"v": 9},
                "tags": ["boundary"],
                "coverage_goal": "boundary",
            },
        ],
    )
    dataset_id = created["dataset_id"]
    compared = service.compare(dataset_id)
    assert compared["summary"]["passed"] == 1
    assert compared["summary"]["failed"] == 1

    report = service.run_regression(dataset_id, actor="tester")
    assert report["passed"] == 1
    assert report["failed"] == 1
    assert report["total"] == 2

    stats = service.statistics(dataset_id)
    assert stats["case_count"] == 2
    assert stats["with_actual"] == 2
    assert stats["latest_regression"]["failed"] == 1

    coverage = service.coverage(dataset_id)
    assert "canonical" in coverage["covered_goals"]
    assert "boundary" in coverage["covered_goals"]
    assert "conflict" in coverage["missing_goals"]
    assert coverage["complete"] is False


def test_import_and_approval_workflow(tmp_path: Path) -> None:
    service = GoldenDatasetService(DatasetStore(tmp_path / "data"))
    imported = service.import_dataset(
        name="Import Pack",
        cases=[
            {
                "case_id": "case_i001",
                "description": "imported",
                "input_fixture": {},
                "expected_output": {"ok": True},
                "tags": ["locale"],
                "coverage_goal": "locale",
            }
        ],
    )
    dataset_id = imported["dataset_id"]
    assert imported["metadata"].get("imported") is True

    submitted = service.transition(dataset_id, action="submit", actor="editor")
    assert submitted["status"] == "review"

    with pytest.raises(WorkflowError):
        service.add_case(
            dataset_id,
            case={
                "case_id": "case_i002",
                "description": "blocked",
                "input_fixture": {},
                "expected_output": {"ok": True},
            },
        )

    approved = service.transition(dataset_id, action="approve", actor="reviewer")
    assert approved["status"] == "approved"
    released = service.transition(dataset_id, action="release", actor="publisher")
    assert released["status"] == "released"


def test_create_rejects_invalid_case(tmp_path: Path) -> None:
    service = GoldenDatasetService(DatasetStore(tmp_path / "data"))
    with pytest.raises(ValidationError):
        service.create_dataset(
            name="Bad",
            cases=[{"case_id": "x", "description": "", "input_fixture": {}}],
        )


def test_coverage_helpers_on_empty(tmp_path: Path) -> None:
    service = GoldenDatasetService(DatasetStore(tmp_path / "data"))
    created = service.create_dataset(name="Empty")
    dataset = service._require(created["dataset_id"])
    stats = compute_statistics(dataset)
    coverage = compute_coverage(dataset)
    assert stats["case_count"] == 0
    assert coverage["complete"] is False
