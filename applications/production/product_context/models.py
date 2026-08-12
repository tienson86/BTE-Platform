"""Product Context Engine V1.0 — delivery orchestration contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class LifeStage(str, Enum):
    """Canonical life stages for product delivery."""

    CHILD = "CHILD"
    TEEN = "TEEN"
    YOUNG_ADULT = "YOUNG_ADULT"
    ADULT = "ADULT"
    MID_CAREER = "MID_CAREER"
    SENIOR = "SENIOR"


class ReaderRole(str, Enum):
    """Who the report is speaking to."""

    SELF = "SELF"
    PARENT = "PARENT"
    SPOUSE = "SPOUSE"
    CONSULTANT = "CONSULTANT"
    UNKNOWN = "UNKNOWN"


class PurchasePackage(str, Enum):
    """Commercial package selection."""

    PACKAGE_A = "PACKAGE_A"  # Quick Insight
    PACKAGE_B = "PACKAGE_B"  # Professional Consulting
    PACKAGE_C = "PACKAGE_C"  # Master Consulting
    PACKAGE_D = "PACKAGE_D"  # Advisor Edition
    UNKNOWN = "UNKNOWN"


class LanguageProfile(str, Enum):
    """How language should be framed — does not rewrite claim truth."""

    GUIDANCE = "GUIDANCE"
    COACHING = "COACHING"
    CONSULTING = "CONSULTING"
    PARENT_SUPPORT = "PARENT_SUPPORT"
    SENIOR_REFLECTION = "SENIOR_REFLECTION"


class ActionProfile(str, Enum):
    """Who actions are addressed to."""

    PARENT_ACTIONS = "PARENT_ACTIONS"
    SELF_DECISIONS = "SELF_DECISIONS"
    LEGACY_PLANNING = "LEGACY_PLANNING"
    DEVELOPMENT_SUPPORT = "DEVELOPMENT_SUPPORT"
    NONE = "NONE"


class ReportType(str, Enum):
    """Requested report family."""

    GENERAL = "GENERAL"
    IDENTITY = "IDENTITY"
    CAREER = "CAREER"
    EXECUTIVE = "EXECUTIVE"
    DEVELOPMENT = "DEVELOPMENT"
    PARENT_GUIDANCE = "PARENT_GUIDANCE"


@dataclass(slots=True)
class ProductContextInput:
    """Canonical input for product context resolution."""

    subject_age: int | None = None
    birth_year: int | None = None
    birth_month: int | None = None
    birth_day: int | None = None
    as_of_year: int | None = None
    as_of_month: int | None = None
    as_of_day: int | None = None
    life_stage: LifeStage | None = None
    reader_role: ReaderRole = ReaderRole.UNKNOWN
    purchase_package: PurchasePackage = PurchasePackage.UNKNOWN
    question_context: str = "GENERAL"
    customer_goal: str = ""
    report_type: ReportType = ReportType.GENERAL
    language: str = "vi"
    versions: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class ProductContextResult:
    """Resolved delivery context — not BaZi truth."""

    reader_role: ReaderRole
    life_stage: LifeStage
    subject_age: int | None
    language_profile: LanguageProfile
    visible_features: list[str] = field(default_factory=list)
    hidden_features: list[str] = field(default_factory=list)
    blocked_sections: list[str] = field(default_factory=list)
    action_profile: ActionProfile = ActionProfile.SELF_DECISIONS
    tone: str = "consultant"
    purchase_package: PurchasePackage = PurchasePackage.UNKNOWN
    safety_blocks: list[str] = field(default_factory=list)
    pass_through: bool = False
    diagnostics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize for validation diagnostics."""
        return {
            "reader_role": self.reader_role.value,
            "life_stage": self.life_stage.value,
            "subject_age": self.subject_age,
            "language_profile": self.language_profile.value,
            "visible_features": list(self.visible_features),
            "hidden_features": list(self.hidden_features),
            "blocked_sections": list(self.blocked_sections),
            "action_profile": self.action_profile.value,
            "tone": self.tone,
            "purchase_package": self.purchase_package.value,
            "safety_blocks": list(self.safety_blocks),
            "pass_through": self.pass_through,
            "diagnostics": dict(self.diagnostics),
        }
