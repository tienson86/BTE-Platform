"""Contact and server-to-server usage contracts."""
import re
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator

Feature = Literal["bazi", "date_selection", "marriage", "childbirth", "naming", "business", "van_han"]

def normalize_phone(value):
    value = re.sub(r"[\s().-]", "", value.strip())
    if not re.fullmatch(r"\+?[0-9]{8,15}", value):
        raise ValueError("Vui lòng nhập số điện thoại hợp lệ (8–15 chữ số).")
    return value

class ContactRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    full_name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=8, max_length=24)
    subject: str = Field(default="Yêu cầu hỗ trợ", max_length=120)
    message: str = Field(min_length=5, max_length=3000)
    channel: Literal["website", "phone", "direct"] = "website"
    _phone = field_validator("phone")(normalize_phone)

class ReserveRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    feature: Feature
    operation_key: str = Field(min_length=1, max_length=160)
    input: dict

class FinishRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    output: dict
    status_code: int = Field(default=200, ge=200, le=299)

class ContactUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    status: Literal["open", "handling", "resolved"]
    admin_note: str = Field(default="", max_length=3000)
