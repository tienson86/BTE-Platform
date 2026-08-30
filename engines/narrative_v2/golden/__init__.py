"""Narrative V2 Golden Dataset — certified baselines only.

Does not modify Narrative, Knowledge, Presentation, or Pack05.
"""

from __future__ import annotations

from engines.narrative_v2.golden.golden_case import GOLDEN_SCHEMA_VERSION, STATUS_FROZEN, GoldenCase
from engines.narrative_v2.golden.golden_dataset import GoldenDataset
from engines.narrative_v2.golden.golden_errors import (
    GoldenEligibilityError,
    GoldenError,
    GoldenImmutabilityError,
    GoldenValidationError,
)
from engines.narrative_v2.golden.golden_history import GoldenHistory
from engines.narrative_v2.golden.golden_registry import GoldenRegistryEntry
from engines.narrative_v2.golden.golden_serializer import stable_hash
from engines.narrative_v2.golden.golden_validator import GoldenValidator

__all__ = [
    "GOLDEN_SCHEMA_VERSION",
    "STATUS_FROZEN",
    "GoldenCase",
    "GoldenDataset",
    "GoldenEligibilityError",
    "GoldenError",
    "GoldenHistory",
    "GoldenImmutabilityError",
    "GoldenRegistryEntry",
    "GoldenValidationError",
    "GoldenValidator",
    "stable_hash",
]
