"""Interpretation output model infrastructure tests (no report rendering)."""

from __future__ import annotations

from engines.interpretation_engine.models import (
    InterpretationResult,
    Metadata,
    ParagraphResult,
    SectionResult,
    SentenceResult,
    TraceInformation,
    VersionInfo,
)


def _metadata(**kwargs) -> Metadata:
    """Build metadata for output tests."""
    return Metadata(
        id=kwargs.get("id", "meta_1"),
        version_info=kwargs.get(
            "version_info",
            VersionInfo(schema_version="1.0.0"),
        ),
        created_at=kwargs.get("created_at", "2026-01-01T00:00:00Z"),
        locale=kwargs.get("locale", "vi"),
    )


class TestOutputModelsInfrastructure:
    """Mock-only interpretation output model coverage."""

    def test_valid_aggregate_and_helpers(self) -> None:
        """Nested output models validate and expose helpers."""
        sentence = SentenceResult(
            id="sent_1",
            sentence_ref_id="s_1",
            section_id="sec_1",
            paragraph_id="par_1",
            rank=1,
            score=1.0,
        )
        paragraph = ParagraphResult(
            id="par_1",
            section_id="sec_1",
            sentences=(sentence,),
        )
        section = SectionResult(
            id="sec_1",
            section_type="personality",
            paragraphs=(paragraph,),
            interpreter_id="interp_personality",
        )
        result = InterpretationResult(
            id="ir_1",
            metadata=_metadata(),
            trace=TraceInformation(
                trace_id="tr_1",
                pipeline_id="pipe",
                source_final_result_id="fr_1",
            ),
            source_final_result_id="fr_1",
            pipeline_id="pipe",
            success=True,
            sections=(section,),
        )
        assert result.validate() is True
        assert result.section_ids() == ("sec_1",)
        assert result.section_for("sec_1") is section
        assert result.section_for("missing") is None
        assert result.sentence_ref_ids() == ("s_1",)
        assert section.paragraph_ids() == ("par_1",)
        assert section.sentence_ref_ids() == ("s_1",)
        assert paragraph.sentence_ref_ids() == ("s_1",)
        assert not hasattr(result, "text")

    def test_validation_failure_paths(self) -> None:
        """Structural mismatches invalidate models."""
        assert VersionInfo(schema_version="").validate() is False
        assert TraceInformation(trace_id="").validate() is False
        assert _metadata(id="").validate() is False
        assert _metadata(version_info=VersionInfo(schema_version="")).validate() is False
        assert SentenceResult(id="", sentence_ref_id="s").validate() is False
        assert SentenceResult(id="s", sentence_ref_id="s", rank=0).validate() is False
        bad_sentence = SentenceResult(
            id="sent",
            sentence_ref_id="s",
            section_id="other",
            paragraph_id="par_1",
        )
        paragraph = ParagraphResult(
            id="par_1",
            section_id="sec_1",
            sentences=(bad_sentence,),
        )
        assert paragraph.validate() is False
        assert ParagraphResult(id="", section_id="sec").validate() is False

        good_sentence = SentenceResult(
            id="sent",
            sentence_ref_id="s",
            section_id="sec_1",
            paragraph_id="par_1",
        )
        good_paragraph = ParagraphResult(
            id="par_1",
            section_id="sec_other",
            sentences=(good_sentence,),
        )
        section = SectionResult(
            id="sec_1",
            section_type="personality",
            paragraphs=(good_paragraph,),
        )
        assert section.validate() is False
        assert SectionResult(id="", section_type="x").validate() is False

        result = InterpretationResult(
            id="",
            metadata=_metadata(),
            trace=TraceInformation(trace_id="tr"),
            source_final_result_id="fr",
            pipeline_id="pipe",
            success=True,
        )
        assert result.validate() is False

        mismatch_trace = InterpretationResult(
            id="ir",
            metadata=_metadata(),
            trace=TraceInformation(
                trace_id="tr",
                pipeline_id="other",
                source_final_result_id="fr",
            ),
            source_final_result_id="fr",
            pipeline_id="pipe",
            success=True,
        )
        assert mismatch_trace.validate() is False

        mismatch_source = InterpretationResult(
            id="ir",
            metadata=_metadata(),
            trace=TraceInformation(
                trace_id="tr",
                pipeline_id="pipe",
                source_final_result_id="other",
            ),
            source_final_result_id="fr",
            pipeline_id="pipe",
            success=True,
        )
        assert mismatch_source.validate() is False

        bad_section_result = InterpretationResult(
            id="ir",
            metadata=_metadata(),
            trace=TraceInformation(trace_id="tr", pipeline_id="pipe"),
            source_final_result_id="fr",
            pipeline_id="pipe",
            success=True,
            sections=(SectionResult(id="", section_type="x"),),
        )
        assert bad_section_result.validate() is False
