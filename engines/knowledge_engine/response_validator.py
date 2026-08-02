"""AI Response Validator — response vs Evidence / Knowledge / Reasoning.

Validates:
- contradiction
- unsupported claims
- missing evidence (paragraph must cite Evidence, Knowledge, Reasoning)
- hallucination risk
- confidence mismatch

Produces ``ValidationReport`` with confidence and warnings.
"""

from __future__ import annotations

import logging
import re
from typing import Any, Mapping

from engines.knowledge_engine.evidence_models import EvidenceItem, EvidencePackage
from engines.knowledge_engine.models import KnowledgeHit, KnowledgeRecord, KnowledgeResult
from engines.knowledge_engine.reasoning_models import (
    ReasoningEdge,
    ReasoningGraph,
    ReasoningNode,
)
from engines.knowledge_engine.validation_models import (
    VALIDATION_CHECKS,
    ParagraphValidation,
    ValidationReport,
    ValidationWarning,
)

logger = logging.getLogger(__name__)

_PARAGRAPH_SPLIT_RE = re.compile(r"\n\s*\n+")
_TOKEN_RE = re.compile(r"[0-9A-Za-zÀ-ỹ_]+", re.UNICODE)
_CLAIMED_CONF_RE = re.compile(
    r"(?i)(?:confidence|độ tin cậy)\s*[:=]?\s*(0?\.\d+|1(?:\.0+)?|\d{1,3})\s*%?"
)
_ABSOLUTE_CLAIM_RE = re.compile(
    r"(?i)\b(chắc chắn|definitely|always|never|guaranteed|không thể sai|"
    r"100%|absolutely)\b"
)

# Explicit citation markers required as Evidence/Knowledge/Reasoning refs.
_EVIDENCE_REF_RE = re.compile(
    r"(?i)(\[evidence\]|\[e\]|\btheo bằng chứng\b|\bbằng chứng:|\bcăn cứ:)"
)
_KNOWLEDGE_REF_RE = re.compile(
    r"(?i)(\[knowledge\]|\[k\]|\btheo tri thức\b|\btheo cổ điển\b|\bkinh điển:|\btri thức:)"
)
_REASONING_REF_RE = re.compile(
    r"(?i)(\[reasoning\]|\[r\]|\btheo lập luận\b|\bchuỗi lập luận\b|\bkết luận:|\blập luận:)"
)

# Polar opposites used for contradiction detection against corpus tokens.
_CONTRADICTION_PAIRS: tuple[tuple[str, str], ...] = (
    ("strong", "weak"),
    ("vượng", "nhược"),
    ("vuong", "nhuoc"),
    ("hot", "cold"),
    ("nóng", "lạnh"),
    ("nong", "lanh"),
    ("warm", "cold"),
    ("favorable", "unfavorable"),
    ("hữu dụng", "bất lợi"),
    ("success", "fail"),
    ("thành", "bại"),
    ("present", "absent"),
)


