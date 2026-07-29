"""
Engine Context

Định nghĩa ngữ cảnh (context) được truyền xuyên suốt
toàn bộ pipeline của BTE Platform.

Calendar
    ↓
Bazi
    ↓
Pattern
    ↓
Score
    ↓
Interpretation
    ↓
Report
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


# ==========================================================
# Engine Log
# ==========================================================

@dataclass(slots=True)
class EngineLog:
    """Thông tin log của Engine."""

    level: str
    message: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


# ==========================================================
# Engine Error
# ==========================================================

@dataclass(slots=True)
class EngineError:
    """Thông tin lỗi phát sinh trong quá trình xử lý."""

    engine: str
    message: str
    detail: Any | None = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


# ==========================================================
# Engine Metadata
# ==========================================================

@dataclass(slots=True)
class EngineMetadata:
    """
    Metadata của pipeline.
    """

    version: str = "1.0.0"

    language: str = "vi"

    timezone: str = "Asia/Ho_Chi_Minh"

    source: str = "BTE Platform"

    created_at: datetime = field(default_factory=datetime.utcnow)


# ==========================================================
# Engine Context
# ==========================================================

@dataclass(slots=True)
class EngineContext:
    """
    Context được truyền qua tất cả Engine.

    Mọi dữ liệu của pipeline đều nằm trong object này.
    """

    # =============================
    # Input
    # =============================

    input: dict[str, Any] = field(default_factory=dict)

    # =============================
    # Output của từng Engine
    # =============================

    calendar: dict[str, Any] = field(default_factory=dict)

    bazi: dict[str, Any] = field(default_factory=dict)

    pattern: dict[str, Any] = field(default_factory=dict)

    score: dict[str, Any] = field(default_factory=dict)

    interpretation: dict[str, Any] = field(default_factory=dict)

    report: dict[str, Any] = field(default_factory=dict)

    # =============================
    # Metadata
    # =============================

    metadata: EngineMetadata = field(
        default_factory=EngineMetadata
    )

    # =============================
    # Runtime
    # =============================

    logs: list[EngineLog] = field(default_factory=list)

    errors: list[EngineError] = field(default_factory=list)

    # ======================================================
    # Stage API
    # ======================================================

    def set_stage(
        self,
        stage: str,
        data: dict[str, Any],
    ) -> None:
        """
        Lưu dữ liệu của một Engine.
        """

        setattr(self, stage, data)

    def get_stage(
        self,
        stage: str,
    ) -> dict[str, Any]:

        return getattr(self, stage)

    # ======================================================
    # Log API
    # ======================================================

    def add_log(
        self,
        level: str,
        message: str,
    ) -> None:

        self.logs.append(
            EngineLog(
                level=level,
                message=message,
            )
        )

    # ======================================================
    # Error API
    # ======================================================

    def add_error(
        self,
        engine: str,
        message: str,
        detail: Any | None = None,
    ) -> None:

        self.errors.append(
            EngineError(
                engine=engine,
                message=message,
                detail=detail,
            )
        )

    # ======================================================
    # Helper
    # ======================================================

    def has_errors(self) -> bool:

        return len(self.errors) > 0

    def clear_logs(self) -> None:

        self.logs.clear()

    def clear_errors(self) -> None:

        self.errors.clear()

    # ======================================================
    # Serialization
    # ======================================================

    def to_dict(self) -> dict[str, Any]:

        return {
            "input": self.input,
            "calendar": self.calendar,
            "bazi": self.bazi,
            "pattern": self.pattern,
            "score": self.score,
            "interpretation": self.interpretation,
            "report": self.report,
            "metadata": {
                "version": self.metadata.version,
                "language": self.metadata.language,
                "timezone": self.metadata.timezone,
                "source": self.metadata.source,
                "created_at": self.metadata.created_at.isoformat(),
            },
            "logs": [
                {
                    "level": log.level,
                    "message": log.message,
                    "timestamp": log.timestamp.isoformat(),
                }
                for log in self.logs
            ],
            "errors": [
                {
                    "engine": err.engine,
                    "message": err.message,
                    "detail": err.detail,
                    "timestamp": err.timestamp.isoformat(),
                }
                for err in self.errors
            ],
        }
