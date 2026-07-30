"""Coverage and statistics helpers."""

from __future__ import annotations

from typing import Any

from applications.validation_console.api.models import GoldenDataset, RegressionReport


def compute_statistics(dataset: GoldenDataset) -> dict[str, Any]:
    """Aggregate case and latest regression statistics."""
    cases = dataset.cases
    with_actual = sum(1 for case in cases if case.actual_output is not None)
    without_actual = len(cases) - with_actual
    tags = sorted({tag for case in cases for tag in case.tags})
    latest = dataset.reports[0] if dataset.reports else None
    return {
        "dataset_id": dataset.dataset_id,
        "case_count": len(cases),
        "with_actual": with_actual,
        "without_actual": without_actual,
        "unique_tags": tags,
        "tag_count": len(tags),
        "report_count": len(dataset.reports),
        "latest_regression": None if latest is None else _report_summary(latest),
        "status": dataset.status,
        "version": dataset.version,
    }


def compute_coverage(dataset: GoldenDataset) -> dict[str, Any]:
    """Compute tag and coverage-goal coverage for the dataset."""
    cases = dataset.cases
    tag_counts: dict[str, int] = {}
    goal_counts: dict[str, int] = {}
    for case in cases:
        for tag in case.tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        goal = case.coverage_goal.strip() or "unspecified"
        goal_counts[goal] = goal_counts.get(goal, 0) + 1

    required_goals = {
        "canonical",
        "boundary",
        "conflict",
        "locale",
    }
    covered_goals = {
        goal for goal in goal_counts if goal in required_goals
    }
    missing_goals = sorted(required_goals - covered_goals)
    coverage_ratio = (
        0.0
        if not required_goals
        else round(len(covered_goals) / len(required_goals), 4)
    )
    return {
        "dataset_id": dataset.dataset_id,
        "case_count": len(cases),
        "tag_coverage": [
            {"tag": tag, "count": count}
            for tag, count in sorted(tag_counts.items())
        ],
        "goal_coverage": [
            {"goal": goal, "count": count}
            for goal, count in sorted(goal_counts.items())
        ],
        "required_goals": sorted(required_goals),
        "covered_goals": sorted(covered_goals),
        "missing_goals": missing_goals,
        "coverage_ratio": coverage_ratio,
        "complete": len(missing_goals) == 0 and len(cases) > 0,
    }


def _report_summary(report: RegressionReport) -> dict[str, Any]:
    return {
        "report_id": report.report_id,
        "ran_at": report.ran_at,
        "total": report.total,
        "passed": report.passed,
        "failed": report.failed,
        "skipped": report.skipped,
        "errors": report.errors,
        "pass_rate": (
            0.0
            if report.total == 0
            else round(report.passed / report.total, 4)
        ),
    }
