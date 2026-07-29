"""Create a distributable zip package of the repository."""

from __future__ import annotations

import argparse
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools._common import REPO_ROOT, read_version

EXCLUDE_DIR_NAMES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "node_modules",
    ".cursor",
}

EXCLUDE_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".log",
}


def should_exclude(path: Path, root: Path) -> bool:
    """Return True if path should be omitted from the package."""
    try:
        rel = path.relative_to(root)
    except ValueError:
        return True
    parts = set(rel.parts)
    if parts & EXCLUDE_DIR_NAMES:
        return True
    if path.suffix in EXCLUDE_SUFFIXES:
        return True
    # skip large local data dumps optionally
    if rel.as_posix().startswith("logs/") and path.is_file():
        return path.name != "README.md"
    return False


def build_zip(root: Path, out_dir: Path, version: str) -> Path:
    """Write zip artifact and return its path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    archive = out_dir / f"bte-platform-{version}-{stamp}.zip"

    count = 0
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if should_exclude(path, root):
                continue
            arcname = path.relative_to(root).as_posix()
            zf.write(path, arcname)
            count += 1
        # embed version marker
        zf.writestr(
            "PACKAGE_INFO.txt",
            f"BTE Platform\nversion={version}\nfiles={count}\n",
        )
    print(f"Wrote {archive} ({count} files)")
    return archive


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Package BTE as zip")
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "dist")
    parser.add_argument("--version", default=None)
    args = parser.parse_args(argv)

    root = args.root.resolve()
    version = args.version or read_version(root)
    build_zip(root, args.out.resolve(), version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
