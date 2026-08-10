# Python Examples

```python
import httpx

BASE = "http://127.0.0.1:8000"
headers = {
    "Request-ID": "req_py_001",
    "Correlation-ID": "corr_py_001",
    "Authorization": "Bearer placeholder-token",
}

with httpx.Client(base_url=BASE, headers=headers, timeout=10.0) as client:
    health = client.get("/health")
    health.raise_for_status()

    created = client.post(
        "/api/v1/analysis",
        headers={"Idempotency-Key": "idem_py_001"},
        json={
            "customer": {"id": "cust_001", "name": "Nguyen Van A"},
            "birth_data": {
                "year": 1990,
                "month": 5,
                "day": 15,
                "hour": 10,
                "minute": 30,
                "calendar_type": "solar",
                "timezone": "Asia/Ho_Chi_Minh",
                "gender": "male",
            },
            "options": {"language": "vi", "report_template": "STANDARD"},
        },
    )
    created.raise_for_status()
    analysis_id = created.json()["data"]["analysis_id"]

    fetched = client.get(f"/api/v1/analysis/{analysis_id}")
    # Unbound design gateway returns 404 until a runtime pipeline is bound.
    print(fetched.status_code, fetched.json())
```

Do not import engines or knowledge packages from client code.

---

END
