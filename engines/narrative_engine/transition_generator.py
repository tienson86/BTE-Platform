"""Transition Generator — soft bridges between sections via Sentence Library."""

from __future__ import annotations

from .models import NarrativeIssue, NarrativeParagraph
from .sentence_library_loader import SentenceLibraryLoader


class TransitionGenerator:
    """
    Insert soft transitions between narrative sections.

    Uses ``02_transition`` labels / module metadata — not LLM, not hard-coded
    interpretation prose. Skips SCHEMA EXAMPLE sentence_pattern bodies.
    """

    def __init__(self, loader: SentenceLibraryLoader | None = None) -> None:
        self.loader = loader or SentenceLibraryLoader()
        self.issues: list[NarrativeIssue] = []

    def apply(self, paragraphs: list[NarrativeParagraph]) -> list[NarrativeParagraph]:
        """Weave transition paragraphs between content sections."""
        self.issues = []
        content = [item for item in paragraphs if not item.is_transition and item.text.strip()]
        if len(content) <= 1:
            return list(paragraphs)

        transition_mod = self.loader.transition_module()
        bridge_label = "transition"
        if transition_mod is not None:
            bridge_label = transition_mod.label_display("transition") or bridge_label
            module_title = transition_mod.module_title
        else:
            module_title = bridge_label

        # Prefer enabled transition sentences from library when present
        pattern = self._enabled_transition_pattern()

        result: list[NarrativeParagraph] = []
        for index, paragraph in enumerate(content):
            result.append(paragraph)
            if index >= len(content) - 1:
                continue
            nxt = content[index + 1]
            # Never insert hard same-section bridges
            if paragraph.section_id == nxt.section_id:
                continue
            text = self._build_bridge(
                previous=paragraph,
                nxt=nxt,
                bridge_label=bridge_label,
                module_title=module_title,
                pattern=pattern,
            )
            if not text:
                continue
            result.append(
                NarrativeParagraph(
                    section_id=f"transition:{paragraph.section_id}->{nxt.section_id}",
                    section_title=module_title,
                    text=text,
                    tone="neutral",
                    unit_count=1,
                    is_transition=True,
                )
            )
            self.issues.append(
                NarrativeIssue(
                    kind="transition",
                    detail=f"Inserted soft transition before '{nxt.section_id}'.",
                    section_id=nxt.section_id,
                    action="insert",
                )
            )
        return result

    def _enabled_transition_pattern(self) -> str:
        """Return first enabled real transition sentence_pattern, else empty."""
        module = self.loader.transition_module()
        if module is None:
            return ""
        for sentence in module.enabled_sentences():
            pattern = str(sentence.get("sentence_pattern") or "").strip()
            if not pattern or "[SCHEMA EXAMPLE]" in pattern:
                continue
            return pattern
        return ""

    def _build_bridge(
        self,
        *,
        previous: NarrativeParagraph,
        nxt: NarrativeParagraph,
        bridge_label: str,
        module_title: str,
        pattern: str,
    ) -> str:
        prev_title = previous.section_title or previous.section_id
        next_title = nxt.section_title or nxt.section_id
        if pattern:
            filled = (
                pattern.replace("{{section}}", next_title)
                .replace("{{from_section}}", prev_title)
                .replace("{{to_section}}", next_title)
            )
            if "[SCHEMA EXAMPLE]" not in filled:
                return filled.strip()
        # Soft connector from labels only — avoids hard topic jumps
        return f"{bridge_label}. {next_title}."
