"""Package a release zip (wrapper around package.py)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools._common import REPO_ROOT, read_version
from tools.package import build_zip


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for package_release."""
    parser = argparse.ArgumentParser(description="Package BTE release zip")
    parser.add_argument("--version", default=None)
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "dist")
    args = parser.parse_args(argv)

    version = (args.version or read_version(REPO_ROOT)).lstrip("v")
    archive = build_zip(REPO_ROOT, args.out.resolve(), version)
    # Stable name for CI release upload
    stable = args.out.resolve() / f"bte-platform-{version}.zip"
    if stable.exists():
        stable.unlink()
    stable.write_bytes(archive.read_bytes())
    print(f"Stable release artifact: {stable}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
