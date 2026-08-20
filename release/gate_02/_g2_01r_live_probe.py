"""G2-01R live identity + Frozen copy check. Does not change engines."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from applications.api.app import create_app
from applications.api.services.result_identity import CUSTOMER_USEFUL_GOD_CONTRACT

ROOT = Path(__file__).resolve().parent

DUNG = {
    "name": "Ngô Đắc Dũng",
    "year": 1985,
    "month": 9,
    "day": 18,
    "hour": 8,
    "minute": 0,
    "gender": "male",
    "timezone": "Asia/Bangkok",
}

TUYEN = {
    "name": "Vũ Thị Thanh Tuyền",
    "year": 1984,
    "month": 7,
    "day": 13,
    "hour": 21,
    "minute": 1,
    "gender": "female",
    "timezone": "Asia/Bangkok",
}


def _pillars(data: dict) -> str:
    bazi = data.get("bazi") or {}

    def one(key: str) -> str:
        item = bazi.get(key) or {}
        return f"{item.get('stem') or ''} {item.get('branch') or ''}".strip()

    return " / ".join(
        [one("year_pillar"), one("month_pillar"), one("day_pillar"), one("hour_pillar")]
    )


def analyze(client: TestClient, spec: dict) -> dict:
    body = {k: v for k, v in spec.items() if k != "name"}
    response = client.post("/api/v1/analyze", json=body)
    assert response.status_code == 200, response.text
    payload = response.json()
    data = payload["data"]
    useful = data.get("useful_god") or {}
    pattern = data.get("pattern") or {}
    strength = data.get("strength") or {}
    meta = data.get("result_meta") or {}
    return {
        "case": spec["name"],
        "http_request_id": payload.get("request_id"),
        "data_analysis_id": data.get("analysis_id"),
        "data_request_id": data.get("request_id"),
        "ids_match": payload.get("request_id") == data.get("analysis_id") == data.get("request_id"),
        "contract": (data.get("useful_god_source") or {}).get("contract"),
        "result_meta_contract": meta.get("customer_contract"),
        "gate_core_freeze": meta.get("gate_core_freeze"),
        "four_pillars": _pillars(data),
        "strength_score": strength.get("strength_score"),
        "strength_level": strength.get("strength_level"),
        "pattern": pattern.get("cach_cuc") or pattern.get("pattern"),
        "detected_special_pattern": pattern.get("detected_special_pattern"),
        "qualification_level": pattern.get("qualification_level"),
        "ug_override_eligible": pattern.get("ug_override_eligible"),
        "overall_dung": useful.get("useful_display"),
        "customer_hy": useful.get("favorable_display"),
        "short_reason": useful.get("short_reason"),
        "climate_preference_label": useful.get("climate_preference_label"),
        "reason_archetype": useful.get("reason_archetype"),
        "dieu_hau": useful.get("climate_display"),
    }


def main() -> None:
    client = TestClient(create_app())
    dung = analyze(client, DUNG)
    tuyen = analyze(client, TUYEN)
    out = {
        "dung": dung,
        "tuyen": tuyen,
        "identity_ok": bool(dung["ids_match"] and tuyen["ids_match"]),
        "contract_ok": dung["contract"] == tuyen["contract"] == CUSTOMER_USEFUL_GOD_CONTRACT,
    }
    dest = ROOT / "G2_01R_LIVE_PROBE.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
