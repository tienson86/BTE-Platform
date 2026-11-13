"""Customer copy keeps interpretations conditional and technical notes private."""
from dataclasses import fields
from consulting.marriage.narrative import catalog
from consulting.marriage.report.customer_copy import customerize
from consulting.marriage.report.final_opinion import compose_final_opinion
from tests.consulting.narrative_fixtures import compose_narrative


def test_catalog_does_not_expose_internal_editorial_language():
    entries = [*catalog._OVERALL.values(), *catalog._DOMAIN_STATE.values(),
               *catalog._FINDING.values(), *catalog._TIMING_STATE.values(),
               *catalog._ACTION.values(), catalog._MIXED_FINDING]
    prohibited = ("tầng quyết định", "không phải suy diễn thêm", "Nguồn là",
                  "lớp kích hoạt", "cùng miền", "trong cùng miền")
    for entry in entries:
        text = " ".join(getattr(entry, f.name) for f in fields(entry))
        assert not any(phrase in text for phrase in prohibited), entry.key


def test_customerize_does_not_turn_chart_interpretation_into_observed_fact():
    text = customerize("Cấu trúc hiện cho thấy xu hướng hỗ trợ.")
    assert "Trong thực tế" not in text
    assert "Đối chiếu hai lá số" in text


def test_missing_cards_do_not_invent_a_strongest_strength():
    _, payload, _ = compose_narrative()
    payload.language_cards = []
    opinion = compose_final_opinion(payload)
    assert "Chưa đủ căn cứ" in opinion["strongest_strength"]
    assert "Chưa đủ căn cứ" in opinion["main_attention"]
