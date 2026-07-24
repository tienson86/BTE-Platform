"""Unit tests for Applications API helpers and schemas."""

from __future__ import annotations

from applications.api.config import APISettings
from applications.api.exceptions import PipelineAPIError, ValidationAPIError
from applications.api.schemas.common import BirthRequest
from applications.api.utils.pillars import pillar_text
from applications.api.utils.serializers import to_jsonable


def test_birth_request_defaults() -> None:
    body = BirthRequest(year=1990, month=5, day=15)
    assert body.hour == 0
    assert body.minute == 0
    assert body.timezone == "Asia/Ho_Chi_Minh"
    assert body.full_name is None
    assert body.birth_place is None


def test_birth_request_customer_metadata() -> None:
    body = BirthRequest(
        year=1990,
        month=5,
        day=15,
        full_name="Nguyễn Văn A",
        birth_place="Hà Nội",
        customer_id="cust-1",
        metadata={"bat_trach": {"cung_phi": "Khảm", "menh_quai": "Khảm", "nhom_trach": "dong"}},
    )
    assert body.full_name == "Nguyễn Văn A"
    assert body.birth_place == "Hà Nội"
    assert body.customer_id == "cust-1"
    assert body.metadata["bat_trach"]["cung_phi"] == "Khảm"


def test_to_jsonable_nested() -> None:
    payload = to_jsonable({"a": 1, "b": (2, 3), "c": {"d": True}})
    assert payload == {"a": 1, "b": [2, 3], "c": {"d": True}}


def test_pillar_text() -> None:
    class Pillar:
        stem = "Jia"
        branch = "Zi"

    assert pillar_text(Pillar()) == "Jia Zi"


def test_pipeline_api_error_defaults() -> None:
    err = PipelineAPIError("boom", details={"stage": "score"})
    assert err.status_code == 500
    assert err.code == "pipeline_error"
    assert err.details == {"stage": "score"}


def test_validation_api_error_status() -> None:
    err = ValidationAPIError("bad")
    assert err.status_code == 422


def test_settings_defaults() -> None:
    cfg = APISettings()
    assert cfg.api_prefix == "/api/v1"
    assert cfg.request_id_header == "X-Request-ID"
    assert cfg.elapsed_header == "X-Elapsed-Ms"
