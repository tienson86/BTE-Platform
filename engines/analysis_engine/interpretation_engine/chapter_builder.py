"""Chapter Builder — group paragraphs into interpretive chapters."""

from __future__ import annotations

from engines.analysis_engine.interpretation_engine.knowledge_access import (
    ASSET_CHAPTERS,
    ASSET_SECTIONS,
    KnowledgeSession,
)
from engines.analysis_engine.interpretation_engine.models import (
    InterpretationChapter,
    InterpretationParagraph,
    InterpretationSection,
)


class ChapterBuilder:
    """Assemble chapters from paragraphs using Knowledge chapter map."""

    def build(
        self,
        paragraphs: tuple[InterpretationParagraph, ...],
        *,
        session: KnowledgeSession,
    ) -> tuple[InterpretationChapter, ...]:
        """Build ordered chapters; unassigned sections form an extras chapter."""
        chapter_cfg = session.get_asset(ASSET_CHAPTERS).data
        section_cfg = session.get_asset(ASSET_SECTIONS).data
        titles = dict(section_cfg.get("titles") or {})
        paragraph_map = {item.section_id: item for item in paragraphs}

        order = tuple(chapter_cfg.get("order") or ())
        definitions = dict(chapter_cfg.get("definitions") or {})

        section_to_chapter: dict[str, str] = {}
        chapters: list[InterpretationChapter] = []
        assigned: set[str] = set()

        for chapter_id in order:
            definition = dict(definitions.get(chapter_id) or {})
            section_ids = tuple(definition.get("section_ids") or ())
            chapter_sections: list[InterpretationSection] = []
            for section_id in section_ids:
                paragraph = paragraph_map.get(section_id)
                if paragraph is None or not paragraph.text.strip():
                    continue
                section_to_chapter[section_id] = chapter_id
                assigned.add(section_id)
                chapter_sections.append(
                    InterpretationSection(
                        section_id=section_id,
                        title=str(titles.get(section_id) or section_id),
                        paragraphs=(paragraph,),
                        body=paragraph.text,
                        sentence_ids=tuple(
                            sentence.sentence_id for sentence in paragraph.sentences
                        ),
                        source_stages=tuple(
                            dict.fromkeys(
                                sentence.source_stage
                                for sentence in paragraph.sentences
                            )
                        ),
                        chapter_id=chapter_id,
                    )
                )
            if not chapter_sections:
                continue
            body = "\n\n".join(section.body for section in chapter_sections)
            chapters.append(
                InterpretationChapter(
                    chapter_id=chapter_id,
                    title=str(definition.get("title") or chapter_id),
                    section_ids=tuple(section.section_id for section in chapter_sections),
                    body=body,
                    sections=tuple(chapter_sections),
                )
            )

        extras = [
            section_id
            for section_id in sorted(paragraph_map)
            if section_id not in assigned and paragraph_map[section_id].text.strip()
        ]
        if extras:
            extra_sections: list[InterpretationSection] = []
            for section_id in extras:
                paragraph = paragraph_map[section_id]
                extra_sections.append(
                    InterpretationSection(
                        section_id=section_id,
                        title=str(titles.get(section_id) or section_id),
                        paragraphs=(paragraph,),
                        body=paragraph.text,
                        sentence_ids=tuple(
                            sentence.sentence_id for sentence in paragraph.sentences
                        ),
                        source_stages=tuple(
                            dict.fromkeys(
                                sentence.source_stage
                                for sentence in paragraph.sentences
                            )
                        ),
                        chapter_id="extras",
                    )
                )
            chapters.append(
                InterpretationChapter(
                    chapter_id="extras",
                    title="Khác",
                    section_ids=tuple(section.section_id for section in extra_sections),
                    body="\n\n".join(section.body for section in extra_sections),
                    sections=tuple(extra_sections),
                )
            )
        return tuple(chapters)
