"""
BTE Platform - Engine Registration.

Đăng ký toàn bộ Engine vào Engine Registry.

File này chỉ nên được gọi một lần khi khởi động hệ thống.
"""

from __future__ import annotations

from .registry import registry

# ==========================================================
# Calendar
# ==========================================================

from engines.calendar_engine.engine import CalendarEngine

# ==========================================================
# Bazi
# ==========================================================

from engines.bazi_engine.engine import BaziEngine

# ==========================================================
# Score
# ==========================================================

from engines.score_engine.engine import ScoreEngine

# ==========================================================
# Pattern
# ==========================================================

from engines.pattern_engine.engine import PatternEngine

# ==========================================================
# Interpretation
# ==========================================================

from engines.interpretation_engine.engine import (
    InterpretationEngine,
)

# ==========================================================
# Report
# ==========================================================

from engines.report_engine.engine import ReportEngine


def register_all_engines() -> None:
    """
    Đăng ký toàn bộ Engine của BTE Platform.

    Hàm này có thể được gọi nhiều lần.
    Những Engine đã tồn tại sẽ được bỏ qua.
    """

    engines = [

        (
            "calendar",
            CalendarEngine,
            "Calendar Engine",
            "Tính lịch âm dương, tiết khí, can chi."
        ),

        (
            "bazi",
            BaziEngine,
            "Bazi Engine",
            "Lập Tứ Trụ Bát Tự."
        ),

        (
            "score",
            ScoreEngine,
            "Score Engine",
            "Tính điểm vượng suy và ngũ hành."
        ),

        (
            "pattern",
            PatternEngine,
            "Pattern Engine",
            "Xác định cách cục và mô hình lá số."
        ),

        (
            "interpretation",
            InterpretationEngine,
            "Interpretation Engine",
            "Diễn giải lá số theo Rule Database."
        ),

        (
            "report",
            ReportEngine,
            "Report Engine",
            "Xuất báo cáo PDF, HTML và JSON."
        ),

    ]

    for (
        name,
        engine_class,
        title,
        description,
    ) in engines:

        if registry.exists(name):
            continue

        registry.register(
            name=name,
            engine_class=engine_class,
            version="1.0.0",
            description=description,
            singleton=True,
            metadata={
                "title": title,
                "module": engine_class.__module__,
                "class": engine_class.__name__,
            },
        )


def unregister_all_engines() -> None:
    """
    Gỡ toàn bộ Engine khỏi Registry.
    """

    for name in list(registry.list()):
        registry.unregister(name)


def registered_engines() -> list[str]:
    """
    Danh sách Engine đã đăng ký.
    """

    return registry.list()


def is_registered(name: str) -> bool:
    """
    Kiểm tra Engine đã được đăng ký hay chưa.
    """

    return registry.exists(name)


def engine_count() -> int:
    """
    Số lượng Engine đã đăng ký.
    """

    return registry.count()
