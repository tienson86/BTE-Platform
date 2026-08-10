# Phase 3 Unified Pattern Contract — RCA

**Sprint:** PILOT-1A  
**Failing tests (full file re-run in PILOT-1A):**  
`test_pattern_view_matches_engine`, `test_orchestrator_pattern_payload_matches_engine`, `test_api_analyze_pattern_matches_engine`  
**Prior partial run:** API suite `-x` stopped at first failure (`test_pattern_view_matches_engine`)  
**Classification:** CONTRACT (+ stale hard-coded pattern expectation)  
**Code changed in this sprint:** No  

---

## 1. Failure statement

### Failure A — view vs portal inequality (original)

Assertion:

```python
assert view.to_dict() == portal
```

where:

- `portal = PatternResult.to_portal_dict()`
- `view = build_pattern_view(result)` → `PatternView.to_dict()`

Observed diff (live dump, critical chart 1987-01-21 04:30 male):

| Side | Keys |
|---|---|
| portal | includes **`success_reason`** |
| view | does **not** include `success_reason` |
| portal-only | `{'success_reason'}` |
| view-only | `∅` |

Example value:

```text
success_reason = "<pattern> cách (fallback — không xác định được Lệnh Tháng)"
```

### Failure B — orchestrator pattern ≠ direct PatternEngine (additional)

Live dump for critical chart `1987-01-21 04:30 male`:

| Path | `pattern` | `cach_cuc` |
|---|---|---|
| Direct `PatternEngine.calculate(PatternContext…)` | `chinh_quan` | Chính Quan |
| `OrchestratorService.run_stage("pattern")` | `chinh_an` | Chính Ấn |

So failures in `test_orchestrator_pattern_payload_matches_engine` / `test_api_analyze_pattern_matches_engine` are **not** merely stale hard-codes: orchestrator and bare engine **disagree** on the selected pattern for the same birth.

Also: orchestrator public pattern slice has **no** `success_reason` (PatternView path), while bare `to_portal_dict()` does.

---

## 2. Producer / consumer map

| Role | Component | Path |
|---|---|---|
| Producer (engine result) | `PatternResult.success_reason` | `engines/pattern_engine/engine.py` |
| Producer (portal serializer) | `PatternResult.to_portal_dict()` | same file — **conditionally adds** `success_reason` when set |
| Adapter / truth builder | `build_pattern_view()` | `applications/api/services/pattern_truth.py` |
| Consumer contract (API view) | `PatternView` / `to_dict()` | `applications/api/models/analysis_result.py` |
| Test consumer | `test_pattern_view_matches_engine` | `applications/api/tests/test_phase3_unified_pattern.py` |

Calculator also sets:

```text
engines/pattern_engine/calculator.py → result["success_reason"] = result["reason"]
```

---

## 3. Exact field

| Attribute | Value |
|---|---|
| Field name | `success_reason` |
| Type | `Optional[str]` on `PatternResult`; omitted from payload when falsy |
| Schema on PatternView | **Absent** — not a dataclass field |
| Public analyze payload today | Uses `PatternView.to_dict()` → **does not publish** `success_reason` |

Related optional portal fields also present on `to_portal_dict` but not on `PatternView`:

- `follow_type`
- `failure_reason`
- `pattern_rank`
- `pattern_quality`
- `combination_status`
- `clash_status`

Only `success_reason` triggered this failure because it is non-empty on the critical fixture chart.

---

## 4. Expected vs actual schema

### Expected by test (implicit)

Exact equality:

```text
PatternView.to_dict()  ==  PatternResult.to_portal_dict()
```

### Actual

| Surface | Schema |
|---|---|
| `to_portal_dict()` | core pattern fields + optional metadata including `success_reason` |
| `PatternView.to_dict()` | fixed core fields only (`success`, `pattern`, `cach_cuc`, `score`, `priority`, `than`, `than_vuong_nhuoc`, `tong_cach`, `dung_than`, `hy_than`, `ky_than`, `dieu_hau`) |

First mismatch: **`success_reason` present on portal, absent on view.**

---

## 5. Version / staleness analysis

| Artifact | Status |
|---|---|
| Producer (`to_portal_dict`) | **Newer** — added optional metadata publish |
| Consumer (`PatternView`) | **Stale relative to portal serializer** — never gained `success_reason` |
| Adapter (`build_pattern_view`) | **Stale** — copies only PatternView fields; drops portal-only keys |
| Test | **Strict equality** assumes view ≡ portal; became brittle when portal grew |

