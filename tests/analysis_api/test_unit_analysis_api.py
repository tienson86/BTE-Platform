"""Unit tests for Analysis Engine REST API."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from engines.analysis_engine.api.auth.jwt import JWTManager
from engines.analysis_engine.api.auth.roles import Permission, Role, has_permission
from engines.analysis_engine.api.config import settings


class TestHealthAndOpenAPI:
    def test_health(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "ok"
        assert body["service"] == "bte-analysis-engine-api"

    def test_health_v1(self, client: TestClient) -> None:
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_openapi_and_swagger(self, client: TestClient) -> None:
        openapi = client.get("/openapi.json")
        assert openapi.status_code == 200
        schema = openapi.json()
        assert schema["info"]["title"]
        assert "BearerAuth" in schema["components"]["securitySchemes"]
        paths = schema["paths"]
        assert "/api/v1/charts" in paths
        assert "/api/v1/analysis" in paths
        assert "/api/v1/interpretation" in paths
        assert "/api/v1/report" in paths
        docs = client.get("/docs")
        assert docs.status_code == 200


class TestJWTAndRoles:
    def test_jwt_roundtrip(self) -> None:
        manager = JWTManager()
        pair = manager.create_access_token(
            subject="u-1",
            role="ANALYST",
            username="analyst",
        )
        claims = manager.decode_access_token(pair.access_token)
        assert claims["sub"] == "u-1"
        assert claims["role"] == "ANALYST"

    def test_role_permissions(self) -> None:
        assert has_permission(Role.ANALYST, Permission.CHART_CREATE)
        assert not has_permission(Role.VIEWER, Permission.CHART_CREATE)
        assert has_permission(Role.ADMIN, Permission.REPORT_GENERATE)

    def test_viewer_forbidden_create_chart(
        self,
        client: TestClient,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(settings, "default_anonymous_role", "VIEWER")
        response = client.post(
            "/api/v1/charts",
            json={"day_master": "Giáp", "year": 1990, "month": 5, "day": 15},
        )
        assert response.status_code == 403

    def test_auth_required_without_token(
        self,
        client: TestClient,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(settings, "auth_required", True)
        response = client.post(
            "/api/v1/charts",
            json={"day_master": "Giáp"},
        )
        assert response.status_code == 401

    def test_token_endpoint_and_bearer_flow(self, client: TestClient) -> None:
        token_resp = client.post(
            "/api/v1/auth/token",
            json={
                "subject": "u-2",
                "username": "analyst2",
                "role": "ANALYST",
            },
        )
        assert token_resp.status_code == 200
        token = token_resp.json()["data"]["access_token"]
        chart = client.post(
            "/api/v1/charts",
            json={"day_master": "Giáp", "year": 1990, "month": 1, "day": 1},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert chart.status_code == 200
        assert chart.json()["data"]["chart_id"].startswith("cht_")


class TestPipelineEndpoints:
    def test_create_chart(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/charts",
            json={
                "day_master": "Giáp",
                "year": 1990,
                "month": 5,
                "day": 15,
                "hour": 10,
                "full_name": "Nguyễn Văn A",
            },
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["chart"]["day_master"] == "Giáp"
        assert "luck" in data["chart"]
        chart_id = data["chart_id"]

        got = client.get(f"/api/v1/charts/{chart_id}")
        assert got.status_code == 200
        assert got.json()["data"]["chart_id"] == chart_id

    def test_chart_not_found(self, client: TestClient) -> None:
        response = client.get("/api/v1/charts/missing")
        assert response.status_code == 404

    def test_full_pipeline_chart_analysis_interpretation_report(
        self,
        client: TestClient,
    ) -> None:
        chart = client.post(
            "/api/v1/charts",
            json={"day_master": "Giáp", "year": 1990, "month": 5, "day": 15},
        ).json()["data"]
        chart_id = chart["chart_id"]

        analysis = client.post(
            "/api/v1/analysis",
            json={"chart_id": chart_id},
        )
        assert analysis.status_code == 200
        analysis_data = analysis.json()["data"]
        assert analysis_data["chart_id"] == chart_id
        assert "summary" in analysis_data
        assert "strength" in analysis_data["stage_ids"]
        analysis_id = analysis_data["analysis_id"]

        interpretation = client.post(
            "/api/v1/interpretation",
            json={"analysis_id": analysis_id},
        )
        assert interpretation.status_code == 200
        interp_data = interpretation.json()["data"]
        assert interp_data["overview"]
        assert interp_data["sections"]
        interpretation_id = interp_data["interpretation_id"]

        report = client.post(
            "/api/v1/report",
            json={
                "interpretation_id": interpretation_id,
                "formats": ["html", "markdown", "pdf", "json"],
                "include_structured_data": True,
                "title": "API Pipeline Report",
            },
        )
        assert report.status_code == 200
        report_data = report.json()["data"]
        assert report_data["html"]
        assert report_data["markdown"]
        assert report_data["json"]
        assert report_data["pdf_size"] and report_data["pdf_size"] > 0
        assert report_data["structured_report"]["sections"]

        got_report = client.get(f"/api/v1/report/{report_data['report_id']}")
        assert got_report.status_code == 200
