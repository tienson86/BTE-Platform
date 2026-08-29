"""UI-10R — Luck Card presentation whitelist, no runtime dump."""

from __future__ import annotations

from applications.customer_portal.config import PORTAL_ROOT

_SRC = PORTAL_ROOT / "src" / "screens" / "commercial_dashboard"
_ADAPTER = _SRC / "luckAdapter.ts"
_CARD = _SRC / "LuckCard.tsx"
_GRID = _SRC / "DashboardGrid.tsx"


def test_lr12_no_engine_and_no_object_dump() -> None:
    adapter = _ADAPTER.read_text(encoding="utf-8")
    card = _CARD.read_text(encoding="utf-8")
    for source in (adapter, card):
        assert "LuckEngine" not in source
        assert "engines/" not in source
        assert "JSON.stringify" not in source
        assert "Object.entries" not in source
    assert "luck_summary" not in adapter
    assert 'CUSTOMER_TREND_KEYS = ["customer_summary", "trend"]' in adapter
    assert "copyCycle" in adapter
    assert "...cycle" not in adapter


def test_lr_card_does_not_render_raw_trend_json() -> None:
    card = _CARD.read_text(encoding="utf-8")
    assert "publishTrend" in card
    assert "dayun_runtime" not in card


def test_dashboard_grid_unchanged_for_luck_slot() -> None:
    grid = _GRID.read_text(encoding="utf-8")
    assert 'card.id === "luck"' in grid
    assert 'card.id === "shensha"' in grid
    assert "SkeletonCard" in grid
