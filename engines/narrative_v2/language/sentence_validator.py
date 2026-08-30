"""SentenceAssetValidator — customer-language asset contract."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.language.language_asset_status import CATEGORIES, CUSTOMER_ELIGIBLE
from engines.narrative_v2.language.language_errors import SentenceAssetValidationError
from engines.narrative_v2.language.sentence_asset import SentenceAsset

FORBIDDEN_CLAIMS: tuple[str, ...] = (
    "chắc chắn thành công",
    "đại cát",
    "rất may mắn",
    "tình duyên sẽ tốt",
    "nên dùng màu đỏ",
    "nên đi hướng Nam",
    "nên mở rộng kinh doanh",
)

ACTION_MARKERS: tuple[str, ...] = ("Bạn nên", "Action Plan", "Priority:")
PREDICTION_MARKERS: tuple[str, ...] = ("chắc chắn", "nhất định", "You will")
TECHNICAL_LEAK: tuple[str, ...] = ("Engine", "NR-REL", "JSON", "{{", "CanonicalAnalysis")
SHORTHAND: tuple[str, ...] = (
    "chỗ dưỡng",
    "việc cần nền",
    "ủ và học có khung",
    "kênh thoát",
    "chế được giữ phép",
    "nền lực",
    "chịu tải",
)


@dataclass(slots=True)
class SentenceAssetValidationOutcome:
    """Asset contract result."""

    passed: bool
    reason: str = ""

    @property
    def status(self) -> str:
        """PASS or FAIL."""
        return "PASS" if self.passed else "FAIL"


class SentenceAssetValidator:
    """Validate one SentenceAsset before runtime customer use."""

    def validate(self, asset: SentenceAsset) -> SentenceAssetValidationOutcome:
        """PASS unless the asset contract is violated."""
        try:
            self.assert_valid(asset)
        except SentenceAssetValidationError as exc:
            return SentenceAssetValidationOutcome(passed=False, reason=exc.message)
        return SentenceAssetValidationOutcome(passed=True)

    def assert_valid(self, asset: SentenceAsset) -> None:
        """Raise if the asset cannot be used at runtime."""
        if not asset.sentence_id.startswith("sentence."):
            raise SentenceAssetValidationError("Sentence id is not stable")
        if not asset.semantic_key:
            raise SentenceAssetValidationError("Sentence missing semantic_key")
        if asset.category not in CATEGORIES:
            raise SentenceAssetValidationError(f"Invalid category: {asset.category}")
        if asset.category == "action":
            raise SentenceAssetValidationError("Action category is not allowed")
        if not asset.source_knowledge_ids:
            raise SentenceAssetValidationError("Sentence missing source Knowledge trace")
        if not asset.meaning_key:
            raise SentenceAssetValidationError("Sentence missing meaning_key")
        if asset.status in CUSTOMER_ELIGIBLE:
            self._check_language(asset)

    def _check_language(self, asset: SentenceAsset) -> None:
        blob = asset.text
        if not blob.startswith("Bạn"):
            raise SentenceAssetValidationError("Approved sentence must address Bạn")
        for claim in FORBIDDEN_CLAIMS:
            if claim in blob:
                raise SentenceAssetValidationError("Unsupported generated claim")
        for token in ACTION_MARKERS:
            if token in blob:
                raise SentenceAssetValidationError("Action in sentence asset")
        for token in PREDICTION_MARKERS:
            if token in blob:
                raise SentenceAssetValidationError("Prediction in sentence asset")
        for token in TECHNICAL_LEAK:
            if token in blob:
                raise SentenceAssetValidationError("Technical leak in sentence asset")
        for token in SHORTHAND:
            if token in blob:
                raise SentenceAssetValidationError("Consultant shorthand in sentence asset")
        if "{" in blob or "}" in blob:
            raise SentenceAssetValidationError("JSON/debug in sentence asset")
