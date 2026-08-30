"""Narrative V2 Commercial Communication public surface."""

from __future__ import annotations

from engines.narrative_v2.communication.communication_context import (
    ConsultingNarrative,
    ConsultingReference,
    StyledSegment,
)
from engines.narrative_v2.communication.communication_engine import CommunicationEngine
from engines.narrative_v2.communication.communication_errors import (
    CommunicationError,
    ConsultingStyleError,
    ConsultingStyleValidationError,
)
from engines.narrative_v2.communication.consulting_style import semantic_fingerprint
from engines.narrative_v2.communication.consulting_style_profile import (
    DEFAULT_PROFILE_ID,
    ConsultingStyleProfile,
    default_profile,
)
from engines.narrative_v2.communication.consulting_style_registry import (
    APPROVED_FRAMES,
    ConsultingStyleRegistry,
)
from engines.narrative_v2.communication.consulting_style_selector import ConsultingStyleSelector
from engines.narrative_v2.communication.consulting_style_validator import (
    ConsultingStyleValidationOutcome,
    ConsultingStyleValidator,
)

__all__ = [
    "APPROVED_FRAMES",
    "DEFAULT_PROFILE_ID",
    "CommunicationEngine",
    "CommunicationError",
    "ConsultingNarrative",
    "ConsultingReference",
    "ConsultingStyleError",
    "ConsultingStyleProfile",
    "ConsultingStyleRegistry",
    "ConsultingStyleSelector",
    "ConsultingStyleValidationError",
    "ConsultingStyleValidationOutcome",
    "ConsultingStyleValidator",
    "StyledSegment",
    "default_profile",
    "semantic_fingerprint",
]
