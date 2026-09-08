"""Number Energy Engine facade (Bát Cực Linh Số / Năng lượng số)."""

from __future__ import annotations

from engines.number_energy.service import NumberEnergyService
from engines.number_energy.types import NumberEnergyResult, PurposeContext


class NumberEnergyEngine:
    """Thin engine facade for number-energy analysis."""

    def __init__(self, service: NumberEnergyService | None = None) -> None:
        self._service = service or NumberEnergyService()

    def analyze(
        self,
        number: str,
        *,
        purpose_context: str = PurposeContext.GENERIC_NUMBER.value,
    ) -> NumberEnergyResult:
        """Analyze a digit string and return a ``NumberEnergyResult``."""
        return self._service.analyze(number, purpose_context=purpose_context)

    def calculate(
        self,
        number: str,
        *,
        purpose_context: str = PurposeContext.GENERIC_NUMBER.value,
    ) -> NumberEnergyResult:
        """Alias of ``analyze`` for orchestrator-style callers."""
        return self.analyze(number, purpose_context=purpose_context)
