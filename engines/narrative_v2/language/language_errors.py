"""Language asset errors."""

from __future__ import annotations


class LanguageAssetError(Exception):
    """Base error for the runtime sentence library."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class SentenceAssetValidationError(LanguageAssetError):
    """Sentence asset failed contract validation."""
