"""Public registration and admin-managed membership settings."""
from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator, field_validator


class MembershipPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    title: str = Field(default="Thành viên BTE Platform", min_length=1, max_length=120)
    description: str = Field(default="Sử dụng các công cụ tư vấn, xem kết quả và tải tài liệu trong tài khoản của bạn.", max_length=1200)
    public_notice: str = Field(default="", max_length=500)
    amount_vnd: int | None = Field(default=None, ge=1000, le=1_000_000_000, strict=True)
    validity_days: int | None = Field(default=None, ge=1, le=3650, strict=True)
    analysis_limit: int | None = Field(default=None, ge=1, le=1_000_000, strict=True)
    bank_name: str = Field(default="SHB", max_length=120)
    bank_account: str = Field(default="28676875", max_length=64, pattern=r"^[0-9 ]*$")
    bank_holder: str = Field(default="Nguyễn Tiến Sơn", max_length=120)
    payment_note: str = Field(default="Chuyển khoản đúng số tiền và nội dung được cấp. Quyền thành viên được mở sau khi quản trị viên xác nhận đã nhận tiền.", max_length=800)
    registration_enabled: bool = False

    @property
    def ready(self) -> bool:
        return bool(self.registration_enabled and self.amount_vnd and self.validity_days
                    and self.bank_name and self.bank_account and self.bank_holder)

    @model_validator(mode="after")
    def configured_when_enabled(self):
        if self.registration_enabled and not self.ready:
            raise ValueError("Cần nhập đầy đủ mức phí, thời hạn và thông tin nhận tiền trước khi mở đăng ký.")
        return self


class MemberRegistration(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    username: str = Field(min_length=3, max_length=64, pattern=r"^[A-Za-z0-9_.-]+$")
    password: SecretStr = Field(min_length=8, max_length=128)
    display_name: str = Field(min_length=1, max_length=120)
    phone: str = Field(min_length=8, max_length=24)

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, value):
        from applications.api.schemas.activity import normalize_phone
        return normalize_phone(value)


class PaymentReport(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    note: str = Field(default="", max_length=500)


class MembershipReview(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    decision: str = Field(pattern=r"^(approve|reject)$")
    expected_reference: str = Field(min_length=8, max_length=64)
    note: str = Field(default="", max_length=500)
