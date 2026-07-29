"""WP14 licensing unit and API tests."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi.testclient import TestClient

from applications.api.app import create_app
from applications.api.config import settings
from applications.api.dependencies import (
    clear_wp11_caches,
    get_auth_service,
    get_settings,
    get_user_store,
)
from applications.api.routes.license import clear_license_cache
from applications.edition import Edition
from applications.features import Feature, features_for_edition, is_feature_enabled
from applications.license import (
    LicenseService,
    LicenseValidator,
    generate_license,
)


def test_edition_feature_catalog() -> None:
    assert Feature.ADMIN_DASHBOARD not in features_for_edition(Edition.COMMUNITY)
    assert Feature.NARRATIVE in features_for_edition(Edition.STANDARD)
    assert is_feature_enabled(Edition.ENTERPRISE, Feature.BATCH_PROCESSING)
    assert not is_feature_enabled(Edition.COMMUNITY, "admin_dashboard")


def test_license_generate_activate_validate(tmp_path: Path) -> None:
    service = LicenseService.from_data_dir(tmp_path)
    issued = service.issue(
        edition=Edition.PROFESSIONAL,
        customer="Demo Co",
        organization="Demo Org",
        days_valid=30,
    )
    assert issued.status == "issued"
    assert issued.license_key.startswith("BTE-PROFESSIONAL-")

    active = service.activate(issued.license_key)
    assert active.status == "active"
    assert active.machine_id

    status = service.status()
    assert status["has_license"] is True
    assert status["validation"]["valid"] is True

    ok = service.validate(feature="report")
    assert ok.valid is True

    denied = service.validate(feature="admin_dashboard")  # professional has it
    assert denied.valid is True

    community = generate_license(
        edition=Edition.COMMUNITY,
        customer="Solo",
        days_valid=30,
    )
    service.repository.save(community)
    service.activate(community.license_key)
    no_admin = service.validate(feature="admin_dashboard")
    assert no_admin.valid is False
    assert no_admin.reason == "feature_disabled"


def test_expiration_and_limits(tmp_path: Path) -> None:
    service = LicenseService.from_data_dir(tmp_path)
    license_obj = generate_license(
        edition=Edition.STANDARD,
        customer="X",
        days_valid=1,
        max_users=2,
        max_cases=3,
    )
    # Force expiry
    past = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
    license_obj.expires_at = past
    service.repository.save(license_obj)

    validator = LicenseValidator()
    expired = validator.validate(license_obj)
    assert expired.valid is False
    assert expired.reason == "expired"

    fresh = generate_license(
        edition=Edition.STANDARD,
        customer="Y",
        days_valid=10,
        max_users=2,
        max_cases=3,
    )
    users = validator.validate(fresh, current_users=5)
    assert users.reason == "max_users_exceeded"
    cases = validator.validate(fresh, current_cases=10)
    assert cases.reason == "max_cases_exceeded"


def _client(tmp_path: Path) -> TestClient:
    settings.data_dir = str(tmp_path / "data")
    get_settings.cache_clear()
    get_user_store.cache_clear()
    get_auth_service.cache_clear()
    clear_wp11_caches()
    clear_license_cache()
    return TestClient(create_app())


def test_license_api_flow(tmp_path: Path) -> None:
    client = _client(tmp_path)

    issued = client.post(
        "/api/v1/license/issue",
        json={
            "edition": "STANDARD",
            "customer": "API Customer",
            "organization": "API Org",
            "days_valid": 90,
        },
    )
    assert issued.status_code == 200
    key = issued.json()["data"]["license"]["license_key"]

    activated = client.post(
        "/api/v1/license/activate",
        json={"license_key": key},
    )
    assert activated.status_code == 200
    assert activated.json()["data"]["license"]["status"] == "active"

    status = client.get("/api/v1/license/status")
    assert status.status_code == 200
    assert status.json()["data"]["has_license"] is True

    features = client.get("/api/v1/license/features")
    assert features.status_code == 200
    assert "narrative" in features.json()["data"]["features"]

    validated = client.post(
        "/api/v1/license/validate",
        json={"feature": "customer_management", "current_users": 1, "current_cases": 1},
    )
    assert validated.status_code == 200
    assert validated.json()["data"]["valid"] is True

    # Existing public health still works
    assert client.get("/api/v1/health").status_code == 200
