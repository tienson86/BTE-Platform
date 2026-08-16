"""Expert Translation Layer — machine reasoning to expert reasoning."""

from engines.interpretation_engine.foundation.narrative.translation.apply import (
    apply_expert_translation,
)
from engines.interpretation_engine.foundation.narrative.translation.loader import (
    load_confidence_bands,
    load_forbidden_terms,
    load_translation_rules,
)
from engines.interpretation_engine.foundation.narrative.translation.models import (
    TRANSLATION_SCOPES,
    ConfidenceBand,
    ExpertTranslationError,
    ForbiddenTermSet,
    TranslationRule,
)
from engines.interpretation_engine.foundation.narrative.translation.translator import (
    confidence_label,
    translate_text,
)
from engines.interpretation_engine.foundation.narrative.translation.validator import (
    assert_customer_narrative_clean,
    assert_customer_text_clean,
    find_forbidden_terms,
)

__all__ = [
    "TRANSLATION_SCOPES",
    "ConfidenceBand",
    "ExpertTranslationError",
    "ForbiddenTermSet",
    "TranslationRule",
    "apply_expert_translation",
    "assert_customer_narrative_clean",
    "assert_customer_text_clean",
    "confidence_label",
    "find_forbidden_terms",
    "load_confidence_bands",
    "load_forbidden_terms",
    "load_translation_rules",
    "translate_text",
]
