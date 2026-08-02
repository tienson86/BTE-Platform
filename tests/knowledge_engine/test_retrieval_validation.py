"""100-sample retrieval validation + retrieval report for Milestone 03."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from engines.knowledge_engine import (
    KNOWLEDGE_FILES,
    REQUIRED_COLUMNS,
    KnowledgeLoader,
    KnowledgeRepository,
    KnowledgeRetriever,
)

SCHEMA = ",".join(REQUIRED_COLUMNS)
REPORT_PATH = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "reports"
    / "knowledge_retrieval_report_m03.md"
)

_ELEMENTS = ["mộc", "hỏa", "thổ", "kim", "thủy"]
_TEN_GODS = [
    "tỷ kiên",
    "kiếp tài",
    "thực thần",
    "thương quan",
    "chính tài",
    "thiên tài",
    "chính quan",
    "thất sát",
    "chính ấn",
    "thiên ấn",
]
_SHENSHA = [
    "hoa cái",
    "thiên át",
    "văn xương",
    "quốc ấn",
    "dịch mã",
    "đào hoa",
    "cô thần",
    "quả tú",
]
_STRENGTH = ["strong", "balanced", "weak"]
_USEFUL = ["mộc", "hỏa", "thổ", "kim", "thủy"]


def _row(
    record_id: str,
    topic: str,
    keyword: str,
    condition: str,
    *,
    priority: int,
    confidence: float,
) -> str:
    return (
        f"{record_id},{topic},{keyword},{condition},"
        f"classical {record_id},modern {record_id},{priority},{confidence},SRC-000001"
    )


def _build_validation_corpus(root: Path) -> Path:
    """Build a deterministic corpus with related + distractor rows."""
    root.mkdir(parents=True, exist_ok=True)
    rows: dict[str, list[str]] = {name: [] for name in KNOWLEDGE_FILES}

    for index, element in enumerate(_ELEMENTS, start=1):
        rows["01_five_elements.csv"].append(
            _row(
                f"KNW-FE-{index:03d}",
                "five_elements",
                f"{element};element",
                f"day_master_element={element}",
                priority=10 + index,
                confidence=0.8 + index * 0.02,
            )
        )

    for index, god in enumerate(_TEN_GODS, start=1):
        rows["03_ten_gods.csv"].append(
            _row(
                f"KNW-TG-{index:03d}",
                "ten_gods",
                god,
                f"ten_gods.items contains {god}",
                priority=20 + index,
                confidence=0.85,
            )
        )

    for index, star in enumerate(_SHENSHA, start=1):
        rows["11_shensha.csv"].append(
            _row(
                f"KNW-SS-{index:03d}",
                "shensha",
                star,
                f"shensha.stars contains {star}",
                priority=15 + index,
                confidence=0.8,
            )
        )

    for index, level in enumerate(_STRENGTH, start=1):
        rows["09_strength.csv"].append(
            _row(
                f"KNW-ST-{index:03d}",
                "strength",
                level,
                f"strength.level={level}",
                priority=12 + index,
                confidence=0.9,
            )
        )

    for index, element in enumerate(_USEFUL, start=1):
        rows["08_useful_god.csv"].append(
            _row(
                f"KNW-UG-{index:03d}",
                "useful_god",
                element,
                f"useful_god.element={element}",
                priority=18 + index,
                confidence=0.88,
            )
        )

    # Distractors that must never appear unless their signals exist.
    rows["12_career.csv"].append(
        _row(
            "KNW-CR-DIST",
            "career",
            "astronaut;unrelated-career",
            "pattern.main_pattern=never_match_pattern",
            priority=99,
            confidence=1.0,
        )
    )
    rows["20_glossary.csv"].append(
        _row(
            "KNW-GL-EMPTY",
            "glossary",
            "",
            "",
            priority=99,
            confidence=1.0,
        )
    )

    for name in KNOWLEDGE_FILES:
        content = "\n".join([SCHEMA, *rows[name]]) + "\n"
        (root / name).write_text(content, encoding="utf-8")
    return root


def _sample_context(index: int) -> dict:
    """Build one of 100 deterministic RuleContext samples."""
    element = _ELEMENTS[index % len(_ELEMENTS)]
    god = _TEN_GODS[index % len(_TEN_GODS)]
    star = _SHENSHA[index % len(_SHENSHA)]
    strength = _STRENGTH[index % len(_STRENGTH)]
    useful = _USEFUL[(index * 2) % len(_USEFUL)]
    second_god = _TEN_GODS[(index * 3) % len(_TEN_GODS)]
    return {
        "sample_id": index,
        "day_master_element": element,
        "bazi": {"day_master_element": element},
        "strength": {"level": strength},
        "useful_god": {"element": useful, "name": useful, "status": "ok"},
        "ten_gods": {"items": list({god, second_god}), "status": "ok"},
        "shensha": {"stars": [star], "status": "ok"},
        "pattern": {"main_pattern": f"pattern_{index % 7}", "name": god},
        "wuxing": {element: {"status": "present"}, "season": "spring"},
        "temperature": {"status": "neutral"},
    }


def _assert_no_unrelated(result, context: dict) -> None:
    """Every accepted hit must be justified by keyword or passing condition."""
    signals = set()
    # lightweight signal mirror for assertions
    for value in (
        context.get("day_master_element"),
        context.get("strength", {}).get("level"),
        context.get("useful_god", {}).get("element"),
        *(context.get("ten_gods", {}).get("items") or []),
        *(context.get("shensha", {}).get("stars") or []),
    ):
        if value:
            signals.add(str(value).lower())

    for hit in result.entries:
        assert hit.id != "KNW-GL-EMPTY"
        assert hit.id != "KNW-CR-DIST"
        assert hit.relevance_score > 0
        assert hit.matched_keywords or hit.matched_conditions
        # Condition-bearing rows must have condition evidence.
        if hit.record.condition.strip():
            assert hit.condition_score == 1.0
        if hit.record.keyword_tokens() and not hit.record.condition.strip():
            assert hit.keyword_score > 0


def test_100_sample_retrieval_validation(tmp_path: Path) -> None:
    db = _build_validation_corpus(tmp_path / "20_knowledge_validation")
    repo = KnowledgeRepository(KnowledgeLoader(db)).load()
    retriever = KnowledgeRetriever(repo, top_k=15, min_relevance=0.12)

    sample_summaries: list[dict] = []
    total_hits = 0
    total_rejected = 0

    for index in range(100):
        context = _sample_context(index)
        result = retriever.retrieve(context)
        _assert_no_unrelated(result, context)
        total_hits += len(result.entries)
        total_rejected += int(result.metadata.get("rejected_count") or 0)
        sample_summaries.append(
            {
                "sample_id": index,
                "accepted": [hit.id for hit in result.entries],
                "accepted_count": len(result.entries),
                "rejected_count": result.metadata.get("rejected_count"),
                "top_relevance": result.entries[0].relevance_score if result.entries else 0.0,
                "signals": result.metadata.get("signals", [])[:12],
            }
        )
        assert result.entries, f"sample {index} returned no related knowledge"
        assert "trace" in result.metadata

    avg_hits = total_hits / 100.0
    report = "\n".join(
        [
            "# Knowledge Retrieval Report — Epic 03 Milestone 03",
            "",
            "## Summary",
            "",
            f"- Samples validated: **100**",
            f"- Total accepted hits: **{total_hits}**",
            f"- Average hits / sample: **{avg_hits:.2f}**",
            f"- Total rejected candidates (sum): **{total_rejected}**",
            f"- Corpus records: **{repo.count()}**",
            f"- Distractor leakage: **0** (KNW-CR-DIST / KNW-GL-EMPTY never accepted)",
            "",
            "## Ranking policy",
            "",
            "- keyword weight 0.45",
            "- condition weight 0.35",
            "- priority weight 0.10",
            "- confidence weight 0.10",
            "- non-empty conditions fail closed",
            "- empty keyword+condition rows always rejected",
            "",
            "## Sample digest (first 10)",
            "",
            "```json",
            json.dumps(sample_summaries[:10], ensure_ascii=False, indent=2),
            "```",
            "",
            "## Compatibility",
            "",
            "- Input: RuleContext only",
            "- Output: KnowledgeResult + metadata.trace",
            "- No calculation engine changes",
            "",
        ]
    )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    assert REPORT_PATH.exists()
    assert avg_hits >= 1.0
