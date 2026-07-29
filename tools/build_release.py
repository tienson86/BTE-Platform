"""Release build orchestration: lint + tests + build checks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools._common import REPO_ROOT, python_executable, read_version, run_command


def write_version(root: Path, version: str) -> None:
    """Update VERSION file for the release build."""
    (root / "VERSION").write_text(version.strip() + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for build_release."""
    parser = argparse.ArgumentParser(description="Build a BTE release")
    parser.add_argument("--version", required=False, default=None)
    parser.add_argument("--skip-tests", action="store_true")
    args = parser.parse_args(argv)

    root = REPO_ROOT
    version = (args.version or read_version(root)).lstrip("v")
    write_version(root, version)
    print(f"Building release {version}")

    py = python_executable()
    run_command([py, "tools/lint.py"])
    run_command([py, "tools/build.py"])
    if not args.skip_tests:
        code = run_command([py, "tools/run_tests.py", "--ci"], check=False)
        if code != 0:
            return code
    print("build_release completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
