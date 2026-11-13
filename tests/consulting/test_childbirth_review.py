"""Regression tests for honest childbirth comparisons and validation."""
from datetime import date
from unittest.mock import Mock
import pytest
from consulting.childbirth.service import evaluate_childbirth_years, analyze_childbirth_plan, _summary, _validate_parent, CHILDBIRTH_NOTICE
from consulting.childbirth.api import _optional_int
from consulting.childbirth.export import build_childbirth_document
from consulting.childbirth.repository import ChildbirthProfile
from consulting.marriage.dto.request import MarriagePersonInput
from consulting.marriage.models.enums import CanonicalGender, FiveElement
from tests.test_childbirth_consulting import _snapshot


def snapshots():
    father = _snapshot(gender=CanonicalGender.MALE, day_master_element=FiveElement.WOOD, day_branch="Tý", useful=FiveElement.FIRE, favorable=FiveElement.FIRE, group="Đông Tứ Trạch", cung="Khảm", shen_sha=("Thiên Ất Quý Nhân",))
    mother = _snapshot(gender=CanonicalGender.FEMALE, day_master_element=FiveElement.WATER, day_branch="Mão", useful=FiveElement.WOOD, group="Đông Tứ Trạch", cung="Tốn")
    return father, mother


def evaluate(father=None, mother=None):
    f,m = snapshots()
    return evaluate_childbirth_years(father_snapshot=father or f,mother_snapshot=mother or m,father_birth_date="1990-01-01",mother_birth_date="1992-01-01",start_year=2026,years_ahead=3)


def test_reasons_retain_both_parents_and_gender_comparison():
    result=evaluate()
    year=next(x for x in result["all_years"] if x["year"]==2026)
    assert len(year["reasons"]) > 6
    assert any("bố" in x for x in year["reasons"])
    assert any("mẹ" in x for x in year["reasons"])
    assert any("Cung Phi" in x for x in year["reasons"])


def test_unknown_hour_does_not_rank_or_publish_midnight_derived_claims():
    f,m=snapshots()
    m.person.birth_data_quality.birth_time_known=False
    result=evaluate(f,m)
    assert result["analysis_status"]=="insufficient_data"
    assert result["recommendations"]==result["all_years"]==[]
    assert result["parents"]["mother"]["useful_elements"]==[]
    assert result["parents"]["mother"]["pattern"] is None
    assert "giờ sinh" in result["limitations"][0]
    assert "bác sĩ" in result["notice"]


def test_sensitive_summary_never_calls_low_score_suitable():
    result=_summary([dict(year=2026,can_chi="Bính Ngọ",score=25,level="sensitive",recommended_child_gender="boy")],False)
    assert "Chưa có năm nổi bật" in result["headline"]
    assert "Nên ưu tiên" not in result["headline"]


@pytest.mark.parametrize("start,count",[(2020,1),(9999,1),(2026,0),(2026,25),(2026.5,1),(2099,2)])
def test_invalid_year_range_rejected_before_runtime(start,count):
    runtime=Mock()
    f=MarriagePersonInput(gender=CanonicalGender.MALE,birth_date="1990-01-01")
    m=MarriagePersonInput(gender=CanonicalGender.FEMALE,birth_date="1992-01-01")
    with pytest.raises(ValueError):
        analyze_childbirth_plan(father=f,mother=m,start_year=start,years_ahead=count,adapter=runtime,today=date(2026,11,13))
    runtime.analyze_normalized.assert_not_called()


@pytest.mark.parametrize("value",[True,2026.5,"abc",float("inf")])
def test_noninteger_options_rejected(value):
    with pytest.raises(ValueError): _optional_int(value)


@pytest.mark.parametrize("dob",["2027-01-01","1890-01-01"])
def test_implausible_parent_birthdate_rejected(dob):
    p=MarriagePersonInput(gender=CanonicalGender.MALE,birth_date=dob)
    with pytest.raises(ValueError): _validate_parent(p,CanonicalGender.MALE,"father",date(2026,11,13))


def test_invalid_time_rejected():
    p=MarriagePersonInput(gender=CanonicalGender.MALE,birth_date="1990-01-01",birth_time="99:00")
    with pytest.raises(ValueError): _validate_parent(p,CanonicalGender.MALE,"father",date(2026,11,13))


def test_document_preserves_all_reasons_and_notice():
    result=evaluate()
    profile=ChildbirthProfile(consultation_id="CB-"+"a"*32,created_at="2026-11-13T00:00:00+00:00",input={"father":{"full_name":"Test A","birth_date":"1990-01-01","birth_time":"04:00"},"mother":{"full_name":"Test B","birth_date":"1992-01-01","birth_time":"06:00"}},result=result)
    doc=build_childbirth_document(profile)
    text="\n".join((block.body or "") for section in doc.sections for block in section.blocks)
    assert doc.notice==CHILDBIRTH_NOTICE
    for item in result["recommendations"]:
        assert all(reason in text for reason in item["reasons"])
    assert "Ưu tiên con" not in text
