"""Build / sanity-check the repository for packaging."""

from __future__ import annotations

import argparse
import compileall
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools._common import REPO_ROOT, read_version


REQUIRED_PATHS = (
    "applications/api/app.py",
    "applications/web_admin/app.py",
    "applications/customer_portal/app.py",
    "deployment/docker/docker-compose.yml",
    "deployment/env/.env.example",
    "VERSION",
)


def check_required_paths(root: Path) -> list[str]:
    """Return missing required relative paths."""
    missing: list[str] = []
    for rel in REQUIRED_PATHS:
        if not (root / rel).exists():
            missing.append(rel)
    return missing


def compile_python(root: Path) -> bool:
    """Byte-compile selected packages (no install)."""
    targets = [
        root / "applications",
        root / "tools",
        root / "engines",
    ]
    ok = True
    for target in targets:
        if not target.exists():
            continue
        print(f"compileall {target.relative_to(root)}")
        if not compileall.compile_dir(str(target), quiet=1):
            ok = False
    return ok


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="BTE build / sanity checks")
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    args = parser.parse_args(argv)

    root = args.root.resolve()
    version = read_version(root)
    print(f"BTE version: {version}")

    missing = check_required_paths(root)
    if missing:
        print("Missing required paths:")
        for item in missing:
            print(f"  - {item}")
        return 1

    if not compile_python(root):
        print("compileall failed")
        return 1

    print("Build checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
