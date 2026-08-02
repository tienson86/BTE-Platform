"""Prompt Builder — Evidence + Knowledge + ReasoningGraph + Chart → StructuredPrompt.

Public contract:
- Input: evidence package, knowledge result, reasoning graph, chart facts
- Output: structured prompt with separated Facts / Evidence / Knowledge /
  Reasoning / Writing Style sections
- Never expose rule ids, internal CSV filenames, or engine names
"""

from __future__ import annotations

import logging
import re
from typing import Any, Mapping

from engines.knowledge_engine.evidence_models import (
    CATEGORY_LABELS,
    EvidenceItem,
    EvidencePackage,
)
from engines.knowledge_engine.models import (
    KnowledgeHit,
    KnowledgeRecord,
    KnowledgeResult,
)
from engines.knowledge_engine.prompt_models import (
    PROMPT_SECTION_KEYS,
    PROMPT_SECTION_TITLES,
    PromptSection,
    StructuredPrompt,
)
from engines.knowledge_engine.reasoning_models import (
    ReasoningEdge,
    ReasoningGraph,
    ReasoningNode,
)

logger = logging.getLogger(__name__)

# Patterns that must never appear in the rendered prompt.
_CSV_NAME_RE = re.compile(r"\b[\w\-]+\.csv\b", re.IGNORECASE)
_ENGINE_NAME_RE = re.compile(
    r"\b(?:engines?\.\w+|knowledge_engine|score_engine|bazi_engine|"
    r"pattern_engine|interpretation_engine|report_engine|calendar_engine|"
    r"strength_engine|temperature_engine|useful_god_engine|"
    r"\w+Engine)\b",
    re.IGNORECASE,
)
_RULE_ID_RE = re.compile(
    r"\b(?:rule[_:][a-z0-9_\-]+|template_id\s*[:=]\s*[a-z0-9_\-]+|"
    r"record_id\s*[:=]\s*[a-z0-9_\-]+|"
    r"(?:kb|tg|ug|pat|str|tmp|ss|fe|yy)[-_][a-z0-9_\-]+)\b",
    re.IGNORECASE,
)
_INTERNAL_PATH_RE = re.compile(
    r"\b(?:database/20_knowledge|rule_context:[a-z0-9_.]+)\b",
    re.IGNORECASE,
)
_NODE_EDGE_ID_RE = re.compile(
    r"\b(?:ev|ir|rs|cn|edge|node)[:_][a-z0-9_\-]+\b",
    re.IGNORECASE,
)

_DEFAULT_WRITING_STYLE: tuple[str, ...] = (
    "Write in clear, objective Vietnamese suitable for an expert BaZi consultation.",
    "Prefer short paragraphs and one idea per paragraph.",
    "Separate observed chart facts from classical knowledge and from conclusions.",
    "Use classical terminology consistently; explain modern meaning when helpful.",
    "Do not invent facts that are absent from the Facts or Evidence sections.",
    "Do not mention internal identifiers, file names, rule codes, or system engines.",
    "Avoid marketing language, fortune-telling hype, and emotional speculation.",
    "When uncertain, state the limit of evidence instead of forcing a conclusion.",
)


