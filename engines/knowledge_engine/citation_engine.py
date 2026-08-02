"""Citation Engine — knowledge records → classical citations.

Supports:
- Uyên Hải Tử Bình
- Tam Mệnh Thông Hội
- Tích Thiên Tủy
- Tử Bình Chân Thuyên
- Other classical references

Each citation stores: reference, chapter, page, citation id.
AI receives citations internally; visible bibliography only when requested.
"""

from __future__ import annotations

import hashlib
import logging
import re
from typing import Any, Mapping

from engines.knowledge_engine.citation_models import (
    CLASSICAL_SOURCE_KEYS,
    CLASSICAL_SOURCES,
    Citation,
    CitationPackage,
)
from engines.knowledge_engine.models import KnowledgeHit, KnowledgeRecord, KnowledgeResult

logger = logging.getLogger(__name__)

_PIPE_SPLIT_RE = re.compile(r"\s*[|｜]\s*")
_CHAPTER_RE = re.compile(
    r"(?i)\b(?:chapter|chương|chuong|ch\.?|quyển|quyen|卷)\s*[=:]?\s*([0-9A-Za-zÀ-ỹ\-]+)"
)
_PAGE_RE = re.compile(
    r"(?i)\b(?:page|trang|tr\.|p\.|頁|页)\s*[=:]?\s*([0-9A-Za-z\-]+)"
)
_CITATION_ID_RE = re.compile(r"(?i)\b(?:CIT[-_]?[A-Z0-9\-]+)\b")


