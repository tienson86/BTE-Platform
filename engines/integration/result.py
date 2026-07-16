"""
Integration Result.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class IntegrationResult:

    success: bool = True

    failed_stage: Optional[str] = None

    message: str = ""

    calendar: Optional[Any] = None

    bazi: Optional[Any] = None

    score: Optional[Any] = None

    pattern: Optional[Any] = None

    interpretation: Optional[Any] = None

    report: Optional[Any] = None
