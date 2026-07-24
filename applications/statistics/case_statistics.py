"""Case statistics (read-only via repository factory)."""

from __future__ import annotations

from typing import Any

from applications.storage.factory import RepositoryBundle, RepositoryFactory
from applications.storage.interfaces.case_repository import CaseRepository


def case_statistics(
    repository: CaseRepository | None = None,
    *,
    bundle: RepositoryBundle | None = None,
) -> dict[str, Any]:
    """Aggregate case counts by customer / engine version."""
    repo = repository or (bundle or RepositoryFactory.create()).cases
    cases = repo.list()
    by_customer: dict[str, int] = {}
    by_engine: dict[str, int] = {}
    for case in cases:
        by_customer[case.customer_id] = by_customer.get(case.customer_id, 0) + 1
        by_engine[case.engine_version] = by_engine.get(case.engine_version, 0) + 1
    return {
        "case_count": len(cases),
        "customers_with_cases": len(by_customer),
        "by_engine_version": by_engine,
    }
