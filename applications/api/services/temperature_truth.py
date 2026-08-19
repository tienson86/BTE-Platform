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
    """Map TemperatureResult to the API TemperatureView contract."""
    data = result.to_portal_dict() if hasattr(result, "to_portal_dict") else {}
    climate_state = str(data.get("climate_state") or data.get("temperature_level") or "warm")
    return TemperatureView(
        temperature_level=climate_state,
        climate_state=climate_state,
        balancing_need=str(data.get("balancing_need") or ""),
        climate_state_label=str(data.get("climate_state_label") or ""),
        balancing_need_label=str(data.get("balancing_need_label") or ""),
        evidence_compact=str(data.get("evidence_compact") or ""),
        month_branch=str(data.get("month_branch") or ""),
        season=str(data.get("season") or ""),
        score_semantic=str(data.get("score_semantic") or "imbalance_intensity"),
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
