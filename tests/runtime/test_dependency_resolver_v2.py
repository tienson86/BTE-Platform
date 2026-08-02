"""Full tests for Runtime Dependency Resolver V2."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from runtime.dependency_policy import (
    RUNTIME_VERSION_POLICY,
    PolicyRequirement,
    default_policy_requirements,
    normalize_distribution_name,
    parse_requirement_line,
    policy_by_name,
)
from runtime.dependency_resolver import (
    DependencyResolver,
    DependencyStatus,
    check_required_packages,
    resolve_package_spec,
    version_satisfies,
)
from runtime.diagnostics import (
    build_dependency_report,
    build_environment_report,
    build_startup_diagnostics,
    format_dependency_table,
    write_diagnostics_files,
)
from runtime.manager import check_requirements


class TestVersionPolicy:
    """Version policy loading and parsing."""

    def test_runtime_policy_covers_core_stack(self) -> None:
        for name in (
            "pandas",
            "python-dateutil",
            "fastapi",
            "uvicorn",
            "pyyaml",
        ):
            assert name in RUNTIME_VERSION_POLICY

    def test_parse_requirement_line(self) -> None:
        req = parse_requirement_line("pandas>=2.3.1")
        assert req is not None
        assert req.distribution == "pandas"
        assert req.specifier == ">=2.3.1"

    def test_parse_extras(self) -> None:
        req = parse_requirement_line("uvicorn[standard]>=0.30.0")
        assert req is not None
        assert req.distribution == "uvicorn"
        assert req.extras == ("standard",)
        assert "standard" in req.pip_token

    def test_default_policy_requirements_merged(self) -> None:
        reqs = default_policy_requirements()
        by_name = {r.distribution: r for r in reqs}
        assert "pandas" in by_name
        assert by_name["pandas"].specifier.startswith(">=")
        assert "python-dateutil" in by_name

    def test_normalize_distribution_name(self) -> None:
        assert normalize_distribution_name("PyYAML") == "pyyaml"
        assert normalize_distribution_name("python_dateutil") == "python-dateutil"


class TestVersionSatisfies:
    """PEP 440 version comparison."""

    def test_satisfies_greater_equal(self) -> None:
        assert version_satisfies("3.0.5", ">=2.3.1") is True
        assert version_satisfies("2.0.0", ">=2.3.1") is False

    def test_empty_specifier_always_ok(self) -> None:
        assert version_satisfies("1.0", "") is True


class TestResolverNames:
    """Dynamic name resolution (hints + metadata, not static-only)."""

    def test_resolve_dateutil_alias(self) -> None:
        resolver = DependencyResolver()
        names = resolver.resolve_names("dateutil")
        assert names.distribution == "python-dateutil"
        assert names.import_name == "dateutil"

    def test_resolve_python_dateutil_distribution(self) -> None:
        resolver = DependencyResolver()
        names = resolver.resolve_names("python-dateutil")
        assert names.distribution == "python-dateutil"
        assert names.import_name == "dateutil"

    def test_resolve_pyyaml(self) -> None:
        resolver = DependencyResolver()
        assert resolver.resolve_names("yaml").distribution == "pyyaml"
        assert resolver.resolve_names("PyYAML").import_name == "yaml"

    def test_resolve_identity_pandas(self) -> None:
        resolver = DependencyResolver()
        names = resolver.resolve_names("pandas")
        assert names.distribution == "pandas"
        assert names.import_name == "pandas"

    def test_compat_resolve_package_spec(self) -> None:
        spec = resolve_package_spec("dateutil")
        assert spec.distribution == "python-dateutil"
        assert spec.import_name == "dateutil"


class TestResolverDiagnosis:
    """Classification: Not Installed / Import Error / Version Conflict."""

    def test_pandas_and_dateutil_ok_when_installed(self) -> None:
        resolver = DependencyResolver()
        results = resolver.diagnose_all(
            names=["pandas", "python-dateutil", "dateutil", "yaml"]
        )
        assert all(item.ok for item in results), results
        assert all(item.status is DependencyStatus.OK for item in results)

    def test_not_installed_status(self) -> None:
        resolver = DependencyResolver()
        req = PolicyRequirement(distribution="no-such-bte-pkg-xyz", specifier=">=1.0")
        with patch.object(resolver, "get_installed_version", return_value=None):
            result = resolver.diagnose(req)
        assert result.status is DependencyStatus.NOT_INSTALLED
        assert result.installed is None
        assert result.package == "no-such-bte-pkg-xyz"
        assert "pip install" in result.suggested_command
        assert result.required == ">=1.0"

    def test_import_error_status(self) -> None:
        resolver = DependencyResolver()
        req = PolicyRequirement(distribution="pandas", specifier=">=2.3.1")

        def _boom(_name: str) -> None:
            raise ImportError("DLL load failed")

        with (
            patch.object(resolver, "get_installed_version", return_value="2.5.0"),
            patch("runtime.dependency_resolver.import_module", side_effect=_boom),
        ):
            result = resolver.diagnose(req)
        assert result.status is DependencyStatus.IMPORT_ERROR
        assert result.installed == "2.5.0"
        assert result.importable is False
        assert "ImportError" in (result.error or "")

    def test_version_conflict_status(self) -> None:
        resolver = DependencyResolver()
        req = PolicyRequirement(distribution="pandas", specifier=">=99.0")

        with (
            patch.object(resolver, "get_installed_version", return_value="2.5.0"),
            patch("runtime.dependency_resolver.import_module", return_value=object()),
        ):
            result = resolver.diagnose(req)
        assert result.status is DependencyStatus.VERSION_CONFLICT
        assert result.installed == "2.5.0"
        assert result.required == ">=99.0"
        assert result.importable is True
        assert "pip install" in result.suggested_command

    def test_failure_table_fields(self) -> None:
        ok, message, results = check_required_packages(names=["pandas"])
        # May be ok; force a failure message shape via diagnose mock path
        resolver = DependencyResolver()
        req = PolicyRequirement(distribution="missing-pkg", specifier=">=1")
        with patch.object(resolver, "get_installed_version", return_value=None):
            diagnosis = resolver.diagnose(req)
        assert diagnosis.package == "missing-pkg"
        assert diagnosis.installed is None
        assert diagnosis.required == ">=1"
        assert "python -m pip install" in diagnosis.suggested_command


class TestReports:
    """Environment / Dependency / Startup diagnostic reports."""

    def test_environment_report(self) -> None:
        report = build_environment_report()
        assert report.executable
        assert report.python_version
        assert report.project_root
        assert report.python_ok is True

    def test_dependency_report_counts(self) -> None:
        report = build_dependency_report(names=["pandas", "python-dateutil"])
        assert report.ok is True
        assert report.counts["total"] == 2
        assert report.counts["ok"] == 2
        table = format_dependency_table(report)
        assert "pandas" in table
        assert "python-dateutil" in table
        assert "Suggested command" in table or "pip install" in table

    def test_startup_diagnostics_ready_for_subset(self) -> None:
        diag = build_startup_diagnostics(names=["pandas", "dateutil", "yaml"])
        assert diag.environment.python_ok is True
        assert diag.dependencies.ok is True
        assert diag.ready is True
        payload = diag.to_dict()
        assert "environment" in payload
        assert "dependencies" in payload
        assert payload["ready"] is True

    def test_write_diagnostics_files(self, tmp_path: Path) -> None:
        diag = build_startup_diagnostics(names=["pandas"])
        json_path, text_path = write_diagnostics_files(diag, log_dir=tmp_path)
        assert json_path.is_file()
        assert text_path.is_file()
        assert (tmp_path / "startup_diagnostics_latest.json").is_file()
        assert "Startup Diagnostics" in text_path.read_text(encoding="utf-8")


class TestManagerIntegration:
    """manager.check_requirements uses Resolver V2 reports."""

    def test_check_requirements_does_not_false_flag_installed(self) -> None:
        result = check_requirements()
        if result.ok:
            assert "satisfy" in result.message.lower() or "OK" in result.message
            return
        # Failure must be tabular and must not claim pandas/dateutil missing
        # when they are installed.
        assert "Package" in result.message
        assert "Installed" in result.message
        assert "Required" in result.message
        lower = result.message.lower()
        # If pandas appears it should not be status not_installed
        if "pandas" in lower:
            assert "pandas" in result.message
            # installed pandas line should not say not_installed for pandas itself
            for line in result.message.splitlines():
                if line.strip().startswith("pandas"):
                    assert "not_installed" not in line

    def test_policy_by_name_filter(self) -> None:
        rows = policy_by_name(["pandas", "uvicorn"])
        assert [r.distribution for r in rows] == ["pandas", "uvicorn"]
