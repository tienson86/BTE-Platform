"""Validators for UnifiedAnalysisContext V2."""

from __future__ import annotations

from dataclasses import fields
from typing import Any

from .models import (
    CONTEXT_CONTRACT,
    SCHEMA_VERSION,
    UnifiedAnalysisContext,
)

VALID_STRENGTH_LEVELS = frozenset({"strong", "weak", "balanced", "unknown"})
VALID_TEMPERATURE_TYPES = frozenset({"cold", "cool", "warm", "hot"})
VALID_TEMPERATURE_LEVELS = VALID_TEMPERATURE_TYPES


class ContextValidationError(Exception):
    """Raised when unified context validation fails."""


class ContextValidator:
    """Validate UnifiedAnalysisContext structure and values."""

    def validate(self, context: UnifiedAnalysisContext) -> dict[str, Any]:
        """Run validation and return report (raises on hard errors)."""
        errors: list[str] = []
        warnings: list[str] = []
        inventory: dict[str, list[str]] = {}

        for section_name in ("calendar", "bazi", "strength", "temperature", "pattern", "useful_god"):
            section = getattr(context, section_name)
            inventory[section_name] = [f.name for f in fields(section)]

        if context.metadata.schema_version != SCHEMA_VERSION:
            warnings.append(f"schema_version mismatch: {context.metadata.schema_version}")

        if not context.bazi.day_master:
            errors.append("missing bazi.day_master")

        if context.strength.level not in VALID_STRENGTH_LEVELS:
            warnings.append(f"invalid strength.level: {context.strength.level}")

        if context.temperature.type not in VALID_TEMPERATURE_TYPES:
            warnings.append(f"invalid temperature.type: {context.temperature.type}")

        if not 0.0 <= context.strength.score <= 1.0 and context.strength.success:
            warnings.append(f"strength.score out of range: {context.strength.score}")

        if not 0.0 <= context.temperature.score <= 1.0 and context.temperature.success:
            warnings.append(f"temperature.score out of range: {context.temperature.score}")

        duplicates = self._find_duplicate_paths(context)
        if duplicates:
            warnings.extend(f"duplicate field path: {d}" for d in duplicates)

        report = {
            "valid": not errors,
            "errors": errors,
            "warnings": warnings,
            "field_inventory": inventory,
            "duplicate_fields": duplicates,
            "schema_version": SCHEMA_VERSION,
            "contract": CONTEXT_CONTRACT,
        }
        context.metadata.validation = report
        if errors:
            raise ContextValidationError("; ".join(errors))
        return report

    @staticmethod
    def _find_duplicate_paths(context: UnifiedAnalysisContext) -> list[str]:
        """Detect duplicate normalized keys across sections."""
        seen: dict[str, str] = {}
        duplicates: list[str] = []
        for section_name in ("strength", "temperature", "pattern", "useful_god"):
            section = getattr(context, section_name)
            for f in fields(section):
                key = f"{section_name}.{f.name}"
                canonical = f.name
                if canonical in seen and seen[canonical] != section_name:
                    duplicates.append(key)
                seen[canonical] = section_name
        return duplicates
