"""Public registration and admin-managed membership settings."""
from typing import Annotated
from applications.api.schemas.activity import Feature
from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator, field_validator


Quota = Annotated[int, Field(ge=0, le=1_000_000, strict=True)]
ALL_FEATURES = ("bazi", "date_selection", "marriage", "childbirth", "naming", "business", "van_han")


class MembershipTier(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    tier: int = Field(ge=1, le=3, strict=True)
    title: str = Field(min_length=1, max_length=120)
    amount_vnd: int = Field(ge=1000, le=1_000_000_000, strict=True)
    validity_days: int | None = Field(default=None, ge=1, le=3650, strict=True)
    analysis_limit: Quota | None = None
    feature_limits: dict[Feature, Quota | None]
    enabled_features: list[Feature]
    referral_reward: int = Field(default=0, ge=0, le=1_000_000, strict=True)
    enabled: bool = True

    @model_validator(mode="after")
    def validate_features(self):
        if set(self.feature_limits) != set(ALL_FEATURES):
            raise ValueError("Cần cấu hình đủ bảy chức năng cho mỗi cấp.")
        if len(self.enabled_features) != len(set(self.enabled_features)):
            raise ValueError("Chức năng bị lặp.")
        self.analysis_limit = self.feature_limits["bazi"] if "bazi" in self.enabled_features else 0
        return self


class MembershipPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    title: str = Field(default="Thành viên BTE Platform", min_length=1, max_length=120)
    description: str = Field(default="Sử dụng các công cụ tư vấn, xem kết quả và tải tài liệu trong tài khoản của bạn.", max_length=1200)
    public_notice: str = Field(default="", max_length=500)
    public_base_url: str = Field(default="", max_length=300)
    amount_vnd: int | None = Field(default=None, ge=1000, le=1_000_000_000, strict=True)
    validity_days: int | None = Field(default=None, ge=1, le=3650, strict=True)
    analysis_limit: int | None = Field(default=None, ge=1, le=1_000_000, strict=True)
    bank_name: str = Field(default="SHB", max_length=120)
    bank_account: str = Field(default="28676875", max_length=64, pattern=r"^[0-9 ]*$")
    bank_holder: str = Field(default="Nguyễn Tiến Sơn", max_length=120)
    payment_note: str = Field(default="Chuyển khoản đúng số tiền và nội dung được cấp. Quyền thành viên được mở sau khi quản trị viên xác nhận đã nhận tiền.", max_length=800)
    registration_enabled: bool = False
    tiers: list[MembershipTier] | None = None

    @field_validator("public_base_url")
    @classmethod
    def validate_public_base_url(cls, value):
        from urllib.parse import urlsplit
        if not value:
            return value
        parsed = urlsplit(value)
        if parsed.scheme not in ("https", "http") or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in ("", "/"):
            raise ValueError("Nhập địa chỉ gốc BTE, ví dụ https://bte.example.vn")
        return value.rstrip("/")

    def configured_tiers(self) -> list[MembershipTier]:
        if self.tiers is not None:
            return sorted(self.tiers, key=lambda tier: tier.tier)
        from applications.api.services.member_rewards import TIERS
        return [MembershipTier(
            **tier, validity_days=self.validity_days,
            feature_limits={feature: tier["analysis_limit"] for feature in ALL_FEATURES},
            enabled_features=list(ALL_FEATURES),
        ) for tier in TIERS.values()]

    @property
    def ready(self) -> bool:
        enabled = [tier for tier in self.configured_tiers() if tier.enabled]
        return bool(self.registration_enabled and enabled and self.bank_name and self.bank_account
                    and self.bank_holder and all(tier.validity_days for tier in enabled))

    @model_validator(mode="after")
    def configured_when_enabled(self):
        if self.tiers is not None and (len(self.tiers) != 3 or {tier.tier for tier in self.tiers} != {1, 2, 3}):
            raise ValueError("Cần cấu hình đúng ba cấp 1, 2 và 3.")
        if self.registration_enabled:
            enabled = [tier for tier in self.configured_tiers() if tier.enabled]
            if not (self.bank_name and self.bank_account and self.bank_holder) or any(not tier.validity_days for tier in enabled):
                raise ValueError("Cần thời hạn cho các gói đang mở và thông tin nhận tiền đầy đủ.")
        return self


class MembershipOrderPlan(MembershipPlan):
    analysis_limit: Quota | None = None
    feature_limits: dict[Feature, Quota | None] | None = None
    enabled_features: list[Feature] | None = None


class MemberRegistration(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    username: str = Field(min_length=3, max_length=64, pattern=r"^[A-Za-z0-9_.-]+$")
    password: SecretStr = Field(min_length=8, max_length=128)
    display_name: str = Field(min_length=1, max_length=120)
    phone: str = Field(min_length=8, max_length=24)
    tier: int = Field(default=1, ge=1, le=3, strict=True)
    referral_code: str = Field(default="", max_length=40, pattern=r"^[A-Za-z0-9-]*$")

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
    decision: str = Field(pattern=r"^(approve|reject|refund)$")
    expected_reference: str = Field(min_length=8, max_length=64)
    note: str = Field(default="", max_length=500)


class LinhThachRedeem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    feature: str = Field(min_length=1, max_length=30)
    operation_key: str = Field(min_length=16, max_length=80, pattern=r"^[A-Za-z0-9-]+$")
