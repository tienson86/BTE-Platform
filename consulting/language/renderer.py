"""Language Pack renderer skeleton. Not bound to live TV-01 Narrative."""

from __future__ import annotations

from consulting.language.exceptions import LanguagePackNotIntegratedError
from consulting.language.models import LanguageEntry, SelectedWording


def render_for_live_tv01(_entry: LanguageEntry, _selected: SelectedWording) -> None:
    """Refuse live replacement. Integration is a later ticket."""
    raise LanguagePackNotIntegratedError(
        "LANG-01 skeleton does not replace TV-01 R02 customer wording"
    )
