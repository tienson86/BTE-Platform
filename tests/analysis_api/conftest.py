"""Fixtures for Analysis Engine API tests."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from engines.analysis_engine.api.app import create_app
from engines.analysis_engine.api.config import settings
from engines.analysis_engine.api.dependencies import get_resource_store


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """Fresh app client with cleared store and auth optional."""
    monkeypatch.setattr(settings, "auth_required", False)
    monkeypatch.setattr(settings, "default_anonymous_role", "ANALYST")
    get_resource_store().clear()
    return TestClient(create_app())