class CitationEngine:
    """Build and render classical citations from knowledge records."""

    def build(
        self,
        knowledge: KnowledgeResult | Mapping[str, Any] | list[Any] | None,
    ) -> CitationPackage:
        """Create a citation package from knowledge hits/records.

        Args:
            knowledge: KnowledgeResult, mapping, or list of records/hits.

        Returns:
            ``CitationPackage`` with one citation per knowledge record that has
            enough identity to cite (record id and/or reference text).
        """
        records = self._normalize_records(knowledge)
        citations: list[Citation] = []
        by_record: dict[str, Citation] = {}
        by_source: dict[str, list[Citation]] = {key: [] for key in CLASSICAL_SOURCE_KEYS}

        for record in records:
            citation = self._citation_from_record(record)
            if citation is None:
                continue
            citations.append(citation)
            if citation.record_id:
                by_record[citation.record_id] = citation
            by_source.setdefault(citation.source_key, []).append(citation)

        package = CitationPackage(
            citations=citations,
            by_record_id=by_record,
            by_source_key=by_source,
            metadata={
                "citation_count": len(citations),
                "source_counts": {
                    key: len(rows) for key, rows in by_source.items() if rows
                },
                "supported_sources": [
                    CLASSICAL_SOURCES[key]["title"] for key in CLASSICAL_SOURCE_KEYS
                ],
                "visible_by_default": False,
            },
        )
        logger.debug("Citation package built count=%s", len(citations))
        return package

    def render(
        self,
        package: CitationPackage | None,
        *,
        visible: bool = False,
    ) -> str:
        """Render citations for AI (internal) or user (visible).

        Args:
            package: Citation package from ``build``.
            visible: When False (default), emit an internal-only block for the AI.
                When True, emit a user-facing bibliography without internal ids.

        Returns:
            Rendered citation text (empty when package has no citations).
        """
        if package is None or not package.citations:
            return ""

        if visible:
            lines = ["## References"]
            for index, citation in enumerate(package.citations, start=1):
                lines.append(f"{index}. {citation.visible_label()}")
            return "\n".join(lines).strip() + "\n"

        lines = [
            "## Internal Sources",
            "Use these knowledge sources for grounding.",
            "Do not display citation ids, chapter/page markers, or bibliography "
            "to the user unless citations are explicitly requested.",
        ]
        for citation in package.citations:
            lines.append(f"- {citation.internal_label()}")
        return "\n".join(lines).strip() + "\n"

    def resolve_source_key(self, reference: str) -> str:
        """Map free-text reference to a classical source key."""
        raw = str(reference or "").strip()
        text = self._normalize_text(raw)
        if not raw:
            return "other"
        lowered_raw = raw.lower()
        for key in CLASSICAL_SOURCE_KEYS:
            if key == "other":
                continue
            meta = CLASSICAL_SOURCES[key]
            title = str(meta["title"])
            if title and title.lower() in lowered_raw:
                return key
            title_norm = self._normalize_text(title)
            if text and title_norm and title_norm in text:
                return key
            for alias in meta.get("aliases") or ():
                alias_text = str(alias)
                if alias_text and alias_text in raw:
                    return key
                alias_norm = self._normalize_text(alias_text)
                if text and alias_norm and alias_norm in text:
                    return key
        return "other"

    def parse_reference_fields(
        self,
        reference: str,
        *,
        chapter: str = "",
        page: str = "",
        citation_id: str = "",
    ) -> dict[str, str]:
        """Parse reference / chapter / page / citation id from record fields.

        Supports structured ``reference`` values such as:
        ``Uyên Hải Tử Bình|chương 5|trang 12``
        or inline markers inside a single reference string.
        """
        raw = str(reference or "").strip()
        chapter_value = str(chapter or "").strip()
        page_value = str(page or "").strip()
        citation_value = str(citation_id or "").strip()
        work = raw

        if raw and _PIPE_SPLIT_RE.search(raw):
            parts = [part.strip() for part in _PIPE_SPLIT_RE.split(raw) if part.strip()]
            if parts:
                work = parts[0]
            if len(parts) >= 2 and not chapter_value:
                chapter_value = self._strip_label(parts[1], kind="chapter")
            if len(parts) >= 3 and not page_value:
                page_value = self._strip_label(parts[2], kind="page")
            if len(parts) >= 4 and not citation_value:
                maybe_id = parts[3]
                if _CITATION_ID_RE.fullmatch(maybe_id) or maybe_id.upper().startswith("CIT"):
                    citation_value = maybe_id

        if not chapter_value:
            match = _CHAPTER_RE.search(raw)
            if match:
                chapter_value = match.group(1).strip()
        if not page_value:
            match = _PAGE_RE.search(raw)
            if match:
                page_value = match.group(1).strip()
        if not citation_value:
            match = _CITATION_ID_RE.search(raw)
            if match:
                citation_value = match.group(0).strip()

        # Prefer clean work title without trailing chapter/page markers.
        work = _CHAPTER_RE.sub("", work)
        work = _PAGE_RE.sub("", work)
        work = _CITATION_ID_RE.sub("", work)
        work = re.sub(r"\s{2,}", " ", work).strip(" ,;-")

        return {
            "reference": work or raw,
            "chapter": chapter_value,
            "page": page_value,
            "citation_id": citation_value,
        }

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _citation_from_record(self, record: KnowledgeRecord) -> Citation | None:
        record_id = str(record.id or "").strip()
        explicit_chapter = str(getattr(record, "chapter", "") or "").strip()
        explicit_page = str(getattr(record, "page", "") or "").strip()
        explicit_citation_id = str(getattr(record, "citation_id", "") or "").strip()

        parsed = self.parse_reference_fields(
            record.reference,
            chapter=explicit_chapter,
            page=explicit_page,
            citation_id=explicit_citation_id,
        )
        reference = parsed["reference"]
        if not record_id and not reference:
            return None

        source_key = self.resolve_source_key(reference or record.reference)
        canonical = str(CLASSICAL_SOURCES[source_key]["title"])
        # Keep non-catalog free-text when classified as other.
        display_reference = canonical if source_key != "other" else (reference or "Classical source")
        if source_key == "other" and not display_reference:
            display_reference = "Other classical references"

        citation_id = parsed["citation_id"] or self._make_citation_id(
            source_key=source_key,
            record_id=record_id,
            chapter=parsed["chapter"],
            page=parsed["page"],
        )

        return Citation(
            citation_id=citation_id,
            reference=display_reference,
            chapter=parsed["chapter"],
            page=parsed["page"],
            record_id=record_id,
            source_key=source_key,
            topic=str(record.topic or ""),
            confidence=float(record.confidence or 0.0),
        )

    def _make_citation_id(
        self,
        *,
        source_key: str,
        record_id: str,
        chapter: str,
        page: str,
    ) -> str:
        code = str(CLASSICAL_SOURCES.get(source_key, CLASSICAL_SOURCES["other"])["code"])
        parts = ["CIT", code]
        if chapter:
            parts.append(f"C{self._slug(chapter)}")
        if page:
            parts.append(f"P{self._slug(page)}")
        if record_id:
            digest = hashlib.sha1(record_id.encode("utf-8")).hexdigest()[:8].upper()
            parts.append(digest)
        else:
            parts.append("NA")
        return "-".join(parts)

    def _normalize_records(
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

    def _normalize_text(self, value: str) -> str:
        text = str(value or "").strip().lower()
        text = text.replace("đ", "d")
        # Fold common Vietnamese tones for alias matching.
        replacements = str.maketrans(
            {
                "á": "a",
                "à": "a",
                "ả": "a",
                "ã": "a",
                "ạ": "a",
                "ă": "a",
                "ắ": "a",
                "ằ": "a",
                "ẳ": "a",
                "ẵ": "a",
                "ặ": "a",
                "â": "a",
                "ấ": "a",
                "ầ": "a",
                "ẩ": "a",
                "ẫ": "a",
                "ậ": "a",
                "é": "e",
                "è": "e",
                "ẻ": "e",
                "ẽ": "e",
                "ẹ": "e",
                "ê": "e",
                "ế": "e",
                "ề": "e",
                "ể": "e",
                "ễ": "e",
                "ệ": "e",
                "í": "i",
                "ì": "i",
                "ỉ": "i",
                "ĩ": "i",
                "ị": "i",
                "ó": "o",
                "ò": "o",
                "ỏ": "o",
                "õ": "o",
                "ọ": "o",
                "ô": "o",
                "ố": "o",
                "ồ": "o",
                "ổ": "o",
                "ỗ": "o",
                "ộ": "o",
                "ơ": "o",
                "ớ": "o",
                "ờ": "o",
                "ở": "o",
                "ỡ": "o",
                "ợ": "o",
                "ú": "u",
                "ù": "u",
                "ủ": "u",
                "ũ": "u",
                "ụ": "u",
                "ư": "u",
                "ứ": "u",
                "ừ": "u",
                "ử": "u",
                "ữ": "u",
                "ự": "u",
                "ý": "y",
                "ỳ": "y",
                "ỷ": "y",
                "ỹ": "y",
                "ỵ": "y",
            }
        )
        text = text.translate(replacements)
        return re.sub(r"[^a-z0-9]+", "", text)

    def _slug(self, value: str) -> str:
        text = re.sub(r"[^A-Za-z0-9]+", "-", str(value or "").strip()).strip("-")
        return text.upper() or "X"

    def _strip_label(self, value: str, *, kind: str) -> str:
        raw = str(value or "").strip()
        if kind == "chapter":
            match = _CHAPTER_RE.search(raw)
            if match:
                return match.group(1).strip()
            return re.sub(r"(?i)^(chapter|chương|chuong|ch\.?|quyển|quyen)\s*", "", raw).strip()
        match = _PAGE_RE.search(raw)
        if match:
            return match.group(1).strip()
        return re.sub(r"(?i)^(page|trang|tr\.|p\.)\s*", "", raw).strip()
