"""Fixtures for Knowledge Console API tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from applications.knowledge_console.api.app import create_app
from applications.knowledge_console.api.store import reset_store


@pytest.fixture
def tmp_store(tmp_path: Path):
    """Isolated asset store for each test."""
    store = reset_store(tmp_path / "kc_data")
    store.clear()
    return store


@pytest.fixture
def client(tmp_store) -> TestClient:
    """Fresh FastAPI client with empty store (no demo seed)."""
    _ = tmp_store
    # Avoid seeding demo assets into the test store.
    app = create_app()
    # create_app seeds when empty — clear again after seed for deterministic tests
    tmp_store.clear()
    return TestClient(app)


@pytest.fixture
def seeded_client(tmp_store) -> TestClient:
    """Client with demo seed assets available."""
    _ = tmp_store
    return TestClient(create_app())
