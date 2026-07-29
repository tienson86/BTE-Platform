"""Shared helpers for engineering tools (WP18)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def read_version(root: Path | None = None) -> str:
    """Read semantic version from VERSION file."""
    path = (root or REPO_ROOT) / "VERSION"
    if not path.is_file():
        return "0.0.0"
    return path.read_text(encoding="utf-8").strip()


def run_command(
    args: list[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
) -> int:
    """Run a subprocess and stream output."""
    print("+", " ".join(args), flush=True)
    completed = subprocess.run(  # noqa: S603
        args,
        cwd=str(cwd or REPO_ROOT),
        check=False,
    )
    if check and completed.returncode != 0:
        raise SystemExit(completed.returncode)
    return completed.returncode


def python_executable() -> str:
    """Return current interpreter path."""
    return sys.executable
