"""RE-3 renderer registry tests."""

from __future__ import annotations

import pytest

from engines.report_engine.rendering.renderer_registry import (
    ACTIVE_RENDERERS,
    FUTURE_RENDERERS,
    RendererRegistry,
)
from engines.report_engine.rendering.rendering_context import RenderingError
from engines.report_engine.rendering.validation import validate_registry


def test_registry_enables_core_renderers_and_disables_future() -> None:
    """PDF/DOCX/HTML/Markdown/JSON are enabled. xlsx/pptx stay disabled."""
    registry = RendererRegistry.default()
    assert registry.enabled_ids() == ACTIVE_RENDERERS
    assert registry.disabled_ids() == FUTURE_RENDERERS
    validate_registry(registry)
    for renderer_id in ACTIVE_RENDERERS:
        record = registry.get(renderer_id)
        assert record.enabled is True
        assert record.deterministic is True
        assert record.mime_type
    with pytest.raises(RenderingError, match="renderer_disabled:pptx"):
        registry.require_enabled("pptx")
