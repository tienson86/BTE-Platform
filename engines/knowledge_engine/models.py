"""Knowledge Engine result models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


REQUIRED_COLUMNS: tuple[str, ...] = (
    "id",
    "topic",
    "keyword",
    "condition",
    "classical_text",
    "modern_interpretation",
    "priority",
    "confidence",
    "reference",
)

KNOWLEDGE_FILES: tuple[str, ...] = (
    "01_five_elements.csv",
    "02_yin_yang.csv",
    "03_ten_gods.csv",
    "04_hidden_stems.csv",
    "05_growth_stage.csv",
    "06_nayin.csv",
    "07_patterns.csv",
    "08_useful_god.csv",
    "09_strength.csv",
    "10_temperature.csv",
    "11_shensha.csv",
    "12_career.csv",
    "13_wealth.csv",
    "14_marriage.csv",
    "15_children.csv",
    "16_health.csv",
    "17_parents.csv",
    "18_luck_cycles.csv",
    "19_feng_shui.csv",
    "20_glossary.csv",
)


@dataclass(slots=True)
class KnowledgeRecord:
    """One classical knowledge entry loaded from ``database/20_knowledge``."""

    id: str
    topic: str
    keyword: str
    condition: str
    classical_text: str
    modern_interpretation: str
    priority: int
    confidence: float
    reference: str
    source_file: str = ""

    def keyword_tokens(self) -> list[str]:
        """Split keyword field into normalized search tokens."""
        raw = self.keyword or ""
        parts: list[str] = []
        for chunk in raw.replace("|", ";").replace(",", ";").split(";"):
            token = chunk.strip().lower()
            if token:
                parts.append(token)
        return parts


@dataclass(slots=True)
class RetrievalTraceEntry:
    """One candidate evaluation step for retrieval explainability."""

    record_id: str
    accepted: bool
    keyword_score: float
    condition_score: float
    priority: int
    confidence: float
    relevance_score: float
    matched_keywords: tuple[str, ...] = ()
    matched_conditions: tuple[str, ...] = ()
    reject_reason: str = ""


@dataclass(slots=True)
class KnowledgeHit:
    """A retrieved knowledge entry with scoring metadata."""

    record: KnowledgeRecord
    keyword_score: float
    condition_score: float
    relevance_score: float
    matched_keywords: tuple[str, ...] = ()
    matched_conditions: tuple[str, ...] = ()

    @property
    def id(self) -> str:
        """Return the underlying record id."""
        return self.record.id

    @property
    def priority(self) -> int:
        """Return record priority."""
        return self.record.priority

    @property
    def confidence(self) -> float:
        """Return record confidence."""
        return self.record.confidence


@dataclass(slots=True)
class KnowledgeResult:
    """Retriever output: ranked hits plus metadata.trace."""

    entries: list[KnowledgeHit]
    metadata: dict[str, Any]

    @property
    def records(self) -> list[KnowledgeRecord]:
        """Return underlying knowledge records in ranked order."""
        return [hit.record for hit in self.entries]

    @property
    def trace(self) -> list[dict[str, Any]]:
        """Return serialized retrieval trace from metadata."""
        raw = self.metadata.get("trace") if self.metadata else None
        return list(raw) if isinstance(raw, list) else []

    def to_dict(self) -> dict[str, Any]:
        """Serialize result for reports and API-friendly consumers."""
        return {
            "entries": [
                {
                    "id": hit.record.id,
                    "topic": hit.record.topic,
                    "keyword": hit.record.keyword,
                    "condition": hit.record.condition,
                    "classical_text": hit.record.classical_text,
                    "modern_interpretation": hit.record.modern_interpretation,
                    "priority": hit.record.priority,
                    "confidence": hit.record.confidence,
                    "reference": hit.record.reference,
                    "source_file": hit.record.source_file,
                    "keyword_score": hit.keyword_score,
                    "condition_score": hit.condition_score,
                    "relevance_score": hit.relevance_score,
                    "matched_keywords": list(hit.matched_keywords),
                    "matched_conditions": list(hit.matched_conditions),
                }
                for hit in self.entries
            ],
            "metadata": dict(self.metadata or {}),
        }
