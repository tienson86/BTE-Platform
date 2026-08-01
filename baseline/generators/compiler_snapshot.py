"""Compiler snapshot generator."""

from __future__ import annotations

from typing import Any

from baseline.constants import SCHEMA_VERSION
from baseline.models import BuildContext


def generate_compiler_snapshot(
    context: BuildContext,
    compiler: dict[str, Any],
) -> dict[str, Any]:
    """Generate compiler snapshot from pipeline and stage contracts."""
    pipeline = compiler.get("pipeline", {})
    stages = compiler.get("stages") or pipeline.get("stages", [])
    stage_ids = []
    for stage in stages:
        stage_id = stage.get("stage_id") or stage.get("id")
        if stage_id:
            stage_ids.append(stage_id)

    contracts = [
        {
            "contract_id": item["filename"],
            "path": item["path"],
            "exists": item["exists"],
            "sha256": item.get("sha256", ""),
        }
        for item in compiler.get("files", [])
    ]

    inputs: list[str] = []
    outputs: list[str] = []
    for stage in pipeline.get("stages", []):
        for value in stage.get("inputs", []):
            if value not in inputs:
                inputs.append(value)
        for value in stage.get("outputs", []):
            if value not in outputs:
                outputs.append(value)

    return {
        "artifact": "compiler_snapshot",
        "schema_version": SCHEMA_VERSION,
        "pack_id": context.pack_id,
        "version": context.version,
        "timestamp": context.timestamp,
        "compiler_stages": stages,
        "contracts": contracts,
        "pipeline": {
            "pipeline_id": pipeline.get("pipeline_id"),
            "pipeline_name": pipeline.get("pipeline_name"),
            "version": pipeline.get("version"),
            "stage_order": stage_ids,
        },
        "inputs": inputs,
        "outputs": outputs,
        "generated_artifacts": [
            "compiler_snapshot.json",
            "compiler_validation_report.json",
            "knowledge/compiler/generated/compiler_snapshot.json",
        ],
        "statistics": compiler.get("statistics", {}),
    }
