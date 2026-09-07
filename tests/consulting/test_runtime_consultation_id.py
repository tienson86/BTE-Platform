"""Consultation ID tests. No business assertions."""

from __future__ import annotations

from datetime import datetime, timezone

from consulting.marriage.runtime.consultation_id import (
    generate_consultation_id,
    is_consultation_id,
)


def test_consultation_id_matches_standard_form() -> None:
    """IDs use MC-YYYYMMDD-XXXXXX."""
    moment = datetime(2026, 9, 7, tzinfo=timezone.utc)
    value = generate_consultation_id(moment)
    assert is_consultation_id(value)
    assert value.startswith("MC-20260907-")
    assert len(value.split("-")[2]) == 6


def test_consultation_id_is_unique_per_call() -> None:
    """Each generated id is distinct. Stability is per runtime, not global."""
    first = generate_consultation_id()
    second = generate_consultation_id()
    assert first != second
    assert is_consultation_id(first)
    assert is_consultation_id(second)
