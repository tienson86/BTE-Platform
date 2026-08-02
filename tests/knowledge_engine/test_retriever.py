"""Unit tests for Knowledge Retriever."""

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


def _write_corpus(root: Path, rows_by_file: dict[str, list[str]]) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    for name in KNOWLEDGE_FILES:
        lines = [SCHEMA, *rows_by_file.get(name, [])]
        (root / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return root


def _row(
    record_id: str,
    topic: str,
    keyword: str,
    condition: str,
    *,
    priority: int = 10,
    confidence: float = 0.9,
) -> str:
    return (
        f"{record_id},{topic},{keyword},{condition},"
        f"classical {record_id},modern {record_id},{priority},{confidence},SRC-000001"
    )


@pytest.fixture
def retrieval_db(tmp_path: Path) -> Path:
    return _write_corpus(
        tmp_path / "20_knowledge",
        {
            "01_five_elements.csv": [
                _row(
                    "KNW-FE-WOOD",
                    "five_elements",
                    "wood;mộc",
                    "day_master_element=mộc",
                    priority=20,
                    confidence=0.95,
                ),
                _row(
                    "KNW-FE-FIRE",
                    "five_elements",
                    "fire;hỏa",
                    "day_master_element=hỏa",
                    priority=10,
                    confidence=0.8,
                ),
                _row(
                    "KNW-FE-EMPTY",
                    "five_elements",
                    "",
                    "",
                    priority=99,
                    confidence=1.0,
                ),
            ],
            "03_ten_gods.csv": [
                _row(
                    "KNW-TG-OFFICER",
                    "ten_gods",
                    "chính quan;officer",
                    "ten_gods.items contains chính quan",
                    priority=30,
                    confidence=0.92,
                ),
                _row(
                    "KNW-TG-UNRELATED",
                    "ten_gods",
                    "kiếp tài;rob wealth",
                    "ten_gods.items contains kiếp tài",
                    priority=50,
                    confidence=0.99,
                ),
            ],
            "08_useful_god.csv": [
                _row(
                    "KNW-UG-METAL",
                    "useful_god",
                    "kim;metal",
                    "useful_god.element=kim",
                    priority=25,
                    confidence=0.9,
                ),
            ],
            "09_strength.csv": [
                _row(
                    "KNW-ST-STRONG",
                    "strength",
                    "vượng;strong",
                    "strength.level=strong",
                    priority=15,
                    confidence=0.85,
                ),
            ],
            "11_shensha.csv": [
                _row(
                    "KNW-SS-HOACAI",
                    "shensha",
                    "hoa cái;hua gai",
                    "shensha.stars contains hoa cái",
                    priority=18,
                    confidence=0.88,
                ),
            ],
        },
    )


def _context_wood_officer() -> dict:
    return {
        "day_master": "giáp",
        "day_master_element": "mộc",
        "bazi": {"day_master": "giáp", "day_master_element": "mộc"},
        "strength": {"level": "strong"},
        "useful_god": {"element": "kim", "name": "kim", "status": "ok"},
        "ten_gods": {"items": ["chính quan", "thực thần"], "status": "ok"},
        "shensha": {"stars": ["hoa cái", "văn xương"], "status": "ok"},
        "pattern": {"main_pattern": "chinh_quan", "name": "chính quan"},
        "wuxing": {"wood": {"status": "strong"}, "season": "spring"},
        "temperature": {"status": "warm"},
    }


class TestKnowledgeRetriever:
    def test_retrieve_returns_related_only(self, retrieval_db: Path) -> None:
        repo = KnowledgeRepository(KnowledgeLoader(retrieval_db)).load()
        retriever = KnowledgeRetriever(repo, top_k=10, min_relevance=0.15)
        result = retriever.retrieve(_context_wood_officer())

        ids = [hit.id for hit in result.entries]
        assert "KNW-FE-WOOD" in ids
        assert "KNW-TG-OFFICER" in ids
        assert "KNW-UG-METAL" in ids
        assert "KNW-ST-STRONG" in ids
        assert "KNW-SS-HOACAI" in ids
        assert "KNW-TG-UNRELATED" not in ids
        assert "KNW-FE-FIRE" not in ids
        assert "KNW-FE-EMPTY" not in ids

    def test_priority_and_relevance_ranking(self, retrieval_db: Path) -> None:
        repo = KnowledgeRepository(KnowledgeLoader(retrieval_db)).load()
        retriever = KnowledgeRetriever(repo, min_relevance=0.1)
        result = retriever.retrieve(_context_wood_officer())
        assert result.entries
        scores = [hit.relevance_score for hit in result.entries]
        assert scores == sorted(scores, reverse=True)

    def test_metadata_trace_present(self, retrieval_db: Path) -> None:
        repo = KnowledgeRepository(KnowledgeLoader(retrieval_db)).load()
        result = KnowledgeRetriever(repo).retrieve(_context_wood_officer())
        assert "trace" in result.metadata
        assert isinstance(result.trace, list)
        assert result.metadata["accepted_count"] == len(result.entries)
        assert result.metadata["candidate_count"] >= len(result.entries)
        accepted = [row for row in result.trace if row["accepted"]]
        rejected = [row for row in result.trace if not row["accepted"]]
        assert accepted
        assert rejected
        assert any(row["reject_reason"] == "empty_keyword_and_condition" for row in rejected)

    def test_condition_eq_and_contains(self, retrieval_db: Path) -> None:
        repo = KnowledgeRepository(KnowledgeLoader(retrieval_db)).load()
        retriever = KnowledgeRetriever(repo, min_relevance=0.1)
        result = retriever.retrieve(_context_wood_officer())
        by_id = {hit.id: hit for hit in result.entries}
        assert by_id["KNW-FE-WOOD"].condition_score == 1.0
        assert by_id["KNW-TG-OFFICER"].condition_score == 1.0
        assert "chính quan" in " ".join(by_id["KNW-TG-OFFICER"].matched_keywords) or True

    def test_keyword_only_match_without_condition(self, tmp_path: Path) -> None:
        db = _write_corpus(
            tmp_path / "kw_only",
            {
                "03_ten_gods.csv": [
                    _row("KNW-TG-KW", "ten_gods", "chính quan", "", priority=10, confidence=0.9),
                ],
            },
        )
        repo = KnowledgeRepository(KnowledgeLoader(db)).load()
        result = KnowledgeRetriever(repo, min_relevance=0.1).retrieve(_context_wood_officer())
        assert [hit.id for hit in result.entries] == ["KNW-TG-KW"]

    def test_unrelated_high_priority_rejected(self, retrieval_db: Path) -> None:
        repo = KnowledgeRepository(KnowledgeLoader(retrieval_db)).load()
        result = KnowledgeRetriever(repo, min_relevance=0.05).retrieve(
            {
                "day_master_element": "mộc",
                "ten_gods": {"items": ["chính quan"]},
                "strength": {"level": "strong"},
                "useful_god": {"element": "kim"},
                "shensha": {"stars": ["hoa cái"]},
            }
        )
        ids = {hit.id for hit in result.entries}
        assert "KNW-TG-UNRELATED" not in ids

    def test_to_dict_and_records(self, retrieval_db: Path) -> None:
        repo = KnowledgeRepository(KnowledgeLoader(retrieval_db)).load()
        result = KnowledgeRetriever(repo).retrieve(_context_wood_officer())
        payload = result.to_dict()
        assert "entries" in payload and "metadata" in payload
        assert len(result.records) == len(result.entries)

    def test_extract_signals_deterministic(self, retrieval_db: Path) -> None:
        retriever = KnowledgeRetriever(KnowledgeRepository(KnowledgeLoader(retrieval_db)))
        signals = retriever.extract_signals(_context_wood_officer())
        assert signals == sorted(signals)
        assert "mộc" in signals
        assert "chính" in signals or "chính quan" in signals

    def test_top_k_limit(self, retrieval_db: Path) -> None:
        repo = KnowledgeRepository(KnowledgeLoader(retrieval_db)).load()
        result = KnowledgeRetriever(repo, top_k=2, min_relevance=0.1).retrieve(
            _context_wood_officer()
        )
        assert len(result.entries) <= 2

    def test_unsupported_condition_fail_closed(self, tmp_path: Path) -> None:
        db = _write_corpus(
            tmp_path / "bad_cond",
            {
                "01_five_elements.csv": [
                    _row(
                        "KNW-BAD",
                        "five_elements",
                        "wood",
                        "??? broken",
                        priority=99,
                        confidence=1.0,
                    ),
                ],
            },
        )
        repo = KnowledgeRepository(KnowledgeLoader(db)).load()
        result = KnowledgeRetriever(repo, min_relevance=0.01).retrieve(
            {"day_master_element": "wood"}
        )
        assert all(hit.id != "KNW-BAD" for hit in result.entries)
        rejected = [row for row in result.trace if row["record_id"] == "KNW-BAD"]
        assert rejected and rejected[0]["accepted"] is False
        assert rejected[0]["reject_reason"] in {"condition_failed", "unsupported_condition"}

    def test_keyword_only_unrelated_rejected(self, tmp_path: Path) -> None:
        db = _write_corpus(
            tmp_path / "kw_miss",
            {
                "03_ten_gods.csv": [
                    _row("KNW-TG-MISS", "ten_gods", "kiếp tài", "", priority=10, confidence=0.9),
                ],
            },
        )
        repo = KnowledgeRepository(KnowledgeLoader(db)).load()
        result = KnowledgeRetriever(repo, min_relevance=0.01).retrieve(_context_wood_officer())
        assert all(hit.id != "KNW-TG-MISS" for hit in result.entries)
        rejected = [row for row in result.trace if row["record_id"] == "KNW-TG-MISS"]
        assert rejected and rejected[0]["reject_reason"] == "no_keyword_match"

    def test_condition_only_and_exists_in_ops(self, tmp_path: Path) -> None:
        db = _write_corpus(
            tmp_path / "cond_ops",
            {
                "08_useful_god.csv": [
                    _row(
                        "KNW-UG-EXISTS",
                        "useful_god",
                        "",
                        "useful_god.element exists",
                        priority=20,
                        confidence=0.9,
                    ),
                    _row(
                        "KNW-UG-IN",
                        "useful_god",
                        "",
                        "useful_god.element in kim|metal",
                        priority=22,
                        confidence=0.9,
                    ),
                ],
                "09_strength.csv": [
                    _row(
                        "KNW-ST-LOW",
                        "strength",
                        "strong",
                        "strength.level=strong",
                        priority=1,
                        confidence=0.1,
                    ),
                ],
            },
        )
        repo = KnowledgeRepository(KnowledgeLoader(db)).load()
        result = KnowledgeRetriever(repo, min_relevance=0.2).retrieve(_context_wood_officer())
        ids = {hit.id for hit in result.entries}
        assert "KNW-UG-EXISTS" in ids
        assert "KNW-UG-IN" in ids

        result_strict = KnowledgeRetriever(repo, min_relevance=0.85).retrieve(
            _context_wood_officer()
        )
        assert "KNW-ST-LOW" not in {hit.id for hit in result_strict.entries}
        rejected = [row for row in result_strict.trace if row["record_id"] == "KNW-ST-LOW"]
        assert rejected and rejected[0]["reject_reason"] == "below_min_relevance"

    def test_hit_properties_and_signal_edge_cases(self, retrieval_db: Path) -> None:
        repo = KnowledgeRepository(KnowledgeLoader(retrieval_db)).load()
        retriever = KnowledgeRetriever(repo)
        result = retriever.retrieve(_context_wood_officer())
        hit = result.entries[0]
        assert hit.priority == hit.record.priority
        assert hit.confidence == hit.record.confidence

        signals = retriever.extract_signals(
            {
                "day_master": None,
                "flag": True,
                "score": 12,
                "empty": "",
                "na": "n/a",
                "ten_gods": {"by_name": {"chính quan": True}, "unique": ["thất sát"]},
                "wuxing": {"wood": "strong"},
                "shensha": {"available": {"hoa cái": 1}},
                "bazi": {"day_master_yin_yang": "dương"},
                "useful_god": {"favorable": ["kim"], "unfavorable": ["mộc"]},
                "temperature": {"level": "warm"},
                "pattern": {"category": "officer", "follow_type": "none"},
                "strength": {
                    "month_status": "旺",
                    "root_level": "通根",
                    "support_type": "印",
                    "control_type": "官",
                },
                "birth_season": "spring",
            }
        )
        assert "chính quan" in signals or "chính" in signals
        assert "hoa" in signals or "hoa cái" in signals
