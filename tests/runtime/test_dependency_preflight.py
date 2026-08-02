"""Tests for runtime dependency preflight (distribution ↔ import mapping)."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from runtime.dependencies import (
    DISTRIBUTION_IMPORT_MAP,
    IMPORT_TO_DISTRIBUTION,
    PackageSpec,
    check_package,
    check_required_packages,
    is_distribution_installed,
    normalize_distribution_name,
    resolve_package_spec,
)
from runtime.manager import check_requirements


class TestNormalizeAndResolve:
    """Name normalization and distribution ↔ import resolution."""

    def test_normalize_distribution_name(self) -> None:
        assert normalize_distribution_name("PyYAML") == "pyyaml"
        assert normalize_distribution_name("python_dateutil") == "python-dateutil"
        assert normalize_distribution_name("  Pandas ") == "pandas"

    def test_resolve_python_dateutil_from_distribution(self) -> None:
        spec = resolve_package_spec("python-dateutil")
        assert spec == PackageSpec(
            distribution="python-dateutil",
            import_name="dateutil",
        )

    def test_resolve_dateutil_from_import_alias(self) -> None:
        """Legacy import-style tokens still map to the pip distribution."""
        spec = resolve_package_spec("dateutil")
        assert spec.distribution == "python-dateutil"
        assert spec.import_name == "dateutil"

    def test_resolve_pyyaml_from_distribution(self) -> None:
        spec = resolve_package_spec("PyYAML")
        assert spec.distribution == "pyyaml"
        assert spec.import_name == "yaml"

    def test_resolve_yaml_from_import_alias(self) -> None:
        spec = resolve_package_spec("yaml")
        assert spec.distribution == "pyyaml"
        assert spec.import_name == "yaml"

    def test_resolve_identity_pandas(self) -> None:
        spec = resolve_package_spec("pandas")
        assert spec.distribution == "pandas"
        assert spec.import_name == "pandas"

    def test_map_is_general_not_dateutil_only(self) -> None:
        assert "python-dateutil" in DISTRIBUTION_IMPORT_MAP
        assert "pyyaml" in DISTRIBUTION_IMPORT_MAP
        assert IMPORT_TO_DISTRIBUTION["dateutil"] == "python-dateutil"
        assert IMPORT_TO_DISTRIBUTION["yaml"] == "pyyaml"
        assert len(DISTRIBUTION_IMPORT_MAP) >= 2

    def test_empty_name_raises(self) -> None:
        with pytest.raises(ValueError):
            resolve_package_spec("  ")


class TestCheckPackage:
    """Per-package import + metadata diagnostics."""

    def test_importable_package_ok_even_if_wrong_metadata_name(self) -> None:
        """
        importlib.metadata has no distribution named 'dateutil', but the
        module imports via python-dateutil. Checker must still pass.
        """
        spec = resolve_package_spec("dateutil")
        assert is_distribution_installed("dateutil") is False
        assert is_distribution_installed("python-dateutil") is True
        result = check_package(spec)
        assert result.ok is True
        assert result.importable is True
        assert result.distribution_found is True

    def test_pandas_importable_ok(self) -> None:
        result = check_package(resolve_package_spec("pandas"))
        assert result.ok is True
        assert result.spec.pip_name == "pandas"

    def test_missing_reports_pip_name_not_import_alias(self) -> None:
        def _boom(_name: str) -> None:
            raise ModuleNotFoundError("No module named 'dateutil'")

        with (
            patch("runtime.dependencies.import_module", side_effect=_boom),
            patch(
                "runtime.dependencies.is_distribution_installed",
                return_value=False,
            ),
        ):
            ok, message, results = check_required_packages(names=["python-dateutil"])
        assert ok is False
        assert message.startswith("Missing packages: python-dateutil")
        assert results[0].spec.pip_name == "python-dateutil"

    def test_distribution_present_but_import_broken_message(self) -> None:
        def _boom(_name: str) -> None:
            raise ImportError("DLL load failed")

        with (
            patch("runtime.dependencies.import_module", side_effect=_boom),
            patch(
                "runtime.dependencies.is_distribution_installed",
                return_value=True,
            ),
        ):
            ok, message, _ = check_required_packages(names=["pandas"])
        assert ok is False
        assert "pandas" in message
        assert "distribution present" in message
        assert "import 'pandas' failed" in message


class TestCheckRequirementsIntegration:
    """manager.check_requirements wiring + real installed packages."""

    def test_installed_pandas_and_dateutil_not_reported_missing(self) -> None:
        ok, message, results = check_required_packages(
            names=["pandas", "python-dateutil", "dateutil", "pyyaml", "yaml"]
        )
        assert ok is True, message
        by_import = {item.spec.import_name: item for item in results}
        assert by_import["pandas"].ok
        assert by_import["dateutil"].ok
        assert by_import["yaml"].ok
        assert "Missing packages" not in message

    def test_manager_does_not_false_flag_installed_core_libs(self) -> None:
        """
        Full required set may still fail on unrelated packages (e.g. uvicorn),
        but must not list pandas or python-dateutil when they import cleanly.
        """
        result = check_requirements()
        if result.ok:
            return
        assert "Missing packages:" in result.message
        missing_segment = result.message.split("Missing packages:", 1)[1]
        missing_segment = missing_segment.split(". Install", 1)[0]
        tokens = []
        for chunk in missing_segment.split(","):
            chunk = chunk.strip()
            if not chunk:
                continue
            tokens.append(chunk.split()[0])
        assert "pandas" not in tokens
        assert "python-dateutil" not in tokens
        assert "dateutil" not in tokens

    def test_check_required_accepts_mixed_spec_styles(self) -> None:
        ok, message, results = check_required_packages(
            names=["pandas", "dateutil", "yaml"]
        )
        assert ok is True, message
        dists = {item.spec.distribution for item in results}
        assert "pandas" in dists
        assert "python-dateutil" in dists
        assert "pyyaml" in dists
