"""Luck Foundation package loading tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from engines.luck_engine.exceptions import LuckPackageLoadError
from engines.luck_engine.timeline import LuckPackageLoader
from engines.luck_engine.timeline_constants import PACKAGE_ID, PUBLISHED_INPUTS, PUBLISHED_OUTPUTS


def test_load_released_luck_foundation() -> None:
    """Released bz_09 package admits with published contracts."""
    loaded = LuckPackageLoader().load()
    assert loaded.package_id == PACKAGE_ID
    assert loaded.package_version == "1.0.0"
    assert loaded.schema_version == "2.0.0"
    assert loaded.status == "released"
    assert loaded.checksum and len(loaded.checksum) == 64
    assert loaded.published_inputs == PUBLISHED_INPUTS
    assert loaded.published_outputs == PUBLISHED_OUTPUTS


def test_missing_package_fails(tmp_path: Path) -> None:
    """Missing PACKAGE.json fails closed."""
    with pytest.raises(LuckPackageLoadError, match="package_not_found"):
        LuckPackageLoader(package_root=tmp_path / "missing").load()


def test_incompatible_constraint_fails() -> None:
    """SemVer constraint mismatch is rejected."""
    with pytest.raises(LuckPackageLoadError, match="incompatible_package_version"):
        LuckPackageLoader().load(version_constraint="^9.0.0")
