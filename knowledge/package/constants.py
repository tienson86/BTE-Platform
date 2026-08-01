"""Constants for Knowledge Package Builder."""

from __future__ import annotations

from typing import Final

SCHEMA_VERSION: Final[str] = "1.0.0"
BUILDER_VERSION: Final[str] = "1.0.0"
DEFAULT_TIMESTAMP: Final[str] = "2026-08-01T00:00:00Z"
# Integrity signing material (deterministic local integrity, not a secret vault key).
SIGNING_KEY_ID: Final[str] = "BTE-PACK-SIGNING-V1"
SIGNING_KEY_MATERIAL: Final[str] = "BTE-PLATFORM-PACK-INTEGRITY-V1"

# Pack definitions — extensible for Pack 02+ without redesign.
PACK_DEFINITIONS: Final[dict[str, dict[str, object]]] = {
    "PACK_01": {
        "pack_id": "PACK_01",
        "title": "Pack 01 — Fundamental Theory",
        "module_id": "01_fundamental_knowledge",
        "version": "1.0.0",
        "status": "released",
        "description": "Golden Foundation Pack for the BTE Knowledge Canon.",
        "records_dir": "knowledge/bazi/01_fundamental_knowledge/records",
        "record_ids": [
            "KR-000001",
            "KR-000002",
            "KR-000003",
            "KR-000004",
            "KR-000005",
            "KR-000006",
            "KR-000007",
            "KR-000008",
            "KR-000009",
            "KR-000010",
            "KR-000011",
            "KR-000012",
            "KR-000013",
            "KR-000014",
            "KR-000015",
        ],
        "record_files": {
            "KR-000001": "KR-000001_YIN_YANG.md",
            "KR-000002": "KR-000002_QI.md",
            "KR-000003": "KR-000003_WU_XING.md",
            "KR-000004": "KR-000004_Heavenly_Stems.md",
            "KR-000005": "KR-000005_Earthly_Branches.md",
            "KR-000006": "KR-000006_Hidden_Stems_Composition_System.md",
            "KR-000007": "KR-000007_Sexagenary_Cycle_Registry.md",
            "KR-000008": "KR-000008_Na_Yin_System.md",
            "KR-000009": "KR-000009_Void_Branch_System.md",
            "KR-000010": "KR-000010_Cycle_Mapping_System.md",
            "KR-000011": "KR-000011_Ten_Gods.md",
            "KR-000012": "KR-000012_Twelve_Growth_Phases.md",
            "KR-000013": "KR-000013_Shen_Sha_System.md",
            "KR-000014": "KR-000014_Combination_Clash_System.md",
            "KR-000015": "KR-000015_Seasonal_Influence_System.md",
        },
        "optional_artifacts": [
            "knowledge/baseline/v1.0.0/baseline_manifest.json",
            "knowledge/baseline/v1.0.0/checksums.json",
            "knowledge/baseline/v1.0.0/statistics.json",
            "knowledge/search/search_index.json",
            "knowledge/search/search_statistics.json",
            "knowledge/graph/generated/v2/graph_manifest.json",
            "knowledge/generated/registry_index.json",
        ],
    },
    "PACK_02": {
        "pack_id": "PACK_02",
        "title": "Pack 02 — Placeholder",
        "module_id": "01_fundamental_knowledge",
        "version": "0.0.0",
        "status": "planned",
        "description": "Future pack scaffold for compatibility testing.",
        "records_dir": "knowledge/bazi/01_fundamental_knowledge/records",
        "record_ids": [],
        "record_files": {},
        "optional_artifacts": [],
    },
}
