"""Citation models for classical knowledge sources."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# Canonical classical works supported by the Citation Engine.
CLASSICAL_SOURCE_KEYS: tuple[str, ...] = (
    "uyen_hai_tu_binh",
    "tam_menh_thong_hoi",
    "dich_thien_tuy",
    "tu_binh_chan_thuyen",
    "other",
)

CLASSICAL_SOURCES: dict[str, dict[str, Any]] = {
    "uyen_hai_tu_binh": {
        "title": "Uyên Hải Tử Bình",
        "code": "UHBP",
        "aliases": (
            "uyên hải tử bình",
            "uyen hai tu binh",
            "渊海子平",
            "yuan hai zi ping",
            "yuanhaiziping",
        ),
    },
    "tam_menh_thong_hoi": {
        "title": "Tam Mệnh Thông Hội",
        "code": "TMTH",
        "aliases": (
            "tam mệnh thông hội",
            "tam menh thong hoi",
            "三命通会",
            "san ming tong hui",
            "sanmingtonghui",
        ),
    },
    "dich_thien_tuy": {
        "title": "Tích Thiên Tủy",
        "code": "DTT",
        "aliases": (
            "tích thiên tủy",
            "tich thien tuy",
            "滴天髓",
            "di tian sui",
            "ditiansui",
            "ịch thiên tủy",
        ),
    },
    "tu_binh_chan_thuyen": {
        "title": "Tử Bình Chân Thuyên",
        "code": "TBCT",
        "aliases": (
            "tử bình chân thuyên",
            "tu binh chan thuyen",
            "子平真诠",
            "zi ping zhen quan",
            "zipingzhenquan",
        ),
    },
    "other": {
        "title": "Other classical references",
        "code": "OTHER",
        "aliases": (),
    },
}


@dataclass(slots=True)
class Citation:
    """One citation bound to a knowledge record."""

    citation_id: str
    reference: str
    chapter: str
    page: str
    record_id: str
    source_key: str
    topic: str = ""
    confidence: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Serialize citation (includes internal identifiers)."""
        return {
            "citation_id": self.citation_id,
            "reference": self.reference,
            "chapter": self.chapter,
            "page": self.page,
            "record_id": self.record_id,
            "source_key": self.source_key,
            "topic": self.topic,
            "confidence": self.confidence,
        }

    def visible_label(self) -> str:
        """Human-facing bibliography line (no record/engine ids)."""
        parts = [self.reference or CLASSICAL_SOURCES.get(self.source_key, {}).get("title", "Classical source")]
        if self.chapter:
            parts.append(f"ch. {self.chapter}")
        if self.page:
            parts.append(f"p. {self.page}")
        return ", ".join(parts)

    def internal_label(self) -> str:
        """AI-facing internal citation line (no knowledge record ids)."""
        return f"{self.citation_id} | {self.visible_label()}"


@dataclass(slots=True)
class CitationPackage:
    """Citation set derived from knowledge records."""

    citations: list[Citation]
    by_record_id: dict[str, Citation] = field(default_factory=dict)
    by_source_key: dict[str, list[Citation]] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def for_record(self, record_id: str) -> Citation | None:
        """Return citation for one knowledge record id."""
        return self.by_record_id.get(str(record_id or "").strip())

    def for_source(self, source_key: str) -> list[Citation]:
        """Return citations for one classical source key."""
        return list(self.by_source_key.get(str(source_key or "").strip().lower(), []))

    def to_dict(self) -> dict[str, Any]:
        """Serialize package."""
        return {
            "citations": [row.to_dict() for row in self.citations],
            "by_record_id": {
                key: value.to_dict() for key, value in self.by_record_id.items()
            },
            "by_source_key": {
                key: [row.to_dict() for row in rows]
                for key, rows in self.by_source_key.items()
            },
            "metadata": dict(self.metadata),
        }
