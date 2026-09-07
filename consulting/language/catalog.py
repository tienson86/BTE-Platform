"""Language Pack catalog facade. Load + validate. No live TV-01 binding."""

from __future__ import annotations

from consulting.language.loader import load_marriage_catalog, load_schema
from consulting.language.models import LanguageCatalog, LanguageEntry
from consulting.language.validator import validate_catalog


def load_validated_marriage_catalog() -> LanguageCatalog:
    """Load marriage YAML and apply schema validation."""
    catalog = load_marriage_catalog()
    validate_catalog(catalog)
    return catalog


def get_entry(catalog: LanguageCatalog, language_key: str) -> LanguageEntry:
    """Return one entry by language_key."""
    return catalog.entries_by_key[language_key]


__all__ = ["load_schema", "load_validated_marriage_catalog", "get_entry"]