class AIResponseValidator:
    """Validate AI narrative output against grounded packages."""

    def __init__(
        self,
        *,
        min_support_overlap: float = 0.18,
        confidence_tolerance: float = 0.25,
        pass_confidence_threshold: float = 0.7,
    ) -> None:
        """Configure overlap and confidence thresholds.

        Args:
            min_support_overlap: Minimum token overlap for a claim to count as supported.
            confidence_tolerance: Allowed gap between claimed and support confidence.
            pass_confidence_threshold: Report ``passed`` when overall confidence >= this.
        """
        self._min_support_overlap = max(0.0, float(min_support_overlap))
        self._confidence_tolerance = max(0.0, float(confidence_tolerance))
        self._pass_confidence_threshold = max(0.0, min(1.0, float(pass_confidence_threshold)))

    def validate(
        self,
        response: str,
        *,
        evidence: EvidencePackage | Mapping[str, Any] | None = None,
        knowledge: KnowledgeResult | Mapping[str, Any] | list[Any] | None = None,
        reasoning: ReasoningGraph | Mapping[str, Any] | None = None,
        claimed_confidence: float | None = None,
    ) -> ValidationReport:
        """Validate an AI response against Evidence, Knowledge, and Reasoning.

        Args:
            response: AI-generated narrative text.
            evidence: Evidence package grounding factual claims.
            knowledge: Retrieved classical knowledge.
            reasoning: Reasoning graph conclusions and chains.
            claimed_confidence: Optional explicit confidence asserted by the caller.

        Returns:
            ``ValidationReport`` with confidence, warnings, and per-check results.
        """
        text = str(response or "").strip()
        corpus = self._build_corpus(evidence, knowledge, reasoning)
        paragraphs = self._split_paragraphs(text)
        paragraph_rows: list[ParagraphValidation] = []
        warnings: list[ValidationWarning] = []

        for index, paragraph in enumerate(paragraphs):
            row = self._validate_paragraph(index, paragraph)
            paragraph_rows.append(row)
            warnings.extend(row.warnings)

        warnings.extend(self._check_contradictions(text, corpus))
        warnings.extend(self._check_unsupported_claims(text, corpus, paragraph_rows))
        warnings.extend(self._check_hallucination_risk(text, corpus))
        warnings.extend(
            self._check_confidence_mismatch(
                text,
                corpus,
                claimed_confidence=claimed_confidence,
            )
        )

        checks = self._summarize_checks(warnings, paragraph_rows)
        confidence = self._score_confidence(checks, corpus, paragraph_rows)
        passed = (
            confidence >= self._pass_confidence_threshold
            and checks["contradiction"]["count"] == 0
            and checks["missing_evidence"]["count"] == 0
            and checks["hallucination_risk"]["count"] == 0
        )

        report = ValidationReport(
            confidence=confidence,
            warnings=warnings,
            paragraphs=paragraph_rows,
            checks=checks,
            passed=passed,
            metadata={
                "paragraph_count": len(paragraph_rows),
                "warning_count": len(warnings),
                "corpus_token_count": len(corpus["tokens"]),
                "support_confidence": corpus["support_confidence"],
                "checks": list(VALIDATION_CHECKS),
            },
        )
        logger.debug(
            "AI response validated confidence=%.3f warnings=%s passed=%s",
            confidence,
            len(warnings),
            passed,
        )
        return report

    # ------------------------------------------------------------------
    # Paragraph / reference checks
    # ------------------------------------------------------------------

    def _validate_paragraph(
        self,
        index: int,
        paragraph: str,
    ) -> ParagraphValidation:
        refs_e = bool(_EVIDENCE_REF_RE.search(paragraph))
        refs_k = bool(_KNOWLEDGE_REF_RE.search(paragraph))
        refs_r = bool(_REASONING_REF_RE.search(paragraph))
        warnings: list[ValidationWarning] = []

        missing: list[str] = []
        if not refs_e:
            missing.append("Evidence")
        if not refs_k:
            missing.append("Knowledge")
        if not refs_r:
            missing.append("Reasoning")
        if missing:
            warnings.append(
                ValidationWarning(
                    code="missing_evidence",
                    severity="high",
                    message=(
                        "Paragraph is missing required references: "
                        + ", ".join(missing)
                    ),
                    paragraph_index=index,
                    detail={"missing": missing},
                )
            )

        return ParagraphValidation(
            index=index,
            text=paragraph,
            references_evidence=refs_e,
            references_knowledge=refs_k,
            references_reasoning=refs_r,
            warnings=warnings,
        )

    def _split_paragraphs(self, text: str) -> list[str]:
        if not text:
            return []
        parts = [part.strip() for part in _PARAGRAPH_SPLIT_RE.split(text) if part.strip()]
        if parts:
            return parts
        return [text]

    # ------------------------------------------------------------------
    # Check implementations
    # ------------------------------------------------------------------

    def _check_contradictions(
        self, text: str, corpus: dict[str, Any]
    ) -> list[ValidationWarning]:
        warnings: list[ValidationWarning] = []
        response_tokens = set(self._tokenize(text))
        support_tokens: set[str] = set(corpus["tokens"])
        if not support_tokens or not response_tokens:
            return warnings

        for left, right in _CONTRADICTION_PAIRS:
            left_in_support = left in support_tokens
            right_in_support = right in support_tokens
            left_in_response = left in response_tokens
            right_in_response = right in response_tokens

            if left_in_support and right_in_response and not right_in_support:
                warnings.append(
                    ValidationWarning(
                        code="contradiction",
                        severity="high",
                        message=(
                            f"Response asserts '{right}' while support indicates '{left}'."
                        ),
                        detail={"support": left, "response": right},
                    )
                )
            if right_in_support and left_in_response and not left_in_support:
                warnings.append(
                    ValidationWarning(
                        code="contradiction",
                        severity="high",
                        message=(
                            f"Response asserts '{left}' while support indicates '{right}'."
                        ),
                        detail={"support": right, "response": left},
                    )
                )

        # Conclusion contradiction: response denies a known conclusion label.
        response_lower = text.lower()
        for conclusion in corpus["conclusions"]:
            if not conclusion:
                continue
            conclusion_lower = conclusion.lower()
            if conclusion_lower in response_lower and not re.search(
                rf"(?i)\b(không|not|never)\b.{{0,40}}{re.escape(conclusion)}",
                text,
            ):
                continue
            neg = re.search(
                rf"(?i)\b(không|not|never)\b.{{0,40}}{re.escape(conclusion)}",
                text,
            )
            if neg:
                warnings.append(
                    ValidationWarning(
                        code="contradiction",
                        severity="high",
                        message=f"Response contradicts reasoning conclusion '{conclusion}'.",
                        detail={"conclusion": conclusion},
                    )
                )
        return warnings

    def _check_unsupported_claims(
        self,
        text: str,
        corpus: dict[str, Any],
        paragraphs: list[ParagraphValidation],
    ) -> list[ValidationWarning]:
        warnings: list[ValidationWarning] = []
        support_tokens: set[str] = set(corpus["tokens"])
        if not text.strip():
            return warnings

        for row in paragraphs:
            claim_tokens = [
                token
                for token in self._tokenize(row.text)
                if token not in {"evidence", "knowledge", "reasoning", "e", "k", "r"}
                and len(token) > 2
            ]
            if not claim_tokens:
                continue
            if not support_tokens:
                warnings.append(
                    ValidationWarning(
                        code="unsupported_claims",
                        severity="high",
                        message="Claim has no Evidence/Knowledge/Reasoning corpus to support it.",
                        paragraph_index=row.index,
                    )
                )
                continue
            overlap = len(set(claim_tokens) & support_tokens) / float(len(set(claim_tokens)))
            if overlap < self._min_support_overlap:
                warnings.append(
                    ValidationWarning(
                        code="unsupported_claims",
                        severity="medium",
                        message="Paragraph claim overlap with support corpus is too low.",
                        paragraph_index=row.index,
                        detail={"overlap": round(overlap, 4)},
                    )
                )
        return warnings

    def _check_hallucination_risk(
        self, text: str, corpus: dict[str, Any]
    ) -> list[ValidationWarning]:
        warnings: list[ValidationWarning] = []
        if not text.strip():
            return warnings

        support_tokens: set[str] = set(corpus["tokens"])
        response_tokens = set(self._tokenize(text))
        # Domain-like tokens: Ten Gods / elements style capitalized or known stems.
        stop = {
            "evidence",
            "knowledge",
            "reasoning",
            "paragraph",
            "because",
            "therefore",
            "người",
            "này",
            "có",
            "và",
            "the",
            "and",
            "with",
            "from",
            "this",
            "that",
            "được",
            "trong",
            "theo",
        }
        # Prefer rare/domain tokens absent from corpus (latin stems, multi-word compounds).
        suspicious = sorted(
            token
            for token in response_tokens
            if len(token) >= 4
            and token not in support_tokens
            and token not in stop
            and (
                any(ch.isdigit() for ch in token)
                or "-" in token
                or token
                in {
                    "jupiter",
                    "mars",
                    "zodiac",
                    "horoscope",
                    "tarot",
                    "quantum",
                }
            )
        )

        absolute = bool(_ABSOLUTE_CLAIM_RE.search(text))
        unknown_ratio = (
            (len(set(response_tokens) - support_tokens - stop) / float(len(response_tokens)))
            if response_tokens
            else 0.0
        )
        if absolute and not support_tokens:
            warnings.append(
                ValidationWarning(
                    code="hallucination_risk",
                    severity="high",
                    message="Absolute claim without any supporting corpus.",
                    detail={"absolute": True},
                )
            )
        elif absolute and (suspicious or unknown_ratio >= 0.45):
            warnings.append(
                ValidationWarning(
                    code="hallucination_risk",
                    severity="high",
                    message="Absolute wording with unsupported or foreign terms.",
                    detail={
                        "unknown_ratio": round(unknown_ratio, 4),
                        "samples": suspicious[:8],
                    },
                )
            )
        elif len(suspicious) >= 2 and unknown_ratio >= 0.4:
            warnings.append(
                ValidationWarning(
                    code="hallucination_risk",
                    severity="medium",
                    message="Multiple unsupported domain terms suggest hallucination risk.",
                    detail={
                        "unknown_ratio": round(unknown_ratio, 4),
                        "samples": suspicious[:8],
                    },
                )
            )
        return warnings

    def _check_confidence_mismatch(
        self,
        text: str,
        corpus: dict[str, Any],
        *,
        claimed_confidence: float | None,
    ) -> list[ValidationWarning]:
        warnings: list[ValidationWarning] = []
        support_conf = float(corpus["support_confidence"])
        claimed = claimed_confidence
        if claimed is None:
            claimed = self._extract_claimed_confidence(text)
        if claimed is None:
            # Absolute language implies near-certain confidence.
            if _ABSOLUTE_CLAIM_RE.search(text):
                claimed = 0.95
            else:
                return warnings

        claimed_value = float(claimed)
        if claimed_value > 1.0:
            claimed_value = claimed_value / 100.0
        claimed_value = max(0.0, min(1.0, claimed_value))

        gap = abs(claimed_value - support_conf)
        if gap > self._confidence_tolerance:
            warnings.append(
                ValidationWarning(
                    code="confidence_mismatch",
                    severity="medium" if gap < 0.45 else "high",
                    message=(
                        "Claimed confidence diverges from Evidence/Knowledge/Reasoning support."
                    ),
                    detail={
                        "claimed_confidence": round(claimed_value, 4),
                        "support_confidence": round(support_conf, 4),
                        "gap": round(gap, 4),
                    },
                )
            )
        return warnings

    # ------------------------------------------------------------------
    # Scoring / summary
    # ------------------------------------------------------------------

    def _summarize_checks(
        self,
        warnings: list[ValidationWarning],
        paragraphs: list[ParagraphValidation],
    ) -> dict[str, dict[str, Any]]:
        checks: dict[str, dict[str, Any]] = {}
        for code in VALIDATION_CHECKS:
            rows = [row for row in warnings if row.code == code]
            checks[code] = {
                "count": len(rows),
                "passed": len(rows) == 0,
                "severities": sorted({row.severity for row in rows}),
            }
        checks["missing_evidence"]["paragraphs_missing_refs"] = sum(
            1 for row in paragraphs if not row.references_all
        )
        return checks

    def _score_confidence(
        self,
        checks: dict[str, dict[str, Any]],
        corpus: dict[str, Any],
        paragraphs: list[ParagraphValidation],
    ) -> float:
        score = 1.0
        penalties = {
            "contradiction": 0.28,
            "unsupported_claims": 0.16,
            "missing_evidence": 0.22,
            "hallucination_risk": 0.24,
            "confidence_mismatch": 0.12,
        }
        for code, penalty in penalties.items():
            count = int(checks.get(code, {}).get("count") or 0)
            if count:
                score -= penalty * min(count, 3)

        if paragraphs:
            grounded = sum(1 for row in paragraphs if row.references_all)
            score *= 0.55 + 0.45 * (grounded / float(len(paragraphs)))
        else:
            score *= 0.4

        support = float(corpus.get("support_confidence") or 0.0)
        if support > 0:
            score = 0.7 * score + 0.3 * support
        else:
            score *= 0.75

        return round(max(0.0, min(1.0, score)), 4)

    # ------------------------------------------------------------------
    # Corpus helpers
    # ------------------------------------------------------------------

    def _build_corpus(
        self,
        evidence: EvidencePackage | Mapping[str, Any] | None,
        knowledge: KnowledgeResult | Mapping[str, Any] | list[Any] | None,
        reasoning: ReasoningGraph | Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        texts: list[str] = []
        confidences: list[float] = []
        conclusions: list[str] = []

        for item in self._evidence_items(evidence):
            texts.append(item.rule)
            texts.append(item.reason)
            texts.append(item.category)
            confidences.append(float(item.confidence))

        for record in self._knowledge_records(knowledge):
            texts.extend(
                [
                    record.topic,
                    record.keyword,
                    record.classical_text,
                    record.modern_interpretation,
                    record.reference,
                ]
            )
            confidences.append(float(record.confidence))

        graph = self._reasoning_graph(reasoning)
        if graph is not None:
            for node in graph.nodes:
                texts.append(node.label)
                texts.append(node.domain)
            for edge in graph.edges:
                texts.append(edge.reason)
                confidences.append(float(edge.confidence))
            conclusions = [
                str(item).strip() for item in graph.conclusions if str(item).strip()
            ]
            texts.extend(graph.conclusions)

        tokens: set[str] = set()
        for chunk in texts:
            tokens.update(self._tokenize(str(chunk)))

        support_confidence = (
            sum(confidences) / float(len(confidences)) if confidences else 0.0
        )
        return {
            "tokens": tokens,
            "support_confidence": max(0.0, min(1.0, support_confidence)),
            "conclusions": conclusions,
            "texts": texts,
        }

    def _evidence_items(
        self, evidence: EvidencePackage | Mapping[str, Any] | None
    ) -> list[EvidenceItem]:
        if evidence is None:
            return []
        if isinstance(evidence, EvidencePackage):
            return list(evidence.items)
        if isinstance(evidence, Mapping):
            rows = evidence.get("items") or []
            items: list[EvidenceItem] = []
            if isinstance(rows, list):
                for row in rows:
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

    def _knowledge_records(
        self, knowledge: KnowledgeResult | Mapping[str, Any] | list[Any] | None
    ) -> list[KnowledgeRecord]:
        if knowledge is None:
            return []
        if isinstance(knowledge, KnowledgeResult):
            return list(knowledge.records)
        if isinstance(knowledge, list):
            return [row for row in (self._as_record(item) for item in knowledge) if row]
        if isinstance(knowledge, Mapping):
            rows = knowledge.get("entries") or knowledge.get("records") or []
            if isinstance(rows, list):
                return [row for row in (self._as_record(item) for item in rows) if row]
        return []

    def _as_record(self, item: Any) -> KnowledgeRecord | None:
        if isinstance(item, KnowledgeRecord):
            return item
        if isinstance(item, KnowledgeHit):
            return item.record
        if isinstance(item, Mapping):
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
                chapter=str(item.get("chapter") or ""),
                page=str(item.get("page") or ""),
                citation_id=str(item.get("citation_id") or ""),
            )
        return None

    def _reasoning_graph(
        self, reasoning: ReasoningGraph | Mapping[str, Any] | None
    ) -> ReasoningGraph | None:
        if reasoning is None:
            return None
        if isinstance(reasoning, ReasoningGraph):
            return reasoning
        if isinstance(reasoning, Mapping):
            nodes = []
            for row in reasoning.get("nodes") or []:
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
            edges = []
            for row in reasoning.get("edges") or []:
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
                conclusions=[str(item) for item in (reasoning.get("conclusions") or [])],
                metadata=dict(reasoning.get("metadata") or {}),
            )
        return None

    def _tokenize(self, text: str) -> list[str]:
        return [token.lower() for token in _TOKEN_RE.findall(str(text or ""))]

    def _extract_claimed_confidence(self, text: str) -> float | None:
        match = _CLAIMED_CONF_RE.search(text or "")
        if not match:
            return None
        raw = match.group(1)
        try:
            value = float(raw)
        except ValueError:
            return None
        if value > 1.0:
            value = value / 100.0
        return max(0.0, min(1.0, value))
