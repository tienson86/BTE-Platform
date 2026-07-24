"""Customer search helpers."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

from applications.customer.models import CustomerModel


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def search_customers(
    customers: Iterable[CustomerModel],
    *,
    name: str | None = None,
    phone: str | None = None,
    email: str | None = None,
    tag: str | None = None,
    created_from: str | None = None,
    created_to: str | None = None,
) -> list[CustomerModel]:
    """
    Filter customers by name / phone / email / tag / created range.

    Name, phone, email use case-insensitive substring match.
    """
    name_q = (name or "").strip().lower()
    phone_q = (phone or "").strip().lower()
    email_q = (email or "").strip().lower()
    tag_q = (tag or "").strip().lower()
    start = _parse_dt(created_from)
    end = _parse_dt(created_to)

    results: list[CustomerModel] = []
    for customer in customers:
        if name_q and name_q not in customer.full_name.lower():
            continue
        if phone_q and phone_q not in (customer.phone or "").lower():
            continue
        if email_q and email_q not in (customer.email or "").lower():
            continue
        if tag_q and tag_q not in [t.lower() for t in customer.tags]:
            continue
        created = _parse_dt(customer.created_at)
        if start and (created is None or created < start):
            continue
        if end and (created is None or created > end):
            continue
        results.append(customer)
    return results
