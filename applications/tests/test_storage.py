"""Unit tests for JSON storage."""

from __future__ import annotations

from pathlib import Path

from applications.storage.file_store import FileStore
from applications.storage.json_store import JsonStore


def test_json_store_roundtrip(tmp_path: Path) -> None:
    store = JsonStore(tmp_path / "demo.json")
    assert store.load_dict() == {}
    store.save({"a": 1, "b": [2, 3]})
    assert store.load_dict() == {"a": 1, "b": [2, 3]}


def test_file_store_write_read(tmp_path: Path) -> None:
    files = FileStore(tmp_path)
    files.write_text("notes/hello.txt", "xin chao")
    assert files.read_text("notes/hello.txt") == "xin chao"
    assert files.ensure_dir("exports").exists()
