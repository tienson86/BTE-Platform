"""Logging catalogs and retention policy. No framework change."""

from applications.logging.logging_catalog import LOGGING_CATALOG
from applications.logging.retention_policy import RETENTION_RULES

__all__ = ["LOGGING_CATALOG", "RETENTION_RULES"]
