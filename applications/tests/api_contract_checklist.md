# API Contract Checklist

Sprint: Beta-2  
Module: public service API

- [x] All resource APIs mounted under `/api/v1/`
- [x] `/api/v2/` is not mounted
- [x] `GET /health` `/live` `/ready` `/version` exist
- [x] `GET /metrics` reserved (501)
- [x] `POST /api/v1/analysis`
- [x] `GET /api/v1/analysis/{id}`
- [x] `GET /api/v1/report/{id}`
- [x] `GET /api/v1/knowledge/{id}`
- [x] Success envelope: status, data, metadata, request_id, timestamp, api_version
- [x] Error body: code, message, details, request_id, timestamp
- [x] No stack traces / Python exceptions / filesystem paths in errors
- [x] Request-ID, Correlation-ID, Idempotency-Key pass-through
- [x] OpenAPI 3.1 documents every public path
- [x] No engine objects in response models

---

END
