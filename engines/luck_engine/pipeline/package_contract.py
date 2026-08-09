"""Verify luck component contracts before pipeline execution."""

from __future__ import annotations

from typing import Any, Mapping

from engines.luck_engine.analysis.analysis_result import luck_analysis_contract
from engines.luck_engine.contracts.timeline_contract import timeline_contract
from engines.luck_engine.decision.decision_result import luck_decision_contract
from engines.luck_engine.exceptions import LuckContractViolationError, LuckPackageLoadError
from engines.luck_engine.pipeline.stage_registry import LuckStageRecord
from engines.luck_engine.timeline.package_loader import (
    LoadedLuckPackage,
    LuckPackageLoader,
    satisfies_version_constraint,
)
from engines.luck_engine.timeline_constants import REQUIRED_SCHEMA_VERSION

DEFAULT_VERSION_CONSTRAINTS: dict[str, str] = {
    "bz_09_luck_foundation": "^1.0.0",
}

REQUIRED_ANALYSIS_VERSION = "1.0.0"
REQUIRED_DECISION_VERSION = "1.0.0"
REQUIRED_AX2_VERSION = "2.0.0"
REQUIRED_AX3_VERSION = "1.0.0"


class LuckPackageContractVerifier:
    """Validate package/component version, schema, dependencies, and published I/O."""

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
        self._loader = LuckPackageLoader()

    def load_timeline_package(self) -> LoadedLuckPackage:
        """Load and admit bz_09 for timeline contract checks."""
        try:
            return self._loader.load(
                version_constraint=self._constraints.get("bz_09_luck_foundation", "^1.0.0"),
            )
        except LuckPackageLoadError as exc:
            raise LuckContractViolationError(str(exc)) from exc

    def verify_timeline_package(self, package: LoadedLuckPackage) -> None:
        """Verify the released Luck Foundation package contract."""
        if package.schema_version != self._required_schema_version:
            raise LuckContractViolationError(
                f"schema_incompatible:{package.package_id}:{package.schema_version}"
            )
        constraint = self._constraints.get(package.package_id)
        if constraint and not satisfies_version_constraint(package.package_version, constraint):
            raise LuckContractViolationError(
                f"version_incompatible:{package.package_id}:{package.package_version}:{constraint}"
            )
        expected = set(timeline_contract()["outputs"])
        if set(package.published_outputs) != expected:
            raise LuckContractViolationError(
                f"output_contract_mismatch:{package.package_id}"
            )
        if set(package.published_inputs) != set(timeline_contract()["inputs"]):
            raise LuckContractViolationError(
                f"input_contract_mismatch:{package.package_id}"
            )

    def verify_analysis_component(self, *, analysis_version: str, ax2_version: str) -> None:
        """Verify LE-2 / AX-2 version and published analysis contract."""
        if analysis_version != REQUIRED_ANALYSIS_VERSION:
            raise LuckContractViolationError(f"analysis_version_incompatible:{analysis_version}")
        if ax2_version != REQUIRED_AX2_VERSION:
            raise LuckContractViolationError(f"ax2_version_incompatible:{ax2_version}")
        contract = luck_analysis_contract()
        if not contract["outputs"]:
            raise LuckContractViolationError("analysis_output_contract_empty")

    def verify_decision_component(self, *, decision_version: str, ax3_version: str) -> None:
        """Verify LE-3 / AX-3 version and published decision contract."""
        if decision_version != REQUIRED_DECISION_VERSION:
            raise LuckContractViolationError(f"decision_version_incompatible:{decision_version}")
        if ax3_version != REQUIRED_AX3_VERSION:
            raise LuckContractViolationError(f"ax3_version_incompatible:{ax3_version}")
        contract = luck_decision_contract()
        if not contract["outputs"]:
            raise LuckContractViolationError("decision_output_contract_empty")

    def verify_payload(self, payload: Mapping[str, Any], stage: LuckStageRecord) -> None:
        """Require declared published outputs to be present."""
        missing = [name for name in stage.published_outputs if name not in payload]
        if missing:
            raise LuckContractViolationError(
                f"missing_published_outputs:{stage.stage_id}:{','.join(missing)}"
            )
        extra_overwrite = [
            name for name in payload if name not in stage.published_outputs and name != "status"
        ]
        if extra_overwrite:
            raise LuckContractViolationError(
                f"undeclared_outputs:{stage.stage_id}:{','.join(sorted(extra_overwrite))}"
            )
