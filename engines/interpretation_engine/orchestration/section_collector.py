"""Section collection for Pack 03 execution pipeline.

Aggregates empty/structural InterpretationSection shells.
No BaZi logic / no narrative content.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.models.section_result import SectionResult

logger = logging.getLogger(__name__)

# Canonical empty section type used by interpreter skeletons.
InterpretationSection = SectionResult


@dataclass(frozen=True, slots=True)
class SectionCollectionResult:
    """Immutable section collection snapshot."""

    sections: tuple[InterpretationSection, ...] = ()
    failed_interpreter_ids: tuple[str, ...] = ()
    messages: tuple[str, ...] = ()
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate collected sections structurally."""
        for section in self.sections:
            if not section.validate():
                return False
        return True

    def section_ids(self) -> tuple[str, ...]:
        """Return ordered section identifiers."""
        return tuple(section.id for section in self.sections)


class SectionCollector:
    """Collect InterpretationSection shells from interpreter execute payloads."""

    def collect_from_dispatch(
        self,
        dispatch_results: tuple[tuple[str, Any], ...],
    ) -> SectionCollectionResult:
        """Collect sections from dispatcher (entry_id, payload) tuples.

        Error isolation: failed interpreter payloads are recorded, not raised.
        """
        sections: list[InterpretationSection] = []
        failed: list[str] = []
        messages: list[str] = []

        for entry_id, payload in dispatch_results:
            section = self._extract_section(payload)
            success = self._is_success(payload)
            if success and section is not None:
                sections.append(section)
                messages.append(f"section_collected:{entry_id}")
                continue
            failed.append(entry_id)
            detail = self._failure_detail(payload)
            messages.append(f"section_skipped:{entry_id}:{detail}")
            logger.warning(
                "section_collection_isolated_failure",
                extra={"interpreter_id": entry_id, "detail": detail},
            )

        return SectionCollectionResult(
            sections=tuple(sections),
            failed_interpreter_ids=tuple(failed),
            messages=tuple(messages),
            attributes={"collected_count": len(sections), "failed_count": len(failed)},
        )

    def _extract_section(self, payload: Any) -> InterpretationSection | None:
        """Extract InterpretationSection from runtime execute result or mapping."""
        candidate = payload
        if hasattr(payload, "payload") and isinstance(payload.payload, Mapping):
            candidate = payload.payload.get("interpretation_section") or payload.payload.get(
                "section"
            )
        elif isinstance(payload, Mapping):
            candidate = payload.get("interpretation_section") or payload.get("section")
        if isinstance(candidate, SectionResult):
            return candidate
        return None

    def _is_success(self, payload: Any) -> bool:
        """Return True when payload indicates successful interpreter execution."""
        if hasattr(payload, "success"):
            return bool(payload.success)
        if isinstance(payload, Mapping):
            return bool(payload.get("success", True))
        return payload is not None

    def _failure_detail(self, payload: Any) -> str:
        """Return a short failure detail string."""
        if hasattr(payload, "messages") and payload.messages:
            return str(payload.messages[0])
        if isinstance(payload, Mapping) and payload.get("messages"):
            messages = payload["messages"]
            if messages:
                return str(messages[0])
        if payload is None:
            return "null_payload"
        return "section_missing"
