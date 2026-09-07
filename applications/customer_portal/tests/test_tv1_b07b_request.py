"""TV1-B07B live request-chain repair contracts."""

from __future__ import annotations

from applications.customer_portal.config import PORTAL_ROOT
from runtime.manager import load_environment, load_services


def test_frontend_does_not_post_to_portless_localhost() -> None:
    """Live UI must use the portal origin, not http://127.0.0.1/backend/..."""
    source = (PORTAL_ROOT / "src" / "features" / "marriage_consulting" / "api.ts").read_text(
        encoding="utf-8"
    )
    assert "http://127.0.0.1${url}" not in source
    assert "window.location.origin" in source
    assert "AbortController" in source
    assert "MARRIAGE_FETCH_TIMEOUT_MS" in source


def test_portal_proxy_does_not_import_marriage() -> None:
    """HTTP composition only. No applications → consulting.marriage reverse import."""
    source = (PORTAL_ROOT / "app.py").read_text(encoding="utf-8")
    assert "consulting.marriage" not in source
    assert "connect=5.0" in source


def test_runtime_starts_marriage_api_before_portal() -> None:
    """Normal BTE startup must launch 8082, not only 8081."""
    services = load_services()
    keys = [item.key for item in services]
    assert "marriage_api" in keys
    assert keys.index("marriage_api") < keys.index("customer_portal")
    marriage = next(item for item in services if item.key == "marriage_api")
    assert marriage.port == 8082
    assert marriage.factory is True
    assert marriage.health_path == "/healthz"
    env = load_environment()
    assert env["BTE_MARRIAGE_API_BASE_URL"] == "http://127.0.0.1:8082"


def test_blank_birth_time_is_omitted_from_request_adapter() -> None:
    """Blank UI time must not be sent as DD/MM/YYYY or empty string."""
    source = (PORTAL_ROOT / "src" / "features" / "marriage_consulting" / "request.ts").read_text(
        encoding="utf-8"
    )
    assert "if (value.birth_time) body.birth_time = value.birth_time;" in source
    assert "parsed.iso" in source
