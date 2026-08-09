"""Deterministic Report module registry (RE-1). None implemented."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from engines.report_engine.exceptions.foundation_error import (
    ReportDuplicateIdError,
    ReportFoundationError,
)
from engines.report_engine.foundation_constants import (
    CANONICAL_MODULE_ORDER,
    MODULE_APPENDIX,
    MODULE_ANALYSIS,
    MODULE_CHART,
    MODULE_COVER,
    MODULE_DECISION,
    MODULE_INTERPRETATION,
    MODULE_LUCK,
    MODULE_OVERVIEW,
    MODULE_STATUS_REGISTERED,
    MODULE_STATUS_UNIMPLEMENTED,
    MODULE_SUMMARY,
    REPORT_VERSION,
)


@dataclass(frozen=True, slots=True)
class ReportModuleRecord:
    """Immutable catalog entry for one future report module."""

    module_id: str
    component: str
    version: str
    dependencies: tuple[str, ...]
    consumed_inputs: tuple[str, ...]
    published_outputs: tuple[str, ...]
    implemented: bool
    enabled: bool
    status: str

    def to_dict(self) -> dict[str, object]:
        """Serialize the module catalog record."""
        return {
            "module_id": self.module_id,
            "component": self.component,
            "version": self.version,
            "dependencies": list(self.dependencies),
            "consumed_inputs": list(self.consumed_inputs),
            "published_outputs": list(self.published_outputs),
            "implemented": self.implemented,
            "enabled": self.enabled,
            "status": self.status,
        }


def _record(
    module_id: str,
    *,
    dependencies: tuple[str, ...] = (),
) -> ReportModuleRecord:
    return ReportModuleRecord(
        module_id=module_id,
        component=f"report_{module_id}",
        version=REPORT_VERSION,
        dependencies=dependencies,
        consumed_inputs=(
            "canonical_analysis_result",
            "canonical_decision_result",
            "canonical_luck_result",
            "canonical_interpretation_result",
        ),
        published_outputs=(f"{module_id}_section",),
        implemented=False,
        enabled=False,
        status=MODULE_STATUS_UNIMPLEMENTED,
    )


def _default_records() -> tuple[ReportModuleRecord, ...]:
    after_cover = (MODULE_COVER,)
    return (
        _record(MODULE_COVER, dependencies=()),
        _record(MODULE_OVERVIEW, dependencies=after_cover),
        _record(MODULE_CHART, dependencies=after_cover),
        _record(MODULE_ANALYSIS, dependencies=after_cover),
        _record(MODULE_DECISION, dependencies=after_cover),
        _record(MODULE_LUCK, dependencies=after_cover),
        _record(MODULE_INTERPRETATION, dependencies=after_cover),
        _record(MODULE_APPENDIX, dependencies=after_cover),
        _record(
            MODULE_SUMMARY,
            dependencies=tuple(item for item in CANONICAL_MODULE_ORDER if item != MODULE_SUMMARY),
        ),
    )


class ReportModuleRegistry:
    """Read-only catalog of future Report modules. None are executable."""

    def __init__(self, records: Iterable[ReportModuleRecord] | None = None) -> None:
        """Load default or injected catalog records."""
        catalog = tuple(records) if records is not None else _default_records()
        ids = [item.module_id for item in catalog]
        if len(ids) != len(set(ids)):
            raise ReportDuplicateIdError("duplicate_module_id")
        by_id = {item.module_id: item for item in catalog}
        ordered = tuple(by_id[module_id] for module_id in CANONICAL_MODULE_ORDER if module_id in by_id)
        extra = tuple(item for item in catalog if item.module_id not in CANONICAL_MODULE_ORDER)
        self._records = ordered + extra
        self._by_id = {item.module_id: item for item in self._records}

    @classmethod
    def default(cls) -> ReportModuleRegistry:
        """Return the frozen default catalog."""
        return cls()

    def get(self, module_id: str) -> ReportModuleRecord:
        """Return one module record or raise."""
        try:
            return self._by_id[module_id]
        except KeyError as exc:
            raise ReportFoundationError(f"unknown_module:{module_id}") from exc

    def contains(self, module_id: str) -> bool:
        """Return True when the module is registered."""
        return module_id in self._by_id

    def implemented_ids(self) -> tuple[str, ...]:
        """Return implemented module identifiers. Empty in RE-1."""
        return tuple(item.module_id for item in self._records if item.implemented)

    def registered_ids(self) -> tuple[str, ...]:
        """Return all registered module identifiers in canonical order."""
        return tuple(item.module_id for item in self._records)

    def resolve_order(self, requested: Sequence[str] | None = None) -> tuple[str, ...]:
        """Return requested modules in dependency order. None are executable."""
        requested_ids = tuple(requested) if requested is not None else self.registered_ids()
        requested_set = set(requested_ids)
        unknown = requested_set - set(self._by_id)
        if unknown:
            raise ReportFoundationError(f"unknown_modules:{','.join(sorted(unknown))}")
        ordered: list[str] = []
        for module_id in CANONICAL_MODULE_ORDER:
            if module_id not in requested_set:
                continue
            record = self.get(module_id)
            missing = [dep for dep in record.dependencies if dep not in requested_set]
            if missing:
                raise ReportFoundationError(
                    f"missing_dependencies:{module_id}:{','.join(missing)}"
                )
            if any(dep not in ordered for dep in record.dependencies):
                raise ReportFoundationError(f"dependency_order:{module_id}")
            ordered.append(module_id)
        return tuple(ordered)

    def to_list(self) -> list[dict[str, object]]:
        """Serialize the full registry."""
        return [item.to_dict() for item in self._records]

    def status_summary(self) -> dict[str, str]:
        """Return module_id → registered/unimplemented status."""
        return {
            item.module_id: MODULE_STATUS_REGISTERED if not item.implemented else "implemented"
            for item in self._records
        }
