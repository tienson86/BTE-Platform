"""Personal Cung Phi / Mệnh Quái from Gregorian year digits.

Does not assume Hạ Nguyên. Ganzhi palace lookup uses the Tam Nguyên of the
reference civil year.
"""

from __future__ import annotations

from dataclasses import dataclass

from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm
from engines.calendar_engine.exceptions import CalendarValidationError
from engines.calendar_engine.tam_nguyen import HA_NGUYEN, yuan_start_year

REMAINDER_WHEN_ZERO = 9

MALE_CUNG_BY_REMAINDER: dict[int, str] = {
    1: "Khảm",
    2: "Ly",
    3: "Cấn",
    4: "Đoài",
    5: "Càn",
    6: "Khôn",
    7: "Tốn",
    8: "Chấn",
    9: "Khôn",
}

FEMALE_CUNG_BY_REMAINDER: dict[int, str] = {
    1: "Cấn",
    2: "Càn",
    3: "Đoài",
    4: "Cấn",
    5: "Ly",
    6: "Khảm",
    7: "Khôn",
    8: "Chấn",
    9: "Tốn",
}

LO_SHU_NUMBER_BY_CUNG: dict[str, int] = {
    "Khảm": 1,
    "Khôn": 2,
    "Chấn": 3,
    "Tốn": 4,
    "Càn": 6,
    "Đoài": 7,
    "Cấn": 8,
    "Ly": 9,
}

EAST_HOUSE_GROUP = "Đông Tứ Trạch"
WEST_HOUSE_GROUP = "Tây Tứ Trạch"
EAST_CUNG = frozenset({"Khảm", "Ly", "Chấn", "Tốn"})
WEST_CUNG = frozenset({"Càn", "Khôn", "Cấn", "Đoài"})

_MALE_GENDER_ALIASES = frozenset({"male", "nam", "m", "1", "man", "boy"})
_FEMALE_GENDER_ALIASES = frozenset({"female", "nu", "nữ", "f", "2", "woman", "girl"})


@dataclass(slots=True)
class CungPhiResult:
    """Personal Cung Phi derived from Gregorian year + gender."""

    remainder: int
    cung_phi: str
    menh_quai: str
    house_group: str
    gua_number: int

    def to_dict(self) -> dict[str, str | int]:
        """Serialize Cung Phi fields. ``nhom_trach`` is the public alias."""
        return {
            "remainder": self.remainder,
            "cung_phi": self.cung_phi,
            "menh_quai": self.menh_quai,
            "house_group": self.house_group,
            "nhom_trach": self.house_group,
            "gua_number": self.gua_number,
        }


def gregorian_digit_sum(year: int) -> int:
    """Sum every decimal digit of the Gregorian birth year."""
    if int(year) < 1:
        raise CalendarValidationError(f"invalid Gregorian birth year: {year}")
    return sum(int(digit) for digit in str(abs(int(year))))


def remainder_from_year(year: int) -> int:
    """Digit-sum modulo 9, with 0 mapped to 9."""
    remainder = gregorian_digit_sum(year) % 9
    return REMAINDER_WHEN_ZERO if remainder == 0 else remainder


def normalize_gender(gender: str | None) -> str:
    """Return canonical ``male`` / ``female``. Never default a missing gender."""
    if gender is None or str(gender).strip() == "":
        raise CalendarValidationError("gender is required for Cung Phi calculation")
    key = str(gender).strip().lower()
    if key in _MALE_GENDER_ALIASES:
        return "male"
    if key in _FEMALE_GENDER_ALIASES:
        return "female"
    raise CalendarValidationError(f"unsupported gender: {gender!r}")


def house_group_for_cung(cung: str) -> str:
    """Return Đông / Tây Tứ Trạch from a palace name."""
    key = (cung or "").strip()
    if key in EAST_CUNG:
        return EAST_HOUSE_GROUP
    if key in WEST_CUNG:
        return WEST_HOUSE_GROUP
    raise CalendarValidationError(f"unknown Cung Phi: {cung!r}")


