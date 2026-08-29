"""UI-09R — ShenSha presentation joins approved knowledge, not a local dictionary."""

from __future__ import annotations

from applications.customer_portal.config import PORTAL_ROOT

_SRC = PORTAL_ROOT / "src"
_ADAPTER = _SRC / "screens" / "commercial_dashboard" / "shenShaAdapter.ts"
_CARD = _SRC / "screens" / "commercial_dashboard" / "ShenShaCard.tsx"
_KNOWLEDGE = _SRC / "adapters" / "shenShaApprovedKnowledge.ts"
_GRID = _SRC / "screens" / "commercial_dashboard" / "DashboardGrid.tsx"
_LUCK = _SRC / "screens" / "commercial_dashboard" / "LuckCard.tsx"


def test_sr6_no_local_card_dictionary() -> None:
    card = _CARD.read_text(encoding="utf-8")
    adapter = _ADAPTER.read_text(encoding="utf-8")
    knowledge = _KNOWLEDGE.read_text(encoding="utf-8")
    assert "approvedShenShaMeaning" in adapter
    assert "domains/shensha" in knowledge
    assert "approvedShenShaMeaning" not in card
    assert "Tốt" not in adapter
    assert "Hung" not in adapter


def test_sr12_grid_and_luck_untouched() -> None:
    grid = _GRID.read_text(encoding="utf-8")
    luck = _LUCK.read_text(encoding="utf-8")
    assert 'card.id === "shensha"' in grid
    assert 'card.id === "luck"' in grid
    assert "Đại Vận hiện tại" in luck
