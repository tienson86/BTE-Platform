"""Contract and validation tests for LE-1 timeline."""

from __future__ import annotations

from typing import Any

import pytest

from engines.luck_engine.contracts import timeline_contract
from engines.luck_engine.exceptions import TimelineValidationError
from engines.luck_engine.timeline import construct_timeline, validate_contract_integrity
from engines.luck_engine.timeline.constants import PUBLISHED_OUTPUTS


def test_timeline_contract_has_no_scores() -> None:
    """Published contract forbids scores and interpretation."""
    contract = timeline_contract()
    assert contract["outputs"] == list(PUBLISHED_OUTPUTS)
    assert contract["scores"] is False
    assert contract["judgments"] is False
    assert contract["interpretation"] is False


def test_forbidden_metadata_field(continuous_timeline_payload: dict[str, Any]) -> None:
    """Judgment keys inside metadata must fail."""
    payload = continuous_timeline_payload
    payload["timeline_metadata"] = {"score": 80}
    with pytest.raises(TimelineValidationError, match="forbidden_field"):
        construct_timeline(**payload)


def test_incompatible_timeline_version(continuous_timeline_payload: dict[str, Any]) -> None:
    """Unknown timeline versions are rejected."""
    payload = continuous_timeline_payload
    with pytest.raises(TimelineValidationError, match="incompatible_timeline_version"):
        construct_timeline(**payload, timeline_version="9.0.0")


def test_contract_integrity_requires_outputs(continuous_timeline_payload: dict[str, Any]) -> None:
    """Missing published keys fail contract integrity."""
    timeline = construct_timeline(**continuous_timeline_payload)
    payload = timeline.to_dict()
    del payload["major_cycles"]
    with pytest.raises(TimelineValidationError, match="contract_missing"):
        validate_contract_integrity(payload)
