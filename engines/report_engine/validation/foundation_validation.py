"""Report Foundation validation (RE-1). No rendering or export."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from engines.report_engine.context.canonical_report_context import (
    CanonicalReportContext,
    interpretation_pipeline_version,
)
from engines.report_engine.contracts.report_contracts import (
    ReportAsset,
    ReportBlock,
    ReportDocument,
    ReportSection,
    report_foundation_contract,
)
from engines.report_engine.exceptions.foundation_error import (
    ReportContractError,
    ReportDuplicateIdError,
    ReportFoundationError,
    ReportVersionError,
)
from engines.report_engine.foundation_constants import (
    CANONICAL_MODULE_ORDER,
    FORBIDDEN_RENDER_FIELDS,
    PUBLISHED_CONTRACTS,
    REPORT_VERSION,
    REQUIRED_ANALYSIS_PIPELINE_VERSION,
    REQUIRED_DECISION_PIPELINE_VERSION,
    REQUIRED_INTERPRETATION_PIPELINE_VERSION,
    REQUIRED_LUCK_PIPELINE_VERSION,
    REQUIRED_SCHEMA_VERSION,
)
from engines.report_engine.registry.module_registry import ReportModuleRegistry

CODE_CONTRACT_OK = "CONTRACT-OK"
CODE_CONTRACT_VIOLATION = "CONTRACT-VIOLATION"
CODE_SCHEMA_VIOLATION = "SCHEMA-VIOLATION"
CODE_DUP_ID = "DUP-ID"
CODE_REGISTRY_OK = "REGISTRY-OK"
CODE_DEP_VIOLATION = "DEP-VIOLATION"
CODE_VERSION_INCOMPATIBLE = "VERSION-INCOMPATIBLE"
CODE_CONTEXT_OK = "CONTEXT-OK"
CODE_CONTEXT_INTEGRITY = "CONTEXT-INTEGRITY"


@dataclass(slots=True)
class FoundationValidationReport:
    """Machine-readable foundation validation report."""

    success: bool
    codes: tuple[str, ...] = ()
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the validation report."""
        return {
            "success": self.success,
            "codes": list(self.codes),
            "details": dict(self.details),
        }


def _contains_forbidden(payload: Any, path: str = "") -> str | None:
    if isinstance(payload, Mapping):
        for key, value in payload.items():
            next_path = f"{path}.{key}" if path else str(key)
            if str(key).lower() in FORBIDDEN_RENDER_FIELDS:
                return next_path
            nested = _contains_forbidden(value, next_path)
            if nested:
                return nested
    elif isinstance(payload, (list, tuple)):
        for index, item in enumerate(payload):
            nested = _contains_forbidden(item, f"{path}[{index}]")
            if nested:
                return nested
    return None


def validate_schema(schema_version: str | None) -> None:
    """Admit only Knowledge schema 2.0.0."""
    if schema_version != REQUIRED_SCHEMA_VERSION:
        raise ReportVersionError(f"schema_incompatible:{schema_version}")


def validate_version_compatibility(
    *,
    report_version: str | None,
    analysis_pipeline_version: str | None,
    decision_pipeline_version: str | None,
    luck_pipeline_version: str | None,
    interpretation_pipeline_version: str | None,
) -> None:
    """Require RE-1 plus AX-2 / AX-3 / AX-4 / IX-1 versions."""
    if report_version != REPORT_VERSION:
        raise ReportVersionError(f"report_version_incompatible:{report_version}")
    if analysis_pipeline_version != REQUIRED_ANALYSIS_PIPELINE_VERSION:
        raise ReportVersionError(f"analysis_pipeline_incompatible:{analysis_pipeline_version}")
    if decision_pipeline_version != REQUIRED_DECISION_PIPELINE_VERSION:
        raise ReportVersionError(f"decision_pipeline_incompatible:{decision_pipeline_version}")
    if luck_pipeline_version != REQUIRED_LUCK_PIPELINE_VERSION:
        raise ReportVersionError(f"luck_pipeline_incompatible:{luck_pipeline_version}")
    if interpretation_pipeline_version != REQUIRED_INTERPRETATION_PIPELINE_VERSION:
        raise ReportVersionError(
            f"interpretation_pipeline_incompatible:{interpretation_pipeline_version}"
        )


def validate_duplicate_ids(identifiers: Sequence[str]) -> None:
    """Reject duplicate structural identifiers."""
    if len(identifiers) != len(set(identifiers)):
        raise ReportDuplicateIdError("duplicate_ids")


