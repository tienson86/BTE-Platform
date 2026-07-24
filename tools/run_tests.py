"""Run project test suites."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools._common import REPO_ROOT, python_executable, run_command

SUITES: dict[str, list[str]] = {
    "applications": [
        "applications/api/tests",
        "applications/tests",
        "applications/storage/tests",
        "applications/web_admin/tests",
        "applications/customer_portal/tests",
    ],
    "infra": [
        "tools",
    ],
    "all": [
        "applications/api/tests",
        "applications/tests",
        "applications/storage/tests",
        "applications/web_admin/tests",
        "applications/customer_portal/tests",
    ],
}


def existing_targets(root: Path, suite: str) -> list[str]:
    """Filter suite paths that exist on disk."""
    targets: list[str] = []
    for rel in SUITES.get(suite, SUITES["applications"]):
        path = root / rel
        if path.exists():
            targets.append(str(path))
    return targets


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Run BTE tests")
    parser.add_argument(
        "--suite",
        choices=sorted(SUITES.keys()) + ["ci"],
        default="applications",
        help="Test suite selector",
    )
    parser.add_argument("--ci", action="store_true", help="Alias for --suite ci")
    parser.add_argument("-q", action="store_true", help="pytest quiet mode")
    args = parser.parse_args(argv)

    suite = "ci" if args.ci else args.suite
    if suite == "ci":
        # CI: applications + lightweight infra/tool checks
        targets = existing_targets(REPO_ROOT, "applications")
        # run tools self-tests via pytest collect if any test_*.py under tools
        tool_tests = list((REPO_ROOT / "tools").glob("test_*.py"))
        targets.extend(str(p) for p in tool_tests)
    else:
        targets = existing_targets(REPO_ROOT, suite)

    if not targets:
        print("No test targets found.")
        return 1

    cmd = [python_executable(), "-m", "pytest", *targets]
    if args.q or suite == "ci":
        cmd.append("-q")
    return run_command(cmd, check=False)


if __name__ == "__main__":
    raise SystemExit(main())
