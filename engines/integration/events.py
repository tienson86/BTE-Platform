"""
BTE Platform - Integration Events.

Định nghĩa toàn bộ sự kiện sử dụng trong Pipeline.
Không sử dụng chuỗi trực tiếp trong mã nguồn.
"""

from __future__ import annotations


class PipelineEvents:
    """
    Các sự kiện chuẩn của Integration Pipeline.
    """

    # ======================================================
    # Pipeline
    # ======================================================

    PIPELINE_INITIALIZED = "pipeline.initialized"

    PIPELINE_STARTED = "pipeline.started"

    PIPELINE_FINISHED = "pipeline.finished"

    PIPELINE_FAILED = "pipeline.failed"

    PIPELINE_RESET = "pipeline.reset"

    # ======================================================
    # Stage
    # ======================================================

    STAGE_STARTED = "stage.started"

    STAGE_FINISHED = "stage.finished"

    STAGE_FAILED = "stage.failed"

    STAGE_SKIPPED = "stage.skipped"

    # ======================================================
    # Calendar
    # ======================================================

    CALENDAR_STARTED = "calendar.started"

    CALENDAR_COMPLETED = "calendar.completed"

    CALENDAR_FAILED = "calendar.failed"

    # ======================================================
    # Bazi
    # ======================================================

    BAZI_STARTED = "bazi.started"

    BAZI_COMPLETED = "bazi.completed"

    BAZI_FAILED = "bazi.failed"

    # ======================================================
    # Score
    # ======================================================

    SCORE_STARTED = "score.started"

    SCORE_COMPLETED = "score.completed"

    SCORE_FAILED = "score.failed"

    # ======================================================
    # Pattern
    # ======================================================

    PATTERN_STARTED = "pattern.started"

    PATTERN_COMPLETED = "pattern.completed"

    PATTERN_FAILED = "pattern.failed"

    # ======================================================
    # Interpretation
    # ======================================================

    INTERPRETATION_STARTED = "interpretation.started"

    INTERPRETATION_COMPLETED = "interpretation.completed"

    INTERPRETATION_FAILED = "interpretation.failed"

    # ======================================================
    # Report
    # ======================================================

    REPORT_STARTED = "report.started"

    REPORT_COMPLETED = "report.completed"

    REPORT_FAILED = "report.failed"

    # ======================================================
    # Validation
    # ======================================================

    VALIDATION_STARTED = "validation.started"

    VALIDATION_COMPLETED = "validation.completed"

    VALIDATION_FAILED = "validation.failed"

    # ======================================================
    # Cache
    # ======================================================

    CACHE_HIT = "cache.hit"

    CACHE_MISS = "cache.miss"

    CACHE_CLEARED = "cache.cleared"

    # ======================================================
    # Logger
    # ======================================================

    LOG_INFO = "log.info"

    LOG_WARNING = "log.warning"

    LOG_ERROR = "log.error"

    LOG_DEBUG = "log.debug"

    @classmethod
    def all(cls) -> list[str]:
        """
        Trả về toàn bộ Event Name.
        """

        return [
            value
            for key, value in cls.__dict__.items()
            if key.isupper()
        ]

    @classmethod
    def exists(cls, event: str) -> bool:
        """
        Kiểm tra Event có tồn tại hay không.
        """

        return event in cls.all()
