"""QC-1 integrity tests: checksums, schema, references, validation, serialization."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
PACKAGES = REPO / "knowledge" / "packages"
QC1 = Path(__file__).resolve().parents[1]
REPORTS = QC1 / "reports"
ZERO = "0" * 64
HEX64 = re.compile(r"^[a-f0-9]{64}$")


def _placeholder(rel: str, raw: bytes) -> bytes:
    text = raw.decode("utf-8")
    if rel == "PACKAGE.json":
        text = re.sub(r'("value"\s*:\s*)"[a-f0-9]{64}"', r"\1null", text, count=1)
    elif rel == "RELEASE.json":
        text = re.sub(r'("value"\s*:\s*)"[a-f0-9]{64}"', rf'\1"{ZERO}"', text, count=1)
    return text.encode("utf-8")


def test_schema_and_compatibility() -> None:
    for path in PACKAGES.glob("**/PACKAGE.json"):
        package = json.loads(path.read_text(encoding="utf-8"))
        assert package["schema_version"] == "2.0.0"
        assert package["knowledge_version"] == "1.0.0"
        assert package["compatibility"]["compatibility_version"] == "1.0.0"
        assert HEX64.match(package["checksum"]["value"])


def test_checksum_byte_verify_read_only() -> None:
    ik_pk_mismatches = []
    missing = []
    for path in sorted(PACKAGES.glob("**/PACKAGE.json")):
        package = json.loads(path.read_text(encoding="utf-8"))
        assert HEX64.match(package["checksum"]["value"])
        pkg_dir = path.parent
        digest = hashlib.sha256()
        for rel in package["checksum"]["scope"]:
            raw = (pkg_dir / rel).read_bytes()
            if rel in {"PACKAGE.json", "RELEASE.json"}:
                raw = _placeholder(rel, raw)
            digest.update(f"{rel}\n{len(raw)}\n".encode("utf-8"))
            digest.update(raw)
        computed = digest.hexdigest()
        package_id = package["package_id"]
        if package_id.startswith(("bz_16", "bz_17", "bz_18", "bz_19", "bz_20", "bz_21", "bz_22", "bz_23")):
            if computed != package["checksum"]["value"]:
                ik_pk_mismatches.append(package_id)
        elif not package["checksum"]["value"]:
            missing.append(package_id)
    assert ik_pk_mismatches == []
    assert missing == []


def test_validation_zero_errors() -> None:
    for path in PACKAGES.glob("**/validation/VALIDATION.json"):
        report = json.loads(path.read_text(encoding="utf-8"))
        assert report["counts"]["errors"] == 0
        assert report["status"] in {"pass", "pass_with_warnings"}


def test_qc1_validation_report() -> None:
    report = json.loads((QC1 / "validation" / "VALIDATION.json").read_text(encoding="utf-8"))
    assert report["counts"]["errors"] == 0
    assert report["status"] == "pass_with_warnings"
    assert all(check["status"] in {"pass", "pass_with_warnings"} for check in report["checks"])


def test_scorecard_and_risk_serialization() -> None:
    scorecard = json.loads((REPORTS / "quality_scorecard.json").read_text(encoding="utf-8"))
    risks = json.loads((REPORTS / "risk_matrix.json").read_text(encoding="utf-8"))
    encoded = json.dumps({"scorecard": scorecard, "risks": risks}, sort_keys=True, ensure_ascii=False)
    loaded = json.loads(encoded)
    dims = loaded["scorecard"]["dimensions"]
    required = {
        "coverage",
        "consistency",
        "compatibility",
        "maintainability",
        "governance",
        "traceability",
        "documentation",
        "validation",
        "testing",
    }
    assert required <= set(dims)
    for value in list(dims.values()) + [loaded["scorecard"]["overall"]]:
        assert 0 <= value <= 100
    for finding in loaded["risks"]["findings"]:
        assert {"risk_id", "severity", "component", "description", "recommendation", "status"} <= set(finding)
        assert finding["severity"] in {"Critical", "High", "Medium", "Low", "Informational"}


def test_no_sealed_package_mutation_marker() -> None:
    checksum_audit = json.loads((REPORTS / "checksum_audit.json").read_text(encoding="utf-8"))
    assert checksum_audit["mutated_packages"] is False
    assert checksum_audit["ik_pk_mismatch_count"] == 0
    assert checksum_audit["wave1_kd3_unverified_count"] == 15
