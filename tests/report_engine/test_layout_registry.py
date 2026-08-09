"""RE-2 layout registry and validation tests."""

from __future__ import annotations

import pytest

from engines.report_engine.layout.block_builder import LayoutBlock
from engines.report_engine.layout.layout_registry import CANONICAL_STAGE_ORDER, LayoutRegistry
from engines.report_engine.layout.layout_result import (
    DIAG_BLOCK_DUPLICATE,
    DIAG_LAYOUT_VIOLATION,
    DIAG_SECTION_DUPLICATE,
    DIAG_THEME_VIOLATION,
)
from engines.report_engine.layout.section_builder import LayoutSection
from engines.report_engine.layout.theme_resolver import ThemeResolution
from engines.report_engine.layout.validation import (
    validate_block_hierarchy,
    validate_registry,
    validate_section_integrity,
    validate_theme,
)


def test_registry_is_complete_and_deterministic() -> None:
    """Eight layout stages are registered, enabled, and ordered."""
    registry = LayoutRegistry.default()
    assert registry.registered_ids() == CANONICAL_STAGE_ORDER
    assert registry.resolve_order() == CANONICAL_STAGE_ORDER
    validate_registry(registry)
    for stage_id in CANONICAL_STAGE_ORDER:
        record = registry.get(stage_id)
        assert record.enabled is True
        assert record.deterministic is True


def test_validation_detects_duplicates_and_theme_violations() -> None:
    """Section/block duplicates and illegal theme ids fail closed."""
    section = LayoutSection(
        section_id="LSEC-cover",
        module_id="cover",
        source_section_ids=(),
        page_id="PAGE-cover",
        sequence=0,
        status="assembled",
    )
    with pytest.raises(ValueError, match=DIAG_SECTION_DUPLICATE):
        validate_section_integrity((section, section))
    block = LayoutBlock(
        block_id="BLK-cover-text-0",
        section_id="LSEC-cover",
        block_type="text",
        source_refs=("title.report",),
        asset_ids=(),
        sequence=0,
        status="assembled",
    )
    with pytest.raises(ValueError, match=DIAG_BLOCK_DUPLICATE):
        validate_block_hierarchy((block, block), (section,))
    bad_theme = ThemeResolution(
        theme_id="other.theme",
        palette_id="bte.report.palette.foundation.v1",
        spacing_id="bte.report.spacing.foundation.v1",
        typography_id="bte.report.typography.foundation.v1",
        icon_set_id="bte.report.icons.foundation.v1",
        status="resolved",
    )
    with pytest.raises(ValueError, match=DIAG_THEME_VIOLATION):
        validate_theme(bad_theme)
    assert DIAG_LAYOUT_VIOLATION == "LAYOUT-VIOLATION"
