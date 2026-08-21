"""One-time G3-02L-R1 container runtime path audit. Read-only."""

from __future__ import annotations

from pathlib import Path

ROOT = Path("/app")

CHECKS = [
    "database",
    "knowledge",
    "knowledge/interpretation",
    "knowledge/interpretation/knowledge_registry.json",
    "knowledge/interpretation/concepts/concept_registry.json",
    "knowledge/interpretation/domains/useful_god",
    "knowledge/interpretation/domains/strength",
    "knowledge/interpretation/domains/pattern",
    "knowledge/interpretation/domains/ten_gods",
    "knowledge/interpretation/domains/shensha",
    "knowledge/interpretation/concepts/core",
    "knowledge/expert_translation/translation_rules.json",
    "knowledge/packages/luck/foundation/PACKAGE.json",
    "knowledge/knowledge_catalog",
    "engines/calendar_engine/data",
    "engines/calendar_engine/solar_terms/data",
    "database/09_hidden_stems",
    "database/11_temperature",
    "database/12_strength",
    "database/13_useful_god",
    "database/14_pattern",
    "database/15_score_engine",
    "database/05_phan_tich/07_than_sat",
    "database/01_du_lieu_goc",
    "database/02_quan_he",
    "database/20_knowledge",
    "database/interpretation_rules",
    "engines/report_engine/templates/v1",
    "knowledge/packages",
    "applications/customer_portal/templates",
    "applications/customer_portal/static",
    "applications/data",
]


def main() -> int:
    print("=== G3-01 + interpretation runtime path audit ===")
    missing: list[str] = []
    for rel in CHECKS:
        path = ROOT / rel
        ok = path.exists()
        kind = "dir" if path.is_dir() else ("file" if path.is_file() else "MISSING")
        print(f"{'OK' if ok else 'MISSING':7} {kind:8} {path}")
        if not ok:
            missing.append(rel)
    print("---")
    domains = ROOT / "knowledge/interpretation/domains"
    if domains.is_dir():
        for directory in sorted(p for p in domains.iterdir() if p.is_dir()):
            print(f"domain {directory.name}: {len(list(directory.glob('*.json')))} json")
    core = ROOT / "knowledge/interpretation/concepts/core"
    print(f"concepts/core json: {len(list(core.glob('*.json'))) if core.is_dir() else 0}")
    print(f"missing_count={len(missing)}")
    for item in missing:
        print("MISSING", item)
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
