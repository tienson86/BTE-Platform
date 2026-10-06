from consulting.childbirth.service import evaluate_childbirth_years
from consulting.marriage.models.enums import CanonicalGender, FiveElement, TenGodVisibility, YinYang
from consulting.marriage.models.person import BirthDataQuality, CanonicalVersionReference, MarriagePersonReference
from consulting.marriage.models.snapshot import (
    DayMasterSnapshot,
    ElementOrStemReference,
    FengShuiSnapshot,
    FiveElementSnapshot,
    MarriageCanonicalSnapshot,
    PatternSnapshot,
    PillarSnapshot,
    PillarValue,
    ShenShaItem,
    ShenShaSnapshot,
    StrengthSnapshot,
    TenGodItem,
    TenGodSnapshot,
    UsefulGodSnapshot,
)


def test_childbirth_filters_years_before_minimum_parent_ages() -> None:
    father = _snapshot(
        gender=CanonicalGender.MALE,
        day_master_element=FiveElement.WOOD,
        day_branch="Tý",
        useful=FiveElement.FIRE,
        group="Đông Tứ Trạch",
        cung="Khảm",
    )
    mother = _snapshot(
        gender=CanonicalGender.FEMALE,
        day_master_element=FiveElement.WATER,
        day_branch="Mão",
        useful=FiveElement.WOOD,
        group="Đông Tứ Trạch",
        cung="Tốn",
    )

    result = evaluate_childbirth_years(
        father_snapshot=father,
        mother_snapshot=mother,
        father_birth_date="2010-06-01",
        mother_birth_date="2012-06-01",
        start_year=2026,
        years_ahead=6,
    )

    assert [item["year"] for item in result["eligibility"]["ineligible_years"]] == [
        2026,
        2027,
        2028,
        2029,
    ]
    assert all(item["year"] >= 2030 for item in result["all_years"])


def test_childbirth_scores_future_years_from_canonical_signals() -> None:
    father = _snapshot(
        gender=CanonicalGender.MALE,
        day_master_element=FiveElement.WOOD,
        day_branch="Tỵ",
        useful=FiveElement.FIRE,
        favorable=FiveElement.WOOD,
        group="Đông Tứ Trạch",
        cung="Khảm",
        shen_sha=("Thiên Ất Quý Nhân",),
    )
    mother = _snapshot(
        gender=CanonicalGender.FEMALE,
        day_master_element=FiveElement.EARTH,
        day_branch="Mùi",
        useful=FiveElement.FIRE,
        favorable=FiveElement.EARTH,
        group="Tây Tứ Trạch",
        cung="Khôn",
        shen_sha=("Văn Xương",),
    )

    result = evaluate_childbirth_years(
        father_snapshot=father,
        mother_snapshot=mother,
        father_birth_date="1995-01-01",
        mother_birth_date="1997-01-01",
        start_year=2026,
        years_ahead=4,
    )

    assert result["status"] == "SUCCESS"
    assert result["recommendations"]
    best = result["recommendations"][0]
    assert best["year"] in {2026, 2027}
    assert best["score"] >= 68
    assert best["recommended_child_gender"] in {"boy", "girl", "either"}
    assert any("Dụng thần" in reason or "con cái" in reason for reason in best["reasons"])


def _snapshot(
    *,
    gender: CanonicalGender,
    day_master_element: FiveElement,
    day_branch: str,
    useful: FiveElement,
    favorable: FiveElement | None = None,
    group: str,
    cung: str,
    shen_sha: tuple[str, ...] = (),
) -> MarriageCanonicalSnapshot:
    pillar = PillarValue(stem="Giáp", branch="Tý", can_chi="Giáp Tý")
    return MarriageCanonicalSnapshot(
        person=MarriagePersonReference(
            analysis_id="TEST",
            gender=gender,
            display_name="Test",
            birth_data_quality=BirthDataQuality(
                birth_date_known=True,
                birth_time_known=True,
                birth_place_known=True,
                timezone_resolved=True,
                completeness_score=1.0,
            ),
            canonical_version=CanonicalVersionReference(),
        ),
        pillars=PillarSnapshot(
            year=pillar,
            month=PillarValue(stem="Ất", branch="Sửu", can_chi="Ất Sửu"),
            day=PillarValue(stem="Bính", branch=day_branch, can_chi=f"Bính {day_branch}"),
            hour=PillarValue(stem="Đinh", branch="Mão", can_chi="Đinh Mão"),
        ),
        day_master=DayMasterSnapshot(
            stem="Bính",
            element=day_master_element,
            yin_yang=YinYang.YANG,
        ),
        five_elements=FiveElementSnapshot(distribution={element: 1.0 for element in FiveElement}),
        strength=StrengthSnapshot(classification="Thân vượng"),
        pattern=PatternSnapshot(pattern_name="Chính Ấn"),
        useful_god=UsefulGodSnapshot(
            useful=[ElementOrStemReference(element=useful, stem="Bính", role="Dụng thần")],
            favorable=(
                [ElementOrStemReference(element=favorable, stem=None, role="Hỷ thần")]
                if favorable
                else []
            ),
            unfavorable=[ElementOrStemReference(element=FiveElement.METAL, role="Kỵ thần")],
        ),
        ten_gods=TenGodSnapshot(
            visible=[
                TenGodItem(name="Thực Thần", visibility=TenGodVisibility.VISIBLE),
                TenGodItem(name="Chính Quan", visibility=TenGodVisibility.VISIBLE),
            ],
            hidden=[],
        ),
        source_analysis_id="TEST",
        shen_sha=ShenShaSnapshot(items=[ShenShaItem(name=name) for name in shen_sha]),
        feng_shui=FengShuiSnapshot(cung_phi=cung, group=group),
    )