def validate_contracts() -> None:
    """Validate the published foundation contract surface."""
    contract = report_foundation_contract()
    missing = [name for name in PUBLISHED_CONTRACTS if name not in contract["contracts"]]
    if missing:
        raise ReportContractError(f"missing_contracts:{','.join(missing)}")
    if (
        contract["rendering"]
        or contract["export"]
        or contract["formatting"]
        or contract["pdf"]
        or contract["docx"]
        or contract["html"]
        or contract["markdown"]
    ):
        raise ReportContractError("rendering_not_allowed")
    if contract["modules"] != list(CANONICAL_MODULE_ORDER):
        raise ReportContractError("module_order_mismatch")


def validate_registry(registry: ReportModuleRegistry) -> None:
    """Validate registry identity, uniqueness, and dependency declarations."""
    ids = registry.registered_ids()
    validate_duplicate_ids(ids)
    if ids != CANONICAL_MODULE_ORDER:
        raise ReportContractError("registry_module_mismatch")
    if registry.implemented_ids():
        raise ReportContractError("modules_must_be_unimplemented")
    registry.resolve_order(ids)
    for module_id in ids:
        record = registry.get(module_id)
        missing = [dep for dep in record.dependencies if not registry.contains(dep)]
        if missing:
            raise ReportContractError(f"unknown_dependency:{module_id}:{','.join(missing)}")


def validate_context_integrity(context: CanonicalReportContext) -> None:
    """Validate sealed upstream snapshots and append-only isolation."""
    analysis = context.analysis_snapshot()
    decision = context.decision_snapshot()
    luck = context.luck_snapshot()
    interpretation = context.interpretation_snapshot()
    if not analysis or not decision or not luck or not interpretation:
        raise ReportContractError("context_snapshot_missing")
    forbidden = _contains_forbidden(context.to_dict())
    if forbidden:
        raise ReportContractError(f"forbidden_field:{forbidden}")
    validate_version_compatibility(
        report_version=context.report_version,
        analysis_pipeline_version=str(analysis.get("pipeline_version") or ""),
        decision_pipeline_version=str(decision.get("decision_pipeline_version") or ""),
        luck_pipeline_version=str(luck.get("luck_pipeline_version") or ""),
        interpretation_pipeline_version=interpretation_pipeline_version(interpretation),
    )
    validate_schema(REQUIRED_SCHEMA_VERSION)


def validate_structural_ids(
    *,
    documents: Sequence[ReportDocument] = (),
    sections: Sequence[ReportSection] = (),
    blocks: Sequence[ReportBlock] = (),
    assets: Sequence[ReportAsset] = (),
) -> None:
    """Validate structural contract identifiers are unique."""
    validate_duplicate_ids([item.document_id for item in documents])
    validate_duplicate_ids([item.section_id for item in sections])
    validate_duplicate_ids([item.block_id for item in blocks])
    validate_duplicate_ids([item.asset_id for item in assets])


def validate_foundation(
    *,
    context: CanonicalReportContext,
    registry: ReportModuleRegistry | None = None,
) -> FoundationValidationReport:
    """Run the full RE-1 validation suite. Failures become codes, not prose."""
    codes: list[str] = []
    details: dict[str, Any] = {}
    catalog = registry or ReportModuleRegistry.default()
    try:
        validate_contracts()
        codes.append(CODE_CONTRACT_OK)
        validate_schema(REQUIRED_SCHEMA_VERSION)
        validate_registry(catalog)
        codes.append(CODE_REGISTRY_OK)
        validate_context_integrity(context)
        codes.append(CODE_CONTEXT_OK)
        return FoundationValidationReport(success=True, codes=tuple(codes), details=details)
    except ReportDuplicateIdError as exc:
        codes.append(CODE_DUP_ID)
        details["error"] = str(exc)
    except ReportVersionError as exc:
        message = str(exc)
        if message.startswith("schema_"):
            codes.append(CODE_SCHEMA_VIOLATION)
        else:
            codes.append(CODE_VERSION_INCOMPATIBLE)
        details["error"] = message
    except ReportContractError as exc:
        message = str(exc)
        if "forbidden" in message or "snapshot" in message:
            codes.append(CODE_CONTEXT_INTEGRITY)
        elif "dependency" in message or "missing_dependencies" in message:
            codes.append(CODE_DEP_VIOLATION)
        else:
            codes.append(CODE_CONTRACT_VIOLATION)
        details["error"] = message
    except ReportFoundationError as exc:
        message = str(exc)
        if "missing_dependencies" in message or "dependency_order" in message:
            codes.append(CODE_DEP_VIOLATION)
        else:
            codes.append(CODE_CONTRACT_VIOLATION)
        details["error"] = message
    return FoundationValidationReport(success=False, codes=tuple(codes), details=details)
