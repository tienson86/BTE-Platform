"""Case history helpers."""

from __future__ import annotations

from typing import Any

from applications.case_management.models import CaseModel
from applications.case_management.repository import CaseRepository


def list_customer_history(
    repository: CaseRepository,
    customer_id: str,
) -> list[dict[str, Any]]:
    """
    Return a lightweight history timeline for a customer.

    Full engine payloads stay on the case record; history lists summaries.
    """
    history: list[dict[str, Any]] = []
    for case in repository.list_by_customer(customer_id):
        history.append(summarize_case(case))
    return history


def summarize_case(case: CaseModel) -> dict[str, Any]:
    """Compact case summary for history listings."""
    report = case.report_result or {}
    narrative = case.narrative_result or {}
    interpretation = case.interpretation_result or {}
    return {
        "case_id": case.case_id,
        "customer_id": case.customer_id,
        "created_at": case.created_at,
        "engine_version": case.engine_version,
        "summary": interpretation.get("summary", ""),
        "report_title": report.get("title", ""),
        "narrative_title": narrative.get("title", ""),
        "sentence_count": interpretation.get("sentence_count", 0),
    }