Not a Knowledge Package version mismatch. This is an **applications ↔ pattern_engine serialization contract drift**.

---

## 6. Genuine regression?

**Yes — two related contract issues**, not flaky asserts.

### Failure A

- PatternEngine still calculates  
- Orchestrator still returns a pattern slice  
- Phase 3 invariant “PatternView is the portal-equivalent SSOT” no longer holds  
- Public API (`PatternView`) silently drops `success_reason` even though engine portal dict has it  

### Failure B

| Path | Result |
|---|---|
| Test harness `_build_pattern_stack()` | `PatternContext` **without** live strength/temperature fields → engine returns `chinh_quan` |
| Orchestrator Stage 3.5–4 | Injects `strength_level` / `strength_score` / `temperature_type` into `PatternContext` before `pattern_engine.calculate` → returns `chinh_an` |

So orchestrator↔engine equality tests fail because the **contexts are not equivalent**, not because PatternView mapping alone differs.

Severity: **Medium–High (P2)** for claiming Phase 3 unified truth; does not block Calendar RCA (CASE-0006).

---

## 7. Root cause

### Failure A

```text
PatternResult.to_portal_dict expanded to publish success_reason
        ↓
PatternView / build_pattern_view were not updated
        ↓
test_pattern_view_matches_engine equality fails
```

Class: **CONTRACT** (producer ahead of consumer + brittle equality test).

### Failure B

```text
Orchestrator enriches PatternContext with Strength + Temperature before PatternEngine.calculate
        ↓
Test stack builds bare PatternContext (no strength/temperature)
        ↓
Same birth → different pattern codes (chinh_an vs chinh_quan)
        ↓
orchestrator/API equality tests fail
```

Class: **CONTRACT / TEST HARNESS DIVERGENCE** (not proven Pattern rule corruption).

Do **not** force either pattern by editing Expected or deleting asserts in PILOT-1A.

---

## 8. Recommended action (do not apply in PILOT-1A unless approved)

Choose one deliberate contract direction:

### Option A — Expand PatternView (preferred if portal should show reason)

1. Add optional `success_reason: str | None = None` (and any other intentional portal metadata) to `PatternView`  
2. Map them in `build_pattern_view`  
3. Publish in `to_dict()` only when set (mirror portal omit-when-empty policy)  
4. Keep test equality  

### Option B — Narrow portal serializer

1. Remove `success_reason` from `to_portal_dict` if it is not part of the frozen public PatternView contract  
2. Keep field on internal `PatternResult` only  

### Option C — Relax test (least preferred alone)

1. Compare core fields only  
2. Still leaves API/view dropping reason — does not fix SSOT  

### Option D — Align Phase 3 test harness with orchestrator context (for Failure B)

1. Build test `PatternContext` the same way orchestrator does (include strength/temperature)  
2. Or compare orchestrator pattern only to an engine call that uses the identical enriched context  
3. Do not hard-code `chinh_quan` unless that is the enriched-path result  

**Immediate fix required for Pilot Replay acceptance?** No.  
**Immediate fix required before claiming Phase 3 unified pattern truth?** Yes — resolve A (Option A/B) and B (Option D) explicitly.

### Stop-before-change note (if implementing later)

| Item | Content |
|---|---|
| Exact root cause | Portal dict includes `success_reason`; PatternView omits it |
| Affected files | `analysis_result.py`, `pattern_truth.py`, and/or `pattern_engine/engine.py` |
| Why incorrect | Breaks stated unified-view invariant |
| Minimal fix | Option A or B above |
| Regression risk | Low if optional field; medium if changing public JSON shape without versioning |
| Test impact | `test_pattern_view_matches_engine` should pass after A or B |

PILOT-1A: **documented only; no code change.**

---

## 9. Evidence commands

```bash
PYTHONPATH=. python -c "from applications.api.tests.test_phase3_unified_pattern import _build_pattern_stack; ..."
python -m pytest applications/api/tests/test_phase3_unified_pattern.py -q
```

PILOT-1A re-run result: **2 passed, 3 failed** (Failures A + B). Golden Dataset: **1 passed**.
