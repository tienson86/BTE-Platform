"""G2-03 — commercial narrative must not read frozen-obsolete analytical fields."""

from __future__ import annotations

from engines.commercial_knowledge.commercial_presentation import commercialize_customer_text
from engines.commercial_knowledge.signal_projection import project_analysis_signals


def test_g2_03_useful_god_ignores_pattern_dung_than() -> None:
    """Customer Dụng comes from useful_god, never pattern.dung_than."""
    signals = project_analysis_signals(
        {
            "pattern": {"dung_than": "Thổ · Mậu · Thiên Ấn", "ky_than": "Hỏa"},
            "useful_god": {
                "useful_display": "Thủy · Nhâm · Thực Thần",
                "unfavorable_display": "Kim · Canh · Tỷ Kiên",
            },
            "strength": {"strength_level": "strong", "strength_score": 1.0},
        }
    )
    assert signals["useful_god"] == "Thủy · Nhâm · Thực Thần"
    assert "Thiên Ấn" not in signals["useful_god"]
    assert signals["weakness_signal_label"] == "Kim · Canh · Tỷ Kiên"


def test_g2_03_canonical_strength_score_is_not_score_engine() -> None:
    """0–1 Strength score must not be read as 0–100 Score Engine."""
    signals = project_analysis_signals(
        {
            "strength": {"strength_level": "strong", "strength_score": 1.0},
            "useful_god": {"useful_display": "Thủy · Nhâm · Thực Thần"},
        }
    )
    assert signals["strength_score_favorable"] is True
    assert signals["weakness_frame"] != "thin"
    assert "mỏng lực" not in str(signals["strength_band_label"])


def test_g2_03_balanced_score_is_not_thin() -> None:
    signals = project_analysis_signals(
        {
            "strength": {"strength_level": "balanced", "strength_score": 0.51},
            "useful_god": {"useful_display": "Mộc · Ất · Chính Tài"},
        }
    )
    assert signals["weakness_frame"] != "thin"
    assert signals["strength_band_label"] == "đang cân bằng"


def test_g2_03_presentation_does_not_call_strong_chart_thin() -> None:
    signals = project_analysis_signals(
        {"strength": {"strength_level": "strong", "strength_score": 1.0}}
    )
    text = commercialize_customer_text(
        "Môi trường gắn mức lực đang mỏng lực. Giữ biên nếu đang mỏng lực.",
        signals,
    )
    assert "mỏng lực" not in text
    assert "Chưa có Hỷ thần bổ trợ riêng" not in commercialize_customer_text(
        "Môi trường thuận: Chưa có Hỷ thần bổ trợ riêng."
    )
