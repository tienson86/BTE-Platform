"""Ontology validation report generator."""

from __future__ import annotations

from collections import Counter
from typing import Any

from baseline.constants import SCHEMA_VERSION
from baseline.models import BuildContext, ValidationFinding, ValidationReport


def validate_ontology(
    context: BuildContext,
    ontology: dict[str, Any],
) -> ValidationReport:
    """Validate ontology classes, hierarchy integrity, and duplicates."""
    findings: list[ValidationFinding] = []
    classes = ontology.get("classes", [])
    class_ids = [str(item.get("id") or "") for item in classes if item.get("id")]
    id_counts = Counter(class_ids)
    class_id_set = set(class_ids)

    for class_id, count in sorted(id_counts.items()):
        if count > 1:
            findings.append(
                ValidationFinding(
                    code="ONT-DUPLICATE",
                    severity="ERROR",
                    message=f"Duplicate ontology class ID '{class_id}'",
                    object_id=class_id,
                )
            )

    for item in classes:
        class_id = str(item.get("id") or "")
        parent = item.get("parent_class")
        if parent and str(parent) not in class_id_set:
            findings.append(
                ValidationFinding(
                    code="ONT-BROKEN-PARENT",
                    severity="ERROR",
                    message=(
                        f"Class '{class_id}' references missing parent '{parent}'"
                    ),
                    object_id=class_id,
                )
            )
        if not item.get("canonical_name"):
            findings.append(
                ValidationFinding(
                    code="ONT-SEMANTIC",
                    severity="WARNING",
                    message=f"Class '{class_id}' missing canonical_name",
                    object_id=class_id,
                )
            )

    referenced_parents = {
        str(item.get("parent_class"))
        for item in classes
        if item.get("parent_class")
    }
    orphans = sorted(
        cid
        for cid in class_id_set
        if cid not in referenced_parents
        and not any(
            str(item.get("id")) == cid and item.get("parent_class") is None
            for item in classes
        )
    )
    # Root classes (parent_class null) are intentional; orphans = non-root with
    # no children and no incoming hierarchy besides self — report only true
    # disconnected non-roots already covered by broken parents.
    leaf_without_parent = [
        str(item.get("id"))
        for item in classes
        if item.get("id")
        and item.get("parent_class") is None
        and str(item.get("id")) != "OCL-000001"
    ]
    for class_id in leaf_without_parent:
        findings.append(
            ValidationFinding(
                code="ONT-ORPHAN",
                severity="WARNING",
                message=(
                    f"Non-root ontology class '{class_id}' has null parent_class"
                ),
                object_id=class_id,
            )
        )

    for entity in ontology.get("entity_types", []):
        ontology_class_id = entity.get("ontology_class_id")
        if ontology_class_id and str(ontology_class_id) not in class_id_set:
            findings.append(
                ValidationFinding(
                    code="ONT-REL-INTEGRITY",
                    severity="ERROR",
                    message=(
                        f"Entity type '{entity.get('id')}' references missing "
                        f"ontology class '{ontology_class_id}'"
                    ),
                    object_id=str(entity.get("id") or ""),
                )
            )

    for file_entry in ontology.get("files", []):
        if not file_entry.get("exists"):
            findings.append(
                ValidationFinding(
                    code="ONT-MISSING-FILE",
                    severity="ERROR",
                    message=f"Missing ontology file: {file_entry['filename']}",
                    path=file_entry["path"],
                )
            )

    status = "PASS" if not any(
        f.severity in {"ERROR", "CRITICAL"} for f in findings
    ) else "FAIL"
    return ValidationReport(
        report_id="VAL-ONTOLOGY-BASELINE-001",
        domain="ontology",
        status=status,
        schema_version=SCHEMA_VERSION,
        findings=findings,
        statistics={
            "class_count": len(classes),
            "duplicate_count": sum(1 for _, c in id_counts.items() if c > 1),
            "orphan_warning_count": len(leaf_without_parent),
            "hierarchy_orphan_candidates": orphans,
            "entity_type_count": len(ontology.get("entity_types", [])),
            "relationship_integrity_errors": sum(
                1 for f in findings if f.code == "ONT-REL-INTEGRITY"
            ),
        },
        metadata={
            "pack_id": context.pack_id,
            "version": context.version,
            "timestamp": context.timestamp,
            "checks": [
                "ontology_integrity",
                "duplicate_ontology_objects",
                "semantic_consistency",
                "orphan_nodes",
                "relationship_integrity",
            ],
        },
    )
