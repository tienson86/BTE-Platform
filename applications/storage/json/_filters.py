"""Shared in-memory filter helpers for JSON backends."""

from __future__ import annotations

from datetime import datetime

from applications.case_management.models import CaseModel
from applications.customer.models import CustomerModel
from applications.storage.interfaces.repository import CaseFilter, CustomerFilter


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def match_customer(customer: CustomerModel, filters: CustomerFilter) -> bool:
    """Return True if customer matches filter criteria."""
    if filters.name:
        needle = filters.name.strip().lower()
        if needle not in customer.full_name.lower():
            return False
    if filters.phone:
        needle = filters.phone.strip().lower()
        if needle not in (customer.phone or "").lower():
            return False
    if filters.email:
        needle = filters.email.strip().lower()
        if needle not in (customer.email or "").lower():
            return False
    if filters.tag:
        needle = filters.tag.strip().lower()
        if needle not in [tag.lower() for tag in customer.tags]:
            return False
    created = _parse_dt(customer.created_at)
    start = _parse_dt(filters.created_from)
    end = _parse_dt(filters.created_to)
    if start and (created is None or created < start):
        return False
    if end and (created is None or created > end):
        return False
    return True


def match_case(case: CaseModel, filters: CaseFilter) -> bool:
    """Return True if case matches filter criteria."""
    if filters.customer_id and case.customer_id != filters.customer_id:
        return False
    if filters.engine_version and case.engine_version != filters.engine_version:
        return False
    created = _parse_dt(case.created_at)
    start = _parse_dt(filters.created_from)
    end = _parse_dt(filters.created_to)
    if start and (created is None or created < start):
        return False
    if end and (created is None or created > end):
        return False
    return True
