"""Detect leftover engine language in customer-facing narrative text."""

from __future__ import annotations

import re
from functools import lru_cache

from engines.interpretation_engine.foundation.narrative.models import (
    NarrativeComposerResult,
)
from engines.interpretation_engine.foundation.narrative.translation.loader import (
    load_forbidden_terms,
)
from engines.interpretation_engine.foundation.narrative.translation.models import (
    ExpertTranslationError,
)


@lru_cache(maxsize=1)
def _compiled_forbidden() -> tuple[tuple[str, ...], tuple[re.Pattern[str], ...]]:
    """Compile forbidden phrases and regexes once."""
    terms = load_forbidden_terms()
    patterns = tuple(re.compile(item, flags=re.IGNORECASE) for item in terms.regex)
    return terms.phrases, patterns


def find_forbidden_terms(text: str) -> tuple[str, ...]:
    """Return forbidden engine/debug fragments found in customer text."""
    blob = str(text or "")
    if not blob.strip():
        return ()
    lowered = blob.casefold()
    phrases, patterns = _compiled_forbidden()
    hits: list[str] = []
    for phrase in phrases:
        if phrase.casefold() in lowered:
            hits.append(phrase)
    for pattern in patterns:
        match = pattern.search(blob)
        if match is not None:
            hits.append(match.group(0))
    return tuple(dict.fromkeys(hits))


def assert_customer_text_clean(text: str, *, source: str = "customer_text") -> None:
    """Fail when customer text still contains engine language."""
    hits = find_forbidden_terms(text)
    if hits:
        preview = "; ".join(hits[:8])
        raise ExpertTranslationError(
            f"{source} contains engine language: {preview}"
        )


def customer_narrative_blob(result: NarrativeComposerResult) -> str:
    """Join rendered sentence text only. Ignore internal ids."""
    return " ".join(
        sentence.text
        for section in result.sections
        for sentence in section.sentences
    )


def assert_customer_narrative_clean(result: NarrativeComposerResult) -> None:
    """Fail when composed customer sentences still leak engine language."""
    assert_customer_text_clean(
        customer_narrative_blob(result),
        source="narrative",
    )
