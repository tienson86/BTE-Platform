"""Canonical identity catalog used by marriage.policy.v1.

These pairs identify stem/branch relations already published by BTE Combination
knowledge. They are matching tables, not score weights.
"""

from __future__ import annotations

from consulting.marriage.models.enums import FiveElement

_STEM_CANON: dict[str, str] = {
    "giap": "Giáp",
    "jia": "Giáp",
    "at": "Ất",
    "yi": "Ất",
    "binh": "Bính",
    "bing": "Bính",
    "dinh": "Đinh",
    "ding": "Đinh",
    "mau": "Mậu",
    "wu": "Mậu",
    "ky": "Kỷ",
    "ji": "Kỷ",
    "canh": "Canh",
    "geng": "Canh",
    "tan": "Tân",
    "xin": "Tân",
    "nham": "Nhâm",
    "ren": "Nhâm",
    "quy": "Quý",
    "gui": "Quý",
}

_BRANCH_CANON: dict[str, str] = {
    "ty": "Tý",
    "ti": "Tý",
    "zi": "Tý",
    "suu": "Sửu",
    "chou": "Sửu",
    "dan": "Dần",
    "yin": "Dần",
    "mao": "Mão",
    "thin": "Thìn",
    "chen": "Thìn",
    "ti_snake": "Tỵ",
    "si": "Tỵ",
    "ngo": "Ngọ",
    "wu_branch": "Ngọ",
    "mui": "Mùi",
    "wei": "Mùi",
    "than": "Thân",
    "shen": "Thân",
    "dau": "Dậu",
    "you": "Dậu",
    "tuat": "Tuất",
    "xu": "Tuất",
    "hoi": "Hợi",
    "hai": "Hợi",
}

_STEM_ELEMENT: dict[str, FiveElement] = {
    "Giáp": FiveElement.WOOD,
    "Ất": FiveElement.WOOD,
    "Bính": FiveElement.FIRE,
    "Đinh": FiveElement.FIRE,
    "Mậu": FiveElement.EARTH,
    "Kỷ": FiveElement.EARTH,
    "Canh": FiveElement.METAL,
    "Tân": FiveElement.METAL,
    "Nhâm": FiveElement.WATER,
    "Quý": FiveElement.WATER,
}

_CONTROL: dict[FiveElement, FiveElement] = {
    FiveElement.WOOD: FiveElement.EARTH,
    FiveElement.EARTH: FiveElement.WATER,
    FiveElement.WATER: FiveElement.FIRE,
    FiveElement.FIRE: FiveElement.METAL,
    FiveElement.METAL: FiveElement.WOOD,
}

STEM_COMBINATIONS: tuple[tuple[str, str, str], ...] = (
    ("Giáp", "Kỷ", "stem_jia_ji"),
    ("Ất", "Canh", "stem_yi_geng"),
    ("Bính", "Tân", "stem_bing_xin"),
    ("Đinh", "Nhâm", "stem_ding_ren"),
    ("Mậu", "Quý", "stem_wu_gui"),
)

BRANCH_COMBINATIONS: tuple[tuple[str, str, str], ...] = (
    ("Tý", "Sửu", "branch_zi_chou"),
    ("Dần", "Hợi", "branch_yin_hai"),
    ("Mão", "Tuất", "branch_mao_xu"),
    ("Thìn", "Dậu", "branch_chen_you"),
    ("Tỵ", "Thân", "branch_si_shen"),
    ("Ngọ", "Mùi", "branch_wu_wei"),
)

BRANCH_CLASHES: tuple[tuple[str, str, str], ...] = (
    ("Tý", "Ngọ", "clash_zi_wu"),
    ("Sửu", "Mùi", "clash_chou_wei"),
    ("Dần", "Thân", "clash_yin_shen"),
    ("Mão", "Dậu", "clash_mao_you"),
    ("Thìn", "Tuất", "clash_chen_xu"),
    ("Tỵ", "Hợi", "clash_si_hai"),
)

BRANCH_HARMS: tuple[tuple[str, str, str], ...] = (
    ("Tý", "Mùi", "harm_zi_wei"),
    ("Sửu", "Ngọ", "harm_chou_wu"),
    ("Dần", "Tỵ", "harm_yin_si"),
    ("Mão", "Thìn", "harm_mao_chen"),
    ("Thân", "Hợi", "harm_shen_hai"),
    ("Dậu", "Tuất", "harm_you_xu"),
)

BRANCH_BREAKS: tuple[tuple[str, str, str], ...] = (
    ("Tý", "Dậu", "destroy_zi_you"),
    ("Sửu", "Thìn", "destroy_chou_chen"),
    ("Dần", "Hợi", "destroy_yin_hai"),
    ("Mão", "Ngọ", "destroy_mao_wu"),
    ("Tỵ", "Thân", "destroy_si_shen"),
    ("Ngọ", "Dậu", "destroy_wu_you"),
)

BRANCH_PUNISH_PAIRS: tuple[tuple[str, str, str], ...] = (
    ("Tý", "Mão", "punish_zi_mao"),
)

BRANCH_SELF_PUNISH: frozenset[str] = frozenset({"Thìn", "Ngọ", "Dậu", "Hợi"})

BRANCH_PUNISH_TRIADS: tuple[tuple[frozenset[str], str], ...] = (
    (frozenset({"Dần", "Tỵ", "Thân"}), "punish_yin_si_shen"),
    (frozenset({"Sửu", "Tuất", "Mùi"}), "punish_chou_xu_wei"),
)

