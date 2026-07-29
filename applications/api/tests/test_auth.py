"""Auth layer tests: password, JWT, API key, HTTP flows."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.api.app import create_app
from applications.api.auth.api_key_manager import APIKeyManager
from applications.api.auth.jwt_manager import JWTError, JWTManager, decode_token
from applications.api.auth.password_hasher import hash_password, verify_password
from applications.api.dependencies import get_auth_service, get_user_store


def _client() -> TestClient:
    get_user_store.cache_clear()
    get_auth_service.cache_clear()
    return TestClient(create_app())


def test_password_hash_and_verify() -> None:
    hashed = hash_password("secret")
    assert hashed != "secret"
    assert verify_password("secret", hashed)
    assert not verify_password("wrong", hashed)


def test_jwt_roundtrip() -> None:
    manager = JWTManager()
    pair = manager.create_pair(
        subject="u-1",
        role="ADMIN",
        username="admin",
    )
    access = decode_token(pair.access_token, expected_type="access")
    refresh = decode_token(pair.refresh_token, expected_type="refresh")
    assert access["sub"] == "u-1"
    assert refresh["type"] == "refresh"
    try:
        decode_token(pair.access_token, expected_type="refresh")
        raise AssertionError("expected JWTError")
    except JWTError:
        pass


def test_api_key_generate_and_verify() -> None:
    manager = APIKeyManager()
    generated = manager.generate()
    assert generated.api_key.startswith("bte_")
    assert manager.verify(generated.api_key, generated.key_hash)
    assert not manager.verify("bte_bad", generated.key_hash)


def test_login_and_me() -> None:
    client = _client()
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200
    tokens = login.json()
    assert tokens["access_token"]
    assert tokens["refresh_token"]
    assert tokens["user"]["role"] == "ADMIN"

    me = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert me.status_code == 200
    assert me.json()["username"] == "admin"


def test_login_invalid_credentials() -> None:
    client = _client()
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "wrong"},
    )
    assert response.status_code == 401


def test_refresh_token() -> None:
    client = _client()
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "consultant", "password": "consultant123"},
    ).json()
    refreshed = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": login["refresh_token"]},
    )
    assert refreshed.status_code == 200
    assert refreshed.json()["access_token"]


def test_api_key_auth() -> None:
    client = _client()
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "staff", "password": "staff123"},
    ).json()
    created = client.post(
        "/api/v1/auth/api-key",
        json={"name": "ci"},
        headers={"Authorization": f"Bearer {login['access_token']}"},
    )
    assert created.status_code == 200
    api_key = created.json()["api_key"]

    me = client.get("/api/v1/auth/me", headers={"X-API-Key": api_key})
    assert me.status_code == 200
    assert me.json()["username"] == "staff"


def test_require_role_and_permission() -> None:
    client = _client()
    customer = client.post(
        "/api/v1/auth/login",
        json={"username": "customer", "password": "customer123"},
    ).json()
    headers = {"Authorization": f"Bearer {customer['access_token']}"}

    denied = client.get("/api/v1/users/admin-check", headers=headers)
    assert denied.status_code == 403

    allowed = client.get("/api/v1/users/permission-check", headers=headers)
    assert allowed.status_code == 200

    admin = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    ).json()
    ok = client.get(
        "/api/v1/users/admin-check",
        headers={"Authorization": f"Bearer {admin['access_token']}"},
    )
    assert ok.status_code == 200


def test_engine_endpoints_remain_public() -> None:
    client = _client()
    response = client.post(
        "/api/v1/calendar",
        json={"year": 1990, "month": 5, "day": 15, "hour": 10},
    )
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_openapi_has_auth_group() -> None:
    client = _client()
    schema = client.get("/openapi.json").json()
    paths = schema["paths"]
    assert "/api/v1/auth/login" in paths
    assert "/api/v1/auth/logout" in paths
    assert "/api/v1/auth/refresh" in paths
    assert "/api/v1/auth/me" in paths
    assert "/api/v1/auth/api-key" in paths
    # Tag present on login operation
    tags = paths["/api/v1/auth/login"]["post"].get("tags", [])
    assert "Auth" in tags
