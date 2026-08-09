"""IE-1 model and result serialization tests."""

from __future__ import annotations

import json

from engines.interpretation_engine.models.foundation_models import (
    ChapterModel,
    MetadataModel,
    ParagraphModel,
    PlaceholderModel,
    ReferenceModel,
    ResultModel,
    SectionModel,
)


def test_runtime_models_round_trip_without_text() -> None:
    """Runtime models serialize deterministically with empty bodies."""
    result = ResultModel(
        sections=(SectionModel(section_id="sec-1", module_id="overview"),),
        chapters=(ChapterModel(chapter_id="ch-1", section_id="sec-1"),),
        paragraphs=(ParagraphModel(paragraph_id="p-1", chapter_id="ch-1"),),
        references=(
            ReferenceModel(
                reference_id="ref-1",
                source="decision",
                field_path="final_useful_god",
                value_ref="Giáp",
            ),
        ),
        placeholders=(
            PlaceholderModel(placeholder_id="ph-1", binding_path="useful_god.useful_god"),
        ),
        metadata=MetadataModel(module_ids=("overview",)),
    )
    encoded = json.dumps(result.to_dict(), sort_keys=True, ensure_ascii=False)
    decoded = json.loads(encoded)
    assert decoded["status"] == "empty"
    assert decoded["sections"][0]["module_id"] == "overview"
    assert decoded["placeholders"][0]["status"] == "unbound"
    assert "generated_text" not in encoded
    assert "sentence" not in encoded
