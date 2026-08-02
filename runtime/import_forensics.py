"""Import Forensics V3 — persistent evidence for import_error incidents.

When a dependency fails to import even once, Runtime writes a forensic
bundle so the failure can be investigated later without reproduction.
"""

from __future__ import annotations

import json
import os
import platform
import sys
import traceback
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from importlib import import_module
from importlib import util as importlib_util
from importlib.metadata import PackageNotFoundError, distribution, metadata
from pathlib import Path
from typing import Any, Sequence

from runtime.dependency_policy import RUNTIME_VERSION_POLICY, normalize_distribution_name
from runtime.dependency_resolver import (
    DependencyStatus,
    PackageDiagnosis,
    distribution_init_path,
    find_shadow_candidates,
    probe_import,
)


RUNTIME_DIR = Path(__file__).resolve().parent
LOG_DIR = RUNTIME_DIR / "logs"

# Environment keys relevant to import resolution.
FORENSIC_ENV_KEYS: tuple[str, ...] = (
    "PYTHONPATH",
    "VIRTUAL_ENV",
    "PYTHONHOME",
    "PYTHONNOUSERSITE",
    "PYTHONSAFEPATH",
    "CONDA_PREFIX",
    "PATH",
)


@dataclass(slots=True)
class ImportForensicsRecord:
    """One import_error forensic capture."""

    package: str
    import_name: str
    timestamp_utc: str
    sys_executable: str
    python_version: str
    cwd: str
    sys_path: list[str]
    find_spec: dict[str, Any]
    distribution_metadata: dict[str, Any]
    module_file: str | None
    traceback: str | None
    platform: dict[str, str]
    environment: dict[str, str | None]
    dependency_chain: list[str]
    shadows: list[str] = field(default_factory=list)
    diagnosis_error: str | None = None
    suggested_command: str | None = None
    probe: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """JSON-serializable dictionary."""
        return asdict(self)


@dataclass(slots=True)
class ImportForensicsReport:
    """Bundle of all import_error forensics from one preflight run."""

    timestamp_utc: str
    count: int
    records: list[ImportForensicsRecord]

    def to_dict(self) -> dict[str, Any]:
        """JSON-serializable dictionary."""
        return {
            "timestamp_utc": self.timestamp_utc,
            "count": self.count,
            "records": [record.to_dict() for record in self.records],
        }


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _capture_environment() -> dict[str, str | None]:
    return {key: os.environ.get(key) for key in FORENSIC_ENV_KEYS}


def _capture_platform() -> dict[str, str]:
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
    }


def _find_spec_payload(import_name: str) -> dict[str, Any]:
    try:
        spec = importlib_util.find_spec(import_name)
    except Exception as exc:  # noqa: BLE001
        return {"error": f"{type(exc).__name__}: {exc}", "found": False}
    if spec is None:
        return {"found": False, "name": import_name}
    locations = list(spec.submodule_search_locations or [])
    return {
        "found": True,
        "name": spec.name,
        "origin": spec.origin,
        "loader": type(spec.loader).__name__ if spec.loader else None,
        "submodule_search_locations": locations,
    }


def _distribution_metadata_payload(distribution_name: str) -> dict[str, Any]:
    try:
        dist = distribution(distribution_name)
        meta = metadata(distribution_name)
    except PackageNotFoundError:
        return {"found": False, "name": distribution_name}
    except Exception as exc:  # noqa: BLE001
        return {
            "found": False,
            "name": distribution_name,
            "error": f"{type(exc).__name__}: {exc}",
        }

    requires: list[str] = []
    try:
        requires = [str(item) for item in (dist.requires or [])]
    except Exception:
        requires = []

    top_level: list[str] = []
    try:
        text = dist.read_text("top_level.txt")
        if text:
            top_level = [line.strip() for line in text.splitlines() if line.strip()]
    except Exception:
        top_level = []

    locate_init = distribution_init_path(distribution_name, top_level[0] if top_level else distribution_name.replace("-", "_"))

    return {
        "found": True,
        "name": dist.metadata["Name"] if "Name" in dist.metadata else distribution_name,
        "version": dist.version,
        "requires": requires,
        "top_level": top_level,
        "locate_init": str(locate_init) if locate_init else None,
        "summary": meta.get("Summary"),
        "home_page": meta.get("Home-page") or meta.get("Project-URL"),
    }


def build_dependency_chain(distribution_name: str, import_name: str) -> list[str]:
    """
    Build a readable dependency chain.

    Example: ``pandas → python-dateutil → dateutil``
    """
    target = normalize_distribution_name(distribution_name)
    consumers: list[str] = []
    for candidate in sorted(RUNTIME_VERSION_POLICY):
        if candidate == target:
            continue
        try:
            dist = distribution(candidate)
        except PackageNotFoundError:
            continue
        for req in dist.requires or []:
            req_name = str(req).split(";", 1)[0].strip()
            for sep in ("[", " ", "<", ">", "=", "!"):
                if sep in req_name:
                    req_name = req_name.split(sep, 1)[0]
            if normalize_distribution_name(req_name) == target:
                consumers.append(candidate)
                break

    chain: list[str] = []
    for item in consumers + [target, import_name]:
        if item and item not in chain:
            chain.append(item)
    return chain


