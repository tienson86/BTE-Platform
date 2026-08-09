"""RE-1 Report module registry tests."""

from __future__ import annotations

import pytest

from engines.report_engine.exceptions.foundation_error import ReportFoundationError
from engines.report_engine.foundation_constants import CANONICAL_MODULE_ORDER
from engines.report_engine.registry.module_registry import ReportModuleRegistry


def test_all_modules_registered_none_implemented() -> None:
    """Nine future modules are catalogued and disabled."""
    registry = ReportModuleRegistry.default()
    assert registry.registered_ids() == CANONICAL_MODULE_ORDER
    assert registry.implemented_ids() == ()
    for module_id in CANONICAL_MODULE_ORDER:
        record = registry.get(module_id)
        assert record.implemented is False
        assert record.enabled is False
        assert record.status == "unimplemented"


def test_summary_depends_on_all_prior_modules() -> None:
    """Summary cannot resolve without the full catalog."""
    registry = ReportModuleRegistry.default()
    assert registry.resolve_order() == CANONICAL_MODULE_ORDER
    with pytest.raises(ReportFoundationError, match="missing_dependencies:summary"):
        registry.resolve_order(("summary",))


def test_registry_serialization_is_deterministic() -> None:
    """Registry list order is stable across instances."""
    first = ReportModuleRegistry.default().to_list()
    second = ReportModuleRegistry.default().to_list()
    assert first == second
    assert [item["module_id"] for item in first] == list(CANONICAL_MODULE_ORDER)
