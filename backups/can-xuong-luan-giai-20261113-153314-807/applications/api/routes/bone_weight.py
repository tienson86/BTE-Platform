"""Standalone Cân Xương calculation for BTE members."""
from datetime import date
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from applications.api.auth.dependencies import CurrentUser
from engines.calendar_engine.algorithms.ganzhi import GanzhiAlgorithm
from engines.calendar_engine.lunar.converter import solar_to_lunar
from engines.can_xuong_engine import CanXuongEngine

router = APIRouter(tags=["Cân Xương"])
engine = CanXuongEngine()

# Newly written verses and plain-language explanations by weight band.
VERSES = (
    (31, (
        "Đường đầu cứ bước chậm thôi",
        "Gom từng việc nhỏ, vun bồi ngày mai",
        "Bền lòng qua những tháng dài",
        "Nền vững rồi sẽ mở lối thênh thang",
    ), "Bài thơ nói về sự kiên trì. Khi việc gì còn khó, có thể chia thành từng bước và làm đều đặn. Kỹ năng và kinh nghiệm tích lũy dần sẽ giúp các bước sau vững hơn."),
    (43, (
        "Góp từng giọt nước thành ao",
        "Học từng điều nhỏ, biết bao điều hay",
        "Chăm lo từ những hôm nay",
        "Mai sau vững bước, dựng xây nếp nhà",
    ), "Ý chính là tích lũy từng chút một. Việc học, công việc và quản lý tiền bạc đều dễ tiến bộ hơn khi có nếp đều đặn và mục tiêu vừa sức."),
    (56, (
        "Gặp mùa thuận gió căng buồm",
        "Tay chèo vững nhịp, nước xuôi đường dài",
        "Có duyên gặp bạn chung vai",
        "Biết vun cơ hội, ngày mai thêm bền",
    ), "Bài thơ gợi hình ảnh có cơ hội và người cùng hỗ trợ. Khi gặp thời điểm thuận lợi, hãy chuẩn bị kỹ, chọn người đồng hành đáng tin và dành sức cho việc có thể làm lâu dài."),
    (72, (
        "Đất lành vun gốc cây xanh",
        "Cành vươn đón nắng, lá xanh che người",
        "Có điều thuận, biết sẻ chia",
        "Giữ lòng chừng mực, phúc kia thêm bền",
    ), "Bài thơ nhấn mạnh việc chăm sóc nền tảng đang có. Khi được gia đình hoặc môi trường nâng đỡ, có thể dùng điều kiện ấy để học hỏi, giúp người và giữ những thói quen tốt."),
)


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
    _, poem, explanation = next(row for row in VERSES if result.total_weight <= row[0])
    return {
        "full_name": body.full_name, "gender": body.gender,
        "birth_date": day.strftime("%d/%m/%Y"), "hour_branch": body.hour_branch,
        "lunar_date": f"{lunar.day:02d}/{lunar.month:02d}/{lunar.year}",
        "lunar_leap": lunar.leap, "year_ganzhi": result.year_ganzhi,
        "weight": result.display_weight, "classification": result.classification,
        "weights": [result.year_chi, result.month_chi, result.day_chi, result.hour_chi],
        "poem": poem, "explanation": explanation,
    }
