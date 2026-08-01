"""Analysis Engine test fixture stubs.

Shared fixture hooks only. No fixture payloads.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest


@pytest.fixture
def analysis_engine_root() -> Path:
    """Return the Analysis Engine package root path."""
    raise NotImplementedError


@pytest.fixture
def fixtures_dir() -> Path:
    """Return the fixtures directory path."""
    raise NotImplementedError


@pytest.fixture
def snapshots_dir() -> Path:
    """Return the snapshots directory path."""
    raise NotImplementedError


@pytest.fixture
def golden_dir() -> Path:
    """Return the golden dataset directory path."""
    raise NotImplementedError


@pytest.fixture
def analysis_context_stub() -> object:
    """Return a shared analysis context stub for framework wiring."""
    raise NotImplementedError
