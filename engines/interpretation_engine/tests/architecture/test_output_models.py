"""Architecture tests for Pack 03 interpretation output models."""

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


def _metadata() -> Metadata:
    """Build valid output metadata."""
    return Metadata(
        id="meta_1",
        version_info=VersionInfo(
            schema_version="0.0.0-architecture",
            engine_version="0.0.0-architecture",
            model_version="1.0.0",
        ),
        created_at="2026-01-01T00:00:00Z",
        locale="vi",
    )


def test_version_and_trace_validate() -> None:
    """VersionInfo and TraceInformation validate structural fields."""
    version = VersionInfo(schema_version="1.0.0")
    assert version.validate() is True
    trace = TraceInformation(
        trace_id="tr_1",
        pipeline_id="interp_pipe",
        source_final_result_id="fr_1",
        events=("started",),
    )
    assert trace.validate() is True
    assert trace.with_event("finished").events == ("started", "finished")


def test_nested_output_model_validate() -> None:
    """InterpretationResult validates nested section/paragraph/sentence shells."""
    sentence = SentenceResult(
        id="sent_1",
        sentence_ref_id="s_personality_a",
        section_id="sec_1",
        paragraph_id="par_1",
        rank=1,
        template_ref_id="tpl_1",
        placeholder_ref_ids=("ph_1",),
    )
    paragraph = ParagraphResult(
        id="par_1",
        section_id="sec_1",
        title_ref="title_ref_1",
        sentences=(sentence,),
    )
    section = SectionResult(
        id="sec_1",
        section_type="personality",
        title_ref="sec_title_1",
        interpreter_id="interp_personality",
        paragraphs=(paragraph,),
    )
    result = InterpretationResult(
        id="ir_1",
        metadata=_metadata(),
        trace=TraceInformation(
            trace_id="tr_1",
            pipeline_id="interp_pipe",
            source_final_result_id="fr_1",
            interpreter_ids=("interp_personality",),
        ),
        source_final_result_id="fr_1",
        pipeline_id="interp_pipe",
        success=True,
        sections=(section,),
        explanation_refs=("exp_1",),
    )
    assert sentence.validate() is True
    assert paragraph.validate() is True
    assert section.validate() is True
    assert result.validate() is True
    assert result.section_ids() == ("sec_1",)
    assert result.sentence_ref_ids() == ("s_personality_a",)
    assert result.section_for("sec_1") is section
    # No report rendering fields on output models.
    assert not hasattr(result, "text")
    assert not hasattr(sentence, "text")


def test_section_mismatch_fails_validation() -> None:
    """Paragraph/section id mismatches invalidate the aggregate."""
    sentence = SentenceResult(
        id="sent_1",
        sentence_ref_id="s_1",
        section_id="sec_other",
        paragraph_id="par_1",
    )
    paragraph = ParagraphResult(
        id="par_1",
        section_id="sec_1",
        sentences=(sentence,),
    )
    assert paragraph.validate() is False
