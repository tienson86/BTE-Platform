"""
Luck Engine provider and evaluator interfaces.

Sprint 4: provider protocols.
Sprint 4.2: single-responsibility evaluator protocols.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from .context import LuckContext
from .evaluation_models import (
    AttackEvaluation,
    StageEvaluation,
    StrengthEvaluation,
    SummaryEvaluation,
    SupportEvaluation,
)

MappingLike = Any


@runtime_checkable
class DayunProvider(Protocol):
    """Provide current / timeline Đại vận pillars."""

    def provide(
        self,
        *,
        calendar: Any,
        bazi: Any,
        rule_context: MappingLike | None = None,
    ) -> Any | None:
        """Return dayun payload or None when not computed."""
        ...


@runtime_checkable
class LiunianProvider(Protocol):
    """Provide Lưu niên (annual) luck."""

    def provide(
        self,
        *,
        calendar: Any,
        bazi: Any,
        dayun: Any | None = None,
    ) -> Any | None:
        """Return liunian payload or None when not computed."""
        ...


@runtime_checkable
class LiuyueProvider(Protocol):
    """Provide Lưu nguyệt (monthly) luck."""

    def provide(
        self,
        *,
        calendar: Any,
        bazi: Any,
        liunian: Any | None = None,
    ) -> Any | None:
        """Return liuyue payload or None when not computed."""
        ...


@runtime_checkable
class LiuriProvider(Protocol):
    """Provide Lưu nhật (daily) luck."""

    def provide(
        self,
        *,
        calendar: Any,
        bazi: Any,
        liuyue: Any | None = None,
    ) -> Any | None:
        """Return liuri payload or None when not computed."""
        ...


@runtime_checkable
class LiushiProvider(Protocol):
    """Provide Lưu thì (hourly) luck."""

    def provide(
        self,
        *,
        calendar: Any,
        bazi: Any,
        liuri: Any | None = None,
    ) -> Any | None:
        """Return liushi payload or None when not computed."""
        ...


@runtime_checkable
class SupportEvaluator(Protocol):
    """Evaluate support elements / level from luck pillars vs chart."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> SupportEvaluation:
        """Return immutable SupportEvaluation (UNKNOWN when no rule)."""
        ...


@runtime_checkable
class AttackEvaluator(Protocol):
    """Evaluate attack elements / level from luck pillars vs chart."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> AttackEvaluation:
        """Return immutable AttackEvaluation (UNKNOWN when no rule)."""
        ...


@runtime_checkable
class LuckStrengthEvaluator(Protocol):
    """Evaluate numeric luck strength when a business rule exists."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> StrengthEvaluation:
        """Return StrengthEvaluation (value NULL when no rule)."""
        ...


@runtime_checkable
class LuckStageEvaluator(Protocol):
    """Evaluate luck stage label when a business rule exists."""

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> StageEvaluation:
        """Return StageEvaluation (UNKNOWN when no rule)."""
        ...


@runtime_checkable
class LuckSummaryBuilder(Protocol):
    """Build structured luck summary from prior evaluation fields only."""

    def build(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> SummaryEvaluation:
        """Return SummaryEvaluation (summary NULL when no rule)."""
        ...


@runtime_checkable
class LuckEvaluator(Protocol):
    """
    Legacy aggregate evaluator (Sprint 4).

    Prefer Support / Attack / Strength / Stage / Summary pipeline (4.2).
    Kept for backward-compatible dependency injection.
    """

    def evaluate(
        self,
        *,
        luck: LuckContext,
        rule_context: MappingLike | None = None,
        score: Any | None = None,
        pattern: Any | None = None,
    ) -> LuckContext:
        """Return an updated LuckContext (new instance; no mutation)."""
        ...
