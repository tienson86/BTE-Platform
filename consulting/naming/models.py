"""Validated inputs for the first naming consultation release."""

from __future__ import annotations

import re
import unicodedata
from datetime import date, datetime
from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


def normalize_name(value: str) -> str:
    return " ".join(unicodedata.normalize("NFC", value).split())


class NamingRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    family_name: str = Field(min_length=1, max_length=80)
    gender: Literal["male", "female"]
    mode: Literal["child", "rename"] = "child"
    current_name: str = Field(default="", max_length=120)
    birth_date: str
    birth_time: str | None = None
    birth_place: str = Field(default="", max_length=160)
    timezone: str = Field(default="Asia/Ho_Chi_Minh", min_length=1, max_length=80)
    count: int = Field(default=8, ge=5, le=10, strict=True)

    @field_validator("family_name", "current_name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        normalized = normalize_name(value)
        if value and not normalized:
            raise ValueError("Vui lòng nhập họ hoặc họ tên hợp lệ.")
        if any(not (character.isalpha() or character in " '-’") for character in normalized):
            raise ValueError("Họ tên chỉ gồm chữ, khoảng trắng, dấu nháy hoặc gạch nối.")
        return normalized

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, value: str) -> str:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError("Ngày sinh cần có định dạng YYYY-MM-DD.")
        parsed = date.fromisoformat(value)
        if not 1900 <= parsed.year <= 2100:
            raise ValueError("Ngày sinh phải nằm trong giai đoạn 1900–2100.")
        return value

    @field_validator("birth_time")
    @classmethod
    def validate_birth_time(cls, value: str | None) -> str | None:
        if value is None or not value.strip():
            return None
        if not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", value):
            raise ValueError("Giờ sinh cần có định dạng HH:mm, từ 00:00 đến 23:59.")
        return value

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except (ZoneInfoNotFoundError, ValueError) as error:
            raise ValueError("Múi giờ không hợp lệ; ví dụ Asia/Ho_Chi_Minh.") from error
        return value

    @model_validator(mode="after")
    def validate_context(self) -> NamingRequest:
        if self.mode == "rename" and not self.current_name:
            raise ValueError("Vui lòng nhập tên hiện tại khi chọn đổi tên.")
        if date.fromisoformat(self.birth_date) > datetime.now(ZoneInfo(self.timezone)).date():
            raise ValueError("V0.1 tư vấn cho người đã sinh; ngày sinh không được ở tương lai.")
        return self
