"""
Engine Result

Chuẩn hóa kết quả trả về của mọi Engine trong BTE Platform.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


# ==========================================================
# Engine Status
# ==========================================================

class EngineStatus(str, Enum):
    """Trạng thái thực thi của Engine."""

    SUCCESS = "success"
    WARNING = "warning"
    FAILED = "failed"
    SKIPPED = "skipped"


# ==========================================================
# Execution Metrics
# ==========================================================

@dataclass(slots=True)
class ExecutionMetrics:
    """Thông tin thống kê quá trình thực thi."""

    started_at: datetime = field(default_factory=datetime.utcnow)

    finished_at: datetime | None = None

    execution_time_ms: float = 0.0

    memory_usage_mb: float | None = None

    cpu_time_ms: float | None = None


# ==========================================================
# Engine Warning
# ==========================================================

@dataclass(slots=True)
class EngineWarning:
    """Thông tin cảnh báo."""

    code: str

    message: str

    detail: Any | None = None


# ==========================================================
# Engine Result
# ==========================================================

@dataclass(slots=True)
class EngineResult:
    """
    Kết quả chuẩn của một Engine.
    """

    engine: str

    status: EngineStatus = EngineStatus.SUCCESS

    data: dict[str, Any] = field(default_factory=dict)

    metrics: ExecutionMetrics = field(
        default_factory=ExecutionMetrics
    )

    warnings: list[EngineWarning] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    # ======================================================
    # Warning
    # ======================================================

    def add_warning(
        self,
        code: str,
        message: str,
        detail: Any | None = None,
    ) -> None:

        self.warnings.append(
            EngineWarning(
                code=code,
                message=message,
                detail=detail,
            )
        )

        if self.status == EngineStatus.SUCCESS:
            self.status = EngineStatus.WARNING

    # ======================================================
    # Error
    # ======================================================

    def add_error(
        self,
        message: str,
    ) -> None:

        self.errors.append(message)

        self.status = EngineStatus.FAILED

    # ======================================================
    # Metadata
    # ======================================================

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.metadata[key] = value

    # ======================================================
    # Helpers
    # ======================================================

    @property
    def ok(self) -> bool:

        return self.status in (
            EngineStatus.SUCCESS,
            EngineStatus.WARNING,
        )

    @property
    def failed(self) -> bool:

        return self.status == EngineStatus.FAILED

    # ======================================================
    # Factory
    # ======================================================

    @classmethod
    def success(
        cls,
        engine: str,
        data: dict[str, Any] | None = None,
    ) -> "EngineResult":

        return cls(
            engine=engine,
            status=EngineStatus.SUCCESS,
            data=data or {},
        )

    @classmethod
    def failed_result(
        cls,
        engine: str,
        message: str,
    ) -> "EngineResult":

        result = cls(
            engine=engine,
            status=EngineStatus.FAILED,
        )

        result.add_error(message)

        return result

    @classmethod
    def skipped(
        cls,
        engine: str,
    ) -> "EngineResult":

        return cls(
            engine=engine,
            status=EngineStatus.SKIPPED,
        )

    # ======================================================
    # Serialization
    # ======================================================

    def to_dict(self) -> dict[str, Any]:

        return {

            "engine": self.engine,

            "status": self.status.value,

            "data": self.data,

            "metrics": {

                "started_at": self.metrics.started_at.isoformat(),

                "finished_at": (
                    self.metrics.finished_at.isoformat()
                    if self.metrics.finished_at
                    else None
                ),

                "execution_time_ms": self.metrics.execution_time_ms,

                "memory_usage_mb": self.metrics.memory_usage_mb,

                "cpu_time_ms": self.metrics.cpu_time_ms,

            },

            "warnings": [

                {

                    "code": w.code,

                    "message": w.message,

                    "detail": w.detail,

                }

                for w in self.warnings

            ],

            "errors": self.errors,

            "metadata": self.metadata,

        }
