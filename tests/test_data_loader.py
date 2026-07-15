"""
Kiểm thử Data Loader.
"""

from pathlib import Path

from engines.score_engine.loader import ScoreLoader


DATABASE = Path("database") / "13_score_engine"


def test_create_loader():

    loader = ScoreLoader(DATABASE)

    assert loader is not None


def test_database_exists():

    assert DATABASE.exists()


def test_group_exists():

    loader = ScoreLoader(DATABASE)

    assert loader.exists("02_wuxing")


def test_list_groups():

    loader = ScoreLoader(DATABASE)

    groups = loader.list_groups()

    assert isinstance(groups, list)

    assert len(groups) > 0


def test_load_group():

    loader = ScoreLoader(DATABASE)

    data = loader.load_group(

        "02_wuxing"

    )

    assert isinstance(data, dict)

    assert len(data) > 0


def test_cache():

    loader = ScoreLoader(DATABASE)

    loader.load_group("02_wuxing")

    assert loader.cache_size() > 0
