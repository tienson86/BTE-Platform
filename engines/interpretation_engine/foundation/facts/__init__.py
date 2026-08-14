"""Domain interpretation facts contracts (Sprint A — structured, not prose)."""

from engines.interpretation_engine.foundation.facts.strength import StrengthInterpretationFacts
from engines.interpretation_engine.foundation.facts.pattern import PatternInterpretationFacts
from engines.interpretation_engine.foundation.facts.useful_god import UsefulGodInterpretationFacts
from engines.interpretation_engine.foundation.facts.ten_gods import TenGodInterpretationFacts
from engines.interpretation_engine.foundation.facts.shensha import ShenShaInterpretationFacts
from engines.interpretation_engine.foundation.facts.luck import LuckInterpretationFacts
from engines.interpretation_engine.foundation.facts.temperature import TemperatureInterpretationFacts
from engines.interpretation_engine.foundation.facts.five_elements import FiveElementsInterpretationFacts

__all__ = [
    "StrengthInterpretationFacts",
    "PatternInterpretationFacts",
    "UsefulGodInterpretationFacts",
    "TenGodInterpretationFacts",
    "ShenShaInterpretationFacts",
    "LuckInterpretationFacts",
    "TemperatureInterpretationFacts",
    "FiveElementsInterpretationFacts",
]
