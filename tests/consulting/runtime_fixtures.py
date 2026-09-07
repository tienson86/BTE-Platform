"""Shared TV1-B02 runtime test fixtures. No business assertions."""

from __future__ import annotations

from typing import Any, Mapping

from consulting.marriage.dto.request import (
    MarriageConsultationRequest,
    MarriagePersonInput,
)
from consulting.marriage.models.enums import CanonicalGender


def person(
    *,
    gender: CanonicalGender,
    birth_date: str,
    birth_time: str | None = "04:30",
    full_name: str | None = " Person ",
    timezone: str | None = " Asia/Ho_Chi_Minh ",
) -> MarriagePersonInput:
    """Build a person input for runtime tests."""
    return MarriagePersonInput(
        gender=gender,
        birth_date=birth_date,
        birth_time=birth_time,
        full_name=full_name,
        timezone=timezone,
    )


def valid_request(
    *,
    time_a: str | None = "04:30",
    time_b: str | None = "10:00",
) -> MarriageConsultationRequest:
    """Return a structurally valid two-person request."""
    return MarriageConsultationRequest(
        person_a=person(
            gender=CanonicalGender.MALE,
            birth_date="1987-01-21",
            birth_time=time_a,
        ),
        person_b=person(
            gender=CanonicalGender.FEMALE,
            birth_date="1990-05-15",
            birth_time=time_b,
        ),
    )


def canonical_payload(*, hour_stem: str = "Mậu") -> dict[str, Any]:
    """Minimal Canonical payload shape used by the snapshot builder."""
    pillar = {
        "stem": "Canh",
        "branch": "Ngọ",
        "hidden_stems": ["Đinh", "Kỷ"],
        "ten_god": "Nhật Chủ",
        "nap_am": "",
        "truong_sinh": "",
    }
    hour = dict(pillar)
    hour["stem"] = hour_stem
    hour["branch"] = "Dần"
    return {
        "bazi": {
            "year_pillar": {"stem": "Bính", "branch": "Dần", "hidden_stems": ["Giáp"], "ten_god": "Thất Sát"},
            "month_pillar": {"stem": "Tân", "branch": "Sửu", "hidden_stems": ["Kỷ"], "ten_god": "Thương Quan"},
            "day_pillar": pillar,
            "hour_pillar": hour,
            "day_master": "Canh",
            "day_master_element": "Kim",
            "day_master_yin_yang": "Dương",
            "shensha": ["Đào Hoa"],
        },
        "five_elements": {"counts": {"wood": 4, "fire": 5, "earth": 6, "metal": 3, "water": 1}},
        "strength": {"strength_level": "strong", "strength_score": 0.87, "confidence": 0.9},
        "pattern": {"pattern": "chinh_an", "cach_cuc": "Chính Ấn"},
        "useful_god": {
            "useful_god": "Chính Quan",
            "useful_element": "Hỏa",
            "useful_stem": "Đinh",
            "favorable_roles": [{"element": "Hỏa", "stem": "Đinh", "ten_god": "Chính Quan"}],
            "unfavorable_roles": [{"element": "Thủy", "stem": "Quý", "ten_god": "Thiên Ấn"}],
            "confidence": 0.8,
        },
        "ten_gods": {
            "visible": [{"ten_god": "Thất Sát", "stem": "Bính", "pillar": "year"}],
            "hidden": [{"ten_god": "Thiên Ấn", "hidden_stem": "Quý", "pillar": "month"}],
        },
        "luck": {
            "cycles": [
                {
                    "index": 0,
                    "year_start": 2020,
                    "year_end": 2029,
                    "stem": "Giáp",
                    "branch": "Tý",
                    "gan_zhi": "Giáp Tý",
                }
            ],
            "current_cycle": {
                "index": 0,
                "year_start": 2020,
                "year_end": 2029,
                "stem": "Giáp",
                "branch": "Tý",
                "gan_zhi": "Giáp Tý",
            },
        },
        "feng_shui": {"cung_phi": "Khảm", "nhom_trach": "Đông Tứ"},
        "bazi_source": {"contract": "li_chun_jdn_v1"},
        "strength_source": {"contract": "analysis_result.StrengthView@1.0"},
        "useful_god_source": {"contract": "analysis_result.UsefulGodView@1.5"},
        "ten_gods_source": {"contract": "ten_gods_result_v1"},
        "pattern_source": {"contract": "pattern_v1"},
    }


class FakeCanonicalRunner:
    """In-memory Canonical runner for runtime tests."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def run_person(
        self,
        *,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        gender: str,
        timezone: str,
    ) -> Mapping[str, Any]:
        """Record invocation metadata and return a Canonical-shaped payload."""
        self.calls.append(
            {
                "year": year,
                "month": month,
                "day": day,
                "hour": hour,
                "minute": minute,
                "gender": gender,
                "timezone": timezone,
            }
        )
        return canonical_payload()
