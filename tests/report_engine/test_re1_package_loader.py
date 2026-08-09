"""RE-1 Report Package loader interface tests."""

from __future__ import annotations

import pytest

from engines.report_engine.exceptions.foundation_error import ReportPackageNotReleasedError
from engines.report_engine.package_loader import ReportPackageLoader


def test_loader_lists_no_packages() -> None:
    """RE-1 admits an empty package catalog."""
    loader = ReportPackageLoader()
    assert loader.list_available() == ()


def test_loader_fails_closed_when_loading() -> None:
    """No Report Package may load before release."""
    loader = ReportPackageLoader()
    with pytest.raises(
        ReportPackageNotReleasedError,
        match="no_report_packages_released:rp_future",
    ):
        loader.load("rp_future")
