# cURL Examples

Base URL example: `http://127.0.0.1:8000`

## Health

```bash
curl -sS http://127.0.0.1:8000/health \
  -H "Request-ID: req_demo_001"
```

```bash
curl -sS http://127.0.0.1:8000/live
curl -sS http://127.0.0.1:8000/ready
curl -sS http://127.0.0.1:8000/version
```

## Create analysis

```bash
curl -sS -X POST http://127.0.0.1:8000/api/v1/analysis \
  -H "Content-Type: application/json" \
  -H "Request-ID: req_demo_002" \
  -H "Correlation-ID: corr_demo_002" \
  -H "Idempotency-Key: idem_demo_002" \
  -H "Authorization: Bearer placeholder-token" \
  -d '{
    "customer": {"id": "cust_001", "name": "Nguyen Van A"},
    "birth_data": {
      "year": 1990,
      "month": 5,
      "day": 15,
      "hour": 10,
      "minute": 30,
      "calendar_type": "solar",
      "timezone": "Asia/Ho_Chi_Minh",
      "gender": "male"
    },
    "options": {"language": "vi", "report_template": "STANDARD"}
  }'
```

## Get resources

```bash
curl -sS http://127.0.0.1:8000/api/v1/analysis/anl_example
curl -sS http://127.0.0.1:8000/api/v1/report/rpt_example
curl -sS http://127.0.0.1:8000/api/v1/knowledge/kn_example
```

## Reserved metrics

```bash
curl -sS -i http://127.0.0.1:8000/metrics
```

Expected: `501` with canonical error `BTE-501-NOT_IMPLEMENTED`.

---

END
