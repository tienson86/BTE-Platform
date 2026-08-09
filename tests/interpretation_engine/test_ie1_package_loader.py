"""IE-1 Interpretation Package loader interface tests."""

from __future__ import annotations

import pytest

from engines.interpretation_engine.exceptions.foundation_error import (
    InterpretationPackageNotReleasedError,
)
from engines.interpretation_engine.package_loader import InterpretationPackageLoader


def test_loader_lists_no_packages() -> None:
    """IE-1 admits an empty package catalog."""
    loader = InterpretationPackageLoader()
    assert loader.list_available() == ()


def test_loader_fails_closed_when_loading() -> None:
    """No Interpretation Package may load before release."""
    loader = InterpretationPackageLoader()
    with pytest.raises(
        InterpretationPackageNotReleasedError,
        match="no_interpretation_packages_released:bz_future",
    ):
        loader.load("bz_future")
