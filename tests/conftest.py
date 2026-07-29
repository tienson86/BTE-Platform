"""
Global pytest configuration.

Toàn bộ Test sẽ dùng chung các Fixture tại đây.
"""

from pathlib import Path

import pytest

from engines.score_engine.loader import ScoreLoader


# =====================================================
# Root
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = PROJECT_ROOT / "database"

# =====================================================
# Fixtures
# =====================================================

@pytest.fixture(scope="session")
def project_root():

    return PROJECT_ROOT


@pytest.fixture(scope="session")
def database_path():

    return DATABASE_PATH


@pytest.fixture(scope="session")
def score_loader():

    return ScoreLoader(

        DATABASE_PATH / "13_score_engine"

    )
