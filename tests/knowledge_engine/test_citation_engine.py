"""Unit tests for Citation Engine (Epic 03 Milestone 08)."""

from __future__ import annotations

from engines.knowledge_engine import (
    CLASSICAL_SOURCE_KEYS,
    CitationEngine,
    KnowledgeHit,
    KnowledgeRecord,
    KnowledgeResult,
    PromptBuilder,
)


def _record(
    record_id: str,
    reference: str,
    *,
    chapter: str = "",
    page: str = "",
    citation_id: str = "",
    topic: str = "ten_gods",
) -> KnowledgeRecord:
    return KnowledgeRecord(
        id=record_id,
        topic=topic,
        keyword="officer",
        condition="",
        classical_text="classical",
        modern_interpretation="modern",
        priority=10,
        confidence=0.9,
        reference=reference,
        chapter=chapter,
        page=page,
        citation_id=citation_id,
    )


class TestCitationEngine:
    def test_supports_four_classical_sources_and_other(self) -> None:
        engine = CitationEngine()
        knowledge = KnowledgeResult(
            entries=[
                KnowledgeHit(
                    record=_record("KNW-1", "Uyên Hải Tử Bình|chương 2|trang 15"),
                    keyword_score=1.0,
                    condition_score=1.0,
                    relevance_score=1.0,
                ),
                KnowledgeHit(
                    record=_record("KNW-2", "Tam Mệnh Thông Hội, chapter 4, page 88"),
                    keyword_score=1.0,
                    condition_score=1.0,
                    relevance_score=1.0,
                ),
                KnowledgeHit(
                    record=_record("KNW-3", "滴天髓"),
                    keyword_score=1.0,
                    condition_score=1.0,
                    relevance_score=1.0,
                ),
                KnowledgeHit(
                    record=_record("KNW-4", "Zi Ping Zhen Quan"),
                    keyword_score=1.0,
                    condition_score=1.0,
                    relevance_score=1.0,
                ),
                KnowledgeHit(
                    record=_record("KNW-5", "Đế Thiên Tùy Bút"),
                    keyword_score=1.0,
                    condition_score=1.0,
                    relevance_score=1.0,
                ),
            ],
            metadata={},
        )
        package = engine.build(knowledge)
        assert set(CLASSICAL_SOURCE_KEYS) >= set(package.by_source_key)
        assert package.for_source("uyen_hai_tu_binh")
        assert package.for_source("tam_menh_thong_hoi")
        assert package.for_source("dich_thien_tuy")
        assert package.for_source("tu_binh_chan_thuyen")
        assert package.for_source("other")
        assert package.citations[0].reference == "Uyên Hải Tử Bình"
        assert package.citations[0].chapter == "2"
        assert package.citations[0].page == "15"
        assert package.citations[0].citation_id.startswith("CIT-UHBP")

    def test_record_supports_reference_chapter_page_citation_id(self) -> None:
        record = _record(
            "KNW-X",
            "Tử Bình Chân Thuyên",
            chapter="3",
            page="21",
            citation_id="CIT-TBCT-C3-P21-KNW-X",
        )
        fields = record.citation_fields()
        assert fields["reference"] == "Tử Bình Chân Thuyên"
        assert fields["chapter"] == "3"
        assert fields["page"] == "21"
        assert fields["citation_id"] == "CIT-TBCT-C3-P21-KNW-X"

        package = CitationEngine().build([record])
        citation = package.for_record("KNW-X")
        assert citation is not None
        assert citation.chapter == "3"
        assert citation.page == "21"
        assert citation.citation_id == "CIT-TBCT-C3-P21-KNW-X"

    def test_internal_render_default_hides_visible_bibliography(self) -> None:
        package = CitationEngine().build(
            [_record("KNW-1", "Uyên Hải Tử Bình|chương 1|trang 9")]
        )
        internal = CitationEngine().render(package, visible=False)
        visible = CitationEngine().render(package, visible=True)
        assert "## Internal Sources" in internal
        assert "Do not display citation ids" in internal
        assert "CIT-" in internal
        assert "## References" not in internal
        assert "## References" in visible
        assert "Uyên Hải Tử Bình" in visible
        assert "CIT-" not in visible
        assert package.metadata["visible_by_default"] is False

    def test_prompt_uses_internal_citations_unless_requested(self) -> None:
        knowledge = KnowledgeResult(
            entries=[
                KnowledgeHit(
                    record=_record(
                        "KNW-1",
                        "Tam Mệnh Thông Hội|chương 7|trang 33",
                    ),
                    keyword_score=1.0,
                    condition_score=1.0,
                    relevance_score=1.0,
                )
            ],
            metadata={},
        )
        hidden = PromptBuilder().build(knowledge=knowledge, show_citations=False)
        shown = PromptBuilder().build(knowledge=knowledge, show_citations=True)

        knowledge_section = hidden.section("knowledge")
        assert knowledge_section is not None
        assert "Reference:" not in knowledge_section.content
        assert "## Internal Sources" in hidden.text
        assert "## References" not in hidden.text
        assert hidden.metadata["citations_visible"] is False

        assert "## References" in shown.text
        assert shown.metadata["citations_visible"] is True

    def test_parse_inline_markers_and_mapping_input(self) -> None:
        engine = CitationEngine()
        parsed = engine.parse_reference_fields(
            "Tích Thiên Tủy chapter=5 page=12 CIT-DTT-DEMO"
        )
        assert engine.resolve_source_key(parsed["reference"]) == "dich_thien_tuy"
        assert parsed["chapter"] == "5"
        assert parsed["page"] == "12"
        assert "CIT-DTT-DEMO" in parsed["citation_id"].upper()

        package = engine.build(
            {
                "entries": [
                    {
                        "id": "KNW-MAP",
                        "topic": "strength",
                        "keyword": "strong",
                        "condition": "",
                        "classical_text": "x",
                        "modern_interpretation": "y",
                        "priority": 1,
                        "confidence": 0.8,
                        "reference": "渊海子平",
                        "chapter": "9",
                        "page": "100",
                    }
                ]
            }
        )
        citation = package.for_record("KNW-MAP")
        assert citation is not None
        assert citation.source_key == "uyen_hai_tu_binh"
        assert citation.chapter == "9"
        assert citation.page == "100"
        assert citation.to_dict()["citation_id"]

    def test_empty_knowledge(self) -> None:
        package = CitationEngine().build(None)
        assert package.citations == []
        assert CitationEngine().render(package) == ""
