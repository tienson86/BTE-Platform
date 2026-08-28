"""CP-01 commercial presentation adapter. Formats composed consulting for display.

Does not match. Does not compose. Does not invent advice.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

COMMERCIAL_PRESENTATION_EMPTY: str = (
    "Chưa có đủ dữ liệu để tạo tư vấn thương mại."
)


@dataclass(slots=True)
class CommercialPresentationSection:
    """One customer-facing consulting section. Trace ids stay internal."""

    domain: str
    title: str
    summary: str
    meaning: tuple[str, ...]
    recommendations: tuple[str, ...]
    source_unit_ids: tuple[str, ...] = ()

    def customer_dict(self) -> dict[str, Any]:
        """Serialize display fields only. Omit source_unit_ids."""
        return {
            "domain": self.domain,
            "title": self.title,
            "summary": self.summary,
            "meaning": list(self.meaning),
            "recommendations": list(self.recommendations),
        }


@dataclass(slots=True)
class CommercialPresentationModel:
    """Display model shared by Portal, HTML, PDF, and DOCX."""

    visible: bool
    status: str
    empty_copy: str = COMMERCIAL_PRESENTATION_EMPTY
    sections: tuple[CommercialPresentationSection, ...] = ()

    def customer_dict(self) -> dict[str, Any]:
        """Serialize customer-facing presentation without trace ids."""
        return {
            "visible": self.visible,
            "status": self.status,
            "empty_copy": self.empty_copy if not self.visible else "",
            "sections": [section.customer_dict() for section in self.sections],
        }

    def customer_texts(self) -> tuple[str, ...]:
        """Ordered customer copy used by HTML, PDF, and DOCX."""
        if not self.visible:
            return ()
        lines: list[str] = []
        for section in self.sections:
            lines.append(section.title)
            if section.summary:
                lines.append(section.summary)
            lines.extend(section.meaning)
            lines.extend(section.recommendations)
        return tuple(lines)


class CommercialPresentationAdapter:
    """Copy composed consulting into a display model. Read only."""

    def adapt(self, payload: Any = None) -> CommercialPresentationModel:
        """Format CommercialComposerResult for presentation. Do not rematch."""
        record = _as_record(payload)
        status = str(record.get("status") or "insufficient")
        raw_sections = record.get("sections") or ()
        sections = tuple(
            section
            for item in raw_sections
            if (section := _as_section(item)) is not None
        )
        if status != "complete" or not sections:
            return CommercialPresentationModel(
                visible=False,
                status="insufficient",
                empty_copy=COMMERCIAL_PRESENTATION_EMPTY,
            )
        return CommercialPresentationModel(
            visible=True,
            status="complete",
            empty_copy="",
            sections=sections,
        )


def _as_record(payload: Any) -> Mapping[str, Any]:
    """Accept a composer result or equivalent mapping."""
    if payload is None:
        return {}
    if hasattr(payload, "to_dict") and callable(payload.to_dict):
        copied = payload.to_dict()
        return copied if isinstance(copied, Mapping) else {}
    if isinstance(payload, Mapping):
        return payload
    return {}


def _as_section(item: Any) -> CommercialPresentationSection | None:
    """Copy stored customer fields. Drop empty units. Keep ids internally."""
    record = item.to_dict() if hasattr(item, "to_dict") and callable(item.to_dict) else item
    if not isinstance(record, Mapping):
        return None
    title = str(record.get("title") or "").strip()
    summary = str(record.get("summary") or "").strip()
    meaning = _string_tuple(record.get("meaning"))
    recommendations = _string_tuple(record.get("recommendations"))
    if not title or not (summary or meaning or recommendations):
        return None
    return CommercialPresentationSection(
        domain=str(record.get("domain") or "").strip(),
        title=title,
        summary=summary,
        meaning=meaning,
        recommendations=recommendations,
        source_unit_ids=_string_tuple(record.get("source_unit_ids")),
    )


def _string_tuple(value: Any) -> tuple[str, ...]:
    """Copy string sequences. Ignore blank entries."""
    if isinstance(value, str):
        text = value.strip()
        return (text,) if text else ()
    if isinstance(value, (list, tuple)):
        return tuple(str(item).strip() for item in value if str(item).strip())
    return ()
