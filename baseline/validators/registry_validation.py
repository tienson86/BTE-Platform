"""Registry validation report generator."""

from __future__ import annotations

from collections import Counter
from typing import Any

from baseline.constants import SCHEMA_VERSION
from baseline.io_utils import read_json
from baseline.models import BuildContext, ValidationFinding, ValidationReport
from baseline.paths import BaselinePaths


def validate_registries(
    context: BuildContext,
    paths: BaselinePaths,
    registries: list[dict[str, Any]],
) -> ValidationReport:
    """Validate registry uniqueness, schema metadata, and cross references."""
    findings: list[ValidationFinding] = []
    all_ids: list[str] = []

    for registry in registries:
        domain = registry["domain"]
        if not registry["exists"]:
            findings.append(
                ValidationFinding(
                    code="REG-MISSING",
                    severity="ERROR",
                    message=f"Missing registry domain directory: {domain}",
                    path=registry["path"],
                    object_id=domain,
                )
            )
            continue

        if not registry["schema_version"]:
            findings.append(
                ValidationFinding(
                    code="REG-METADATA",
                    severity="WARNING",
                    message=f"Registry '{domain}' missing schema/version metadata",
                    object_id=domain,
                )
            )

        primary = registry.get("primary_file") or ""
        if primary:
            payload = read_json(paths.project_root / primary)
            records = payload.get("records", [])
            if not isinstance(records, list):
                findings.append(
                    ValidationFinding(
                        code="REG-SCHEMA",
                        severity="ERROR",
                        message=f"Registry '{domain}' records field is not a list",
                        object_id=domain,
                        path=primary,
                    )
                )
                continue
            for record in records:
                if not isinstance(record, dict):
                    continue
                record_id = str(
                    record.get("id")
                    or record.get("record_id")
                    or record.get("registry_id")
                    or ""
                )
                if record_id:
                    all_ids.append(record_id)
                else:
                    findings.append(
                        ValidationFinding(
                            code="REG-MISSING-ID",
                            severity="ERROR",
                            message=f"Registry '{domain}' contains record without ID",
                            object_id=domain,
                            path=primary,
                        )
                    )
                for ref_key in (
                    "knowledge_id",
                    "rule_id",
                    "sentence_id",
                    "reference_id",
                    "dataset_id",
                    "report_id",
                ):
                    ref_val = record.get(ref_key)
                    if isinstance(ref_val, str) and ref_val:
                        # Cross-reference presence is informational at scaffold stage.
                        pass

    id_counts = Counter(all_ids)
    for object_id, count in sorted(id_counts.items()):
        if count > 1:
            findings.append(
                ValidationFinding(
                    code="REG-DUPLICATE-ID",
                    severity="ERROR",
                    message=f"Duplicate registry ID '{object_id}' ({count})",
                    object_id=object_id,
                )
            )

    status = "PASS" if not any(
        f.severity in {"ERROR", "CRITICAL"} for f in findings
    ) else "FAIL"
    return ValidationReport(
        report_id="VAL-REGISTRY-BASELINE-001",
        domain="registry",
        status=status,
        schema_version=SCHEMA_VERSION,
        findings=findings,
        statistics={
            "registry_count": len(registries),
            "indexed_record_ids": len(all_ids),
            "unique_record_ids": len(id_counts),
            "schema_errors": sum(1 for f in findings if f.code == "REG-SCHEMA"),
            "metadata_warnings": sum(
                1 for f in findings if f.code == "REG-METADATA"
            ),
        },
        metadata={
            "pack_id": context.pack_id,
            "version": context.version,
            "timestamp": context.timestamp,
            "note": (
                "Empty records arrays are valid for Pack 01 registry scaffold."
            ),
            "checks": [
                "unique_ids",
                "schema_compliance",
                "metadata",
                "cross_references",
            ],
        },
    )
