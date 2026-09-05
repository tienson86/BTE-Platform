"""P7-IMP-01 foundation: serializable Pack 07 runtime contract shells."""

from __future__ import annotations

import json

from engines.core.register_engines import is_registered, register_all_engines
from engines.detailed_interpretation_engine.constants import SCHEMA_RUNTIME_CONTRACT
from engines.detailed_interpretation_engine.factories import (
    api_model_from_runtime,
    consulting_model_from_runtime,
    empty_canonical_runtime_result,
    export_model_from_runtime,
)
from engines.detailed_interpretation_engine.schema_registry import registered_schema_ids
from engines.detailed_interpretation_engine.serialization import (
    deserialize_runtime_result,
    dumps_runtime_result,
    loads_runtime_result,
    serialize_runtime_result,
)
from engines.detailed_interpretation_engine.service import DetailedInterpretationService


def test_empty_runtime_preserves_analysis_id_and_versions() -> None:
    result = empty_canonical_runtime_result("an-p7-001", chart_id="chart-1")
    assert result.analysis_id == "an-p7-001"
    assert result.identity.analysis_id == "an-p7-001"
    assert result.metadata.analysis_id == "an-p7-001"
    assert result.metadata.contract_version == SCHEMA_RUNTIME_CONTRACT
    assert result.metadata.content_hash
    assert result.optimization.state.value == "not_evaluated"
    assert result.domains.authority.natal.domain_id == "authority"


def test_serialize_deserialize_roundtrip() -> None:
    original = empty_canonical_runtime_result("an-p7-002")
    payload = serialize_runtime_result(original)
    restored = deserialize_runtime_result(payload)
    assert restored.analysis_id == "an-p7-002"
    assert restored.metadata.contract_version == original.metadata.contract_version
    assert restored.metadata.content_hash == original.metadata.content_hash
    again = serialize_runtime_result(restored)
    assert json.dumps(payload, sort_keys=True) == json.dumps(again, sort_keys=True)


def test_json_dumps_loads_roundtrip() -> None:
    original = empty_canonical_runtime_result("an-p7-003")
    restored = loads_runtime_result(dumps_runtime_result(original))
    assert restored.analysis_id == original.analysis_id
    assert restored.metadata.schema_version == original.metadata.schema_version


def test_projections_share_analysis_id() -> None:
    result = empty_canonical_runtime_result("an-p7-004")
    export = export_model_from_runtime(result)
    api = api_model_from_runtime(result)
    consulting = consulting_model_from_runtime(result)
    assert export.analysis_id == "an-p7-004"
    assert api.analysis_id == "an-p7-004"
    assert consulting.analysis_id == "an-p7-004"
    assert api.contract.analysis_id == "an-p7-004"


def test_service_and_engine_registry() -> None:
    register_all_engines()
    assert is_registered("detailed_interpretation")
    service = DetailedInterpretationService()
    result = service.empty_published_result("an-p7-005")
    payload = service.serialize(result)
    restored = service.deserialize(payload)
    assert restored.analysis_id == "an-p7-005"
    assert SCHEMA_RUNTIME_CONTRACT in registered_schema_ids()
