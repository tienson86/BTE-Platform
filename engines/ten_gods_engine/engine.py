"""Ten Gods Core Engine public facade."""

from __future__ import annotations

from engines.ten_gods_engine.calculator import PillarInput, TenGodsCalculator
from engines.ten_gods_engine.models import TenGodsResult


class TenGodsEngine:
    """Canonical Ten Gods Core Engine."""

    def __init__(self, *, calculator: TenGodsCalculator | None = None) -> None:
        self._calculator = calculator or TenGodsCalculator()

    def calculate(
        self,
        *,
        day_master: str,
        pillars: dict[str, dict[str, str]],
        case_id: str | None = None,
    ) -> TenGodsResult:
        """Calculate Ten Gods from four pillars and day master."""
        parsed = {
            pillar: PillarInput(
                stem=str(values["stem"]),
                branch=str(values["branch"]),
            )
            for pillar, values in pillars.items()
        }
        return self._calculator.calculate(
            day_master=day_master,
            pillars=parsed,
            case_id=case_id,
        )

    def calculate_from_stems(
        self,
        *,
        day_master: str,
        year_stem: str,
        year_branch: str,
        month_stem: str,
        month_branch: str,
        day_stem: str,
        day_branch: str,
        hour_stem: str,
        hour_branch: str,
        case_id: str | None = None,
    ) -> TenGodsResult:
        """Convenience API for explicit pillar stems and branches."""
        return self.calculate(
            day_master=day_master,
            pillars={
                "year": {"stem": year_stem, "branch": year_branch},
                "month": {"stem": month_stem, "branch": month_branch},
                "day": {"stem": day_stem, "branch": day_branch},
                "hour": {"stem": hour_stem, "branch": hour_branch},
            },
            case_id=case_id,
        )
