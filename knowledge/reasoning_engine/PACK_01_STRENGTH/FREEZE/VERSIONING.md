# Versioning — FROZEN V1.0

| Field | Value |
|-------|-------|
| Document | VERSIONING |
| Status | FROZEN |

---

# 1. Four versions on every NarrativePlan

| Field | This freeze |
|-------|-------------|
| `catalog_version` | `1.0.0` — schema of Knowledge Units |
| `knowledge_version` | Interpretation Knowledge pack version (`1.0.0` as authored) |
| `reasoning_version` | Reasoning design + this freeze policy (`1.0.0`) |
| `narrative_version` | NarrativePlan / composer contract (`1.0.0`) |

Also record `standard_version` (Interpretation Standard `1.0.0`) as a fifth compatibility pin.

---

# 2. Compatibility

| Change | Bump |
|--------|------|
| Add optional catalog field | catalog minor |
| Change meaning of a reason code | catalog/reasoning **major** |
| Add reason code | reasoning minor |
| Change budget caps | reasoning minor (golden CASE-0001 must be re-accepted) |
| Change published Strength class mapping | forbidden in V1.0 |
| Knowledge prose edit | knowledge version; do not silently keep old traces |

V1.0 implementations must refuse to run if catalog_version major ≠ 1.

---

# 3. CASE-0001

Golden reference is pinned to freeze `1.0.0`.

A policy bump that changes CASE-0001’s kept unit set requires a new golden acceptance — not a silent drift.

---

END
