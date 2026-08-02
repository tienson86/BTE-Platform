"""Unit tests for Knowledge Engine loader and repository."""

from __future__ import annotations

from pathlib import Path

import pytest

from engines.knowledge_engine import (
    KNOWLEDGE_FILES,
    REQUIRED_COLUMNS,
    KnowledgeLoadError,
    KnowledgeLoader,
    KnowledgeRecord,
    KnowledgeRepository,
    KnowledgeSchemaError,
)

SCHEMA = ",".join(REQUIRED_COLUMNS)


def _write_corpus(root: Path, rows_by_file: dict[str, list[str]] | None = None) -> Path:
    """Create a full 20-file knowledge corpus under ``root``."""
    root.mkdir(parents=True, exist_ok=True)
    rows_by_file = rows_by_file or {}
    for name in KNOWLEDGE_FILES:
        lines = [SCHEMA]
        lines.extend(rows_by_file.get(name, []))
        (root / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return root


def _row(
    record_id: str,
    topic: str = "five_elements",
    keyword: str = "wood;moc",
    *,
    priority: int = 10,
    confidence: float = 0.9,
) -> str:
    return (
        f"{record_id},{topic},{keyword},day_master=wood,"
        f"classical,{topic} modern,{priority},{confidence},SRC-000001"
    )


@pytest.fixture
def empty_db(tmp_path: Path) -> Path:
    return _write_corpus(tmp_path / "20_knowledge")


@pytest.fixture
def sample_db(tmp_path: Path) -> Path:
    return _write_corpus(
        tmp_path / "20_knowledge",
        {
            "01_five_elements.csv": [
                _row("KNW-FE-001", "five_elements", "wood|moc", priority=20, confidence=0.95),
                _row("KNW-FE-002", "five_elements", "fire", priority=5, confidence=0.8),
            ],
            "03_ten_gods.csv": [
                _row("KNW-TG-001", "ten_gods", "chinh quan;officer", priority=15, confidence=0.9),
            ],
            "11_shensha.csv": [
                _row("KNW-SS-001", "shensha", "hoa cai", priority=12, confidence=0.85),
            ],
        },
    )


class TestKnowledgeRecord:
    def test_keyword_tokens_split_delimiters(self) -> None:
        record = KnowledgeRecord(
            id="KNW-1",
            topic="t",
            keyword="Wood; moc | Fire, earth",
            condition="",
            classical_text="",
            modern_interpretation="",
            priority=1,
            confidence=0.5,
            reference="",
        )
        assert record.keyword_tokens() == ["wood", "moc", "fire", "earth"]

    def test_keyword_tokens_empty(self) -> None:
        record = KnowledgeRecord(
            id="KNW-1",
            topic="t",
            keyword="",
            condition="",
            classical_text="",
            modern_interpretation="",
            priority=0,
            confidence=0.0,
            reference="",
        )
        assert record.keyword_tokens() == []


class TestKnowledgeLoader:
    def test_load_all_empty_schema_corpus(self, empty_db: Path) -> None:
        loader = KnowledgeLoader(empty_db)
        records = loader.load_all()
        assert records == []
        assert loader.is_loaded() is True
        assert loader.cache_size() == len(KNOWLEDGE_FILES)

    def test_load_all_reads_sample_rows(self, sample_db: Path) -> None:
        loader = KnowledgeLoader(sample_db)
        records = loader.load_all()
        assert len(records) == 4
        ids = {row.id for row in records}
        assert ids == {"KNW-FE-001", "KNW-FE-002", "KNW-TG-001", "KNW-SS-001"}
        first = next(row for row in records if row.id == "KNW-FE-001")
        assert first.topic == "five_elements"
        assert first.priority == 20
        assert first.confidence == pytest.approx(0.95)
        assert first.source_file == "01_five_elements.csv"
        assert first.reference == "SRC-000001"

    def test_load_all_uses_cache(self, sample_db: Path) -> None:
        loader = KnowledgeLoader(sample_db)
        first = loader.load_all()
        second = loader.load_all()
        assert first == second
        assert loader.cache_size() == len(KNOWLEDGE_FILES)

    def test_load_file_cache_and_clear(self, sample_db: Path) -> None:
        loader = KnowledgeLoader(sample_db)
        rows = loader.load_file("01_five_elements.csv")
        assert len(rows) == 2
        assert loader.cache_size() == 1
        again = loader.load_file("01_five_elements.csv")
        assert again == rows
        loader.clear_cache()
        assert loader.cache_size() == 0
        assert loader.is_loaded() is False

    def test_expected_files(self, empty_db: Path) -> None:
        loader = KnowledgeLoader(empty_db)
        assert loader.expected_files() == KNOWLEDGE_FILES

    def test_default_path_points_to_repo_knowledge(self) -> None:
        loader = KnowledgeLoader()
        assert loader.database_path.name == "20_knowledge"
        assert loader.database_path.exists()
        records = loader.load_all()
        assert isinstance(records, list)

    def test_missing_directory(self, tmp_path: Path) -> None:
        loader = KnowledgeLoader(tmp_path / "missing")
        with pytest.raises(KnowledgeLoadError, match="not found"):
            loader.load_all()

    def test_path_is_file_not_directory(self, tmp_path: Path) -> None:
        target = tmp_path / "not_a_dir"
        target.write_text("x", encoding="utf-8")
        loader = KnowledgeLoader(target)
        with pytest.raises(KnowledgeLoadError, match="not a directory"):
            loader.load_all()

    def test_missing_csv_file(self, empty_db: Path) -> None:
        (empty_db / "01_five_elements.csv").unlink()
        loader = KnowledgeLoader(empty_db)
        with pytest.raises(KnowledgeLoadError, match="not found"):
            loader.load_all()

    def test_invalid_schema_header(self, tmp_path: Path) -> None:
        root = tmp_path / "bad"
        _write_corpus(root)
        (root / "01_five_elements.csv").write_text("id,topic\nKNW-1,t\n", encoding="utf-8")
        loader = KnowledgeLoader(root)
        with pytest.raises(KnowledgeSchemaError, match="Invalid schema"):
            loader.load_all()

    def test_missing_header(self, tmp_path: Path) -> None:
        root = tmp_path / "bad"
        _write_corpus(root)
        (root / "01_five_elements.csv").write_text("", encoding="utf-8")
        loader = KnowledgeLoader(root)
        with pytest.raises(KnowledgeSchemaError, match="Missing header"):
            loader.load_file("01_five_elements.csv")

    def test_empty_id_rejected(self, tmp_path: Path) -> None:
        root = _write_corpus(
            tmp_path / "bad",
            {"01_five_elements.csv": [_row("", "five_elements", "wood")]},
        )
        # Force empty id cell
        (root / "01_five_elements.csv").write_text(
            SCHEMA + "\n,five_elements,wood,c,cl,mo,1,0.5,SRC\n",
            encoding="utf-8",
        )
        loader = KnowledgeLoader(root)
        with pytest.raises(KnowledgeSchemaError, match="Empty id"):
            loader.load_all()

    def test_duplicate_id_rejected(self, tmp_path: Path) -> None:
        root = _write_corpus(
            tmp_path / "dup",
            {
                "01_five_elements.csv": [_row("KNW-DUP", "five_elements", "wood")],
                "03_ten_gods.csv": [_row("KNW-DUP", "ten_gods", "officer")],
            },
        )
        loader = KnowledgeLoader(root)
        with pytest.raises(KnowledgeSchemaError, match="Duplicate knowledge id"):
            loader.load_all()

    def test_invalid_priority(self, tmp_path: Path) -> None:
        root = _write_corpus(tmp_path / "bad")
        (root / "01_five_elements.csv").write_text(
            SCHEMA + "\nKNW-1,t,k,c,cl,mo,not-int,0.5,SRC\n",
            encoding="utf-8",
        )
        loader = KnowledgeLoader(root)
        with pytest.raises(KnowledgeSchemaError, match="Invalid priority"):
            loader.load_all()

    def test_invalid_confidence(self, tmp_path: Path) -> None:
        root = _write_corpus(tmp_path / "bad")
        (root / "01_five_elements.csv").write_text(
            SCHEMA + "\nKNW-1,t,k,c,cl,mo,1,not-float,SRC\n",
            encoding="utf-8",
        )
        loader = KnowledgeLoader(root)
        with pytest.raises(KnowledgeSchemaError, match="Invalid confidence"):
            loader.load_all()

    def test_confidence_out_of_range(self, tmp_path: Path) -> None:
        root = _write_corpus(tmp_path / "bad")
        (root / "01_five_elements.csv").write_text(
            SCHEMA + "\nKNW-1,t,k,c,cl,mo,1,1.5,SRC\n",
            encoding="utf-8",
        )
        loader = KnowledgeLoader(root)
        with pytest.raises(KnowledgeSchemaError, match="out of range"):
            loader.load_all()

    def test_blank_rows_skipped(self, tmp_path: Path) -> None:
        root = _write_corpus(tmp_path / "blank")
        (root / "01_five_elements.csv").write_text(
            SCHEMA + "\n,,,,,,,,\n" + _row("KNW-FE-010") + "\n",
            encoding="utf-8",
        )
        loader = KnowledgeLoader(root)
        records = loader.load_all()
        assert [row.id for row in records] == ["KNW-FE-010"]

    def test_default_priority_confidence_when_blank(self, tmp_path: Path) -> None:
        root = _write_corpus(tmp_path / "defaults")
        (root / "01_five_elements.csv").write_text(
            SCHEMA + "\nKNW-1,topic,key,cond,cl,mo,,,SRC\n",
            encoding="utf-8",
        )
        loader = KnowledgeLoader(root)
        records = loader.load_all()
        assert len(records) == 1
        assert records[0].priority == 0
        assert records[0].confidence == 0.0


class TestKnowledgeRepository:
    def test_get_by_id(self, sample_db: Path) -> None:
        repo = KnowledgeRepository(KnowledgeLoader(sample_db)).load()
        found = repo.get_by_id("KNW-TG-001")
        assert found is not None
        assert found.topic == "ten_gods"
        assert repo.get_by_id("missing") is None
        assert repo.get_by_id("  ") is None

    def test_find_by_topic_exact_and_fuzzy(self, sample_db: Path) -> None:
        repo = KnowledgeRepository(KnowledgeLoader(sample_db)).load()
        exact = repo.find_by_topic("five_elements", exact=True)
        assert {row.id for row in exact} == {"KNW-FE-001", "KNW-FE-002"}
        assert exact[0].id == "KNW-FE-001"  # higher priority first
        fuzzy = repo.find_by_topic("five")
        assert {row.id for row in fuzzy} == {"KNW-FE-001", "KNW-FE-002"}
        assert repo.find_by_topic("") == []
        assert repo.find_by_topic("nope", exact=True) == []

    def test_find_by_keyword(self, sample_db: Path) -> None:
        repo = KnowledgeRepository(KnowledgeLoader(sample_db)).load()
        wood = repo.find_by_keyword("wood")
        assert [row.id for row in wood] == ["KNW-FE-001"]
        officer = repo.find_by_keyword("officer")
        assert [row.id for row in officer] == ["KNW-TG-001"]
        hoa = repo.find_by_keyword("hoa")
        assert [row.id for row in hoa] == ["KNW-SS-001"]
        assert repo.find_by_keyword("") == []

    def test_search_intersection(self, sample_db: Path) -> None:
        repo = KnowledgeRepository(KnowledgeLoader(sample_db)).load()
        by_id = repo.search(record_id="KNW-FE-001")
        assert [row.id for row in by_id] == ["KNW-FE-001"]
        mixed = repo.search(topic="five_elements", keyword="fire")
        assert [row.id for row in mixed] == ["KNW-FE-002"]
        none = repo.search(topic="five_elements", keyword="officer")
        assert none == []
        all_rows = repo.search()
        assert len(all_rows) == 4

    def test_count_all_and_lazy_load(self, sample_db: Path) -> None:
        repo = KnowledgeRepository(KnowledgeLoader(sample_db))
        assert repo.is_indexed() is False
        assert repo.count() == 4
        assert repo.is_indexed() is True
        assert len(repo.all()) == 4

    def test_reload_picks_up_changes(self, sample_db: Path) -> None:
        repo = KnowledgeRepository(KnowledgeLoader(sample_db)).load()
        assert repo.count() == 4
        with (sample_db / "20_glossary.csv").open("a", encoding="utf-8") as handle:
            handle.write(_row("KNW-GL-001", "glossary", "term") + "\n")
        repo.reload()
        assert repo.count() == 5
        assert repo.get_by_id("KNW-GL-001") is not None

    def test_default_repository_loads_production_schema(self) -> None:
        repo = KnowledgeRepository()
        assert repo.loader.database_path.name == "20_knowledge"
        assert repo.count() >= 0
        assert isinstance(repo.all(), list)

    def test_find_by_keyword_raw_substring_fallback(self, tmp_path: Path) -> None:
        root = _write_corpus(
            tmp_path / "kw",
            {
                "01_five_elements.csv": [
                    # Tokens are "ho" and "acai"; query "o;a" only matches raw field.
                    _row("KNW-FE-RAW", "five_elements", "ho;acai", priority=1, confidence=0.7),
                ],
            },
        )
        repo = KnowledgeRepository(KnowledgeLoader(root)).load()
        hits = repo.find_by_keyword("o;a")
        assert [row.id for row in hits] == ["KNW-FE-RAW"]

    def test_oserror_on_unreadable_file(self, empty_db: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        loader = KnowledgeLoader(empty_db)

        def _boom(*_args: object, **_kwargs: object) -> object:
            raise OSError("permission denied")

        monkeypatch.setattr(Path, "open", _boom)
        with pytest.raises(KnowledgeLoadError, match="Failed to read"):
            loader.load_file("01_five_elements.csv")
