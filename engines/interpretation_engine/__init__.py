"""
Interpretation Engine Package
============================

Đóng gói module Interpretation Engine.

Export các thành phần chính:

- InterpretationEngine
- InterpretationBuilder
- SentenceGenerator
- Formatter


Sử dụng:

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

    "format_result"

]
