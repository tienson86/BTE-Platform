"""PACK 06 Date Selection report exceptions."""

from __future__ import annotations


class DateSelectionReportError(Exception):
    """Base error for Date Selection report foundation."""


class DateSelectionReportValidationError(DateSelectionReportError):
    """SearchResult or ReportModel failed integrity validation."""


class DateSelectionReportTemplateError(DateSelectionReportError):
    """Presentation or template structure failed validation."""
