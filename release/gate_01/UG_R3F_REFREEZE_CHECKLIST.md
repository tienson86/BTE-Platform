# UG-R3F — Refreeze checklist

**Date:** 2026-08-20  
**Status to freeze against:** existing-knowledge reachability for `str_003` is repaired. Knowledge gaps listed below remain **V1.1**, non-blocking for Useful God V1.0.

Do **not** start G1-FINAL from this checklist. Do **not** update Golden Dataset / snapshots / expected JSON until a separate freeze task.

---

## Freeze what is repaired

- [x] `str_003` consumes canonical Chính Quan whether **visible or hidden**.
- [x] Provenance preserved (`officer_provenance`: visibility, pillar, stem, branch).
- [x] No duplicate `Chính Quan` token / no duplicate `str_003` candidate when the same god is visible and hidden.
- [x] `str_003` CSV token remains `Chính Quan` (not Thất Sát). Priority 82 unchanged.
- [x] Pattern `officer_elements` remains visible-only (Pattern specials unchanged).
- [x] `jia_wang` **not** added to `spc_004` (rule definition does not include it).
- [x] Điều hậu (`sea_*` / `tmp_*`) remains a separate layer from Overall.
- [x] No silent climate fallback. Incomplete copy unchanged.
- [x] Flow unique-max / G1-06 semantics unchanged. Flow still non-competitive.
- [x] Hỷ/Kỵ taken from the **winning Overall** structural row (Tuyền/Sơn no longer stale `str_004` Hỷ).
- [x] Strength / Pattern / G1-05 occurrence counts not retuned.
- [x] Five control cases re-run fresh.
- [x] 101-case live recompute; Golden **not** edited.
- [x] API restarted; live Tuyền Analyze verified (no ResultStore cache in this API).

---

## Do not freeze as complete theory (UG-V1.1-KNOWLEDGE)

Non-blocking for V1.0:

- [ ] **A.** Strong → Hao / Tài path  
- [ ] **B.** Strong + Thất Sát → Chế path  
- [ ] **C.** Main Pattern → Overall Useful God reconciliation  
- [ ] **D.** Flow competitiveness  
- [ ] **E.** Chính Quan vs Thất Sát visibility/weighting research  
- [ ] **F.** Multi-candidate reconciliation rather than fixed class mapping  
- [ ] **G.** `jia_wang` onto `spc_004` (explicit CSV omission; field exists, rule does not)

Also still out of V1.0: new Mộc rule, new priority, new Flow priority, Kiếp Tài → Useful God.

---

## Vũ Thị Thanh Tuyền live gate

| Check | Expected after UG-R3F |
|-------|------------------------|
| Strength | **0.66 strong** |
| Pattern | **Kiếp Tài** |
| Điều hậu | **Nhiệt / Cần làm mát / ưu tiên Thủy** (`sea_002`) |
| Overall | **`str_003` Mộc · Ất · Chính Quan** (existing priority; not hard-coded) |
| Hỷ / Kỵ | From `str_003`: Chính Quan + Thực Thần / Tỷ Kiên + Kiếp Tài |
| Not | `sea_002` as Overall; not stale `str_004` Kim · Canh · Thực Thần |

---

## Regression commands (module only)

```
python -m pytest tests/useful_god tests/temperature/test_g1_04_temperature_binding.py tests/report_engine/test_g1_06_useful_god_binding.py tests/report_engine/test_g1_04_temperature_binding.py tests/report_engine/test_g1_05_five_elements_binding.py tests/report_engine/test_case_0001_report_input.py -q
```

Result this run: **51 passed.**

---

## Product Owner

| Question | This patch |
|----------|------------|
| Accept Tuyền Overall = Mộc · Ất · Chính Quan (`str_003`) with Điều hậu Thủy separate? | **Yes — existing `str_003` priority.** |
| Wire `jia_wang` into `spc_004`? | **No — not in rule definition.** |
| Author V1.1 knowledge items A–G? | **Defer. Non-blocking.** |
| Allow G1-FINAL / Golden update? | **Not from this task. STOP.** |

**Freeze string:**

`UG-R3F: EXISTING-KNOWLEDGE REACHABILITY REPAIRED — USEFUL GOD V1.0 FREEZE READY`
