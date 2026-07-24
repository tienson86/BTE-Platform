"""Infra self-tests for WP18 tools."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools._common import REPO_ROOT, read_version
from tools.build import check_required_paths
from tools.lint import check_deployment_config


def test_version_file_readable() -> None:
    version = read_version(REPO_ROOT)
    parts = version.split(".")
    assert len(parts) == 3
    assert all(part.isdigit() for part in parts)


def test_required_build_paths() -> None:
    assert check_required_paths(REPO_ROOT) == []


def test_deployment_config() -> None:
    assert check_deployment_config(REPO_ROOT) == []


def test_tools_modules_importable() -> None:
    import tools.build as build
    import tools.lint as lint
    import tools.package as package
    import tools.run_tests as run_tests

    assert callable(build.main)
    assert callable(lint.main)
    assert callable(package.main)
    assert callable(run_tests.main)
