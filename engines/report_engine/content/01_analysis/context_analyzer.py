"""Normalize InterpretationResult into an analysis-friendly context bag."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Mapping


class ContextAnalyzer:
    """
    Analyze InterpretationResult structure.

    Produces grouped_rules and raw section metrics used by other analyzers.
    """

    def analyze(self, interpretation: Any) -> dict[str, Any]:
        """
        Return a normalized analysis bag.

        Keys: sections, grouped_rules, summary, sentences, rule_count,
        section_rule_counts, confidence.
        """
        data = self._to_mapping(interpretation)
        sections = self._normalize_sections(data.get("sections"))
        sentences = list(data.get("sentences") or [])
        grouped = self._group_rules(sections, sentences)

        section_rule_counts = {
            name: len(rules) for name, rules in grouped.items()
        }
        return {
            "summary": str(data.get("summary") or ""),
            "sections": sections,
            "sentences": sentences,
            "grouped_rules": grouped,
            "section_rule_counts": section_rule_counts,
            "rule_count": sum(section_rule_counts.values()),
            "confidence": self._as_float(data.get("confidence"), default=0.0),
            "matched_rule_count": self._as_float(
                data.get("matched_rule_count"),
                default=float(len(data.get("rules_used") or [])),
            ),
            "resolved_rule_count": self._as_float(
                data.get("resolved_rule_count"),
                default=0.0,
            ),
            "rules_used": list(data.get("rules_used") or []),
        }

    def _group_rules(
        self,
        sections: dict[str, dict[str, Any]],
        sentences: list[Any],
    ) -> dict[str, list[dict[str, Any]]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for name, section in sections.items():
            rules: list[dict[str, Any]] = []
            for rule in section.get("rules") or []:
                if isinstance(rule, Mapping):
                    item = dict(rule)
                    item.setdefault("section", name)
                    rules.append(item)
            grouped[name] = rules

        for sentence in sentences:
            if not isinstance(sentence, Mapping):
                continue
            section = str(sentence.get("section") or "summary")
            text = str(
                sentence.get("sentence")
                or sentence.get("description")
                or ""
            ).strip()
            if not text:
                continue
            bucket = grouped.setdefault(section, [])
            # Avoid exact duplicate rule_id+text pairs
            rule_id = str(sentence.get("rule_id") or "")
            if any(
                str(item.get("rule_id") or "") == rule_id
                and str(item.get("sentence") or item.get("description") or "") == text
                for item in bucket
            ):
                continue
            bucket.append(
                {
                    "rule_id": rule_id,
                    "section": section,
                    "sentence": text,
                    "description": text,
                    "priority": sentence.get("priority", 0),
                    "confidence": sentence.get("confidence", 0),
                    "source": "sentence",
                }
            )
        return grouped

    def _normalize_sections(self, sections: Any) -> dict[str, dict[str, Any]]:
        if not sections:
            return {}
        if isinstance(sections, Mapping):
            result: dict[str, dict[str, Any]] = {}
            for name, section in sections.items():
                result[str(name)] = self._section_to_dict(section, str(name))
            return result
        if isinstance(sections, list):
            result = {}
            for index, section in enumerate(sections):
                payload = self._section_to_dict(section, f"section_{index}")
                name = str(payload.get("name") or f"section_{index}")
                result[name] = payload
            return result
        return {}

    def _section_to_dict(self, section: Any, default_name: str) -> dict[str, Any]:
        if isinstance(section, Mapping):
            payload = dict(section)
            payload.setdefault("name", default_name)
            payload.setdefault("rules", list(payload.get("rules") or []))
            return payload
        if is_dataclass(section):
            payload = asdict(section)
            payload.setdefault("name", default_name)
            return payload
        return {
            "name": getattr(section, "name", default_name),
            "rules": list(getattr(section, "rules", []) or []),
            "positive_rules": list(getattr(section, "positive_rules", []) or []),
            "negative_rules": list(getattr(section, "negative_rules", []) or []),
            "warnings": list(getattr(section, "warnings", []) or []),
            "score": getattr(section, "score", 0),
        }

    def _to_mapping(self, interpretation: Any) -> dict[str, Any]:
        if interpretation is None:
            return {}
        if isinstance(interpretation, Mapping):
            return dict(interpretation)
        if is_dataclass(interpretation):
            return asdict(interpretation)
        if hasattr(interpretation, "to_dict"):
            try:
                payload = interpretation.to_dict()
                if isinstance(payload, dict):
                    return payload
            except Exception:
                pass
        payload: dict[str, Any] = {}
        for key in (
            "summary",
            "sections",
            "sentences",
            "rules_used",
            "confidence",
            "matched_rule_count",
            "resolved_rule_count",
            "priority_resolution",
        ):
            if hasattr(interpretation, key):
                payload[key] = getattr(interpretation, key)
        return payload

    @staticmethod
    def _as_float(value: Any, *, default: float = 0.0) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default
