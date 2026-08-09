"""Verify report component contracts before pipeline execution."""

from __future__ import annotations

from typing import Any, Mapping

from engines.report_engine.contracts.report_contracts import report_foundation_contract
from engines.report_engine.foundation_constants import REPORT_VERSION, REQUIRED_SCHEMA_VERSION
from engines.report_engine.layout.layout_context import LAYOUT_VERSION
from engines.report_engine.pipeline.diagnostics import ReportContractViolationError
from engines.report_engine.pipeline.stage_registry import ReportStageRecord
from engines.report_engine.rendering.rendering_context import RENDER_VERSION

REQUIRED_ANALYSIS_PIPELINE_VERSION = "2.0.0"
REQUIRED_DECISION_PIPELINE_VERSION = "1.0.0"
REQUIRED_LUCK_PIPELINE_VERSION = "1.0.0"
REQUIRED_INTERPRETATION_PIPELINE_VERSION = "1.0.0"

DEFAULT_VERSION_CONSTRAINTS: dict[str, str] = {
    "canonical_analysis_pipeline": "==2.0.0",
    "canonical_decision_pipeline": "==1.0.0",
    "canonical_luck_pipeline": "==1.0.0",
    "canonical_interpretation_pipeline": "==1.0.0",
    "report_foundation": "==1.0.0",
    "report_layout_engine": "==1.0.0",
    "report_rendering_engine": "==1.0.0",
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


class ReportPackageContractVerifier:
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

    def verify_foundation_component(self, *, report_version: str) -> None:
        """Verify RE-1 foundation contract and schema."""
        if self._required_schema_version != REQUIRED_SCHEMA_VERSION:
            raise ReportContractViolationError(
                f"schema_incompatible:{self._required_schema_version}"
            )
        constraint = self._constraints.get("report_foundation", "==1.0.0")
        if not satisfies_version_constraint(report_version, constraint):
            raise ReportContractViolationError(
                f"version_incompatible:report_foundation:{report_version}:{constraint}"
            )
        contract = report_foundation_contract()
        if contract["report_version"] != REPORT_VERSION:
            raise ReportContractViolationError("foundation_contract_version_mismatch")
        if contract["rendering"] or contract["export"] or contract["pdf"]:
            raise ReportContractViolationError("foundation_contract_forbids_rendering")

    def verify_layout_component(
        self,
        *,
        layout_version: str,
        ax2_version: str,
        ax3_version: str,
        ax4_version: str,
        ix1_version: str,
    ) -> None:
        """Verify RE-2 and upstream pipeline versions."""
        constraint = self._constraints.get("report_layout_engine", "==1.0.0")
        if not satisfies_version_constraint(layout_version, constraint):
            raise ReportContractViolationError(
                f"version_incompatible:layout:{layout_version}:{constraint}"
            )
        if layout_version != LAYOUT_VERSION:
            raise ReportContractViolationError(f"layout_version_incompatible:{layout_version}")
        self._verify_upstream_versions(ax2_version, ax3_version, ax4_version, ix1_version)

    def verify_rendering_component(
        self,
        *,
        render_version: str,
        ax2_version: str,
        ax3_version: str,
        ax4_version: str,
        ix1_version: str,
    ) -> None:
        """Verify RE-3 and upstream pipeline versions."""
        constraint = self._constraints.get("report_rendering_engine", "==1.0.0")
        if not satisfies_version_constraint(render_version, constraint):
            raise ReportContractViolationError(
                f"version_incompatible:rendering:{render_version}:{constraint}"
            )
        if render_version != RENDER_VERSION:
            raise ReportContractViolationError(f"render_version_incompatible:{render_version}")
        self._verify_upstream_versions(ax2_version, ax3_version, ax4_version, ix1_version)

    def verify_payload(self, payload: Mapping[str, Any], stage: ReportStageRecord) -> None:
        """Require declared published outputs to be present."""
        missing = [name for name in stage.published_outputs if name not in payload]
        if missing:
            raise ReportContractViolationError(
                f"missing_published_outputs:{stage.stage_id}:{','.join(missing)}"
            )
        extra = [name for name in payload if name not in stage.published_outputs and name != "status"]
        if extra:
            raise ReportContractViolationError(
                f"undeclared_outputs:{stage.stage_id}:{','.join(sorted(extra))}"
            )

    def _verify_upstream_versions(
        self,
        ax2_version: str,
        ax3_version: str,
        ax4_version: str,
        ix1_version: str,
    ) -> None:
        checks = (
            ("canonical_analysis_pipeline", ax2_version, REQUIRED_ANALYSIS_PIPELINE_VERSION),
            ("canonical_decision_pipeline", ax3_version, REQUIRED_DECISION_PIPELINE_VERSION),
            ("canonical_luck_pipeline", ax4_version, REQUIRED_LUCK_PIPELINE_VERSION),
            (
                "canonical_interpretation_pipeline",
                ix1_version,
                REQUIRED_INTERPRETATION_PIPELINE_VERSION,
            ),
        )
        for key, actual, expected_default in checks:
            constraint = self._constraints.get(key, f"=={expected_default}")
            if not actual or not satisfies_version_constraint(actual, constraint):
                raise ReportContractViolationError(
                    f"version_incompatible:{key}:{actual}:{constraint}"
                )
