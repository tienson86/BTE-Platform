"""Collect narrative units from InterpretationResult + ReportModel."""

from __future__ import annotations

import re
from typing import Any, Mapping

from .models import NarrativeUnit
from .sentence_library_loader import SentenceLibraryLoader

# Report / Interpretation section id → sentence library module
SECTION_TO_SENTENCE_MODULE: dict[str, str] = {
    "summary": "01_intro",
    "strength": "03_strength",
    "pattern": "04_pattern",
    "useful_god": "05_useful_god",
    "personality": "06_personality",
    "career": "07_career",
    "wealth": "08_wealth",
    "relationship": "09_relationship",
    "health": "10_health",
    "children": "11_children",
    "luck": "12_luck_cycle",
    "luck_cycle": "12_luck_cycle",
    "yearly_fortune": "13_yearly",
    "year": "13_yearly",
    "conclusion": "14_conclusion",
    "warning": "03_strength",
    "weakness": "03_strength",
}


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?…])\s+|(?<=[。！？])\s+|\n+")


def _as_dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return dict(value)
    if hasattr(value, "to_dict"):
        try:
            payload = value.to_dict()
            if isinstance(payload, dict):
                return payload
        except Exception:
            pass
    payload: dict[str, Any] = {}
    for key in ("summary", "sections", "sentences", "title", "metadata", "paragraphs"):
        if hasattr(value, key):
            payload[key] = getattr(value, key)
    return payload


def _split_text(text: str) -> list[str]:
    parts = [part.strip() for part in _SENTENCE_SPLIT.split(str(text or "")) if part.strip()]
    return parts or ([] if not str(text or "").strip() else [str(text).strip()])


def _tone_from_text(text: str, allowed: tuple[str, ...]) -> str:
    lower = text.lower()
    if any(token in lower for token in ("cảnh báo", "warning", "bat loi", "bất lợi", "xấu")):
        return "serious" if "serious" in allowed else "negative"
    if any(token in lower for token in ("khuyến nghị", "recommend", "nên", "thuận lợi", "tốt")):
        return "positive" if "positive" in allowed else "friendly"
    return "neutral" if "neutral" in allowed else (allowed[0] if allowed else "neutral")


def _intent_from_section(section_id: str, text: str, intents: tuple[str, ...]) -> str:
    if section_id in {"summary"} and "summarize" in intents:
        return "summarize"
    if section_id in {"conclusion"} and "conclude" in intents:
        return "conclude"
    lower = text.lower()
    if any(token in lower for token in ("cảnh báo", "warning")) and "warn" in intents:
        return "warn"
    if any(token in lower for token in ("khuyến nghị", "nên")) and "recommend" in intents:
        return "recommend"
    return "describe" if "describe" in intents else (intents[0] if intents else "describe")


class NarrativeSourceCollector:
    """Build ordered NarrativeUnit list from Interpretation + Report."""

    def __init__(self, loader: SentenceLibraryLoader | None = None) -> None:
        self.loader = loader or SentenceLibraryLoader()

    def collect(
        self,
        interpretation: Any,
        report: Any,
    ) -> list[NarrativeUnit]:
        """Merge report sections with interpretation sentences; prefer report order."""
        tones = self.loader.tones()
        intents = self.loader.intents()
        report_data = _as_dict(report)
        interp_data = _as_dict(interpretation)

        units: list[NarrativeUnit] = []
        seen: set[str] = set()

        # 1) ReportModel sections (template-ordered)
        for section in report_data.get("sections") or []:
            section_obj = section
            if not isinstance(section, Mapping):
                section_obj = {
                    "id": getattr(section, "id", ""),
                    "title": getattr(section, "title", ""),
                    "content": getattr(section, "content", ""),
                    "order": getattr(section, "order", 0),
                    "visible": getattr(section, "visible", True),
                }
            if not section_obj.get("visible", True):
                continue
            section_id = str(section_obj.get("id") or "")
            title = str(section_obj.get("title") or section_id)
            content = str(section_obj.get("content") or "").strip()
            for text in _split_text(content):
                key = text.strip().lower()
                if not key or key in seen:
                    continue
                seen.add(key)
                units.append(
                    NarrativeUnit(
                        text=text,
                        section_id=section_id,
                        section_title=title,
                        tone=_tone_from_text(text, tones),
                        intent=_intent_from_section(section_id, text, intents),
                        priority=50.0,
                        source="report",
                    )
                )

        # 2) Interpretation sentences not already covered
        for sentence in interp_data.get("sentences") or []:
            if not isinstance(sentence, Mapping):
                continue
            text = str(sentence.get("sentence") or "").strip()
            key = text.lower()
            if not text or key in seen:
                continue
            seen.add(key)
            section_id = str(sentence.get("section") or "summary")
            title = self._section_title(section_id, report_data)
            try:
                priority = float(sentence.get("priority") or 0)
            except (TypeError, ValueError):
                priority = 0.0
            units.append(
                NarrativeUnit(
                    text=text,
                    section_id=section_id,
                    section_title=title,
                    tone=_tone_from_text(text, tones),
                    intent=_intent_from_section(section_id, text, intents),
                    priority=priority,
                    source="interpretation",
                    rule_id=str(sentence.get("rule_id") or ""),
                )
            )

        # 3) Interpretation summary if empty
        summary = str(interp_data.get("summary") or "").strip()
        if summary and summary.lower() not in seen and not units:
            for text in _split_text(summary):
                units.append(
                    NarrativeUnit(
                        text=text,
                        section_id="summary",
                        section_title=self._section_title("summary", report_data),
                        tone="neutral",
                        intent="summarize",
                        priority=100.0,
                        source="interpretation.summary",
                    )
                )

        return units

    def _section_title(self, section_id: str, report_data: Mapping[str, Any]) -> str:
        for section in report_data.get("sections") or []:
            sid = section.get("id") if isinstance(section, Mapping) else getattr(section, "id", "")
            if str(sid) == section_id:
                title = (
                    section.get("title")
                    if isinstance(section, Mapping)
                    else getattr(section, "title", "")
                )
                if title:
                    return str(title)
        module_key = SECTION_TO_SENTENCE_MODULE.get(section_id, "")
        module = self.loader.get_module(module_key) if module_key else None
        if module is not None:
            return module.module_title
        return section_id
