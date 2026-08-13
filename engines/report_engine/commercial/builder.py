"""Commercial Report Builder — compose PDF from canonical narrative + features."""

from __future__ import annotations

from typing import Any

from engines.report_engine.commercial.leak_filter import (
    is_feature_available,
    sanitize_paragraphs,
)
from engines.report_engine.commercial.models import (
    COMMERCIAL_REPORT_VERSION,
    CommercialBuildRequest,
    CommercialChapter,
    CommercialCover,
    CommercialFeatureInput,
    CommercialReport,
    CommercialSection,
    ReportAudience,
)
from engines.report_engine.commercial.theme_hook import resolve_theme
from engines.report_engine.narrative_binding import (
    CANONICAL_SECTION_IDS,
    MISSING_NARRATIVE_DIAGNOSTIC,
    NARRATIVE_SOURCE,
    extract_canonical_sections,
    is_usable_narrative_result,
)

_CHAPTER_TITLES = {
    "identity": "Danh tính",
    "career": "Sự nghiệp",
    "executive": "Tư vấn tổng hợp",
}

_GENDER_LABEL = {
    "male": "Nam",
    "female": "Nữ",
    "nam": "Nam",
    "nữ": "Nữ",
    "nu": "Nữ",
}


class CommercialReportBuilder:
    """Assemble Cover → Pack 05 narrative → optional Advisor appendix."""

    version = COMMERCIAL_REPORT_VERSION

    def build(self, request: CommercialBuildRequest) -> CommercialReport:
        """Compose a commercial consulting report from canonical NarrativeResult."""
        audience = (
            ReportAudience.ADVISOR if request.advisor_mode else ReportAudience.CUSTOMER
        )
        theme = resolve_theme(
            primary_theme=request.primary_theme,
            active_theme_ids=list(request.active_theme_ids),
            capacity_level=request.capacity_level,
            has_conflicts=request.has_conflicts,
            purchase_package=request.purchase_package,
            writing_variant=request.writing_variant,
        )
        cover = self._build_cover(request, theme.customer_name)
        narrative_payload = request.narrative_result
        narrative_ok = is_usable_narrative_result(narrative_payload)
        chapters = [self._canonical_narrative_chapter(narrative_payload)]
        supporting: list[CommercialChapter] = []
        identity = self._chapter("identity", request.identity)
        if identity is not None:
            supporting.append(identity)
        career = self._chapter("career", request.career)
        if career is not None:
            supporting.append(career)
        executive = self._chapter("executive", request.executive)
        if executive is not None:
            supporting.append(executive)

        appendix: list[CommercialSection] = []
        if audience == ReportAudience.ADVISOR:
            appendix = self._build_appendix(request)

        return CommercialReport(
            cover=cover,
            chapters=chapters,
            audience=audience,
            theme=theme,
            appendix=appendix,
            supporting_chapters=supporting,
            canonical_narrative=dict(narrative_payload) if narrative_ok else None,
            footer=self._footer(audience),
            version=self.version,
            diagnostics={
                "theme_library": theme.to_dict(),
                "commercial_language": "wired",
                "chapter_ids": [chapter.chapter_id for chapter in chapters],
                "supporting_feature_ids": [item.chapter_id for item in supporting],
                "narrative_source": (
                    NARRATIVE_SOURCE if narrative_ok else MISSING_NARRATIVE_DIAGNOSTIC
                ),
                "canonical_section_ids": [
                    section.section_id for section in chapters[0].sections
                ],
                "parent_context": request.parent_context,
                "audience": audience.value,
            },
        )

    def _canonical_narrative_chapter(
        self,
        payload: dict[str, Any] | None,
    ) -> CommercialChapter:
        """Customer PDF spine from Pack 05 NarrativeResult — no prose rewrite."""
        if not is_usable_narrative_result(payload):
            return CommercialChapter(
                chapter_id="canonical_narrative",
                title="Bản luận Bát tự",
                sections=[
                    CommercialSection(
                        section_id=MISSING_NARRATIVE_DIAGNOSTIC,
                        title="Chẩn đoán",
                        paragraphs=[
                            "Canonical NarrativeResult is required but was not provided.",
                        ],
                    )
                ],
            )
        assert payload is not None
        sections: list[CommercialSection] = []
        extracted = extract_canonical_sections(payload)
        by_id = {item["id"]: item for item in extracted}
        for section_id in CANONICAL_SECTION_IDS:
            item = by_id.get(section_id)
            if item is None:
                continue
            paragraphs = [part for part in item["body"].split("\n\n") if part.strip()]
            if not paragraphs:
                continue
            sections.append(
                CommercialSection(
                    section_id=item["id"],
                    title=item["title"],
                    paragraphs=paragraphs,
                )
            )
        return CommercialChapter(
            chapter_id="canonical_narrative",
            title="Bản luận Bát tự",
            sections=sections,
            available=True,
        )

    def _build_cover(
        self,
        request: CommercialBuildRequest,
        consulting_class: str,
    ) -> CommercialCover:
        heading = "Báo cáo tư vấn"
        subtitle = "Một bản tư vấn — đọc như một cuộc trao đổi, không như bảng tính."
        if request.parent_context:
            heading = "Báo cáo đồng hành phụ huynh"
            subtitle = "Đọc với vai trò phụ huynh — không phải tư vấn nghề người lớn."
        meta_rows: list[tuple[str, str]] = []
        if request.client_name:
            meta_rows.append(("Khách hàng", request.client_name))
        if request.case_id:
            meta_rows.append(("Hồ sơ", request.case_id))
        if request.birth_date:
            meta_rows.append(("Ngày sinh", request.birth_date))
        if request.birth_place:
            meta_rows.append(("Nơi sinh", request.birth_place))
        gender = _GENDER_LABEL.get((request.gender or "").strip().lower(), "")
        if gender:
            meta_rows.append(("Giới tính", gender))
        cover_class = "" if request.parent_context else consulting_class
        if cover_class:
            meta_rows.append(("Hướng tư vấn", cover_class))
        return CommercialCover(
            heading=heading,
            client_name=request.client_name,
            case_id=request.case_id,
            consulting_class=cover_class,
            subtitle=subtitle,
            meta_rows=meta_rows,
        )

    def _chapter(
        self,
        chapter_id: str,
        feature: CommercialFeatureInput | None,
    ) -> CommercialChapter | None:
        if feature is None:
            return None
        if not is_feature_available(feature.status, feature.body):
            return None
        sections: list[CommercialSection] = []
        for section_id, title, paragraphs in feature.sections:
            cleaned = sanitize_paragraphs(list(paragraphs))
            if not cleaned:
                continue
            sections.append(
                CommercialSection(
                    section_id=section_id,
                    title=title,
                    paragraphs=cleaned,
                )
            )
        if not sections:
            body_parts = sanitize_paragraphs(
                [part.strip() for part in (feature.body or "").split("\n\n") if part.strip()]
            )
            if not body_parts:
                return None
            sections.append(
                CommercialSection(
                    section_id=chapter_id,
                    title=_CHAPTER_TITLES[chapter_id],
                    paragraphs=body_parts,
                )
            )
        return CommercialChapter(
            chapter_id=chapter_id,
            title=feature.title or _CHAPTER_TITLES[chapter_id],
            sections=sections,
            available=True,
        )

    def _build_appendix(self, request: CommercialBuildRequest) -> list[CommercialSection]:
        """Advisor-only technical appendix — never customer PDF."""
        sections: list[CommercialSection] = []
        if request.appendix_rows:
            lines = [f"{label}: {value}" for label, value in request.appendix_rows if value]
            if lines:
                sections.append(
                    CommercialSection(
                        section_id="appendix_scores",
                        title="Phụ lục — điểm và chẩn đoán",
                        paragraphs=lines,
                    )
                )
        cleaned = sanitize_paragraphs(list(request.appendix_paragraphs))
        if cleaned:
            sections.append(
                CommercialSection(
                    section_id="appendix_trace",
                    title="Phụ lục — vết luận và bằng chứng",
                    paragraphs=cleaned,
                )
            )
        return sections

    @staticmethod
    def _footer(audience: ReportAudience) -> str:
        if audience == ReportAudience.ADVISOR:
            return "BTE · Bản tư vấn (chế độ cố vấn) · phụ lục kỹ thuật không gửi khách"
        return "BTE · Báo cáo tư vấn"
