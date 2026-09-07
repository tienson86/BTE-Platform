"""TV-01 Marriage Consulting enumerations.

Canonical contract values from the data model. No scoring logic.
"""

from __future__ import annotations

from enum import Enum


class CanonicalGender(str, Enum):
    """Canonical gender contract reused by TV-01."""

    MALE = "male"
    FEMALE = "female"


class FiveElement(str, Enum):
    """Canonical five-element contract."""

    WOOD = "wood"
    FIRE = "fire"
    EARTH = "earth"
    METAL = "metal"
    WATER = "water"


class YinYang(str, Enum):
    """Canonical yin/yang contract."""

    YIN = "yin"
    YANG = "yang"


class MarriageDomain(str, Enum):
    """TV-01 evaluation domains."""

    OVERALL = "overall"
    FIVE_ELEMENTS = "five_elements"
    STEM_BRANCH = "stem_branch"
    TEN_GODS = "ten_gods"
    INTERACTION = "interaction"
    FINANCE = "finance"
    FAMILY = "family"
    CHILDREN = "children"
    LUCK = "luck"


class MarriageEvidenceType(str, Enum):
    """Logical evidence taxonomy. Not a scoring table."""

    ELEMENT_SUPPORT = "element_support"
    ELEMENT_CONFLICT = "element_conflict"
    USEFUL_GOD_SUPPORT = "useful_god_support"
    UNFAVORABLE_ACTIVATION = "unfavorable_activation"
    STEM_COMBINATION = "stem_combination"
    STEM_CONTROL = "stem_control"
    BRANCH_COMBINATION = "branch_combination"
    BRANCH_CLASH = "branch_clash"
    BRANCH_HARM = "branch_harm"
    BRANCH_PUNISHMENT = "branch_punishment"
    BRANCH_BREAK = "branch_break"
    BRANCH_MEETING = "branch_meeting"
    TEN_GOD_SUPPORT = "ten_god_support"
    TEN_GOD_PRESSURE = "ten_god_pressure"
    ROLE_COMPLEMENT = "role_complement"
    ROLE_CONFLICT = "role_conflict"
    PATTERN_SUPPORT = "pattern_support"
    PATTERN_DAMAGE = "pattern_damage"
    PATTERN_RESCUE = "pattern_rescue"
    LUCK_ALIGNMENT = "luck_alignment"
    LUCK_MISALIGNMENT = "luck_misalignment"
    SHEN_SHA_SUPPORT = "shen_sha_support"
    SHEN_SHA_RISK = "shen_sha_risk"
    FENG_SHUI_REFERENCE = "feng_shui_reference"


class EvidenceDirection(str, Enum):
    """Polarity of an evidence atom."""

    POSITIVE = "positive"
    NEGATIVE = "negative"
    MIXED = "mixed"
    NEUTRAL = "neutral"


class EvidenceSignificance(str, Enum):
    """Significance of an evidence atom. Independent of direction."""

    CRITICAL = "critical"
    MAJOR = "major"
    MODERATE = "moderate"
    MINOR = "minor"


class RelationshipSubject(str, Enum):
    """Direction of relationship impact."""

    A_TO_B = "A_TO_B"
    B_TO_A = "B_TO_A"
    MUTUAL = "MUTUAL"
    SHARED = "SHARED"


class PersonSide(str, Enum):
    """Person A or Person B in a consultation."""

    A = "A"
    B = "B"


class FindingType(str, Enum):
    """Finding semantic type."""

    STRENGTH = "strength"
    RISK = "risk"
    BOTTLENECK = "bottleneck"
    SUPPORT = "support"
    CONDITION = "condition"
    TIMING = "timing"
    MIXED = "mixed"


class FindingPriority(str, Enum):
    """Finding priority contract."""

    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    P5 = "P5"


class DomainGrade(str, Enum):
    """Compatibility grade contract."""

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"


class FindingRelation(str, Enum):
    """Cross-domain finding relation."""

    SUPPORTS = "supports"
    AMPLIFIES = "amplifies"
    REDUCES = "reduces"
    CONFLICTS = "conflicts"
    DEPENDS_ON = "depends_on"


class RecommendationType(str, Enum):
    """Recommendation action type."""

    REINFORCE_STRENGTH = "reinforce_strength"
    REDUCE_CONFLICT = "reduce_conflict"
    COMMUNICATION = "communication"
    FINANCIAL_STRUCTURE = "financial_structure"
    FAMILY_STRUCTURE = "family_structure"
    TIMING_AWARENESS = "timing_awareness"
    ROLE_BALANCE = "role_balance"
    GENERAL = "general"


class TimingStatus(str, Enum):
    """Timing period status. No extreme fortune wording."""

    SUPPORTIVE = "supportive"
    STABLE = "stable"
    MIXED = "mixed"
    SENSITIVE = "sensitive"


class ConfidenceLevel(str, Enum):
    """Canonical confidence level."""

    HIGH = "high"
    MEDIUM = "medium"
    REFERENCE_ONLY = "reference_only"


class MarriageRuntimeStatus(str, Enum):
    """Runtime envelope status."""

    SUCCESS = "SUCCESS"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"


class TenGodVisibility(str, Enum):
    """Visibility of a ten-god item."""

    VISIBLE = "visible"
    HIDDEN = "hidden"
