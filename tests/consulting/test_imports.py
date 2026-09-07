"""Skeleton import tests. No business assertions."""

from __future__ import annotations

import importlib

import pytest

PACKAGE_MODULES = (
    "consulting",
    "consulting.marriage",
    "consulting.marriage.constants",
    "consulting.marriage.exceptions",
    "consulting.marriage.models",
    "consulting.marriage.dto",
    "consulting.marriage.contracts",
    "consulting.marriage.orchestrator",
    "consulting.marriage.runtime",
    "consulting.marriage.policy",
    "consulting.marriage.evidence",
    "consulting.marriage.finding",
    "consulting.marriage.decision",
    "consulting.marriage.recommendation",
    "consulting.marriage.report",
    "consulting.marriage.presentation",
    "consulting.marriage.api",
    "consulting.marriage.ui",
    "consulting.marriage.repository",
    "consulting.marriage.adapters",
    "consulting.marriage.validation",
)


@pytest.mark.parametrize("module_name", PACKAGE_MODULES)
def test_package_imports(module_name: str) -> None:
    """Each skeleton package must import without executing business logic."""
    module = importlib.import_module(module_name)
    assert module is not None


def test_public_exports() -> None:
    """Public TV-01 contract names must be importable from the package root."""
    from consulting.marriage import (
        BUILD_PHASE,
        MODULE_ID,
        MarriageApiContract,
        MarriageDecisionContext,
        MarriageOrchestrator,
        MarriagePolicyProvider,
        MarriageRecommendationProvider,
        MarriageReportProfile,
        MarriageRepository,
        MarriageRuntimeContext,
        MarriageUILayoutProfile,
        MarriageValidationContract,
        wire_marriage_runtime,
    )

    assert MODULE_ID == "TV-01_MARRIAGE"
    assert BUILD_PHASE == "TV1-B01"
    assert MarriageOrchestrator is not None
    assert MarriageRuntimeContext is not None
    assert MarriageRepository is not None
    assert MarriagePolicyProvider is not None
    assert MarriageDecisionContext is not None
    assert MarriageRecommendationProvider is not None
    assert MarriageReportProfile is not None
    assert MarriageUILayoutProfile is not None
    assert MarriageApiContract is not None
    assert MarriageValidationContract is not None
    assert callable(wire_marriage_runtime)
