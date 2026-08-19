"""10 Day Masters × 10 stems = 100 mapping regression.

Expected Ten God is derived from STEM polarity + ngũ hành generate/control
rules in ``quy_tac.md``. It does not copy ``ten_god_name`` and is not
tied to Golden CASE-0001.
"""

from __future__ import annotations

import csv
from pathlib import Path

from engines.bazi_engine.ten_god import (
    POLARITY_DIFF,
    POLARITY_SAME,
    RELATION_DM_CONTROLS,
    RELATION_DM_GENERATES,
    RELATION_OTHER_CONTROLS,
    RELATION_OTHER_GENERATES,
    RELATION_SAME,
    element_relation,
    polarity_relation,
    stem_element,
    stem_mapping_facts,
    stem_yin_yang,
    ten_god_name,
)

# Independent oracle — copied from STEM identity + quy_tac Chính/Thiên.
_STEM_META: dict[str, tuple[str, str]] = {
    "Giáp": ("Mộc", "Dương"),
    "Ất": ("Mộc", "Âm"),
    "Bính": ("Hỏa", "Dương"),
    "Đinh": ("Hỏa", "Âm"),
    "Mậu": ("Thổ", "Dương"),
    "Kỷ": ("Thổ", "Âm"),
    "Canh": ("Kim", "Dương"),
    "Tân": ("Kim", "Âm"),
    "Nhâm": ("Thủy", "Dương"),
    "Quý": ("Thủy", "Âm"),
}

_STEMS = tuple(_STEM_META.keys())

_GENERATES: dict[str, str] = {
    "Mộc": "Hỏa",
    "Hỏa": "Thổ",
    "Thổ": "Kim",
    "Kim": "Thủy",
    "Thủy": "Mộc",
}

_CONTROLS: dict[str, str] = {
    "Mộc": "Thổ",
    "Hỏa": "Kim",
    "Thổ": "Thủy",
    "Kim": "Mộc",
    "Thủy": "Hỏa",
}

_CSV_PATH = (
    Path(__file__).resolve().parents[2]
    / "database"
    / "02_quan_he"
    / "thap_than"
    / "du_lieu.csv"
)


def _expected_relation(day_master: str, other: str) -> str:
    dm_el, other_el = _STEM_META[day_master][0], _STEM_META[other][0]
    if dm_el == other_el:
        return RELATION_SAME
    if _GENERATES[other_el] == dm_el:
        return RELATION_OTHER_GENERATES
    if _GENERATES[dm_el] == other_el:
        return RELATION_DM_GENERATES
    if _CONTROLS[dm_el] == other_el:
        return RELATION_DM_CONTROLS
    if _CONTROLS[other_el] == dm_el:
        return RELATION_OTHER_CONTROLS
    raise AssertionError(f"no ngũ hành relation for {day_master}×{other}")


def _expected_polarity(day_master: str, other: str) -> str:
    same = _STEM_META[day_master][1] == _STEM_META[other][1]
    return POLARITY_SAME if same else POLARITY_DIFF


def _expected_ten_god(day_master: str, other: str) -> str:
    relation = _expected_relation(day_master, other)
    same = _expected_polarity(day_master, other) == POLARITY_SAME
    if relation == RELATION_SAME:
        return "Tỷ Kiên" if same else "Kiếp Tài"
    if relation == RELATION_OTHER_GENERATES:
        return "Thiên Ấn" if same else "Chính Ấn"
    if relation == RELATION_DM_GENERATES:
        return "Thực Thần" if same else "Thương Quan"
    if relation == RELATION_DM_CONTROLS:
        return "Thiên Tài" if same else "Chính Tài"
    if relation == RELATION_OTHER_CONTROLS:
        return "Thất Sát" if same else "Chính Quan"
    raise AssertionError(f"no Ten God for {day_master}×{other}")


def _load_csv() -> dict[tuple[str, str], dict[str, str]]:
    rows: dict[tuple[str, str], dict[str, str]] = {}
    with _CSV_PATH.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            key = (str(row["nhat_chu"]), str(row["doi_tuong"]))
            rows[key] = row
    return rows


def test_mapping_matrix_100() -> None:
    """Every Day Master × stem pair matches oracle, algorithm, and CSV."""
    csv_rows = _load_csv()
    failures: list[str] = []
    count = 0
    for day_master in _STEMS:
        for other in _STEMS:
            count += 1
            expected_element = _STEM_META[other][0]
            expected_polarity = _STEM_META[other][1]
            expected_relation = _expected_relation(day_master, other)
            expected_yin_yang = _expected_polarity(day_master, other)
            expected_god = _expected_ten_god(day_master, other)
            facts = stem_mapping_facts(day_master, other)
            csv_row = csv_rows.get((day_master, other))
            checks = {
                "element": (
                    expected_element,
                    stem_element(other),
                    facts["element"],
                ),
                "polarity": (
                    expected_polarity,
                    stem_yin_yang(other),
                    facts["yin_yang"],
                ),
                "relationship": (
                    expected_relation,
                    element_relation(day_master, other),
                    facts["element_relation"],
                ),
                "yin_yang_relation": (
                    expected_yin_yang,
                    polarity_relation(day_master, other),
                    facts["polarity_relation"],
                ),
                "ten_god": (
                    expected_god,
                    ten_god_name(day_master, other),
                    facts["ten_god"],
                ),
            }
            for name, (oracle, algorithm, fact) in checks.items():
                if oracle != algorithm or oracle != fact:
                    failures.append(
                        f"{day_master}×{other} {name}: "
                        f"oracle={oracle!r} algorithm={algorithm!r} facts={fact!r}"
                    )
            if csv_row is None:
                failures.append(f"{day_master}×{other} missing CSV row")
                continue
            if csv_row["quan_he_ngu_hanh"] != expected_relation:
                failures.append(
                    f"{day_master}×{other} CSV relation "
                    f"{csv_row['quan_he_ngu_hanh']!r} != {expected_relation!r}"
                )
            if csv_row["quan_he_am_duong"] != expected_yin_yang:
                failures.append(
                    f"{day_master}×{other} CSV polarity "
                    f"{csv_row['quan_he_am_duong']!r} != {expected_yin_yang!r}"
                )
            if csv_row["thap_than"] != expected_god:
                failures.append(
                    f"{day_master}×{other} CSV ten god "
                    f"{csv_row['thap_than']!r} != {expected_god!r}"
                )
    assert count == 100
    assert len(csv_rows) == 100
    assert failures == []
