"""Verify interpretation component contracts before pipeline execution."""

from __future__ import annotations

from typing import Any, Mapping

from engines.interpretation_engine.composition.composition_context import ASSEMBLY_VERSION
from engines.interpretation_engine.contracts.interpretation_contracts import (
    interpretation_foundation_contract,
)
from engines.interpretation_engine.foundation_constants import (
    INTERPRETATION_VERSION,
    REQUIRED_SCHEMA_VERSION,
)
from engines.interpretation_engine.knowledge.composition_context import COMPOSITION_VERSION
from engines.interpretation_engine.pipeline.diagnostics import InterpretationContractViolationError
from engines.interpretation_engine.pipeline.stage_registry import InterpretationStageRecord

REQUIRED_ANALYSIS_PIPELINE_VERSION = "2.0.0"
REQUIRED_DECISION_PIPELINE_VERSION = "1.0.0"
REQUIRED_LUCK_PIPELINE_VERSION = "1.0.0"

DEFAULT_VERSION_CONSTRAINTS: dict[str, str] = {
    "canonical_analysis_pipeline": "==2.0.0",
    "canonical_decision_pipeline": "==1.0.0",
    "canonical_luck_pipeline": "==1.0.0",
    "interpretation_foundation": "==1.0.0",
    "knowledge_selection_engine": "==1.0.0",
    "interpretation_composition_engine": "==1.0.0",
}


def parse_semver(value: str) -> tuple[int, int, int]:
    """Parse a dotted major.minor.patch version string."""
    parts = value.split(".")
    if len(parts) < 3:
        raise ValueError(f"invalid_semver:{value}")
    try:
        return int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError as exc:
        raise ValueError(f"invalid_semver:{value}") from exc


def satisfies_version_constraint(version: str, constraint: str) -> bool:
    """Return True when version satisfies a simple SemVer constraint."""
    version_tuple = parse_semver(version)
    text = constraint.strip()
    if text.startswith("^"):
        base = parse_semver(text[1:])
        return version_tuple >= base and version_tuple[0] == base[0]
    if text.startswith(">="):
        return version_tuple >= parse_semver(text[2:].strip())
    if text.startswith("=="):
        return version_tuple == parse_semver(text[2:].strip())
    return version_tuple == parse_semver(text)


class InterpretationPackageContractVerifier:
    """Validate component version, schema, dependencies, and published I/O."""

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

    def verify_foundation_component(self, *, interpretation_version: str) -> None:
        """Verify IE-1 foundation contract and schema."""
        if self._required_schema_version != REQUIRED_SCHEMA_VERSION:
            raise InterpretationContractViolationError(
                f"schema_incompatible:{self._required_schema_version}"
            )
        constraint = self._constraints.get("interpretation_foundation", "==1.0.0")
        if not satisfies_version_constraint(interpretation_version, constraint):
            raise InterpretationContractViolationError(
                f"version_incompatible:interpretation_foundation:{interpretation_version}:{constraint}"
            )
        contract = interpretation_foundation_contract()
        if contract["interpretation_version"] != INTERPRETATION_VERSION:
            raise InterpretationContractViolationError("foundation_contract_version_mismatch")
        if contract["text_generation"] or contract["reports"] or contract["ai"]:
            raise InterpretationContractViolationError("foundation_contract_forbids_text")

    def verify_knowledge_component(
        self,
        *,
        knowledge_version: str,
        ax2_version: str,
        ax3_version: str,
        ax4_version: str,
    ) -> None:
        """Verify IE-2 and upstream pipeline versions."""
        constraint = self._constraints.get("knowledge_selection_engine", "==1.0.0")
        if not satisfies_version_constraint(knowledge_version, constraint):
            raise InterpretationContractViolationError(
                f"version_incompatible:knowledge_selection:{knowledge_version}:{constraint}"
            )
        self._verify_upstream_versions(ax2_version, ax3_version, ax4_version)
        if knowledge_version != COMPOSITION_VERSION:
            raise InterpretationContractViolationError(
                f"knowledge_version_incompatible:{knowledge_version}"
            )

    def verify_composition_component(
        self,
        *,
        composition_version: str,
        ax2_version: str,
        ax3_version: str,
        ax4_version: str,
    ) -> None:
        """Verify IE-3 and upstream pipeline versions."""
        constraint = self._constraints.get("interpretation_composition_engine", "==1.0.0")
        if not satisfies_version_constraint(composition_version, constraint):
            raise InterpretationContractViolationError(
                f"version_incompatible:composition:{composition_version}:{constraint}"
            )
        self._verify_upstream_versions(ax2_version, ax3_version, ax4_version)
        if composition_version != ASSEMBLY_VERSION:
            raise InterpretationContractViolationError(
                f"composition_version_incompatible:{composition_version}"
            )

    def verify_payload(self, payload: Mapping[str, Any], stage: InterpretationStageRecord) -> None:
        """Require declared published outputs to be present."""
        missing = [name for name in stage.published_outputs if name not in payload]
        if missing:
            raise InterpretationContractViolationError(
                f"missing_published_outputs:{stage.stage_id}:{','.join(missing)}"
            )
        extra = [name for name in payload if name not in stage.published_outputs and name != "status"]
        if extra:
            raise InterpretationContractViolationError(
                f"undeclared_outputs:{stage.stage_id}:{','.join(sorted(extra))}"
            )

    def _verify_upstream_versions(self, ax2_version: str, ax3_version: str, ax4_version: str) -> None:
        checks = (
            ("canonical_analysis_pipeline", ax2_version, REQUIRED_ANALYSIS_PIPELINE_VERSION),
            ("canonical_decision_pipeline", ax3_version, REQUIRED_DECISION_PIPELINE_VERSION),
            ("canonical_luck_pipeline", ax4_version, REQUIRED_LUCK_PIPELINE_VERSION),
        )
        for key, actual, expected_default in checks:
            constraint = self._constraints.get(key, f"=={expected_default}")
            if not actual or not satisfies_version_constraint(actual, constraint):
                raise InterpretationContractViolationError(
                    f"version_incompatible:{key}:{actual}:{constraint}"
                )