def _attempt_import_with_traceback(import_name: str) -> tuple[str | None, str | None]:
    """Return ``(module_file, traceback_text)`` for a live import attempt."""
    try:
        module = import_module(import_name)
        return getattr(module, "__file__", None), None
    except Exception:
        return None, traceback.format_exc()


def capture_import_forensics(
    *,
    package: str,
    import_name: str,
    diagnosis: PackageDiagnosis | None = None,
) -> ImportForensicsRecord:
    """Capture a full forensic record for one failing import."""
    timestamp = _utc_now()
    probe = probe_import(import_name, distribution_name=package)
    module_file, tb = _attempt_import_with_traceback(import_name)
    if module_file is None and probe.get("module_file"):
        module_file = str(probe["module_file"])
    if tb is None and probe.get("error"):
        # Import may have been poisoned in-process; keep probe error + stack if any.
        tb = str(probe["error"])

    return ImportForensicsRecord(
        package=package,
        import_name=import_name,
        timestamp_utc=timestamp,
        sys_executable=sys.executable,
        python_version=platform.python_version(),
        cwd=str(Path.cwd().resolve()),
        sys_path=[str(item) for item in sys.path],
        find_spec=_find_spec_payload(import_name),
        distribution_metadata=_distribution_metadata_payload(package),
        module_file=module_file,
        traceback=tb,
        platform=_capture_platform(),
        environment=_capture_environment(),
        dependency_chain=build_dependency_chain(package, import_name),
        shadows=find_shadow_candidates(import_name),
        diagnosis_error=diagnosis.error if diagnosis else None,
        suggested_command=diagnosis.suggested_command if diagnosis else None,
        probe={k: v for k, v in probe.items() if k != "sys_path_head"},
    )


def collect_import_forensics(
    packages: Sequence[PackageDiagnosis],
) -> ImportForensicsReport | None:
    """Collect forensics for every ``import_error`` diagnosis."""
    failed = [item for item in packages if item.status is DependencyStatus.IMPORT_ERROR]
    if not failed:
        return None
    records = [
        capture_import_forensics(
            package=item.package,
            import_name=item.import_name,
            diagnosis=item,
        )
        for item in failed
    ]
    return ImportForensicsReport(
        timestamp_utc=_utc_now(),
        count=len(records),
        records=records,
    )


def format_import_forensics(report: ImportForensicsReport) -> str:
    """Human-readable import forensics text."""
    lines = [
        "BTE Runtime - Import Forensics V3",
        "=" * 48,
        f"Timestamp: {report.timestamp_utc}",
        f"Import errors: {report.count}",
        "",
    ]
    for index, record in enumerate(report.records, start=1):
        lines.extend(
            [
                f"--- Case {index}: {record.package} / import {record.import_name} ---",
                f"sys.executable: {record.sys_executable}",
                f"Python version: {record.python_version}",
                f"CWD: {record.cwd}",
                f"Platform: {record.platform.get('platform')}",
                f"Dependency chain: {' -> '.join(record.dependency_chain)}",
                f"module.__file__: {record.module_file or '-'}",
                f"Suggested: {record.suggested_command or '-'}",
                "",
                "[environment]",
            ]
        )
        for key, value in record.environment.items():
            lines.append(f"  {key}={value!r}")
        lines.append("")
        lines.append("[find_spec]")
        lines.append(json.dumps(record.find_spec, indent=2, ensure_ascii=False))
        lines.append("")
        lines.append("[distribution_metadata]")
        lines.append(
            json.dumps(record.distribution_metadata, indent=2, ensure_ascii=False)
        )
        lines.append("")
        lines.append("[sys.path]")
        for entry in record.sys_path:
            lines.append(f"  - {entry}")
        if record.shadows:
            lines.append("")
            lines.append("[shadow_candidates]")
            for shadow in record.shadows:
                lines.append(f"  - {shadow}")
        lines.append("")
        lines.append("[traceback]")
        lines.append(record.traceback or "(no traceback captured)")
        lines.append("")
    return "\n".join(lines)


def write_import_forensics(
    report: ImportForensicsReport,
    *,
    log_dir: Path | None = None,
) -> tuple[Path, Path]:
    """Persist import forensics JSON + text (latest + stamped archive)."""
    target = log_dir or LOG_DIR
    target.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = target / f"import_forensics_{stamp}.json"
    text_path = target / f"import_forensics_{stamp}.txt"
    latest_json = target / "import_forensics_latest.json"
    latest_text = target / "import_forensics_latest.txt"

    payload = json.dumps(report.to_dict(), indent=2, ensure_ascii=False)
    text = format_import_forensics(report)
    json_path.write_text(payload, encoding="utf-8")
    text_path.write_text(text, encoding="utf-8")
    latest_json.write_text(payload, encoding="utf-8")
    latest_text.write_text(text, encoding="utf-8")
    return latest_json, latest_text


def write_import_forensics_from_diagnoses(
    packages: Sequence[PackageDiagnosis],
    *,
    log_dir: Path | None = None,
) -> tuple[Path, Path] | None:
    """
    If any diagnosis is ``import_error``, write forensics and return paths.

    Returns ``None`` when there is nothing to capture.
    """
    report = collect_import_forensics(packages)
    if report is None:
        return None
    return write_import_forensics(report, log_dir=log_dir)
