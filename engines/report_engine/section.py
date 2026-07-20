"""
BTE Platform
Report Engine

File: section.py
Version: 1.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ==========================================================
# Section Type
# ==========================================================

class SectionType(str, Enum):
    """
    Loại Section trong báo cáo.
    """

    GENERAL = "general"

    BASIC_INFO = "basic_info"

    BAZI = "bazi"

    FIVE_ELEMENTS = "five_elements"

    STRENGTH = "strength"

    TEN_GODS = "ten_gods"

    PATTERN = "pattern"

    USEFUL_GOD = "useful_god"

    SHEN_SHA = "shen_sha"

    LUCK = "luck"

    INTERPRETATION = "interpretation"

    CONCLUSION = "conclusion"

    RECOMMENDATION = "recommendation"

    APPENDIX = "appendix"


# ==========================================================
# Section Status
# ==========================================================

class SectionStatus(str, Enum):
    """
    Trạng thái Section.
    """

    DRAFT = "draft"

    READY = "ready"

    HIDDEN = "hidden"


# ==========================================================
# Report Section
# ==========================================================

@dataclass(slots=True)
class ReportSection:
    """
    Một Section trong báo cáo.
    """

    id: str

    title: str

    type: SectionType

    content: str = ""

    order: int = 0

    visible: bool = True

    status: SectionStatus = SectionStatus.READY

    score: dict[str, Any] = field(
        default_factory=dict
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    children: list["ReportSection"] = field(
        default_factory=list
    )

    tags: list[str] = field(
        default_factory=list
    )

    notes: list[str] = field(
        default_factory=list
    )

    def add_child(
        self,
        section: "ReportSection",
    ) -> None:
        """
        Thêm Section con.
        """
        self.children.append(section)

    def add_tag(
        self,
        tag: str,
    ) -> None:
        """
        Thêm tag.
        """
        if tag not in self.tags:
            self.tags.append(tag)

    def add_note(
        self,
        note: str,
    ) -> None:
        """
        Thêm ghi chú.
        """
        self.notes.append(note)

    def to_dict(self) -> dict[str, Any]:
        """
        Chuyển Section thành dict.
        """
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type.value,
            "content": self.content,
            "order": self.order,
            "visible": self.visible,
            "status": self.status.value,
            "score": self.score,
            "metadata": self.metadata,
            "tags": self.tags,
            "notes": self.notes,
            "children": [
                child.to_dict()
                for child in self.children
            ],
        }
