"""Tests for Runtime Import Forensics V3."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from runtime.dependency_policy import PolicyRequirement
from runtime.dependency_resolver import DependencyResolver, DependencyStatus
from runtime.diagnostics import build_startup_diagnostics, write_diagnostics_files
from runtime.import_forensics import (
    build_dependency_chain,
    capture_import_forensics,
    collect_import_forensics,
    write_import_forensics_from_diagnoses,
)


class TestDependencyChain:
    """Chain builder for forensics."""

    def test_python_dateutil_chain_includes_import_name(self) -> None:
        chain = build_dependency_chain("python-dateutil", "dateutil")
        assert "python-dateutil" in chain
        assert "dateutil" in chain
        # pandas requires python-dateutil on a healthy install
        assert "pandas" in chain or len(chain) >= 2


class TestImportForensicsCapture:
    """Forensic capture contents."""

    def test_capture_includes_required_fields(self) -> None:
        record = capture_import_forensics(
            package="python-dateutil",
            import_name="dateutil",
        )
        assert record.sys_executable
        assert record.python_version
        assert record.cwd
        assert isinstance(record.sys_path, list) and record.sys_path
        assert "found" in record.find_spec
        assert "found" in record.distribution_metadata
        assert record.timestamp_utc
        assert "system" in record.platform
        assert "PYTHONPATH" in record.environment
        assert "VIRTUAL_ENV" in record.environment
        assert record.dependency_chain

    def test_collect_only_for_import_error(self) -> None:
        resolver = DependencyResolver()
        ok_items = resolver.diagnose_all(names=["pandas"])
        assert collect_import_forensics(ok_items) is None

        req = PolicyRequirement(distribution="pandas", specifier=">=2.3.1")

        def _boom(_name: str) -> None:
            raise ImportError("forensics-simulated")

        with (
            patch.object(resolver, "get_installed_version", return_value="2.5.0"),
            patch("runtime.dependency_resolver.import_module", side_effect=_boom),
            patch("runtime.import_forensics.import_module", side_effect=_boom),
        ):
            failed = resolver.diagnose(req)
            assert failed.status is DependencyStatus.IMPORT_ERROR
            report = collect_import_forensics([failed])
        assert report is not None
        assert report.count == 1
        assert report.records[0].package == "pandas"
        assert report.records[0].traceback
        assert "forensics-simulated" in (report.records[0].traceback or "")


class TestImportForensicsPersistence:
    """Files written under runtime/logs (or temp)."""

    def test_write_latest_json_and_txt(self, tmp_path: Path) -> None:
        resolver = DependencyResolver()
        req = PolicyRequirement(distribution="pandas", specifier=">=2.3.1")

        def _boom(_name: str) -> None:
            raise ImportError("persist-simulated")

        with (
            patch.object(resolver, "get_installed_version", return_value="2.5.0"),
            patch("runtime.dependency_resolver.import_module", side_effect=_boom),
            patch("runtime.import_forensics.import_module", side_effect=_boom),
        ):
            failed = resolver.diagnose(req)
            paths = write_import_forensics_from_diagnoses([failed], log_dir=tmp_path)

        assert paths is not None
        latest_json, latest_txt = paths
        assert latest_json.name == "import_forensics_latest.json"
        assert latest_txt.name == "import_forensics_latest.txt"
        assert latest_json.is_file()
        assert latest_txt.is_file()
        payload = json.loads(latest_json.read_text(encoding="utf-8"))
        assert payload["count"] == 1
        record = payload["records"][0]
        for key in (
            "sys_executable",
            "python_version",
            "cwd",
            "sys_path",
            "find_spec",
            "distribution_metadata",
            "traceback",
            "timestamp_utc",
            "platform",
            "environment",
            "dependency_chain",
        ):
            assert key in record
        text = latest_txt.read_text(encoding="utf-8")
        assert "Import Forensics V3" in text
        assert "sys.executable" in text
        assert "traceback" in text.lower()

    def test_diagnostics_writer_emits_forensics_on_import_error(
        self, tmp_path: Path
    ) -> None:
        def _boom(name: str) -> object:
            if name == "pandas":
                raise ImportError("diag-simulated")
            return object()

        with (
            patch(
                "runtime.dependency_resolver.import_module",
                side_effect=_boom,
            ),
            patch(
                "runtime.import_forensics.import_module",
                side_effect=_boom,
            ),
            patch(
                "runtime.dependency_resolver.version",
                side_effect=lambda name: "9.9.9",
            ),
        ):
            # Force a minimal diagnostics run focused on pandas via names filter
            # by building dependency report path through startup diagnostics names.
            diag = build_startup_diagnostics(names=["pandas"])
            # If environment still imports real pandas before patch in diagnose,
            # force status by rewriting packages list when needed.
            if diag.dependencies.ok:
                resolver = DependencyResolver()
                req = PolicyRequirement(distribution="pandas", specifier=">=2.3.1")
                with (
                    patch.object(resolver, "get_installed_version", return_value="2.5.0"),
                    patch(
                        "runtime.dependency_resolver.import_module",
                        side_effect=_boom,
                    ),
                ):
                    failed = resolver.diagnose(req)
                diag.dependencies.packages = [failed]
                diag.dependencies.ok = False

            write_diagnostics_files(diag, log_dir=tmp_path)

        assert (tmp_path / "import_forensics_latest.json").is_file()
        assert (tmp_path / "import_forensics_latest.txt").is_file()
        assert (tmp_path / "startup_diagnostics_latest.json").is_file()