def gua_number_for_cung(cung: str) -> int:
    """Lo Shu number for a palace name (never 5)."""
    try:
        return LO_SHU_NUMBER_BY_CUNG[cung.strip()]
    except KeyError as exc:
        raise CalendarValidationError(f"unknown Cung Phi: {cung!r}") from exc


def cung_name_for_remainder(remainder: int, gender: str) -> str:
    """Map remainder 1–9 to palace name using the gender table."""
    sex = normalize_gender(gender)
    table = MALE_CUNG_BY_REMAINDER if sex == "male" else FEMALE_CUNG_BY_REMAINDER
    try:
        return table[int(remainder)]
    except KeyError as exc:
        raise CalendarValidationError(f"invalid Cung Phi remainder: {remainder}") from exc


def calculate_cung_phi(*, year: int, gender: str | None) -> CungPhiResult:
    """Personal Cung Phi from Gregorian birth year digits and gender."""
    remainder = remainder_from_year(year)
    cung = cung_name_for_remainder(remainder, gender)
    return CungPhiResult(
        remainder=remainder,
        cung_phi=cung,
        menh_quai=cung,
        house_group=house_group_for_cung(cung),
        gua_number=gua_number_for_cung(cung),
    )


def _normalize_ganzhi(ganzhi: str) -> str:
    text = " ".join((ganzhi or "").split())
    if not text:
        raise CalendarValidationError("ganzhi is required")
    return text


def jiazi_index(ganzhi: str) -> int:
    """Return 0–59 index of a Hoa Giáp label (Giáp Tý = 0)."""
    key = _normalize_ganzhi(ganzhi)
    parts = key.split()
    if len(parts) < 2:
        raise CalendarValidationError(f"unknown Ganzhi: {ganzhi!r}")
    try:
        stem_i = GanzhiAlgorithm.STEM.index(parts[0])
        branch_i = GanzhiAlgorithm.BRANCH.index(parts[1])
    except ValueError as exc:
        raise CalendarValidationError(f"unknown Ganzhi: {ganzhi!r}") from exc
    for index in range(60):
        if index % 10 == stem_i and index % 12 == branch_i:
            return index
    raise CalendarValidationError(f"unknown Ganzhi: {ganzhi!r}")


def year_for_ganzhi_in_yuan(
    ganzhi: str,
    *,
    tam_nguyen: str,
    reference_year: int,
) -> int:
    """Civil year of ``ganzhi`` inside the given Nguyên of ``reference_year``'s cycle."""
    start = yuan_start_year(reference_year, tam_nguyen)
    return start + jiazi_index(ganzhi)


def ganzhi_label_for_year(year: int) -> str:
    """60 Hoa Giáp label of a civil year inside its Tam Nguyên block (Giáp Tý = 0)."""
    start = yuan_start_year(year)
    index = (int(year) - start) % 60
    return f"{GanzhiAlgorithm.STEM[index % 10]} {GanzhiAlgorithm.BRANCH[index % 12]}"


def cung_for_ganzhi(
    ganzhi: str,
    *,
    tam_nguyen: str,
    reference_year: int,
    gender: str | None = "male",
) -> str:
    """Palace for a Hoa Giáp label in a specific Tam Nguyên.

    Intrinsic date/hour Cung uses the male mapping of that Yuan's civil year.
    Does not fall back to Hạ Nguyên.
    """
    if not tam_nguyen:
        raise CalendarValidationError("tam_nguyen is required for Ganzhi Cung lookup")
    year = year_for_ganzhi_in_yuan(
        ganzhi,
        tam_nguyen=tam_nguyen,
        reference_year=reference_year,
    )
    return calculate_cung_phi(year=year, gender=gender or "male").cung_phi


def ha_nguyen_cung_for_ganzhi(ganzhi: str, *, reference_year: int = 1984) -> str:
    """Hạ Nguyên palace for a Ganzhi — explicit Yuan, never an implicit default."""
    return cung_for_ganzhi(
        ganzhi,
        tam_nguyen=HA_NGUYEN,
        reference_year=reference_year,
        gender="male",
    )
