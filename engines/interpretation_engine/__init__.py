"""
Interpretation Engine Package
============================

Đóng gói module Interpretation Engine.

Export các thành phần chính (legacy runtime):

- InterpretationEngine
- InterpretationBuilder
- SentenceGenerator
- Formatter

Pack 03 architecture skeleton lives in sibling packages
(``api/``, ``pipeline/``, ``contracts/``, ``interpreters/``, …).
See ``ARCHITECTURE_README.md``. Legacy public exports below are unchanged.

Pack 04 narrative path (AnalysisResult → NarrativeInterpretationResult):

from engines.interpretation_engine import InterpretationEngine
from engines.interpretation_engine.pack04 import NarrativeInterpretationResult

engine = InterpretationEngine()
result = engine.interpret_from_analysis(analysis_result)

Sử dụng (legacy):

from engines.interpretation_engine import InterpretationEngine

engine = InterpretationEngine()

result = engine.run(context)
"""


# =====================================================
# CORE ENGINE
# =====================================================


from .engine import (
    InterpretationEngine,
    analyze_bazi
)



# =====================================================
# BUILDER
# =====================================================


from .interpretation_builder import (
    InterpretationBuilder,
)

# Compatibility aliases — symbols live in legacy_builder
from .legacy_builder import (
    InterpretationResult,
    InterpretationSection,
)



# =====================================================
# SENTENCE
# =====================================================


from .sentence_generator import (
    SentenceGenerator,
    generate_sentences
)



# =====================================================
# FORMATTER
# =====================================================


from .formatter import (
    Formatter,
    format_result
)



# =====================================================
# PACK 04 (narrative) — lazy exports
# =====================================================


def __getattr__(name: str):
    """Lazy Pack 04 exports (avoid Score Engine import at package init)."""
    if name == "EngineResult":
        from .pack04 import EngineResult

        return EngineResult
    if name == "NarrativeInterpretationResult":
        from .pack04 import NarrativeInterpretationResult

        return NarrativeInterpretationResult
    if name == "Pack04Pipeline":
        from .pack04 import Pack04Pipeline

        return Pack04Pipeline
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")



# =====================================================
# PACKAGE VERSION
# =====================================================


__version__ = "1.0.0"




# =====================================================
# PUBLIC API
# =====================================================


__all__ = [

    # Engine

    "InterpretationEngine",

    "analyze_bazi",



    # Builder

    "InterpretationBuilder",

    "InterpretationResult",

    "InterpretationSection",



    # Sentence

    "SentenceGenerator",

    "generate_sentences",



    # Formatter

    "Formatter",

    "format_result",



    # Pack 04

    "EngineResult",

    "NarrativeInterpretationResult",

    "Pack04Pipeline",

]
