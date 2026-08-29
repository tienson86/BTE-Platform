"""UI-03R2 Tứ Trụ short Nạp âm — copy-only identity binding, TuTruPanel unchanged."""

from __future__ import annotations

from applications.customer_portal.config import PORTAL_ROOT

_SRC = PORTAL_ROOT / "src"
_ADAPTER = _SRC / "screens" / "commercial_dashboard" / "adapter.ts"
_FOUR = _SRC / "screens" / "commercial_dashboard" / "FourPillars.tsx"
_BAZI = _SRC / "screens" / "commercial_dashboard" / "baziAdapter.ts"
_PANEL = _SRC / "components" / "canonical" / "TuTruPanel.tsx"
_DATE = _SRC / "features" / "date_selection" / "components.tsx"


def test_r2_identity_uses_published_nayin_element() -> None:
    adapter = _ADAPTER.read_text(encoding="utf-8")
    assert "nayin_element" in adapter
    assert "baziPillar?.nap_am" not in adapter
    assert "engines." not in adapter


def test_r2_bazi_keeps_full_nap_am() -> None:
    bazi = _BAZI.read_text(encoding="utf-8")
    assert "nap_am" in bazi


def test_r2_shared_tu_tru_panel_and_good_date_unchanged() -> None:
    panel = _PANEL.read_text(encoding="utf-8")
    date_source = _DATE.read_text(encoding="utf-8")
    four = _FOUR.read_text(encoding="utf-8")
    assert "TuTruPanel" in four
    assert "nayin_element" in date_source
    assert "nayin_lookup" not in panel
    assert "NAP_AM_MAP" not in panel
