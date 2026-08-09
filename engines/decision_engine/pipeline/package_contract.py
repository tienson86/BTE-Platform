"""Verify released decision package contracts before execution."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from engines.decision_engine.exceptions import ContractViolationError
from engines.decision_engine.pipeline.diagnostics import DecisionDiagnostic
from engines.decision_engine.pipeline.package_loader import (
    REQUIRED_SCHEMA_VERSION,
    LoadedPackage,
    satisfies_version_constraint,
)
from engines.decision_engine.pipeline.stage_registry import DecisionStageRecord

DEFAULT_VERSION_CONSTRAINTS: dict[str, str] = {
    "bz_06_useful_god_foundation": "^1.0.0",
    "bz_07_useful_god_priority": "^1.0.0",
    "bz_08_useful_god_override": "^1.0.0",
}

_BINDING_METADATA_KEYS = frozenset(
    {
        "stage_id",
        "package_id",
        "package_version",
        "schema_version",
        "knowledge_version",
        "compatibility_version",
        "status",
        "rule_count",
        "produced_signals",
        "consumed_signals",
        "upstream_stages",
        "snapshot_facts",
        "rule_ids",
        "trace_step",
    }
)


class DecisionPackageContractVerifier:
    """Validate package version, schema, dependencies, and published I/O."""

    def __init__(
        self,
        *,
        version_constraints: Mapping[str, str] | None = None,
        required_schema_version: str = REQUIRED_SCHEMA_VERSION,
    ) -> None:
        """Initialize expected SemVer constraints."""
        self._constraints = dict(DEFAULT_VERSION_CONSTRAINTS)
        self._constraints.update(version_constraints or {})
        self._required_schema_version = required_schema_version

    def verify(
        self,
        package: LoadedPackage,
        *,
        stage: DecisionStageRecord | None = None,
        loaded_packages: Mapping[str, LoadedPackage] | None = None,
    ) -> list[DecisionDiagnostic]:
        """Verify one package. Raises ContractViolationError on hard failure."""
        if package.package_type != "decision":
            raise ContractViolationError(
                f"package_type_mismatch:{package.package_id}:{package.package_type}"
            )
        if package.schema_version != self._required_schema_version:
            raise ContractViolationError(
                f"schema_incompatible:{package.package_id}:{package.schema_version}"
            )
        constraint = self._constraints.get(package.package_id)
        if constraint and not satisfies_version_constraint(
            package.package_version,
            constraint,
        ):
            raise ContractViolationError(
                f"version_incompatible:{package.package_id}:"
                f"{package.package_version}:{constraint}"
            )
        if stage is not None and stage.package_id != package.package_id:
            raise ContractViolationError(
                f"package_stage_mismatch:{stage.stage_id}:{package.package_id}"
            )
        if stage is not None:
            self._verify_published_contracts(package, stage)
        if loaded_packages is not None:
            self._verify_dependency_contract(package, loaded_packages)
        return []

    def verify_payload(
        self,
        payload: Mapping[str, Any],
        stage: DecisionStageRecord,
    ) -> None:
        """Reject undeclared analytical outputs on a published payload."""
        produced = set(stage.published_outputs)
        extra = [
            key
            for key in payload
            if key not in _BINDING_METADATA_KEYS and key not in produced
        ]
        declared = payload.get("produced_signals")
        if isinstance(declared, (list, tuple)):
            extra.extend(name for name in declared if name not in produced)
        if extra:
            raise ContractViolationError(
                f"undeclared_outputs:{stage.stage_id}:{','.join(sorted(set(extra)))}"
            )

    def _verify_published_contracts(
        self,
        package: LoadedPackage,
        stage: DecisionStageRecord,
    ) -> None:
        published_inputs = _read_asset_names(package.root, "published_inputs.json")
        published_outputs = _read_asset_names(package.root, "published_outputs.json")
        if published_inputs is not None:
            missing = [name for name in stage.published_inputs if name not in published_inputs]
            unexpected = [name for name in published_inputs if name not in stage.published_inputs]
            if missing or unexpected:
                raise ContractViolationError(
                    f"input_contract_mismatch:{package.package_id}:"
                    f"missing={','.join(missing)}:extra={','.join(unexpected)}"
                )
        if published_outputs is not None:
            missing = [name for name in published_outputs if name not in stage.published_outputs]
            if missing:
                raise ContractViolationError(
                    f"output_contract_mismatch:{package.package_id}:"
                    f"missing={','.join(missing)}"
                )

    def _verify_dependency_contract(
        self,
        package: LoadedPackage,
        loaded_packages: Mapping[str, LoadedPackage],
    ) -> None:
        dep_path = package.root / "DEPENDENCIES.json"
        if not dep_path.is_file():
            raise ContractViolationError(f"missing_dependencies_file:{package.package_id}")
        payload = json.loads(dep_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ContractViolationError(f"invalid_dependencies:{package.package_id}")
        by_id = {item.package_id: item for item in loaded_packages.values()}
        for entry in payload.get("optional") or []:
            if not isinstance(entry, dict):
                continue
            dep_id = str(entry.get("package_id", ""))
            constraint = str(entry.get("version_constraint", ""))
            present = by_id.get(dep_id)
            if present is None or not constraint:
                continue
            if not satisfies_version_constraint(present.package_version, constraint):
                raise ContractViolationError(
                    f"dependency_contract_incompatible:{package.package_id}:{dep_id}"
                )


def _read_asset_names(root: Path, filename: str) -> tuple[str, ...] | None:
    path = root / "assets" / filename
    if not path.is_file():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return None
    items = payload.get("inputs") if "inputs" in payload else payload.get("outputs")
    if not isinstance(items, list):
        return None
    names: list[str] = []
    for item in items:
        if isinstance(item, dict) and item.get("name"):
            names.append(str(item["name"]))
    return tuple(names)
