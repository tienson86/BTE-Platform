"""Request normalization tests. No business assertions."""

from __future__ import annotations

from consulting.marriage.runtime.normalizer import normalize_marriage_request
from tests.consulting.runtime_fixtures import valid_request


def test_normalize_trims_display_fields_and_keeps_canonical_formats() -> None:
    """Normalization trims names/timezone and keeps date/time strings."""
    normalized = normalize_marriage_request(valid_request())
    assert normalized.person_a.full_name == "Person"
    assert normalized.person_a.timezone == "Asia/Ho_Chi_Minh"
    assert normalized.person_a.birth_date == "1987-01-21"
    assert normalized.person_a.birth_time == "04:30"
    assert normalized.person_b.birth_date == "1990-05-15"


def test_normalize_preserves_missing_birth_time() -> None:
    """Missing birth time stays None. No default hour is assigned."""
    normalized = normalize_marriage_request(valid_request(time_a=None, time_b=None))
    assert normalized.person_a.birth_time is None
    assert normalized.person_b.birth_time is None
