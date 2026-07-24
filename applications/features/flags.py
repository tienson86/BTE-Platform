"""Feature flag catalog."""

from __future__ import annotations

from enum import Enum

from applications.edition.editions import Edition


class Feature(str, Enum):
    """Licensable feature flags (WP14)."""

    CALENDAR = "calendar"
    BAZI = "bazi"
    REPORT = "report"
    NARRATIVE = "narrative"
    CUSTOMER_MANAGEMENT = "customer_management"
    ADMIN_DASHBOARD = "admin_dashboard"
    EXPORT_PDF = "export_pdf"
    API_ACCESS = "api_access"
    BATCH_PROCESSING = "batch_processing"


# Features granted per edition (cumulative by design).
EDITION_FEATURES: dict[Edition, frozenset[Feature]] = {
    Edition.COMMUNITY: frozenset(
        {
            Feature.CALENDAR,
            Feature.BAZI,
            Feature.REPORT,
        }
    ),
    Edition.STANDARD: frozenset(
        {
            Feature.CALENDAR,
            Feature.BAZI,
            Feature.REPORT,
            Feature.NARRATIVE,
            Feature.CUSTOMER_MANAGEMENT,
            Feature.API_ACCESS,
        }
    ),
    Edition.PROFESSIONAL: frozenset(
        {
            Feature.CALENDAR,
            Feature.BAZI,
            Feature.REPORT,
            Feature.NARRATIVE,
            Feature.CUSTOMER_MANAGEMENT,
            Feature.ADMIN_DASHBOARD,
            Feature.EXPORT_PDF,
            Feature.API_ACCESS,
            Feature.BATCH_PROCESSING,
        }
    ),
    Edition.ENTERPRISE: frozenset(Feature),
}


def features_for_edition(edition: Edition | str) -> frozenset[Feature]:
    """Return the feature set for an edition."""
    value = Edition(edition) if not isinstance(edition, Edition) else edition
    return EDITION_FEATURES.get(value, frozenset())


def is_feature_enabled(
    edition: Edition | str,
    feature: Feature | str,
    *,
    enabled_features: list[str] | None = None,
) -> bool:
    """
    True if feature is allowed.

    When ``enabled_features`` is provided on a license, it acts as an allow-list
    intersected with the edition catalog (empty list = edition defaults only).
    """
    feat = feature if isinstance(feature, Feature) else Feature(feature)
    catalog = features_for_edition(edition)
    if feat not in catalog:
        return False
    if enabled_features is None:
        return True
    if not enabled_features:
        return True
    return feat.value in enabled_features or feat.name in enabled_features