BRANCH_MEETING_TRIADS: tuple[tuple[frozenset[str], str], ...] = (
    (frozenset({"Thân", "Tý", "Thìn"}), "triad_water"),
    (frozenset({"Dần", "Ngọ", "Tuất"}), "triad_fire"),
    (frozenset({"Tỵ", "Dậu", "Sửu"}), "triad_metal"),
    (frozenset({"Hợi", "Mão", "Mùi"}), "triad_wood"),
)

_WEALTH_ROLES: frozenset[str] = frozenset(
    {"chinh tai", "thien tai", "chinh_tai", "thien_tai", "wealth"}
)
_WEALTH_PRESSURE_ROLES: frozenset[str] = frozenset({"kiep tai", "rob wealth"})


def _fold(token: str) -> str:
    """Fold a label for alias lookup."""
    raw = token.strip().lower()
    replacements = (
        ("á", "a"),
        ("à", "a"),
        ("ả", "a"),
        ("ã", "a"),
        ("ạ", "a"),
        ("ă", "a"),
        ("ắ", "a"),
        ("ấ", "a"),
        ("ầ", "a"),
        ("ẩ", "a"),
        ("ẫ", "a"),
        ("ậ", "a"),
        ("é", "e"),
        ("è", "e"),
        ("ẻ", "e"),
        ("ẽ", "e"),
        ("ẹ", "e"),
        ("ê", "e"),
        ("ế", "e"),
        ("ề", "e"),
        ("ể", "e"),
        ("ễ", "e"),
        ("ệ", "e"),
        ("í", "i"),
        ("ì", "i"),
        ("ỉ", "i"),
        ("ĩ", "i"),
        ("ị", "i"),
        ("ó", "o"),
        ("ò", "o"),
        ("ỏ", "o"),
        ("õ", "o"),
        ("ọ", "o"),
        ("ô", "o"),
        ("ố", "o"),
        ("ồ", "o"),
        ("ổ", "o"),
        ("ỗ", "o"),
        ("ộ", "o"),
        ("ơ", "o"),
        ("ớ", "o"),
        ("ờ", "o"),
        ("ở", "o"),
        ("ỡ", "o"),
        ("ợ", "o"),
        ("ú", "u"),
        ("ù", "u"),
        ("ủ", "u"),
        ("ũ", "u"),
        ("ụ", "u"),
        ("ư", "u"),
        ("ứ", "u"),
        ("ừ", "u"),
        ("ử", "u"),
        ("ữ", "u"),
        ("ự", "u"),
        ("ý", "y"),
        ("ỳ", "y"),
        ("ỷ", "y"),
        ("ỹ", "y"),
        ("ỵ", "y"),
        ("đ", "d"),
    )
    folded = raw
    for src, dst in replacements:
        folded = folded.replace(src, dst)
    return folded


def normalize_stem(token: str | None) -> str | None:
    """Return the canonical Vietnamese stem label."""
    if not token:
        return None
    stripped = token.strip()
    if stripped in _STEM_ELEMENT:
        return stripped
    return _STEM_CANON.get(_fold(stripped))


def normalize_branch(token: str | None) -> str | None:
    """Return the canonical Vietnamese branch label."""
    if not token:
        return None
    stripped = token.strip()
    canonical_branches = {
        "Tý",
        "Sửu",
        "Dần",
        "Mão",
        "Thìn",
        "Tỵ",
        "Ngọ",
        "Mùi",
        "Thân",
        "Dậu",
        "Tuất",
        "Hợi",
    }
    if stripped in canonical_branches:
        return stripped
    if any(char in stripped for char in ("ỵ", "Ỵ")):
        return "Tỵ"
    folded = _fold(stripped)
    if folded == "zi":
        return "Tý"
    if folded == "si":
        return "Tỵ"
    if folded == "wu":
        return "Ngọ"
    return _BRANCH_CANON.get(folded)


def stem_element(token: str | None) -> FiveElement | None:
    """Map a stem identity onto its five-element."""
    canonical = normalize_stem(token)
    if canonical is None:
        return None
    return _STEM_ELEMENT.get(canonical)


def pair_relation(
    pairs: tuple[tuple[str, str, str], ...],
    left: str | None,
    right: str | None,
) -> str | None:
    """Return a relation id when two canonical tokens match a pair."""
    a = left
    b = right
    if a is None or b is None:
        return None
    for first, second, relation_id in pairs:
        if (a == first and b == second) or (a == second and b == first):
            return relation_id
    return None


def stem_controls(source: FiveElement | None, target: FiveElement | None) -> bool:
    """Return True when source controls target on the five-element cycle."""
    if source is None or target is None:
        return False
    return _CONTROL.get(source) is target


def normalize_role(token: str | None) -> str:
    """Fold a ten-god role label for catalog matching."""
    return _fold(token or "")


def is_wealth_role(token: str | None) -> bool:
    """Return True when the role is a wealth star identity."""
    folded = normalize_role(token)
    if folded in _WEALTH_PRESSURE_ROLES or "kiep tai" in folded:
        return False
    return folded in _WEALTH_ROLES


def is_wealth_pressure_role(token: str | None) -> bool:
    """Return True when the role is a wealth-competition identity."""
    folded = normalize_role(token)
    return folded in _WEALTH_PRESSURE_ROLES or "kiep tai" in folded
