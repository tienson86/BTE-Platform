"""Baseline diff engine entrypoints."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from baseline.constants import DEFAULT_BUILD_TIMESTAMP
from baseline.diff.engine.baseline_compare import (
    compare_compiler_snapshots,
    compare_dependency_snapshots,
    compare_ontology_snapshots,
    compare_registry_snapshots,
    compare_validation_snapshots,
)
from baseline.diff.engine.report_generator import (
    generate_diff_html,
    generate_diff_json,
    generate_diff_markdown,
)
from baseline.diff.engine.snapshot_loader import SnapshotLoader
from baseline.io_utils import write_text
from baseline.paths import resolve_project_root

logger = logging.getLogger(__name__)


class BaselineDiffEngine:
    """Compare two baseline versions and emit multi-format reports."""

    def __init__(self, project_root: Path | None = None) -> None:
        """Initialize diff engine."""
        self.project_root = resolve_project_root(project_root)

    def list_versions(self) -> list[str]:
        """List available baseline version directory names (e.g. v1.0.0)."""
        baseline_root = self.project_root / "knowledge" / "baseline"
        if not baseline_root.is_dir():
            return []
        return sorted(
            path.name
            for path in baseline_root.iterdir()
            if path.is_dir()
            and path.name.startswith("v")
            and (path / "baseline_manifest.json").is_file()
        )

    def resolve_version_dir(self, version_or_path: str) -> Path:
        """Resolve `1.0.0`, `v1.0.0`, or an absolute/relative directory."""
        raw = Path(version_or_path)
        if raw.is_dir():
            return raw.resolve()
        text = version_or_path.strip()
        if not text.startswith("v"):
            text = f"v{text}"
        candidate = self.project_root / "knowledge" / "baseline" / text
        if candidate.is_dir():
            return candidate.resolve()
        raise FileNotFoundError(
            f"Baseline version directory not found: {version_or_path}"
        )

    def compare(
        self,
        old: str,
        new: str,
        output_dir: Path | None = None,
    ) -> dict[str, Any]:
        """Compare two baselines and optionally write reports."""
        old_dir = self.resolve_version_dir(old)
        new_dir = self.resolve_version_dir(new)
        old_loader = SnapshotLoader(old_dir)
        new_loader = SnapshotLoader(new_dir)
        old_snaps = old_loader.load_all()
        new_snaps = new_loader.load_all()

        domains: dict[str, Any] = {}
        if (
            "registry_snapshot.json" in old_snaps
            and "registry_snapshot.json" in new_snaps
        ):
            domains["registry"] = compare_registry_snapshots(
                old_snaps["registry_snapshot.json"],
                new_snaps["registry_snapshot.json"],
            )
        if (
            "ontology_snapshot.json" in old_snaps
            and "ontology_snapshot.json" in new_snaps
        ):
            domains["ontology"] = compare_ontology_snapshots(
                old_snaps["ontology_snapshot.json"],
                new_snaps["ontology_snapshot.json"],
            )
        if (
            "dependency_snapshot.json" in old_snaps
            and "dependency_snapshot.json" in new_snaps
        ):
            domains["dependency"] = compare_dependency_snapshots(
                old_snaps["dependency_snapshot.json"],
                new_snaps["dependency_snapshot.json"],
            )
        if (
            "compiler_snapshot.json" in old_snaps
            and "compiler_snapshot.json" in new_snaps
        ):
            domains["compiler"] = compare_compiler_snapshots(
                old_snaps["compiler_snapshot.json"],
                new_snaps["compiler_snapshot.json"],
            )
        if (
            "validation_snapshot.json" in old_snaps
            and "validation_snapshot.json" in new_snaps
        ):
            domains["validation"] = compare_validation_snapshots(
                old_snaps["validation_snapshot.json"],
                new_snaps["validation_snapshot.json"],
            )
        if "statistics.json" in old_snaps and "statistics.json" in new_snaps:
            domains["statistics"] = {
                "changed": old_snaps["statistics.json"] != new_snaps["statistics.json"],
                "old": old_snaps["statistics.json"],
                "new": new_snaps["statistics.json"],
            }
        if "checksums.json" in old_snaps and "checksums.json" in new_snaps:
            old_files = old_snaps["checksums.json"].get("files", {})
            new_files = new_snaps["checksums.json"].get("files", {})
            domains["checksums"] = {
                "added": sorted(set(new_files) - set(old_files)),
                "removed": sorted(set(old_files) - set(new_files)),
                "changed": sorted(
                    key
                    for key in sorted(set(old_files) & set(new_files))
                    if old_files[key] != new_files[key]
                ),
            }

        changed_domains = [
            name
            for name, payload in domains.items()
            if self._domain_changed(payload)
        ]
        result = {
            "artifact": "baseline_diff",
            "old_version": old_dir.name,
            "new_version": new_dir.name,
            "old_path": old_dir.as_posix(),
            "new_path": new_dir.as_posix(),
            "timestamp": DEFAULT_BUILD_TIMESTAMP,
            "available_versions": self.list_versions(),
            "domains": domains,
            "summary": {
                "changed_domains": changed_domains,
                "breaking": any(
                    domain in changed_domains
                    for domain in (
                        "registry",
                        "ontology",
                        "dependency",
                        "compiler",
                        "validation",
                    )
                ),
            },
        }

        target = output_dir
        if target is None:
            target = (
                self.project_root
                / "knowledge"
                / "baseline"
                / "diff"
                / f"{old_dir.name}_to_{new_dir.name}"
            )
        target.mkdir(parents=True, exist_ok=True)
        write_text(target / "baseline_diff.json", generate_diff_json(result))
        write_text(target / "baseline_diff.md", generate_diff_markdown(result))
        write_text(target / "baseline_diff.html", generate_diff_html(result))
        logger.info("Wrote baseline diff reports to %s", target)
        result["output_dir"] = target.as_posix()
        return result

    @staticmethod
    def _domain_changed(payload: dict[str, Any]) -> bool:
        if payload.get("changed") is True:
            return True
        for key, value in payload.items():
            if key.endswith("_changed") and value:
                return True
            if isinstance(value, dict):
                if value.get("added") or value.get("removed") or value.get("changed"):
                    return True
                nested = (
                    value.get("classes")
                    or value.get("rules")
                    or value.get("contracts")
                    or value.get("academic_edges")
                )
                if isinstance(nested, dict) and (
                    nested.get("added")
                    or nested.get("removed")
                    or nested.get("changed")
                ):
                    return True
            if isinstance(value, list) and key in {"added", "removed", "changed"}:
                if value:
                    return True
        if payload.get("added") or payload.get("removed") or payload.get("changed"):
            if isinstance(payload.get("changed"), list):
                return bool(payload.get("added") or payload.get("removed") or payload.get("changed"))
        return False


def diff_baselines(
    old: str,
    new: str,
    project_root: Path | None = None,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    """Convenience API for baseline comparison."""
    return BaselineDiffEngine(project_root=project_root).compare(
        old, new, output_dir=output_dir
    )
