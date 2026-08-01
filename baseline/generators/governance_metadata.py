"""Governance metadata generator."""

from __future__ import annotations

from typing import Any

from baseline.constants import SCHEMA_VERSION
from baseline.models import BuildContext, ValidationReport


def generate_governance_metadata(
    context: BuildContext,
    validation_reports: dict[str, ValidationReport],
    inventories: dict[str, Any],
) -> dict[str, Any]:
    """Generate freeze/baseline/compiler/validation/release readiness metadata."""
    kr_ok = all(item["exists"] for item in inventories["knowledge_records"])
    registry_ok = all(item["exists"] for item in inventories["registries"])
    ontology_ok = all(item.get("exists") for item in inventories["ontology"]["files"])
    compiler_ok = all(item.get("exists") for item in inventories["compiler"]["files"])
    validation_ok = all(
        item.get("exists") for item in inventories["validation"]["files"]
    )

    report_statuses = {
        name: report.status for name, report in sorted(validation_reports.items())
    }
    all_validations_pass = all(
        status == "PASS" for status in report_statuses.values()
    )

    readiness = {
        "freeze_readiness": kr_ok and all_validations_pass,
        "baseline_readiness": kr_ok and registry_ok and ontology_ok,
        "compiler_readiness": compiler_ok,
        "validation_readiness": validation_ok and all_validations_pass,
        "release_readiness": (
            kr_ok
            and registry_ok
            and ontology_ok
            and compiler_ok
            and validation_ok
            and all_validations_pass
        ),
    }

    return {
        "artifact": "governance_metadata",
        "schema_version": SCHEMA_VERSION,
        "pack_id": context.pack_id,
        "version": context.version,
        "timestamp": context.timestamp,
        "freeze_readiness": {
            "ready": readiness["freeze_readiness"],
            "criteria": {
                "all_kr_present": kr_ok,
                "all_validations_pass": all_validations_pass,
            },
        },
        "baseline_readiness": {
            "ready": readiness["baseline_readiness"],
            "criteria": {
                "knowledge_records": kr_ok,
                "registries": registry_ok,
                "ontology": ontology_ok,
            },
        },
        "compiler_readiness": {
            "ready": readiness["compiler_readiness"],
            "criteria": {"compiler_contracts_present": compiler_ok},
        },
        "validation_readiness": {
            "ready": readiness["validation_readiness"],
            "criteria": {
                "validation_contracts_present": validation_ok,
                "validation_reports": report_statuses,
            },
        },
        "release_readiness": {
            "ready": readiness["release_readiness"],
            "criteria": {
                "freeze_readiness": readiness["freeze_readiness"],
                "baseline_readiness": readiness["baseline_readiness"],
                "compiler_readiness": readiness["compiler_readiness"],
                "validation_readiness": readiness["validation_readiness"],
            },
        },
        "overall_status": (
            "READY_FOR_FREEZE"
            if readiness["release_readiness"]
            else "NOT_READY"
        ),
    }
