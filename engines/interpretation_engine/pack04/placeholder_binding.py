"""Placeholder binding for Pack 04 sentence templates."""

from __future__ import annotations

import re
from typing import Any

from .models import NarrativeSentence
from .narrative_context import NarrativeContext

_PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z0-9_]+)\}")


class PlaceholderBinder:
    """Stage — Placeholder Binding."""

    def bind(
        self,
        selected: list[dict[str, Any]],
        context: NarrativeContext,
    ) -> list[NarrativeSentence]:
        """Render sentence templates with narrative placeholders."""
        rendered: list[NarrativeSentence] = []
        for item in selected:
            rule = item.get("rule") or {}
            sentence = item.get("sentence") or {}
            template = str(sentence.get("text") or "")
            used: dict[str, str] = {}
            text = _PLACEHOLDER_RE.sub(
                lambda match: self._replace(match, context.placeholders, used),
                template,
            )
            confidence = float(
                getattr(
                    getattr(context.analysis, str(rule.get("section") or ""), None),
                    "confidence",
                    0.0,
                )
                or 0.0
            )
            # Section nodes use float confidence; overview/summary may not.
            if not confidence:
                confidence = float(context.analysis.confidence.by_dimension.get(
                    str(rule.get("section") or ""),
                    0.5,
                ) or 0.5)

            rendered.append(
                NarrativeSentence(
                    sentence_id=str(sentence.get("sentence_id") or ""),
                    section=str(rule.get("section") or sentence.get("section") or ""),
                    template_id=str(sentence.get("template_id") or ""),
                    text=text,
                    placeholders=used,
                    evidence_ids=list(context.evidence_ids),
                    confidence=confidence,
                    rule_id=str(rule.get("rule_id") or ""),
                )
            )
        return rendered

    @staticmethod
    def _replace(
        match: re.Match[str],
        placeholders: dict[str, str],
        used: dict[str, str],
    ) -> str:
        key = match.group(1)
        value = placeholders.get(key, "")
        used[key] = value
        return value
