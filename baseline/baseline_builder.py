"""One-command Pack 01 baseline builder."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

from baseline.checksums import build_checksums, build_statistics
from baseline.constants import (
    BASELINE_VERSION,
    DEFAULT_BUILD_TIMESTAMP,
    PACK_ID,
    SCHEMA_VERSION,
)
from baseline.generators.compiler_snapshot import generate_compiler_snapshot
from baseline.generators.dependency_snapshot import generate_dependency_snapshot
from baseline.generators.governance_metadata import generate_governance_metadata
from baseline.generators.knowledge_graph import (
    build_knowledge_graph,
    export_dot,
    export_graphml,
    export_mermaid,
)
from baseline.generators.manifest import generate_baseline_manifest
from baseline.generators.ontology_snapshot import generate_ontology_snapshot
from baseline.generators.registry_snapshot import generate_registry_snapshot
from baseline.generators.release_packaging import (
    generate_freeze_inventory,
    generate_release_artifacts,
    generate_release_inventory,
    generate_release_manifest,
    generate_release_metadata,
)
from baseline.generators.reports import (
    generate_build_report,
    generate_freeze_readiness_md,
    generate_release_candidate_md,
    generate_validation_report_md,
)
from baseline.generators.validation_snapshot import generate_validation_snapshot
from baseline.inventory import (
    discover_compiler,
    discover_extra_kr_files,
    discover_graph_specs,
    discover_knowledge_records,
    discover_ontology,
    discover_registries,
    discover_validation,
)
from baseline.io_utils import (
    copy_file,
    read_json,
    relative_posix,
    sha256_file,
    write_json,
    write_text,
)
from baseline.models import BuildContext
from baseline.paths import BaselinePaths, resolve_project_root
from baseline.validators.compiler_validation import validate_compiler
from baseline.validators.graph_validation import validate_graph
from baseline.validators.ontology_validation import validate_ontology
from baseline.validators.registry_validation import validate_registries

logger = logging.getLogger(__name__)


class BaselineBuilder:
    """Generate the full Pack 01 baseline artifact set."""

    def __init__(
        self,
        project_root: Path | None = None,
        version: str = BASELINE_VERSION,
        timestamp: str | None = None,
    ) -> None:
        """Initialize builder with deterministic version/timestamp."""
        root = resolve_project_root(project_root)
        self.version = version
        self.timestamp = (
            timestamp
            or os.environ.get("SOURCE_DATE_EPOCH_ISO")
            or DEFAULT_BUILD_TIMESTAMP
        )
        self.paths = BaselinePaths(root, version)
        self.context = BuildContext(
            project_root=str(self.paths.project_root),
            version=version,
            timestamp=self.timestamp,
            pack_id=PACK_ID,
            schema_version=SCHEMA_VERSION,
        )

    def build(self) -> dict[str, Any]:
        """Rebuild the entire baseline and return a summary dictionary."""
        logger.info(
            "Building Pack 01 baseline v%s at %s",
            self.version,
            self.timestamp,
        )
        self.paths.ensure_output_dirs()

        inventories = self._discover()
        extras = discover_extra_kr_files(self.paths)

        ontology_snap = generate_ontology_snapshot(
            self.context, inventories["ontology"]
        )
        registry_snap = generate_registry_snapshot(
            self.context, inventories["registries"]
        )
        dependency_snap = generate_dependency_snapshot(
            self.context, inventories["knowledge_records"]
        )
        compiler_snap = generate_compiler_snapshot(
            self.context, inventories["compiler"]
        )
        validation_snap = generate_validation_snapshot(
            self.context, inventories["validation"]
        )
        graph = build_knowledge_graph(
            self.context,
            inventories["knowledge_records"],
            inventories["ontology"],
            dependency_snap,
        )

        reports = {
            "compiler": validate_compiler(
                self.context,
                self.paths,
                inventories["compiler"],
                inventories["knowledge_records"],
            ),
            "ontology": validate_ontology(self.context, inventories["ontology"]),
            "registry": validate_registries(
                self.context, self.paths, inventories["registries"]
            ),
            "graph": validate_graph(self.context, graph),
        }

        governance = generate_governance_metadata(
            self.context, reports, inventories
        )
        coverage = validation_snap.get("coverage", {})
        statistics = build_statistics(
            inventories["knowledge_records"],
            inventories["registries"],
            inventories["ontology"],
            inventories["validation"],
            inventories["compiler"],
            dependency_snap,
            graph,
            coverage,
        )

        known_issues = self._known_issues(extras, reports, inventories)
        manifest = generate_baseline_manifest(
            self.context, self.paths, inventories
        )

        written: dict[str, Path] = {}
        written["baseline_manifest.json"] = self._write_json(
            "baseline_manifest.json", manifest
        )
        written["ontology_snapshot.json"] = self._write_json(
            "ontology_snapshot.json", ontology_snap
        )
        written["registry_snapshot.json"] = self._write_json(
            "registry_snapshot.json", registry_snap
        )
        written["dependency_snapshot.json"] = self._write_json(
            "dependency_snapshot.json", dependency_snap
        )
        written["compiler_snapshot.json"] = self._write_json(
            "compiler_snapshot.json", compiler_snap
        )
        written["validation_snapshot.json"] = self._write_json(
            "validation_snapshot.json", validation_snap
        )
        written["knowledge_graph.json"] = self._write_json(
            "knowledge_graph.json", graph
        )
        written["knowledge_graph.graphml"] = self._write_text(
            "knowledge_graph.graphml", export_graphml(graph)
        )
        written["knowledge_graph.dot"] = self._write_text(
            "knowledge_graph.dot", export_dot(graph)
        )
        written["knowledge_graph.mmd"] = self._write_text(
            "knowledge_graph.mmd", export_mermaid(graph)
        )
        written["governance_metadata.json"] = self._write_json(
            "governance_metadata.json", governance
        )
        written["compiler_validation_report.json"] = self._write_json(
            "compiler_validation_report.json", reports["compiler"].to_dict()
        )
        written["ontology_validation_report.json"] = self._write_json(
            "ontology_validation_report.json", reports["ontology"].to_dict()
        )
        written["registry_validation_report.json"] = self._write_json(
            "registry_validation_report.json", reports["registry"].to_dict()
        )
        written["graph_validation_report.json"] = self._write_json(
            "graph_validation_report.json", reports["graph"].to_dict()
        )
        written["statistics.json"] = self._write_json(
            "statistics.json", statistics
        )
        written["known_issues.json"] = self._write_json(
            "known_issues.json", known_issues
        )

        validation_summary = {
            name: report.status for name, report in reports.items()
        }
        written["build_report.md"] = self._write_text(
            "build_report.md",
            generate_build_report(
                self.context.to_dict(),
                sorted(written.keys()),
                statistics,
                validation_summary,
            ),
        )
        written["validation_report.md"] = self._write_text(
            "validation_report.md",
            generate_validation_report_md(reports),
        )
        written["release_candidate.md"] = self._write_text(
            "release_candidate.md",
            generate_release_candidate_md(governance, statistics),
        )
        written["freeze_readiness.md"] = self._write_text(
            "freeze_readiness.md",
            generate_freeze_readiness_md(governance),
        )

        artifact_paths = {
            name: relative_posix(path, self.paths.project_root)
            for name, path in written.items()
        }
        release_manifest = generate_release_manifest(
            self.context, governance, statistics
        )
        release_metadata = generate_release_metadata(self.context, governance)
        release_inventory = generate_release_inventory(self.context, inventories)
        freeze_inventory = generate_freeze_inventory(
            self.context, artifact_paths, governance
        )

        written["release_manifest.json"] = self._write_json(
            "release_manifest.json", release_manifest
        )
        written["release_metadata.json"] = self._write_json(
            "release_metadata.json", release_metadata
        )
        written["release_inventory.json"] = self._write_json(
            "release_inventory.json", release_inventory
        )
        written["freeze_inventory.json"] = self._write_json(
            "freeze_inventory.json", freeze_inventory
        )

        # Checksums cover sources + generated artifacts written so far.
        checksums = build_checksums(
            self.paths.project_root,
            inventories["knowledge_records"],
            inventories["registries"],
            inventories["ontology"]["files"],
            written,
        )
        written["checksums.json"] = self._write_json(
            "checksums.json", checksums
        )
        checksums["files"][
            relative_posix(written["checksums.json"], self.paths.project_root)
        ] = sha256_file(written["checksums.json"])
        checksums["count"] = len(checksums["files"])
        write_json(written["checksums.json"], checksums)

        artifact_paths["checksums.json"] = relative_posix(
            written["checksums.json"], self.paths.project_root
        )
        release_artifacts = generate_release_artifacts(
            self.context,
            artifact_paths,
            checksums["files"],
        )
        written["release_artifacts.json"] = self._write_json(
            "release_artifacts.json", release_artifacts
        )
        # Include release_artifacts in checksum map after write.
        checksums["files"][
            relative_posix(
                written["release_artifacts.json"], self.paths.project_root
            )
        ] = sha256_file(written["release_artifacts.json"])
        checksums["count"] = len(checksums["files"])
        write_json(written["checksums.json"], checksums)

        self._mirror_generated(written, governance, compiler_snap, reports)
        summary = {
            "version": self.version,
            "timestamp": self.timestamp,
            "output_dir": relative_posix(
                self.paths.version_dir, self.paths.project_root
            ),
            "artifact_count": len(written),
            "artifacts": sorted(written.keys()),
            "validation": validation_summary,
            "overall_status": governance.get("overall_status"),
            "statistics": statistics,
            "known_issues": known_issues,
        }
        write_json(self.paths.version_dir / "build_summary.json", summary)
        self._update_versions_index(summary)
        logger.info(
            "Baseline build complete: %s artifacts, status=%s",
            len(written),
            governance.get("overall_status"),
        )
        return summary

    def _update_versions_index(self, summary: dict[str, Any]) -> None:
        """Maintain a multi-version index for 1.x / 2.x lifecycle support."""
        index_path = self.paths.baseline_root / "versions_index.json"
        versions: list[dict[str, Any]] = []
        if index_path.is_file():
            try:
                existing = read_json(index_path)
                if isinstance(existing, dict):
                    versions = list(existing.get("versions", []))
            except (OSError, ValueError):
                versions = []
        entry = {
            "version": self.version,
            "directory": f"v{self.version}",
            "path": relative_posix(self.paths.version_dir, self.paths.project_root),
            "timestamp": self.timestamp,
            "status": summary.get("overall_status"),
            "artifact_count": summary.get("artifact_count"),
        }
        versions = [item for item in versions if item.get("version") != self.version]
        versions.append(entry)
        versions = sorted(versions, key=lambda item: str(item.get("version", "")))
        write_json(
            index_path,
            {
                "artifact": "versions_index",
                "schema_version": SCHEMA_VERSION,
                "pack_id": PACK_ID,
                "supported_patterns": ["1.0.x", "1.1.x", "1.2.x", "2.x"],
                "versions": versions,
            },
        )

    def validate_only(self, *, persist: bool = True) -> dict[str, Any]:
        """Run Sprint 2 validations and optionally persist validation artifacts."""
        inventories = self._discover()
        dependency_snap = generate_dependency_snapshot(
            self.context, inventories["knowledge_records"]
        )
        graph = build_knowledge_graph(
            self.context,
            inventories["knowledge_records"],
            inventories["ontology"],
            dependency_snap,
        )
        reports = {
            "compiler": validate_compiler(
                self.context,
                self.paths,
                inventories["compiler"],
                inventories["knowledge_records"],
            ),
            "ontology": validate_ontology(self.context, inventories["ontology"]),
            "registry": validate_registries(
                self.context, self.paths, inventories["registries"]
            ),
            "graph": validate_graph(self.context, graph),
        }
        validation_snap = generate_validation_snapshot(
            self.context, inventories["validation"]
        )
        governance = generate_governance_metadata(
            self.context, reports, inventories
        )
        status = (
            "PASS"
            if all(r.status == "PASS" for r in reports.values())
            else "FAIL"
        )
        result: dict[str, Any] = {
            "status": status,
            "reports": {name: report.to_dict() for name, report in reports.items()},
            "coverage": validation_snap.get("coverage", {}),
            "statistics": validation_snap.get("statistics", {}),
            "governance": governance,
        }
        if persist:
            self.paths.ensure_output_dirs()
            artifacts = {
                "validation_snapshot.json": validation_snap,
                "governance_metadata.json": governance,
                "compiler_validation_report.json": reports["compiler"].to_dict(),
                "ontology_validation_report.json": reports["ontology"].to_dict(),
                "registry_validation_report.json": reports["registry"].to_dict(),
                "graph_validation_report.json": reports["graph"].to_dict(),
            }
            written: dict[str, Path] = {}
            for name, payload in artifacts.items():
                written[name] = self._write_json(name, payload)
            write_json(
                self.paths.governance_generated / "governance_metadata.json",
                governance,
            )
            write_json(
                self.paths.validation_generated / "validation_snapshot.json",
                validation_snap,
            )
            for name in (
                "compiler_validation_report.json",
                "ontology_validation_report.json",
                "registry_validation_report.json",
                "graph_validation_report.json",
            ):
                copy_file(written[name], self.paths.validation_generated / name)
            write_json(
                self.paths.compiler_generated / "compiler_validation_report.json",
                reports["compiler"].to_dict(),
            )
            result["persisted_artifacts"] = sorted(written.keys())
            result["output_dir"] = relative_posix(
                self.paths.version_dir, self.paths.project_root
            )
        return result

    def _discover(self) -> dict[str, Any]:
        return {
            "knowledge_records": discover_knowledge_records(self.paths),
            "registries": discover_registries(self.paths),
            "ontology": discover_ontology(self.paths),
            "compiler": discover_compiler(self.paths),
            "validation": discover_validation(self.paths),
            "graph": discover_graph_specs(self.paths),
        }

    def _write_json(self, filename: str, payload: dict[str, Any]) -> Path:
        path = self.paths.artifact(filename)
        write_json(path, payload)
        return path

    def _write_text(self, filename: str, text: str) -> Path:
        path = self.paths.artifact(filename)
        write_text(path, text)
        return path

    def _mirror_generated(
        self,
        written: dict[str, Path],
        governance: dict[str, Any],
        compiler_snap: dict[str, Any],
        reports: dict[str, Any],
    ) -> None:
        """Mirror selected artifacts into generated/ directories."""
        write_json(
            self.paths.governance_generated / "governance_metadata.json",
            governance,
        )
        write_json(
            self.paths.compiler_generated / "compiler_snapshot.json",
            compiler_snap,
        )
        write_json(
            self.paths.compiler_generated / "compiler_validation_report.json",
            reports["compiler"].to_dict(),
        )
        write_json(
            self.paths.validation_generated / "validation_snapshot.json",
            read_json(written["validation_snapshot.json"]),
        )
        for name in (
            "compiler_validation_report.json",
            "ontology_validation_report.json",
            "registry_validation_report.json",
            "graph_validation_report.json",
            "validation_report.md",
        ):
            copy_file(written[name], self.paths.validation_generated / name)
        for name in (
            "knowledge_graph.json",
            "knowledge_graph.graphml",
            "knowledge_graph.dot",
            "knowledge_graph.mmd",
            "graph_validation_report.json",
        ):
            copy_file(written[name], self.paths.graph_generated / name)

    def _known_issues(
        self,
        extras: list[str],
        reports: dict[str, Any],
        inventories: dict[str, Any],
    ) -> dict[str, Any]:
        issues: list[dict[str, Any]] = []
        if extras:
            issues.append(
                {
                    "id": "KI-000001",
                    "severity": "WARNING",
                    "title": "Unexpected KR filenames present",
                    "detail": extras,
                    "proposal": (
                        "Keep canonical PACK_01_MANIFEST filenames only; "
                        "archive or rename unexpected files outside freeze scope."
                    ),
                }
            )
        empty_registries = [
            item["registry_id"]
            for item in inventories["registries"]
            if item["record_count"] == 0
        ]
        if empty_registries:
            issues.append(
                {
                    "id": "KI-000002",
                    "severity": "INFO",
                    "title": "Registry scaffolds have empty records arrays",
                    "detail": empty_registries,
                    "proposal": (
                        "Expected for Pack 01 scaffold. Populate registries in a "
                        "future versioned release without changing schema."
                    ),
                }
            )
        warnings = []
        for name, report in reports.items():
            for finding in report.findings:
                if finding.severity == "WARNING":
                    warnings.append(
                        {
                            "domain": name,
                            "code": finding.code,
                            "message": finding.message,
                        }
                    )
        if warnings:
            issues.append(
                {
                    "id": "KI-000003",
                    "severity": "INFO",
                    "title": "Validation warnings present",
                    "detail": warnings,
                    "proposal": (
                        "Review warnings before formal freeze ceremony; "
                        "do not alter KR/registry/governance sources to silence them."
                    ),
                }
            )
        return {
            "artifact": "known_issues",
            "count": len(issues),
            "issues": issues,
        }


def build_baseline(
    project_root: Path | None = None,
    version: str = BASELINE_VERSION,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Convenience API to build the Pack 01 baseline."""
    return BaselineBuilder(
        project_root=project_root,
        version=version,
        timestamp=timestamp,
    ).build()
