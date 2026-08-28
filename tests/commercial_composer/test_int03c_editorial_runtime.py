"""INT-03C Editorial Composer runtime. Applies frozen INT-03B rules only."""

from __future__ import annotations

from pathlib import Path

from engines.commercial_composer import compose_commercial_narrative
from engines.commercial_composer.rules import CUSTOMER_SECTION_ORDER


ROOT = Path(__file__).resolve().parents[2]
COMPOSER_DIR = ROOT / "engines" / "commercial_composer"


def _block(
    *sentences: str,
    paths: tuple[str, ...] = (),
    topics: tuple[str, ...] = (),
) -> dict[str, object]:
    return {
        "sentences": list(sentences),
        "source_paths": list(paths or ("integrated",) * len(sentences)),
        "topic_ids": list(topics or ("strength",) * len(sentences)),
        "available": bool(sentences),
        "insufficient": not bool(sentences),
    }


def _integrated() -> dict[str, object]:
    return {
        "executive_summary": _block(
            "Nhật chủ được đọc là Thân vượng.",
            "Dụng thần đã công bố là Hỏa · Đinh · Chính Quan.",
            "Cách cục đã công bố là Chính Ấn.",
            "Đại Vận hiện tại đã công bố là Ất Tỵ.",
            paths=(
                "strength.strength_level",
                "useful_god.useful_display",
                "pattern.cach_cuc",
                "luck.current_dayun",
            ),
            topics=("strength", "useful_god", "pattern", "luck"),
        ),
        "observation": _block(
            "Phân loại lực đã công bố vẫn là Thân vượng.",
            "Điểm lực đã công bố là 0.87.",
            paths=("strength.strength_level", "strength.strength_score"),
        ),
        "reasoning": _block(
            "Yếu tố hỗ trợ lực Nhật chủ: Tướng.",
            "Yếu tố suy giảm lực Nhật chủ: Quan Sát.",
            "Yếu tố hỗ trợ Dụng thần: Hỷ thần, str_003, pat_ca_01.",
            '{"kind": "five_layer_luck_runtime_summary"}',
            paths=(
                "strength.evidence_pack.positive",
                "strength.evidence_pack.negative",
                "useful_god.evidence_pack.positive",
                "luck.luck_summary",
            ),
        ),
        "impact": _block("Với thế Thân vượng đã công bố, nhịp vận hành nghiêng về chủ động."),
        "recommendation": _block(
            "Ưu tiên hướng Dụng thần đã công bố: Hỏa.",
            "Ưu tiên hướng Dụng thần đã công bố: Hỏa · Đinh · Chính Quan.",
            "Hạn chế Kỵ thần đã công bố: Kim.",
            "Hướng điều hậu đã công bố: Cần ôn ấm.",
            paths=(
                "useful_god",
                "useful_god",
                "useful_god.unfavorable_display",
                "temperature",
            ),
        ),
        "summary": _block(
            "Nhật chủ được đọc là Thân vượng. Dụng thần đã công bố là Hỏa · Đinh · Chính Quan."
        ),
    }


def test_executive_summary_selects_and_prioritizes() -> None:
    """Tổng quan is selected findings, not concatenated topic summaries."""
    unit = compose_commercial_narrative(_integrated())
    texts = [sentence.text for sentence in unit.executive_summary.sentences]
    assert texts == [
        "Nhật chủ được đọc là Thân vượng.",
        "Dụng thần đã công bố là Hỏa · Đinh · Chính Quan.",
        "Cách cục đã công bố là Chính Ấn.",
        "Đại Vận hiện tại đã công bố là Ất Tỵ.",
    ]
    assert "Phân loại lực đã công bố vẫn là Thân vượng." not in texts
    assert all("." in text for text in texts)


