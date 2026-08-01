"""Compiler validation report generator."""

from __future__ import annotations

from collections import Counter
from typing import Any

from baseline.constants import SCHEMA_VERSION
from baseline.inventory import collect_ids
from baseline.io_utils import read_json
from baseline.models import BuildContext, ValidationFinding, ValidationReport
from baseline.paths import BaselinePaths


def validate_compiler(
    context: BuildContext,
    paths: BaselinePaths,
    compiler: dict[str, Any],
    knowledge_records: list[dict[str, Any]],
) -> ValidationReport:
    """Validate compiler contracts, duplicate IDs, and dependency resolution."""
    findings: list[ValidationFinding] = []
    id_counter: Counter[str] = Counter()

    for file_entry in compiler.get("files", []):
        if not file_entry.get("exists"):
            findings.append(
                ValidationFinding(
                    code="CMP-MISSING-FILE",
                    severity="ERROR",
                    message=f"Missing compiler contract file: {file_entry['filename']}",
                    path=file_entry["path"],
                )
            )
            continue
        payload = read_json(paths.project_root / file_entry["path"])
        for object_id in collect_ids(payload):
            id_counter[object_id] += 1

    for object_id, count in sorted(id_counter.items()):
        if count > 1 and object_id.startswith(("STAGE-", "PIPE-", "ERR-")):
            # Stage IDs intentionally appear in both pipeline and registry.
            if object_id.startswith("STAGE-") and count <= 2:
                continue
            findings.append(
                ValidationFinding(
                    code="CMP-DUPLICATE-ID",
                    severity="ERROR",
                    message=f"Duplicate compiler ID '{object_id}' seen {count} times",
                    object_id=object_id,
                )
            )

    pipeline = compiler.get("pipeline", {})
    stages = pipeline.get("stages", [])
    stage_ids = {
        stage.get("id") or stage.get("stage_id")
        for stage in stages
        if stage.get("id") or stage.get("stage_id")
    }
    for stage in stages:
        stage_id = stage.get("id") or stage.get("stage_id")
        for dep in stage.get("dependencies", []):
            if dep not in stage_ids:
                findings.append(
                    ValidationFinding(
                        code="CMP-BROKEN-REF",
                        severity="ERROR",
                        message=(
                            f"Stage '{stage_id}' depends on missing stage '{dep}'"
                        ),
                        object_id=str(stage_id or ""),
                    )
                )

    registry_stages = {
        stage.get("stage_id") for stage in compiler.get("stages", [])
    }
    for stage_id in sorted(sid for sid in stage_ids if sid):
        if registry_stages and stage_id not in registry_stages:
            findings.append(
                ValidationFinding(
                    code="CMP-CONTRACT-MISMATCH",
                    severity="WARNING",
                    message=(
                        f"Pipeline stage '{stage_id}' missing from stage_registry"
                    ),
                    object_id=str(stage_id),
                )
            )

    missing_kr = [item["record_id"] for item in knowledge_records if not item["exists"]]
    for record_id in missing_kr:
        findings.append(
            ValidationFinding(
                code="CMP-REGISTRY-LOAD",
                severity="ERROR",
                message=f"Cannot resolve Knowledge Record for compile: {record_id}",
                object_id=record_id,
            )
        )

    if not stages:
        findings.append(
            ValidationFinding(
                code="CMP-EMPTY-PIPELINE",
                severity="ERROR",
                message="Compiler pipeline has no stages",
            )
        )

    status = "PASS" if not any(
        f.severity in {"ERROR", "CRITICAL"} for f in findings
    ) else "FAIL"
    return ValidationReport(
        report_id="VAL-COMPILER-BASELINE-001",
        domain="compiler",
        status=status,
        schema_version=SCHEMA_VERSION,
        findings=findings,
        statistics={
            "contract_files": len(compiler.get("files", [])),
            "stage_count": len(stages),
            "unique_ids": len(id_counter),
            "missing_kr_count": len(missing_kr),
            "broken_reference_count": sum(
                1 for f in findings if f.code == "CMP-BROKEN-REF"
            ),
            "duplicate_id_count": sum(
                1 for f in findings if f.code == "CMP-DUPLICATE-ID"
            ),
        },
        metadata={
            "pack_id": context.pack_id,
            "version": context.version,
            "timestamp": context.timestamp,
            "checks": [
                "duplicate_ids",
                "broken_references",
                "compiler_contracts",
                "registry_loading",
                "dependency_resolution",
            ],
        },
    )
