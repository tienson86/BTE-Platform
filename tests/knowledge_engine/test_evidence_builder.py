"""Unit tests for Evidence Builder (Epic 03 Milestone 05)."""

from __future__ import annotations

import json
from pathlib import Path

from engines.knowledge_engine import (
    CATEGORY_LABELS,
    EVIDENCE_CATEGORIES,
    EvidenceBuilder,
    EvidenceItem,
)


REPORT_PATH = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "reports"
    / "knowledge_evidence_validation_m05.md"
)


def _rich_context() -> dict:
    return {
        "day_master": "Bính",
        "day_master_element": "Hỏa",
        "birth_season": "summer",
        "bazi": {
            "day_master": "Bính",
            "day_master_element": "Hỏa",
            "day_master_yin_yang": "Dương",
            "year_pillar": {"stem": "Canh", "branch": "Ngọ"},
            "month_pillar": {"stem": "Ất", "branch": "Tỵ"},
            "day_pillar": {"stem": "Bính", "branch": "Ngọ"},
            "hour_pillar": {"stem": "Quý", "branch": "Tỵ"},
            "ten_gods": ["Thất Sát", "Chính Ấn"],
            "shensha": ["Hoa Cái"],
        },
        "wuxing": {
            "season": "summer",
            "fire": {"status": "strong", "count": 7},
            "water": {"status": "weak", "count": 1},
            "wood": "present",
        },
        "ten_gods": {
            "status": "ok",
            "items": ["Chính Quan", "Thất Sát"],
            "by_name": {"Thiên Ấn": True, "Kiếp Tài": False},
        },
        "useful_god": {
            "status": "ok",
            "name": "Thủy",
            "element": "Thủy",
            "favorable": ["Kim"],
            "unfavorable": ["Hỏa"],
        },
        "pattern": {
            "main_pattern": "chinh_quan",
            "name": "Chính Quan",
            "status": "ok",
            "follow_type": "none",
            "category": "officer",
        },
        "strength": {
            "level": "strong",
            "month_status": "旺",
            "root_level": "通根",
            "support_type": "印",
            "control_type": "官",
        },
        "temperature": {
            "status": "warm",
            "hot_score": 0.7,
            "cold_score": 0.2,
        },
        "shensha": {
            "status": "ok",
            "stars": ["Hoa Cái", "Văn Xương"],
            "available": {"Quốc Ấn": True, "Dịch Mã": False},
        },
    }


class TestEvidenceBuilder:
    def test_all_categories_extracted(self) -> None:
        package = EvidenceBuilder().build(_rich_context())
        for key in EVIDENCE_CATEGORIES:
            assert key in package.categories
            assert package.categories[key], f"missing items for {key}"
            assert package.for_category(key)

    def test_item_fields_present(self) -> None:
        package = EvidenceBuilder().build(_rich_context())
        assert package.items
        for item in package.items:
            assert item.rule
            assert item.reason
            assert 0.0 <= item.confidence <= 1.0
            assert item.source.startswith("rule_context:")
            assert item.category in EVIDENCE_CATEGORIES

    def test_no_duplicated_evidence(self) -> None:
        # Duplicate day_master at top-level and bazi should collapse by rule+source.
        context = {
            "day_master": "Bính",
            "bazi": {"day_master": "Bính"},
            "ten_gods": {"items": ["Chính Quan", "Chính Quan"]},
            "shensha": {"stars": ["Hoa Cái", "Hoa Cái"]},
        }
        package = EvidenceBuilder().build(context)
        keys = [item.dedupe_key for item in package.items]
        assert len(keys) == len(set(keys))
        # Same rule+source from repeated list values should appear once.
        ten_god_rules = [
            item.rule for item in package.categories["ten_gods"] if item.rule.startswith("present=")
        ]
        assert ten_god_rules.count("present=Chính Quan") == 1

    def test_duplicate_removed_metadata(self) -> None:
        builder = EvidenceBuilder()
        # Force duplicate by collecting same source twice through by_name + items.
        context = {
            "ten_gods": {
                "items": ["Chính Quan"],
                "by_name": {"Chính Quan": True},
            }
        }
        package = builder.build(context)
        # items and by_name use different sources, so both may remain.
        # Inject explicit duplicates via second build merge simulation:
        item = EvidenceItem(
            category="ten_gods",
            rule="present=Chính Quan",
            reason="dup",
            confidence=0.5,
            source="rule_context:ten_gods.items",
        )
        unique, removed = builder._dedupe(package.items + [item, item])
        assert removed >= 1
        assert len({row.dedupe_key for row in unique}) == len(unique)

    def test_empty_context(self) -> None:
        package = EvidenceBuilder().build({})
        assert package.items == []
        assert package.metadata["item_count"] == 0
        assert package.metadata["duplicate_removed"] == 0
        assert package.trace
        assert len(package.trace) == len(EVIDENCE_CATEGORIES)

    def test_to_dict_and_labels(self) -> None:
        package = EvidenceBuilder().build(_rich_context())
        payload = package.to_dict()
        assert set(payload["categories"]) >= set(EVIDENCE_CATEGORIES)
        first = payload["items"][0]
        assert first["category_label"] == CATEGORY_LABELS[first["category"]]
        assert "metadata" in payload

    def test_pillar_and_element_edges(self) -> None:
        package = EvidenceBuilder().build(_rich_context())
        bazi_rules = {item.rule for item in package.categories["bazi"]}
        assert "day_master=Bính" in bazi_rules
        assert "year_pillar=Canh Ngọ" in bazi_rules
        fe_rules = {item.rule for item in package.categories["five_elements"]}
        assert "fire.status=strong" in fe_rules
        assert "fire.count=7" in fe_rules


