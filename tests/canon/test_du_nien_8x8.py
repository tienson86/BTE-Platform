"""Canonical Du Niên 8×8 matrix tests. Knowledge lookup only."""

from __future__ import annotations

from pathlib import Path

from consulting.canon.du_nien import (
    CANON_PATH,
    PALACES,
    RELATIONSHIP_IDS,
    load_matrix,
    lookup,
)

ROOT = Path(__file__).resolve().parents[2]
FORBIDDEN_COPY = (
    "chắc chắn ly hôn",
    "khắc chết",
    "đại hung",
    "không nên cưới",
)
REPRESENTATIVE = (
    ("Khảm", "Tốn", "sinh_khi", "Sinh Khí"),
    ("Khảm", "Chấn", "thien_y", "Thiên Y"),
    ("Khảm", "Ly", "dien_nien", "Diên Niên"),
    ("Khảm", "Khảm", "phuc_vi", "Phục Vị"),
    ("Khôn", "Khảm", "tuyet_menh", "Tuyệt Mệnh"),
    ("Khôn", "Chấn", "ngu_quy", "Ngũ Quỷ"),
    ("Khảm", "Càn", "luc_sat", "Lục Sát"),
    ("Khảm", "Đoài", "hoa_hai", "Họa Hại"),
)


def test_khon_to_kham_is_tuyet_menh() -> None:
    """Khôn → Khảm is Tuyệt Mệnh, never Ngũ Quỷ."""
    item = lookup("Khôn", "Khảm")
    assert item is not None
    assert item.relationship_id == "tuyet_menh"
    assert item.relationship_label == "Tuyệt Mệnh"
    assert item.category == "unfavorable"
    assert lookup("Khôn", "Khảm").relationship_label != "Ngũ Quỷ"


def test_full_matrix_has_64_unique_ordered_pairs() -> None:
    """Exactly eight palaces and 64 ordered pairs, no duplicates or gaps."""
    matrix = load_matrix()
    assert len(PALACES) == 8
    assert set(PALACES) == {
        "Khảm",
        "Khôn",
        "Chấn",
        "Tốn",
        "Càn",
        "Đoài",
        "Cấn",
        "Ly",
    }
    assert len(matrix) == 64
    assert {key[0] for key in matrix} == set(PALACES)
    assert {key[1] for key in matrix} == set(PALACES)
    assert len(set(matrix)) == 64
    for source in PALACES:
        for target in PALACES:
            item = matrix[(source, target)]
            assert item.relationship_id in RELATIONSHIP_IDS
            assert item.relationship_label
            assert item.category in {"favorable", "unfavorable"}


def test_each_source_row_contains_all_eight_relationships() -> None:
    """Each palace maps to all eight Du Niên identities exactly once."""
    matrix = load_matrix()
    for source in PALACES:
        ids = {matrix[(source, target)].relationship_id for target in PALACES}
        assert ids == set(RELATIONSHIP_IDS)


def test_matrix_is_directional() -> None:
    """Approved contract is ordered-pair lookup. A,B is not assumed equal to B,A."""
    forward = lookup("Khảm", "Ly")
    reverse = lookup("Ly", "Khảm")
    assert forward is not None and reverse is not None
    assert (forward.source_palace, forward.target_palace) == ("Khảm", "Ly")
    assert (reverse.source_palace, reverse.target_palace) == ("Ly", "Khảm")
    assert forward.relationship_id != reverse.relationship_id
    same = lookup("Khôn", "Khảm")
    mirrored = lookup("Khảm", "Khôn")
    assert same is not None and mirrored is not None
    assert same.relationship_label == "Tuyệt Mệnh"
    assert mirrored.relationship_label == "Tuyệt Mệnh"


def test_representative_relationship_types() -> None:
    """One canonical example exists for each relationship identity."""
    for source, target, rel_id, label in REPRESENTATIVE:
        item = lookup(source, target)
        assert item is not None
        assert item.relationship_id == rel_id
        assert item.relationship_label == label
        assert item.relationship_id == rel_id


def test_customer_label_matches_relationship_id() -> None:
    """Every pair's label belongs to the same catalog id."""
    matrix = load_matrix()
    labels = {item.relationship_id: item.relationship_label for item in matrix.values()}
    assert labels["sinh_khi"] == "Sinh Khí"
    assert labels["thien_y"] == "Thiên Y"
    assert labels["dien_nien"] == "Diên Niên"
    assert labels["phuc_vi"] == "Phục Vị"
    assert labels["tuyet_menh"] == "Tuyệt Mệnh"
    assert labels["ngu_quy"] == "Ngũ Quỷ"
    assert labels["luc_sat"] == "Lục Sát"
    assert labels["hoa_hai"] == "Họa Hại"
    for item in matrix.values():
        assert labels[item.relationship_id] == item.relationship_label


def test_customer_wording_is_not_fatalistic() -> None:
    """Secondary copy must not claim divorce or death."""
    for item in load_matrix().values():
        blob = f"{item.customer_summary} {item.expert_summary}".lower()
        for phrase in FORBIDDEN_COPY:
            assert phrase not in blob


def test_single_canonical_file_is_the_runtime_source() -> None:
    """Runtime loader points at knowledge/canon/du_nien_8x8.yaml only."""
    assert CANON_PATH == ROOT / "knowledge" / "canon" / "du_nien_8x8.yaml"
    assert CANON_PATH.is_file()
    assert "Khôn" in CANON_PATH.read_text(encoding="utf-8")


def test_no_competing_active_matrix_in_runtime_code() -> None:
    """Production Python must not keep a second 8×8 palace-pair table."""
    skip_parts = {"tests", ".venv", "node_modules", "__pycache__", "docs"}
    leaks: list[str] = []
    for path in ROOT.rglob("*.py"):
        if any(part in skip_parts for part in path.parts):
            continue
        if path.name == "du_nien.py" and "consulting" in path.parts and "canon" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if '("Khôn", "Khảm")' in text or "('Khôn', 'Khảm')" in text:
            leaks.append(str(path.relative_to(ROOT)))
        if text.count('("Khảm"') >= 8 and "Tuyệt Mệnh" in text and "Ngũ Quỷ" in text:
            leaks.append(str(path.relative_to(ROOT)))
    assert leaks == []
