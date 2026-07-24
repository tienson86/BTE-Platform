"""WP13 administration & operations tests."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from applications.admin.dashboard_service import DashboardService
from applications.admin.health_service import HealthService
from applications.api.app import create_app
from applications.api.config import settings
from applications.api.dependencies import (
    clear_wp11_caches,
    get_auth_service,
    get_settings,
    get_user_store,
)
from applications.audit.activity_logger import ActivityLogger
from applications.audit.audit_log import AuditLog
from applications.monitoring.metrics import MetricsCollector
from applications.statistics.api_statistics import api_statistics
from applications.storage.factory import StorageConfig


def test_metrics_and_api_statistics() -> None:
    metrics = MetricsCollector()
    metrics.record_request(
        method="GET",
        path="/api/v1/health",
        status_code=200,
        elapsed_ms=12.5,
        user_id="u1",
    )
    metrics.record_request(
        method="POST",
        path="/api/v1/analyze",
        status_code=500,
        elapsed_ms=40.0,
    )
    snap = api_statistics(metrics)
    assert snap["request_count"] == 2
    assert snap["error_count"] == 1
    assert snap["active_users"] == 1


def test_activity_logger_classifies_events() -> None:
    log = AuditLog()
    logger = ActivityLogger(log)
    logger.record_from_request(
        method="POST",
        path="/api/v1/auth/login",
        status_code=200,
        username="admin",
    )
    logger.record_from_request(
        method="POST",
        path="/api/v1/customers",
        status_code=200,
        user_id="u-admin",
        username="admin",
    )
    logger.record_from_request(
        method="POST",
        path="/api/v1/customers/abc/analyze",
        status_code=200,
        username="admin",
    )
    events = log.list(limit=10)
    types = {e["event_type"] for e in events}
    assert "login" in types
    assert "create_customer" in types
    assert "analyze" in types


def test_dashboard_and_health(tmp_path: Path) -> None:
    config = StorageConfig(backend="json", data_dir=str(tmp_path / "data"))
    dash = DashboardService(
        metrics=MetricsCollector(),
        storage_config=config,
    ).build()
    assert dash["customer_count"] == 0
    assert dash["storage_backend"] == "json"
    assert "uptime_seconds" in dash

    health = HealthService(storage_config=config).check()
    assert health["status"] in {"ok", "degraded"}
    assert health["checks"]["storage"]["status"] == "ok"


def _admin_client(tmp_path: Path) -> TestClient:
    settings.data_dir = str(tmp_path / "data")
    get_settings.cache_clear()
    get_user_store.cache_clear()
    get_auth_service.cache_clear()
    clear_wp11_caches()
    return TestClient(create_app())


def test_admin_api_requires_admin(tmp_path: Path) -> None:
    client = _admin_client(tmp_path)
    denied = client.get("/api/v1/admin/dashboard")
    assert denied.status_code == 401

    customer_login = client.post(
        "/api/v1/auth/login",
        json={"username": "customer", "password": "customer123"},
    ).json()
    forbidden = client.get(
        "/api/v1/admin/dashboard",
        headers={"Authorization": f"Bearer {customer_login['access_token']}"},
    )
    assert forbidden.status_code == 403

    admin_login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    ).json()
    headers = {"Authorization": f"Bearer {admin_login['access_token']}"}

    for path in (
        "/api/v1/admin/dashboard",
        "/api/v1/admin/system",
        "/api/v1/admin/health",
        "/api/v1/admin/config",
        "/api/v1/admin/statistics",
        "/api/v1/admin/audit",
    ):
        response = client.get(path, headers=headers)
        assert response.status_code == 200, path
        assert response.json()["success"] is True

    # login should appear in audit via ops middleware
    audit = client.get("/api/v1/admin/audit", headers=headers).json()
    assert audit["data"]["count"] >= 1
