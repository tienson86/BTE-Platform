"""Shared fixtures for Narrative V2 evidence tests."""

from __future__ import annotations

from typing import Any

import pytest

from applications.api.services.orchestrator import OrchestratorService
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST


@pytest.fixture(scope="module")
def case_0001_canonical() -> dict[str, Any]:
    """Real CASE-0001 CanonicalAnalysis through luck. No hardcoded engine facts."""
    request = CASE_0001_REQUEST
    return OrchestratorService().run_stage(
        "luck",
        year=request.year,
        month=request.month,
        day=request.day,
        hour=request.hour,
        minute=request.minute,
        gender=request.gender,
        timezone=request.timezone,
    )
