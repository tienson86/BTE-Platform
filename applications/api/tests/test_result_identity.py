"""Customer Analyze identity stamp — not an engine test."""

from __future__ import annotations

from applications.api.services.result_identity import (
    CUSTOMER_USEFUL_GOD_CONTRACT,
    GATE_CORE_FREEZE,
    stamp_customer_result_identity,
)


def test_stamp_copies_request_id_as_analysis_id() -> None:
    payload = {
        "useful_god": {"useful_display": "Thủy · Nhâm · Thực Thần"},
        "useful_god_source": {"contract": CUSTOMER_USEFUL_GOD_CONTRACT},
    }
    stamped = stamp_customer_result_identity(payload, "req-canonical-1")
    assert stamped["analysis_id"] == "req-canonical-1"
    assert stamped["request_id"] == "req-canonical-1"
    assert stamped["useful_god_source"]["contract"] == CUSTOMER_USEFUL_GOD_CONTRACT
    assert stamped["result_meta"]["analysis_id"] == "req-canonical-1"
    assert stamped["result_meta"]["customer_contract"] == CUSTOMER_USEFUL_GOD_CONTRACT
    assert stamped["result_meta"]["gate_core_freeze"] == GATE_CORE_FREEZE
    assert stamped["useful_god"]["useful_display"] == "Thủy · Nhâm · Thực Thần"


def test_stamp_does_not_invent_id_when_request_id_missing() -> None:
    stamped = stamp_customer_result_identity({"useful_god": {}}, None)
    assert "analysis_id" not in stamped or stamped.get("analysis_id") in (None, "")
    assert stamped["result_meta"]["analysis_id"] is None
    assert stamped["useful_god_source"]["contract"] == CUSTOMER_USEFUL_GOD_CONTRACT
