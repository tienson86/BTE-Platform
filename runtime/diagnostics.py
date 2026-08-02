"""Runtime environment, dependency, and startup diagnostic reports."""

from __future__ import annotations

import json
import platform
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from runtime.dependency_policy import PolicyRequirement
from runtime.dependency_resolver import (
    DependencyResolver,
    DependencyStatus,
    PackageDiagnosis,
)
from runtime.import_forensics import write_import_forensics_from_diagnoses


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = Path(__file__).resolve().parent
LOG_DIR = RUNTIME_DIR / "logs"


@dataclass(slots=True)
class EnvironmentReport:
    """Interpreter and host environment snapshot."""

    python_version: str
    python_version_info: tuple[int, int, int]
    executable: str
    platform: str
    platform_release: str
    machine: str
    cwd: str
    project_root: str
    timestamp_utc: str
    implementation: str = field(default_factory=lambda: platform.python_implementation())

    @property
    def python_ok(self) -> bool:
        """Runtime requires Python >= 3.10."""
        major, minor, _ = self.python_version_info
        return (major, minor) >= (3, 10)


@dataclass(slots=True)
class DependencyReport:
    """Aggregated dependency diagnosis."""

    packages: list[PackageDiagnosis]
    ok: bool
    summary: str
    counts: dict[str, int]

    @property
    def failed(self) -> list[PackageDiagnosis]:
        """Packages that are not OK."""
        return [p for p in self.packages if not p.ok]


@dataclass(slots=True)
class StartupDiagnostics:
    """Full startup preflight diagnostics payload."""

    environment: EnvironmentReport
    dependencies: DependencyReport
    ready: bool
    timestamp_utc: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """JSON-serializable dictionary."""
        return {
            "timestamp_utc": self.timestamp_utc,
            "ready": self.ready,
            "notes": list(self.notes),
            "environment": asdict(self.environment),
            "dependencies": {
                "ok": self.dependencies.ok,
                "summary": self.dependencies.summary,
                "counts": self.dependencies.counts,
                "packages": [
                    {
                        "package": p.package,
                        "import_name": p.import_name,
                        "installed": p.installed,
                        "required": p.required,
                        "status": p.status.value,
                        "suggested_command": p.suggested_command,
                        "error": p.error,
                        "distribution_found": p.distribution_found,
                        "importable": p.importable,
                        "resolve_source": p.resolve_source,
                    }
                    for p in self.dependencies.packages
                ],
            },
        }


def build_environment_report(
    *,
    project_root: Path | None = None,
    cwd: Path | None = None,
) -> EnvironmentReport:
    """Capture the current Python environment."""
    info = sys.version_info
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return EnvironmentReport(
        python_version=platform.python_version(),
        python_version_info=(info.major, info.minor, info.micro),
        executable=sys.executable,
        platform=platform.system(),
        platform_release=platform.release(),
        machine=platform.machine(),
        cwd=str((cwd or Path.cwd()).resolve()),
        project_root=str((project_root or ROOT).resolve()),
        timestamp_utc=now,
    )


def build_dependency_report(
    *,
    resolver: DependencyResolver | None = None,
    requirements: Sequence[PolicyRequirement] | None = None,
    names: Sequence[str] | None = None,
) -> DependencyReport:
    """Run Resolver V2 and aggregate a dependency report."""
    engine = resolver or DependencyResolver()
    packages = engine.diagnose_all(requirements=requirements, names=names)
    counts = {
        "total": len(packages),
        "ok": sum(1 for p in packages if p.status is DependencyStatus.OK),
        "not_installed": sum(
            1 for p in packages if p.status is DependencyStatus.NOT_INSTALLED
        ),
        "import_error": sum(
            1 for p in packages if p.status is DependencyStatus.IMPORT_ERROR
        ),
        "version_conflict": sum(
            1 for p in packages if p.status is DependencyStatus.VERSION_CONFLICT
        ),
    }
    ok = counts["ok"] == counts["total"]
    if ok:
        summary = f"All {counts['total']} required packages satisfy policy."
    else:
        summary = (
            f"{counts['total'] - counts['ok']} issue(s): "
            f"not_installed={counts['not_installed']}, "
            f"import_error={counts['import_error']}, "
            f"version_conflict={counts['version_conflict']}"
        )
    return DependencyReport(
        packages=packages,
        ok=ok,
        summary=summary,
        counts=counts,
    )


