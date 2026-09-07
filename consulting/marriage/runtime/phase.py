"""B02 runtime constants. Does not change TV1-B01 identity constants."""

from __future__ import annotations

from typing import Final

BUILD_PHASE_B02: Final[str] = "TV1-B02"
CANONICAL_STOP_STAGE: Final[str] = "luck"
DEFAULT_CANONICAL_TIMEZONE: Final[str] = "Asia/Ho_Chi_Minh"
UNBOUND_VERSION: Final[str] = "unbound"

B02_PIPELINE_STAGES: Final[tuple[str, ...]] = (
    "request_validation",
    "birth_input_normalization",
    "canonical_analysis_a",
    "canonical_analysis_b",
    "canonical_contract_validation",
    "snapshot_builder",
)

QUALITY_FLAG_COUNT: Final[int] = 4
