"""Customer statistics (read-only via repository factory)."""

from __future__ import annotations

from typing import Any

from applications.storage.factory import RepositoryBundle, RepositoryFactory
from applications.storage.interfaces.customer_repository import CustomerRepository


def customer_statistics(
    repository: CustomerRepository | None = None,
    *,
    bundle: RepositoryBundle | None = None,
) -> dict[str, Any]:
    """Aggregate customer counts and tag distribution."""
    repo = repository or (bundle or RepositoryFactory.create()).customers
    customers = repo.list()
    tags: dict[str, int] = {}
    with_email = 0
    with_phone = 0
    for customer in customers:
        if customer.email:
            with_email += 1
        if customer.phone:
            with_phone += 1
        for tag in customer.tags:
            tags[tag] = tags.get(tag, 0) + 1
    return {
        "customer_count": len(customers),
        "with_email": with_email,
        "with_phone": with_phone,
        "tag_counts": tags,
    }