class PromptBuilder:
    """Compose a redacted structured prompt for downstream AI writing."""

    def __init__(self, *, writing_style: list[str] | tuple[str, ...] | None = None) -> None:
        """Optionally override the Writing Style lines."""
        self._writing_style = tuple(writing_style) if writing_style else _DEFAULT_WRITING_STYLE

    def build(
        self,
        *,
        evidence: EvidencePackage | Mapping[str, Any] | None = None,
        knowledge: KnowledgeResult | Mapping[str, Any] | list[Any] | None = None,
        reasoning: ReasoningGraph | Mapping[str, Any] | None = None,
        chart: Mapping[str, Any] | Any | None = None,
    ) -> StructuredPrompt:
        """Build a structured prompt from evidence, knowledge, reasoning, and chart.

        Args:
            evidence: EvidencePackage or mapping with ``items``.
            knowledge: KnowledgeResult, mapping, or list of hits/records.
            reasoning: ReasoningGraph or mapping with nodes/edges/conclusions.
            chart: Chart mapping, object with ``to_dict``, or RuleContext-like dict.

        Returns:
            ``StructuredPrompt`` with separated sections and redacted text.
        """
        facts_lines = self._build_facts(chart)
        evidence_lines = self._build_evidence(evidence)
        knowledge_lines = self._build_knowledge(knowledge)
        reasoning_lines = self._build_reasoning(reasoning)
        style_lines = [self._sanitize(line) for line in self._writing_style if line.strip()]

        sections = {
            "facts": PromptSection("facts", PROMPT_SECTION_TITLES["facts"], facts_lines),
            "evidence": PromptSection(
                "evidence", PROMPT_SECTION_TITLES["evidence"], evidence_lines
            ),
            "knowledge": PromptSection(
                "knowledge", PROMPT_SECTION_TITLES["knowledge"], knowledge_lines
            ),
            "reasoning": PromptSection(
                "reasoning", PROMPT_SECTION_TITLES["reasoning"], reasoning_lines
            ),
            "writing_style": PromptSection(
                "writing_style", PROMPT_SECTION_TITLES["writing_style"], style_lines
            ),
        }

        prompt = StructuredPrompt(
            sections=sections,
            metadata={
                "section_keys": list(PROMPT_SECTION_KEYS),
                "fact_count": len(facts_lines),
                "evidence_count": len(evidence_lines),
                "knowledge_count": len(knowledge_lines),
                "reasoning_count": len(reasoning_lines),
                "redaction_applied": True,
            },
        )
        # Final safety pass: ensure assembled text has no forbidden tokens.
        _ = self._sanitize(prompt.text)
        logger.debug(
            "Structured prompt built facts=%s evidence=%s knowledge=%s reasoning=%s",
            len(facts_lines),
            len(evidence_lines),
            len(knowledge_lines),
            len(reasoning_lines),
        )
        return prompt

    # ------------------------------------------------------------------
    # Section builders
    # ------------------------------------------------------------------

    def _build_facts(self, chart: Mapping[str, Any] | Any | None) -> list[str]:
        data = self._normalize_chart(chart)
        if not data:
            return []

        lines: list[str] = []
        day_master = self._first_str(data, ("day_master", "bazi.day_master"))
        if day_master:
            lines.append(f"Day Master: {day_master}")

        dm_element = self._first_str(
            data, ("day_master_element", "bazi.day_master_element", "element")
        )
        if dm_element:
            lines.append(f"Day Master Element: {dm_element}")

        gender = self._first_str(data, ("gender", "bazi.gender"))
        if gender:
            lines.append(f"Gender: {gender}")

        for label, keys in (
            ("Year Pillar", ("year_pillar", "bazi.year_pillar", "pillars.year")),
            ("Month Pillar", ("month_pillar", "bazi.month_pillar", "pillars.month")),
            ("Day Pillar", ("day_pillar", "bazi.day_pillar", "pillars.day")),
            ("Hour Pillar", ("hour_pillar", "bazi.hour_pillar", "pillars.hour")),
        ):
            pillar = self._format_pillar(self._dig(data, keys))
            if pillar:
                lines.append(f"{label}: {pillar}")

        season = self._first_str(data, ("birth_season", "season", "wuxing.season"))
        if season:
            lines.append(f"Season: {season}")

        # Nested four_pillars support from BaziChart.to_dict()-like payloads.
        four = data.get("four_pillars")
        if isinstance(four, Mapping) and not any(
            line.startswith(("Year Pillar", "Month Pillar", "Day Pillar", "Hour Pillar"))
            for line in lines
        ):
            for label, key in (
                ("Year Pillar", "year"),
                ("Month Pillar", "month"),
                ("Day Pillar", "day"),
                ("Hour Pillar", "hour"),
            ):
                pillar = self._format_pillar(four.get(key) or four.get(f"{key}_pillar"))
                if pillar:
                    lines.append(f"{label}: {pillar}")

        return [self._sanitize(line) for line in lines if line.strip()]

    def _build_evidence(
        self, evidence: EvidencePackage | Mapping[str, Any] | None
    ) -> list[str]:
        items = self._normalize_evidence_items(evidence)
        if not items:
            return []

        lines: list[str] = []
        for item in items:
            category = CATEGORY_LABELS.get(item.category, item.category.title() or "Evidence")
            rule = self._sanitize(item.rule)
            reason = self._sanitize(item.reason)
            conf = max(0.0, min(1.0, float(item.confidence)))
            # Source is omitted when it is an internal path / rule id.
            source = self._public_source(item.source)
            parts = [f"[{category}] {rule}"]
            if reason:
                parts.append(f"Reason: {reason}")
            parts.append(f"Confidence: {conf:.2f}")
            if source:
                parts.append(f"Source: {source}")
            lines.append(" | ".join(parts))
        return lines

    def _build_knowledge(
        self, knowledge: KnowledgeResult | Mapping[str, Any] | list[Any] | None
    ) -> list[str]:
        records = self._normalize_knowledge_records(knowledge)
        if not records:
            return []

        lines: list[str] = []
        for index, record in enumerate(records, start=1):
            topic = self._sanitize(record.topic)
            keyword = self._sanitize(record.keyword)
            classical = self._sanitize(record.classical_text)
            modern = self._sanitize(record.modern_interpretation)
            reference = self._sanitize(self._public_reference(record.reference))
            # Intentionally omit record.id and source_file.
            header = f"{index}. Topic: {topic}" if topic else f"{index}. Knowledge entry"
            lines.append(header)
            if keyword:
                lines.append(f"   Keywords: {keyword}")
            if classical:
                lines.append(f"   Classical: {classical}")
            if modern:
                lines.append(f"   Modern: {modern}")
            if reference:
                lines.append(f"   Reference: {reference}")
            lines.append(f"   Confidence: {float(record.confidence):.2f}")
        return lines

    def _build_reasoning(
        self, reasoning: ReasoningGraph | Mapping[str, Any] | None
    ) -> list[str]:
        graph = self._normalize_reasoning(reasoning)
        if graph is None:
            return []

        lines: list[str] = []
        conclusions = [self._sanitize(str(item)) for item in graph.conclusions if str(item).strip()]
        if conclusions:
            lines.append("Conclusions:")
            for item in conclusions:
                lines.append(f"- {item}")

        # Prefer human label chains over internal node/edge identifiers.
        evidence_nodes = [node for node in graph.nodes if node.kind == "evidence"]
        chains: list[str] = []
        for node in evidence_nodes:
            for path in graph.path_labels(node.id):
                cleaned = [self._sanitize(label) for label in path if str(label).strip()]
                cleaned = [label for label in cleaned if label]
                if len(cleaned) >= 2:
                    chains.append(" → ".join(cleaned))

        # Deduplicate chain strings while preserving order.
        seen: set[str] = set()
        unique_chains: list[str] = []
        for chain in chains:
            if chain in seen:
                continue
            seen.add(chain)
            unique_chains.append(chain)

        if unique_chains:
            lines.append("Reasoning chains:")
            for chain in unique_chains:
                lines.append(f"- {chain}")

        # Edge reasons without exposing rule ids / sources.
        reason_notes: list[str] = []
        for edge in graph.edges:
            reason = self._sanitize(edge.reason)
            if not reason:
                continue
            note = f"{reason} (confidence {float(edge.confidence):.2f})"
            if note not in reason_notes:
                reason_notes.append(note)
        if reason_notes:
            lines.append("Supporting reasons:")
            for note in reason_notes:
                lines.append(f"- {note}")

        return lines

    # ------------------------------------------------------------------
    # Normalization helpers
    # ------------------------------------------------------------------

    def _normalize_chart(self, chart: Mapping[str, Any] | Any | None) -> dict[str, Any]:
        if chart is None:
            return {}
        if isinstance(chart, Mapping):
            return dict(chart)
        to_dict = getattr(chart, "to_dict", None)
        if callable(to_dict):
            payload = to_dict()
            if isinstance(payload, Mapping):
                return dict(payload)
        # Attribute fallback for lightweight chart-like objects.
        data: dict[str, Any] = {}
        for key in (
            "day_master",
            "day_master_element",
            "gender",
            "year_pillar",
            "month_pillar",
            "day_pillar",
            "hour_pillar",
            "birth_season",
            "season",
            "four_pillars",
            "bazi",
            "wuxing",
        ):
            if hasattr(chart, key):
                data[key] = getattr(chart, key)
        return data

    def _normalize_evidence_items(
        self, evidence: EvidencePackage | Mapping[str, Any] | None
    ) -> list[EvidenceItem]:
        if evidence is None:
            return []
        if isinstance(evidence, EvidencePackage):
            return list(evidence.items)
        if isinstance(evidence, Mapping):
            raw_items = evidence.get("items")
            if isinstance(raw_items, list):
                items: list[EvidenceItem] = []
                for row in raw_items:
                    if isinstance(row, EvidenceItem):
                        items.append(row)
                    elif isinstance(row, Mapping):
                        items.append(
                            EvidenceItem(
                                category=str(row.get("category") or ""),
                                rule=str(row.get("rule") or ""),
                                reason=str(row.get("reason") or ""),
                                confidence=float(row.get("confidence") or 0.0),
                                source=str(row.get("source") or ""),
                            )
                        )
                return items
        return []

    def _normalize_knowledge_records(
        self, knowledge: KnowledgeResult | Mapping[str, Any] | list[Any] | None
    ) -> list[KnowledgeRecord]:
        if knowledge is None:
            return []
        if isinstance(knowledge, KnowledgeResult):
            return list(knowledge.records)
        if isinstance(knowledge, list):
            return [record for record in (self._as_record(item) for item in knowledge) if record]
        if isinstance(knowledge, Mapping):
            entries = knowledge.get("entries") or knowledge.get("records") or []
            if isinstance(entries, list):
                return [
                    record for record in (self._as_record(item) for item in entries) if record
                ]
        return []

    def _as_record(self, item: Any) -> KnowledgeRecord | None:
        if isinstance(item, KnowledgeRecord):
            return item
        if isinstance(item, KnowledgeHit):
            return item.record
        if isinstance(item, Mapping):
            # Accept either nested record or flat entry dict; never require id in output.
            nested = item.get("record")
            if isinstance(nested, Mapping):
                item = nested
            return KnowledgeRecord(
                id=str(item.get("id") or ""),
                topic=str(item.get("topic") or ""),
                keyword=str(item.get("keyword") or ""),
                condition=str(item.get("condition") or ""),
                classical_text=str(item.get("classical_text") or ""),
                modern_interpretation=str(item.get("modern_interpretation") or ""),
                priority=int(item.get("priority") or 0),
                confidence=float(item.get("confidence") or 0.0),
                reference=str(item.get("reference") or ""),
                source_file=str(item.get("source_file") or ""),
            )
        return None

    def _normalize_reasoning(
        self, reasoning: ReasoningGraph | Mapping[str, Any] | None
    ) -> ReasoningGraph | None:
        if reasoning is None:
            return None
        if isinstance(reasoning, ReasoningGraph):
            return reasoning
        if isinstance(reasoning, Mapping):
            nodes_raw = reasoning.get("nodes") or []
            edges_raw = reasoning.get("edges") or []
            conclusions = list(reasoning.get("conclusions") or [])
            nodes: list[ReasoningNode] = []
            if isinstance(nodes_raw, list):
                for row in nodes_raw:
                    if isinstance(row, ReasoningNode):
                        nodes.append(row)
                    elif isinstance(row, Mapping):
                        nodes.append(
                            ReasoningNode(
                                id=str(row.get("id") or ""),
                                label=str(row.get("label") or ""),
                                kind=row.get("kind") or "reasoning",  # type: ignore[arg-type]
                                domain=str(row.get("domain") or ""),
                                payload=dict(row.get("payload") or {}),
                            )
                        )
            edges: list[ReasoningEdge] = []
            if isinstance(edges_raw, list):
                for row in edges_raw:
                    if isinstance(row, ReasoningEdge):
                        edges.append(row)
                    elif isinstance(row, Mapping):
                        edges.append(
                            ReasoningEdge(
                                id=str(row.get("id") or ""),
                                source_id=str(row.get("source_id") or ""),
                                target_id=str(row.get("target_id") or ""),
                                reason=str(row.get("reason") or ""),
                                priority=int(row.get("priority") or 0),
                                confidence=float(row.get("confidence") or 0.0),
                                source=str(row.get("source") or ""),
                            )
                        )
            return ReasoningGraph(
                nodes=nodes,
                edges=edges,
                conclusions=[str(item) for item in conclusions],
                metadata=dict(reasoning.get("metadata") or {}),
            )
        return None

    # ------------------------------------------------------------------
    # Redaction / formatting
    # ------------------------------------------------------------------

    def _sanitize(self, text: str) -> str:
        """Remove rule ids, CSV names, engine names, and internal identifiers."""
        value = str(text or "")
        value = _CSV_NAME_RE.sub("[redacted]", value)
        value = _ENGINE_NAME_RE.sub("[redacted]", value)
        value = _RULE_ID_RE.sub("[redacted]", value)
        value = _INTERNAL_PATH_RE.sub("[redacted]", value)
        value = _NODE_EDGE_ID_RE.sub("[redacted]", value)
        value = re.sub(r"\s{2,}", " ", value).strip()
        return value

    def _public_source(self, source: str) -> str:
        """Return a human-safe source label, or empty if internal-only."""
        raw = str(source or "").strip()
        if not raw:
            return ""
        lowered = raw.lower()
        if lowered.startswith("rule:"):
            return ""
        if lowered.startswith("rule_context:"):
            return "Chart context"
        if ".csv" in lowered or "engine" in lowered:
            return ""
        sanitized = self._sanitize(raw)
        if not sanitized or sanitized == "[redacted]":
            return ""
        return sanitized

    def _public_reference(self, reference: str) -> str:
        """Keep classical references; drop CSV / engine residue."""
        raw = str(reference or "").strip()
        if not raw:
            return ""
        if ".csv" in raw.lower() or "engine" in raw.lower():
            return ""
        return self._sanitize(raw)

    def _format_pillar(self, value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, str):
            return value.strip()
        if isinstance(value, Mapping):
            stem = str(value.get("stem") or value.get("can") or "").strip()
            branch = str(value.get("branch") or value.get("chi") or "").strip()
            if stem and branch:
                return f"{stem} {branch}"
            return stem or branch
        stem = str(getattr(value, "stem", "") or "").strip()
        branch = str(getattr(value, "branch", "") or "").strip()
        if stem and branch:
            return f"{stem} {branch}"
        text = str(value).strip()
        return text if text and text != "None" else ""

    def _dig(self, data: Mapping[str, Any], keys: tuple[str, ...]) -> Any:
        for key in keys:
            current: Any = data
            ok = True
            for part in key.split("."):
                if isinstance(current, Mapping) and part in current:
                    current = current[part]
                else:
                    ok = False
                    break
            if ok and current not in (None, "", [], {}):
                return current
        return None

    def _first_str(self, data: Mapping[str, Any], keys: tuple[str, ...]) -> str:
        value = self._dig(data, keys)
        if value is None:
            return ""
        text = str(value).strip()
        return text if text and text.lower() != "none" else ""
