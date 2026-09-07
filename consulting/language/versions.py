"""Language Pack version tokens. Independent of Decision / Narrative versions."""

from __future__ import annotations

from typing import Final

LANGUAGE_PACK_VERSION: Final[str] = "consulting.language.pack@1.0.0"
MARRIAGE_CATALOG_VERSION: Final[str] = "consulting.language.marriage@1.0.0"
MARRIAGE_MODULE_LANGUAGE_VERSION: Final[str] = "marriage.language@1.0.0"
SCHEMA_VERSION: Final[str] = "1.0.0"
PLACEHOLDER_TOKEN: Final[str] = "__PRODUCT_OWNER_WORDING_REQUIRED__"
DEFAULT_AUDIENCE: Final[str] = "customer"
DEFAULT_TONE: Final[str] = "professional_warm"
FALLBACK_HEADLINE: Final[str] = "Kết luận đánh giá chưa có bản diễn đạt đã duyệt."
FALLBACK_MEANING: Final[str] = "Trạng thái ngữ nghĩa đã có, nhưng khóa ngôn ngữ chưa được gắn."
MAX_SUPPORTING_FACTS: Final[int] = 4
MAX_LIMITATIONS: Final[int] = 3
