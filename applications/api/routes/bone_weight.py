"""Standalone Cân Xương calculation for BTE members."""
from datetime import date
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from applications.api.auth.dependencies import CurrentUser
from applications.api.services.bone_weight_poems import poem_for_weight
from applications.api.services.bone_weight_readings import reading_for_weight
from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm
from engines.calendar_engine.lunar.converter import solar_to_lunar
from engines.can_xuong_engine import CanXuongEngine

router = APIRouter(tags=["Cân Xương"])
engine = CanXuongEngine()

class BoneWeightRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    full_name: str = Field(min_length=2, max_length=160)
    gender: Literal["male", "female"]
    birth_date: date = Field(ge=date(1900, 1, 1), le=date(2100, 12, 31))
    hour_branch: Literal["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]


@router.post("/can-xuong")
def calculate_bone_weight(body: BoneWeightRequest, user: CurrentUser):
    if not user.has_member_access():
        raise HTTPException(403, "Tính năng dành cho thành viên còn hiệu lực.")
    day = body.birth_date
    lunar = solar_to_lunar(day.day, day.month, day.year, time_zone=7)
    year = GanzhiAlgorithm.year(lunar.year)
    result = engine.calculate(
        year_ganzhi=f"{year['can']} {year['chi']}",
        lunar_month=lunar.month,
        lunar_day=lunar.day,
        hour_branch=body.hour_branch,
    )
    return {
        "full_name": body.full_name, "gender": body.gender,
        "birth_date": day.strftime("%d/%m/%Y"), "hour_branch": body.hour_branch,
        "lunar_date": f"{lunar.day:02d}/{lunar.month:02d}/{lunar.year}",
        "lunar_leap": lunar.leap, "year_ganzhi": result.year_ganzhi,
        "weight": result.display_weight, "classification": result.classification,
        "weights": [result.year_chi, result.month_chi, result.day_chi, result.hour_chi],
        "poem": poem_for_weight(result.total_weight),
        "explanation": reading_for_weight(result.total_weight),
    }
