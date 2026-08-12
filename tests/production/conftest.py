"""Shared production test fixtures."""

from __future__ import annotations

import pytest

from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.orchestrator import ProductionEndToEndOrchestrator


@pytest.fixture(scope="module")
def case_0001_generic_result(tmp_path_factory):
    """Run CASE-0001 through generic pipeline once per module."""
    export_dir = tmp_path_factory.mktemp("case_0001_generic")
    return ProductionEndToEndOrchestrator().run_case_0001(export_dir=export_dir)
