"""G1-PREFINAL: in-process Analyze contract check (fresh app, no stale ResultStore)."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from applications.api.app import create_app
from engines.useful_god_engine.presentation import INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY

BODY = {
    "year": 1987,
    "month": 1,
    "day": 21,
    "hour": 4,
    "minute": 30,
    "gender": "male",
    "timezone": "Asia/Bangkok",
    "full_name": "Nguyễn Tiến Sơn",
}


def main() -> None:
    client = TestClient(create_app())
    response = client.post("/api/v1/analyze", json=BODY)
    payload = response.json()
    data = payload.get("data") or payload
    useful = data.get("useful_god") or {}
    source = data.get("useful_god_source") or {}
    result = {
        "http_status": response.status_code,
        "request_id": payload.get("request_id"),
        "contract": source.get("contract"),
        "useful_display": useful.get("useful_display"),
        "favorable_display": useful.get("favorable_display"),
        "canonical_favorable_display": useful.get("canonical_favorable_display"),
        "unfavorable_display": useful.get("unfavorable_display"),
        "short_reason_has_str": "str_003" in str(useful.get("short_reason") or ""),
        "hy_is_customer": useful.get("favorable_display")
        == INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY,
        "hy_not_internal": useful.get("favorable_display")
        != useful.get("canonical_favorable_display"),
        "strength": (data.get("strength") or {}).get("strength_level"),
        "pattern": (data.get("pattern") or {}).get("cach_cuc"),
        "pillars": " / ".join(
            [
                f"{(data.get('bazi') or {}).get('year_pillar', {}).get('stem')} {(data.get('bazi') or {}).get('year_pillar', {}).get('branch')}",
                f"{(data.get('bazi') or {}).get('month_pillar', {}).get('stem')} {(data.get('bazi') or {}).get('month_pillar', {}).get('branch')}",
                f"{(data.get('bazi') or {}).get('day_pillar', {}).get('stem')} {(data.get('bazi') or {}).get('day_pillar', {}).get('branch')}",
                f"{(data.get('bazi') or {}).get('hour_pillar', {}).get('stem')} {(data.get('bazi') or {}).get('hour_pillar', {}).get('branch')}",
            ]
        ),
    }
    Path("release/gate_01/G1_PREFINAL_API_CONTRACT.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
