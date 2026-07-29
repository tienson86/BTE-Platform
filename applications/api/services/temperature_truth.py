"""Temperature view adapters for API contract."""

from __future__ import annotations

from applications.api.models.analysis_result import TemperatureView


def temperature_source_fingerprint() -> dict[str, str]:
    return {
        "layer": "applications.api.services.temperature_truth",
        "contract": "analysis_result.TemperatureView@1.0",
        "owner": "api_ssot",
    }


def build_temperature_view(result) -> TemperatureView:
    data = result.to_portal_dict() if hasattr(result, "to_portal_dict") else {}
    return TemperatureView(
        temperature_level=str(data.get("temperature_level") or "warm"),
        temperature_score=float(data.get("temperature_score") or 0.0),
        warm_score=float(data.get("warm_score") or 0.0),
        cold_score=float(data.get("cold_score") or 0.0),
        dry_score=float(data.get("dry_score") or 0.0),
        humid_score=float(data.get("humid_score") or 0.0),
        reasoning=str(data.get("reasoning") or ""),
        confidence=float(data.get("confidence") or 0.0),
        matched_rules=[str(x) for x in (data.get("matched_rules") or [])],
        recommendations=list(data.get("recommendations") or []),
    )
