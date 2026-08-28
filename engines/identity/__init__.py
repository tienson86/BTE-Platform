"""BTE Canonical Identity Layer.

Not an engine. Sits between Calendar/Bazi outputs and Presentation.

Sprint 02 publishes person, calendar, four pillars, bone weight, luck,
and interpretation identifiers.
"""

from engines.identity.assemble import (
    build_canonical_identity,
    canonical_identity_from_bazi,
    merge_person_into_identity_payload,
)
from engines.identity.four_pillars import (
    four_pillar_identity_from_bazi,
    four_pillar_identity_from_labels,
    pillar_identity_from_ganzhi,
)
from engines.identity.models import (
    BoneWeightIdentity,
    CalendarIdentity,
    CanonicalIdentity,
    FourPillarIdentity,
    InterpretationIdentity,
    LuckIdentity,
    PersonIdentity,
    PillarIdentity,
)

__all__ = [
    "BoneWeightIdentity",
    "CalendarIdentity",
    "CanonicalIdentity",
    "FourPillarIdentity",
    "InterpretationIdentity",
    "LuckIdentity",
    "PersonIdentity",
    "PillarIdentity",
    "build_canonical_identity",
    "canonical_identity_from_bazi",
    "four_pillar_identity_from_bazi",
    "four_pillar_identity_from_labels",
    "merge_person_into_identity_payload",
    "pillar_identity_from_ganzhi",
]
