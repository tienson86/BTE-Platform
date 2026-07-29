"""Tone Controller — normalize tone using Sentence Library schema + labels."""

from __future__ import annotations

from collections import Counter

from .models import NarrativeIssue, NarrativeUnit
from .sentence_library_loader import SentenceLibraryLoader
from .source_collector import SECTION_TO_SENTENCE_MODULE


class ToneController:
    """
    Align unit tone to schema tones and apply label cues (no LLM).

    Does not invent interpretation content — only wraps/normalizes presentation.
    """

    def __init__(self, loader: SentenceLibraryLoader | None = None) -> None:
        self.loader = loader or SentenceLibraryLoader()
        self.issues: list[NarrativeIssue] = []

    def apply(
        self,
        units: list[NarrativeUnit],
        *,
        target_tone: str | None = None,
    ) -> list[NarrativeUnit]:
        """Normalize tones; optionally bias toward a global target tone."""
        self.issues = []
        allowed = self.loader.tones()
        default = "neutral" if "neutral" in allowed else (allowed[0] if allowed else "neutral")
        global_tone = target_tone if target_tone in allowed else self._dominant_tone(units, default)

        result: list[NarrativeUnit] = []
        for unit in units:
            tone = unit.tone if unit.tone in allowed else default
            # Soft-normalize extreme conflicts toward global professional/neutral when mixed
            if global_tone == "professional" and tone in {"friendly"}:
                tone = "professional"
            if global_tone == "neutral" and tone not in allowed:
                tone = default

            text = unit.text
            label_prefix = self._label_prefix(unit)
            if label_prefix and not text.startswith(label_prefix):
                # Only prefix warnings/recommendations for clarity — not every sentence
                if unit.intent in {"warn", "recommend"} or tone in {"serious", "negative"}:
                    if unit.intent == "warn" or tone in {"serious", "negative"}:
                        warn = self._label_for(unit.section_id, "warning")
                        if warn and warn.lower() not in text.lower():
                            text = f"{warn}: {text}"
                            self.issues.append(
                                NarrativeIssue(
                                    kind="tone",
                                    detail=f"Applied warning label '{warn}'.",
                                    section_id=unit.section_id,
                                    action="prefix",
                                )
                            )
                    elif unit.intent == "recommend":
                        rec = self._label_for(unit.section_id, "recommendation")
                        if rec and rec.lower() not in text.lower():
                            text = f"{rec}: {text}"
                            self.issues.append(
                                NarrativeIssue(
                                    kind="tone",
                                    detail=f"Applied recommendation label '{rec}'.",
                                    section_id=unit.section_id,
                                    action="prefix",
                                )
                            )

            result.append(
                NarrativeUnit(
                    text=text,
                    section_id=unit.section_id,
                    section_title=unit.section_title,
                    tone=tone,
                    intent=unit.intent if unit.intent in self.loader.intents() else "describe",
                    priority=unit.priority,
                    source=unit.source,
                    rule_id=unit.rule_id,
                    is_transition=unit.is_transition,
                )
            )
        return result

    def resolve_document_tone(self, units: list[NarrativeUnit]) -> str:
        """Pick dominant document tone from schema-allowed set."""
        allowed = self.loader.tones()
        default = "neutral" if "neutral" in allowed else (allowed[0] if allowed else "neutral")
        return self._dominant_tone(units, default)

    @staticmethod
    def _dominant_tone(units: list[NarrativeUnit], default: str) -> str:
        if not units:
            return default
        counts = Counter(unit.tone for unit in units)
        return counts.most_common(1)[0][0]

    def _label_for(self, section_id: str, label_code: str) -> str:
        module_id = SECTION_TO_SENTENCE_MODULE.get(section_id, "")
        module = self.loader.get_module(module_id) if module_id else None
        if module is None:
            module = self.loader.transition_module()
        if module is None:
            return ""
        return module.label_display(label_code)

    def _label_prefix(self, unit: NarrativeUnit) -> str:
        if unit.intent == "warn":
            return self._label_for(unit.section_id, "warning")
        if unit.intent == "recommend":
            return self._label_for(unit.section_id, "recommendation")
        return ""
