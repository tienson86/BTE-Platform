"""Consulting Language Pack exceptions. Schema and catalog only."""

from __future__ import annotations


class LanguagePackError(Exception):
    """Base Language Pack error."""


class LanguageCatalogError(LanguagePackError):
    """YAML catalog failed schema or uniqueness rules."""


class LanguageSelectionError(LanguagePackError):
    """Variant selection failed for a known entry."""


class LanguagePackNotIntegratedError(LanguagePackError):
    """Live TV-01 must not consume Language Pack in LANG-01."""