def test_evidence_validation_report() -> None:
    """Generate Milestone 05 validation report from representative contexts."""
    builder = EvidenceBuilder()
    samples = [
        ("rich", _rich_context()),
        (
            "minimal_officer",
            {
                "ten_gods": {"items": ["Chính Quan"]},
                "pattern": {"main_pattern": "chinh_quan"},
                "strength": {"level": "strong"},
            },
        ),
        (
            "weak_water",
            {
                "day_master_element": "Thủy",
                "strength": {"level": "weak"},
                "useful_god": {"element": "Thổ", "status": "ok"},
                "temperature": {"status": "cold", "cold_score": 0.8},
                "shensha": {"stars": ["Cô Thần"]},
            },
        ),
        ("empty", {}),
    ]

    rows = []
    total_items = 0
    total_dupes = 0
    for name, context in samples:
        package = builder.build(context)
        keys = [item.dedupe_key for item in package.items]
        assert len(keys) == len(set(keys))
        total_items += len(package.items)
        total_dupes += int(package.metadata.get("duplicate_removed") or 0)
        rows.append(
            {
                "sample": name,
                "item_count": len(package.items),
                "categories_present": package.metadata.get("categories_present"),
                "duplicate_removed": package.metadata.get("duplicate_removed"),
                "sample_rules": [item.rule for item in package.items[:8]],
            }
        )

    report = "\n".join(
        [
            "# Evidence Builder Validation Report — Epic 03 Milestone 05",
            "",
            "## Summary",
            "",
            f"- Samples validated: **{len(samples)}**",
            f"- Total evidence items: **{total_items}**",
            f"- Duplicates removed across builds: **{total_dupes}**",
            f"- Categories supported: **{', '.join(CATEGORY_LABELS[k] for k in EVIDENCE_CATEGORIES)}**",
            "",
            "## Evidence item contract",
            "",
            "- `rule`",
            "- `reason`",
            "- `confidence`",
            "- `source`",
            "",
            "## Dedup policy",
            "",
            "- Key: `category|rule|source` (case-insensitive)",
            "- Repeated identical facts are kept once",
            "",
            "## Sample digest",
            "",
            "```json",
            json.dumps(rows, ensure_ascii=False, indent=2),
            "```",
            "",
            "## Compatibility",
            "",
            "- Input: RuleContext only",
            "- No calculation engine changes",
            "- No UI changes",
            "",
        ]
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    assert REPORT_PATH.exists()
    assert total_items > 0