def build_startup_diagnostics(
    *,
    resolver: DependencyResolver | None = None,
    names: Sequence[str] | None = None,
) -> StartupDiagnostics:
    """Build combined environment + dependency startup diagnostics."""
    env = build_environment_report()
    deps = build_dependency_report(resolver=resolver, names=names)
    notes: list[str] = []
    if not env.python_ok:
        notes.append("Python < 3.10 is unsupported.")
    if not deps.ok:
        notes.append(deps.summary)
    ready = env.python_ok and deps.ok
    return StartupDiagnostics(
        environment=env,
        dependencies=deps,
        ready=ready,
        timestamp_utc=env.timestamp_utc,
        notes=notes,
    )


def format_dependency_table(report: DependencyReport) -> str:
    """Human-readable dependency failure / status table."""
    lines = [
        f"{'Package':<22} {'Installed':<12} {'Required':<14} {'Status':<18} Suggested command",
        "-" * 100,
    ]
    for item in report.packages:
        lines.append(
            f"{item.package:<22} {str(item.installed or '-'):<12} "
            f"{item.required:<14} {item.status.value:<18} {item.suggested_command}"
        )
        if item.error:
            lines.append(f"  detail: {item.error}")
    return "\n".join(lines)


def format_environment_report(report: EnvironmentReport) -> str:
    """Human-readable environment report."""
    return "\n".join(
        [
            f"Python:      {report.python_version} ({report.implementation})",
            f"Executable:  {report.executable}",
            f"Platform:    {report.platform} {report.platform_release} ({report.machine})",
            f"CWD:         {report.cwd}",
            f"Project:     {report.project_root}",
            f"Timestamp:   {report.timestamp_utc}",
        ]
    )


def format_startup_diagnostics(diag: StartupDiagnostics) -> str:
    """Human-readable startup diagnostics block."""
    parts = [
        "BTE Runtime - Startup Diagnostics",
        "=" * 40,
        "[Environment]",
        format_environment_report(diag.environment),
        "",
        "[Dependencies]",
        diag.dependencies.summary,
        format_dependency_table(diag.dependencies),
        "",
        f"Ready: {diag.ready}",
    ]
    if diag.notes:
        parts.append("Notes:")
        parts.extend(f"  - {note}" for note in diag.notes)
    return "\n".join(parts)


def write_diagnostics_files(
    diag: StartupDiagnostics,
    *,
    log_dir: Path | None = None,
) -> tuple[Path, Path]:
    """Persist JSON + text diagnostics under runtime/logs."""
    target = log_dir or LOG_DIR
    target.mkdir(parents=True, exist_ok=True)

    # Import Forensics V3 — durable evidence for even a single import_error.
    forensics_paths = write_import_forensics_from_diagnoses(
        diag.dependencies.packages,
        log_dir=target,
    )
    if forensics_paths is not None:
        diag.notes.append(
            "Import forensics written: "
            f"{forensics_paths[0].name} / {forensics_paths[1].name}"
        )

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = target / f"startup_diagnostics_{stamp}.json"
    text_path = target / f"startup_diagnostics_{stamp}.txt"
    latest_json = target / "startup_diagnostics_latest.json"
    latest_text = target / "startup_diagnostics_latest.txt"

    payload = json.dumps(diag.to_dict(), indent=2, ensure_ascii=False)
    text = format_startup_diagnostics(diag)
    json_path.write_text(payload, encoding="utf-8")
    text_path.write_text(text, encoding="utf-8")
    latest_json.write_text(payload, encoding="utf-8")
    latest_text.write_text(text, encoding="utf-8")
    return json_path, text_path
