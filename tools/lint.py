"""Lint / format / import / deployment-config checks."""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools._common import REPO_ROOT, python_executable, run_command

LINT_TARGETS = (
    "applications/api",
    "applications/web_admin",
    "applications/customer_portal",
    "applications/storage",
    "applications/admin",
    "applications/license",
    "tools",
)

DEPLOYMENT_REQUIRED = (
    "deployment/docker/docker-compose.yml",
    "deployment/docker/Dockerfile.api",
    "deployment/docker/Dockerfile.web_admin",
    "deployment/docker/Dockerfile.customer_portal",
    "deployment/env/.env.example",
    "deployment/windows/start_all.bat",
    "deployment/linux/start_all.sh",
    "configs/services.json",
)


def check_deployment_config(root: Path) -> list[str]:
    """Validate deployment files exist and compose YAML parses."""
    errors: list[str] = []
    for rel in DEPLOYMENT_REQUIRED:
        if not (root / rel).is_file():
            errors.append(f"missing {rel}")

    compose = root / "deployment/docker/docker-compose.yml"
    if compose.is_file():
        try:
            import yaml  # type: ignore

            data = yaml.safe_load(compose.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or "services" not in data:
                errors.append("docker-compose.yml missing services")
            else:
                for name in ("api", "web_admin", "customer_portal"):
                    if name not in data["services"]:
                        errors.append(f"compose missing service: {name}")
        except Exception as exc:  # noqa: BLE001 - surface parse errors
            errors.append(f"compose parse error: {exc}")
    return errors


def check_python_syntax(paths: list[Path]) -> list[str]:
    """Parse Python files with ast."""
    errors: list[str] = []
    for path in paths:
        try:
            source = path.read_text(encoding="utf-8")
            ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            errors.append(f"syntax {path}: {exc}")
    return errors


def iter_python_files(root: Path, rel_targets: tuple[str, ...]) -> list[Path]:
    """Collect .py files under targets."""
    files: list[Path] = []
    for rel in rel_targets:
        base = root / rel
        if base.is_file() and base.suffix == ".py":
            files.append(base)
            continue
        if base.is_dir():
            files.extend(sorted(base.rglob("*.py")))
    return files


def maybe_run_ruff(root: Path) -> int:
    """Run ruff check on engineering tools if installed; otherwise skip."""
    code = run_command(
        [python_executable(), "-m", "ruff", "--version"],
        check=False,
    )
    if code != 0:
        print("ruff not installed — skipping ruff (syntax/deployment still checked)")
        return 0
    # Keep ruff scoped to tools/ so CI does not rewrite application code.
    targets = [str(root / "tools")]
    return run_command(
        [python_executable(), "-m", "ruff", "check", *targets],
        check=False,
    )


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="BTE lint / quality checks")
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument("--skip-ruff", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()

    errors = check_deployment_config(root)
    py_files = iter_python_files(root, LINT_TARGETS)
    errors.extend(check_python_syntax(py_files))

    if errors:
        print("Lint errors:")
        for err in errors:
            print(f"  - {err}")
        return 1

    if not args.skip_ruff:
        code = maybe_run_ruff(root)
        if code != 0:
            return code

    print(f"Lint OK ({len(py_files)} Python files checked).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
