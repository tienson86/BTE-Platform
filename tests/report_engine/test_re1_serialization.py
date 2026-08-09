"""RE-1 model and result serialization tests."""

from __future__ import annotations

import json

from engines.report_engine.models.foundation_models import (
    AssetModel,
    BlockModel,
    DocumentModel,
    MetadataModel,
    PlaceholderModel,
    ResultModel,
    SectionModel,
)


def test_runtime_models_round_trip_without_rendering() -> None:
    """Runtime models serialize deterministically with empty bodies."""
    result = ResultModel(
        document=DocumentModel(document_id="doc-1", section_ids=("sec-1",)),
        sections=(SectionModel(section_id="sec-1", module_id="cover"),),
        blocks=(BlockModel(block_id="blk-1", section_id="sec-1"),),
        assets=(
            AssetModel(
                asset_id="ast-1",
                asset_type="chart_ref",
                source_ref="analysis.seasonal",
            ),
        ),
        placeholders=(
            PlaceholderModel(placeholder_id="ph-1", binding_path="useful_god.useful_god"),
        ),
        metadata=MetadataModel(module_ids=("cover",)),
    )
    encoded = json.dumps(result.to_dict(), sort_keys=True, ensure_ascii=False)
    decoded = json.loads(encoded)
    assert decoded["status"] == "empty"
    assert decoded["sections"][0]["module_id"] == "cover"
    assert decoded["placeholders"][0]["status"] == "unbound"
    assert "generated_text" not in encoded
    assert "html" not in encoded
    assert "markdown" not in encoded
    assert "pdf" not in encoded