def test_deduplication_emits_strength_meaning_once() -> None:
    """Repeated Thân vượng from observation is not added to Tổng quan."""
    unit = compose_commercial_narrative(_integrated())
    exec_texts = [sentence.text for sentence in unit.executive_summary.sentences]
    assert exec_texts.count("Nhật chủ được đọc là Thân vượng.") == 1
    assert not any("vẫn là Thân vượng" in text for text in exec_texts)


def test_recommendation_merge_keeps_longest_published() -> None:
    """Overlapping Dụng thần recs keep the strongest published version."""
    unit = compose_commercial_narrative(_integrated())
    texts = [sentence.text for sentence in unit.key_recommendation.sentences]
    assert "Ưu tiên hướng Dụng thần đã công bố: Hỏa · Đinh · Chính Quan." in texts
    assert "Ưu tiên hướng Dụng thần đã công bố: Hỏa." not in texts
    assert "Hạn chế Kỵ thần đã công bố: Kim." in texts
    assert "Hướng điều hậu đã công bố: Cần ôn ấm." in texts


def test_machine_cleanup_drops_rule_ids_and_json() -> None:
    """str_003, pat_ca_01, JSON, and compact scores never reach customers."""
    unit = compose_commercial_narrative(_integrated())
    joined = " ".join(
        sentence.text
        for slot in (
            "executive_summary",
            "current_situation",
            "strengths",
            "risks",
            "key_recommendation",
            "conclusion",
        )
        for sentence in getattr(unit, slot).sentences
    )
    assert "str_003" not in joined
    assert "pat_ca_01" not in joined
    assert "five_layer_luck_runtime_summary" not in joined
    assert "{" not in joined
    assert "0.87" not in joined


def test_customer_section_order_and_traceability() -> None:
    """Customer order is six sections. Every sentence cites Integrated ids."""
    unit = compose_commercial_narrative(_integrated())
    payload = unit.to_dict()
    assert payload["customer_section_order"] == list(CUSTOMER_SECTION_ORDER)
    assert unit.overall_reading.insufficient is True
    assert unit.status == "complete"
    for slot in CUSTOMER_SECTION_ORDER:
        for sentence in getattr(unit, slot).sentences:
            assert sentence.integrated_slots
            assert sentence.integrated_sentence_ids
            assert all(item.startswith("integrated.") for item in sentence.integrated_sentence_ids)


def test_no_new_facts_or_engine_imports() -> None:
    """Editorial runtime copies published prose and does not call analytical engines."""
    unit = compose_commercial_narrative(_integrated())
    published = [
        sentence.text
        for slot in CUSTOMER_SECTION_ORDER
        for sentence in getattr(unit, slot).sentences
    ]
    source = {
        "Nhật chủ được đọc là Thân vượng.",
        "Dụng thần đã công bố là Hỏa · Đinh · Chính Quan.",
        "Cách cục đã công bố là Chính Ấn.",
        "Đại Vận hiện tại đã công bố là Ất Tỵ.",
        "Phân loại lực đã công bố vẫn là Thân vượng.",
        "Với thế Thân vượng đã công bố, nhịp vận hành nghiêng về chủ động.",
        "Yếu tố suy giảm lực Nhật chủ: Quan Sát.",
        "Ưu tiên hướng Dụng thần đã công bố: Hỏa.",
        "Ưu tiên hướng Dụng thần đã công bố: Hỏa · Đinh · Chính Quan.",
        "Hạn chế Kỵ thần đã công bố: Kim.",
        "Hướng điều hậu đã công bố: Cần ôn ấm.",
        "Nhật chủ được đọc là Thân vượng. Dụng thần đã công bố là Hỏa · Đinh · Chính Quan.",
    }
    assert set(published) <= source
    joined = "\n".join(path.read_text(encoding="utf-8") for path in COMPOSER_DIR.glob("*.py"))
    assert "from engines.calendar" not in joined
    assert "from engines.strength" not in joined
    assert "from engines.identity" not in joined
    assert "from engines.report_engine" not in joined
    assert "def calculate(" not in joined
    assert "openai" not in joined.lower()
