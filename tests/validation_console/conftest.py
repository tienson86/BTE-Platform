"""Fixtures for Validation Console tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from applications.validation_console.api.app import create_app
from applications.validation_console.api.store import reset_store


@pytest.fixture
def tmp_store(tmp_path: Path):
    """Isolated dataset store."""
    store = reset_store(tmp_path / "vc_data")
    store.clear()
    return store


@pytest.fixture
def client(tmp_store) -> TestClient:
    """Fresh client with empty workspace (demo seed cleared)."""
    _ = tmp_store
    app = create_app()
    tmp_store.clear()
    return TestClient(app)
