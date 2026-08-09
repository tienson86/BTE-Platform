"""QC-1 registry tests. Read-only over sealed packages."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[4]
PACKAGES = REPO / "knowledge" / "packages"
REPORTS = ROOT / "reports"

EXPECTED = [f"bz_{n:02d}_" for n in range(1, 24)]


def _packages() -> list[dict]:
    rows = []
    for path in sorted(PACKAGES.glob("**/PACKAGE.json")):
        rows.append(json.loads(path.read_text(encoding="utf-8")))
    return rows


def test_registry_count_and_unique_ids() -> None:
    packages = _packages()
    ids = [item["package_id"] for item in packages]
    assert len(packages) == 23
    assert len(set(ids)) == 23


def test_registry_bz_01_through_bz_23_present() -> None:
    ids = [item["package_id"] for item in _packages()]
    for prefix in EXPECTED:
        assert any(item.startswith(prefix) for item in ids), prefix


def test_registry_released_status() -> None:
    for item in _packages():
        assert item["status"] == "released"
        assert item["language"] == "vi"


def test_registry_report_serialization() -> None:
    payload = json.loads((REPORTS / "package_registry.json").read_text(encoding="utf-8"))
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    assert json.loads(encoded)["package_count"] == 23
    assert len(payload["packages"]) == 23
    assert re.fullmatch(r"[a-f0-9]{64}", str(payload["packages"][0]["checksum"]["stored"] or ""))
