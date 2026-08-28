"""BTE Canonical Identity Layer.

Not an engine. Sits between Calendar/Bazi outputs and Presentation.

Sprint 03 publishes existing engine fields onto the identity contract.
Does not calculate missing domains.
"""

from engines.identity.assemble import (
    build_canonical_identity,
    canonical_identity_from_bazi,
    luck_payload_for_identity,
    merge_person_into_identity_payload,
)
from engines.identity.contract import IDENTITY_CONTRACT, UNPUBLISHED
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
    "IDENTITY_CONTRACT",
    "UNPUBLISHED",
    "build_canonical_identity",
    "canonical_identity_from_bazi",
    "luck_payload_for_identity",
    "four_pillar_identity_from_bazi",
    "four_pillar_identity_from_labels",
    "merge_person_into_identity_payload",
    "pillar_identity_from_ganzhi",
]
