"""Unit tests for registry checksum utilities."""

from __future__ import annotations

from pathlib import Path

from services.registry_checksum import (
    checksum_file,
    checksum_payload,
    checksum_record,
    verify_checksum,
)


def test_checksum_payload_is_stable() -> None:
    payload = {"b": 2, "a": 1}
    assert checksum_payload(payload) == checksum_payload({"a": 1, "b": 2})


def test_checksum_file_and_verify(tmp_path: Path) -> None:
    path = tmp_path / "sample.json"
    path.write_text('{"ok": true}\n', encoding="utf-8")
    digest = checksum_file(path)
    assert verify_checksum(digest, path=path)
    assert not verify_checksum("deadbeef", path=path)


def test_checksum_record() -> None:
    record = {"identity": {"registry_id": "KREG-000001"}}
    assert len(checksum_record(record)) == 64
