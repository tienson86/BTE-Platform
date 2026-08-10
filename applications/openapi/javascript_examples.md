# JavaScript Examples

```javascript
const BASE = "http://127.0.0.1:8000";

const headers = {
  "Content-Type": "application/json",
  "Request-ID": "req_js_001",
  "Correlation-ID": "corr_js_001",
  Authorization: "Bearer placeholder-token",
};

const health = await fetch(`${BASE}/health`, { headers });
const healthBody = await health.json();

const created = await fetch(`${BASE}/api/v1/analysis`, {
  method: "POST",
  headers: {
    ...headers,
    "Idempotency-Key": "idem_js_001",
  },
  body: JSON.stringify({
    customer: { id: "cust_001", name: "Nguyen Van A" },
    birth_data: {
      year: 1990,
      month: 5,
      day: 15,
      hour: 10,
      minute: 30,
      calendar_type: "solar",
      timezone: "Asia/Ho_Chi_Minh",
      gender: "male",
    },
    options: { language: "vi", report_template: "STANDARD" },
  }),
});

const createdBody = await created.json();
const analysisId = createdBody.data?.analysis_id;

const report = await fetch(`${BASE}/api/v1/report/${analysisId ?? "rpt_example"}`, {
  headers,
});
```

Clients must consume `status`, `data`, `metadata`, `request_id`, `timestamp`, and `api_version`.  
Error bodies expose `code`, `message`, `details`, `request_id`, and `timestamp` only.

---

END
