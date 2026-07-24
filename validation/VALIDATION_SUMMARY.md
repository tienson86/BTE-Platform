# BTE Platform — RC1 Validation Summary

**Date:** 2026-07-24  
**Harness:** `validation/rc1_audit_runner.py`  
**Cases path:** `validation/real_cases/`

---

## Result

| Item | Value |
|------|------:|
| Cases | 20 |
| PASS | 20 |
| FAIL | 0 |
| Runner WARN_COUNT | 0 |
| ERRORS | 0 |
| day_master API NOTE | 20 / 20 |

---

## Case inventory

Each case contains:

- `input.json` — year, month, day, hour, minute, gender, timezone  
- `expected.json` — structural contract (day pillar required; day_master optional NOTE)  
- `actual.json` — full pipeline JSON snapshot  
- `diff.md` — PASS/FAIL + notes  

| ID | Status | Elapsed (ms) | Day pillar (stem/branch) |
|----|--------|-------------:|--------------------------|
| case_01 | PASS | 253.4 | Bính / Dần |
| case_02 | PASS | 247.2 | Mậu / Thân |
| case_03 | PASS | 253.2 | Đinh / Dậu |
| case_04 | PASS | 235.4 | Quý / Mão |
| case_05 | PASS | 249.6 | Kỷ / Mão |
| case_06 | PASS | 250.1 | Kỷ / Sửu |
| case_07 | PASS | 249.8 | Kỷ / Sửu |
| case_08 | PASS | 301.7 | Quý / Sửu |
| case_09 | PASS | 309.9 | Mậu / Tuất |
| case_10 | PASS | 270.3 | Mậu / Tý |
| case_11 | PASS | 306.0 | Đinh / Mão |
| case_12 | PASS | 346.0 | Mậu / Tuất |
| case_13 | PASS | 239.0 | Canh / Tý |
| case_14 | PASS | 306.0 | Ất / Hợi |
| case_15 | PASS | 235.0 | Mậu / Tuất |
| case_16 | PASS | 223.4 | Mậu / Thìn |
| case_17 | PASS | 207.0 | Mậu / Ngọ |
| case_18 | PASS | 332.2 | Bính / Thân |
| case_19 | PASS | 269.3 | Quý / Dậu |
| case_20 | PASS | 261.4 | Bính / Thìn |

Average elapsed: **~267 ms**.

---

## End-to-end checks

| Layer | Result |
|-------|--------|
| Calendar → Narrative pipeline | OK, no exceptions |
| Customer Portal UI smoke | OK |
| Web Admin UI smoke | OK |
| Admin API RBAC | 401 / 403 / 200 as expected |
| License status | OK |

---

## Contract caveat

Expected checks treat missing API `bazi.day_master` as **NOTE**, not FAIL:

- Engine object exposes `day_master` (e.g. sample meta `"Bính"`).
- API serialization via `to_dict`/`asdict` skips `@property`, so JSON omits it.
- Day pillar remains present and validated.

---

## Artifacts produced

| File | Purpose |
|------|---------|
| `validation/AUDIT_REPORT.md` | Architecture audit (20 checklist items) |
| `validation/SYSTEM_HEALTH.md` | Engine + surface health |
| `validation/DEPENDENCY_GRAPH.md` | Runtime + app dependency graph |
| `validation/PERFORMANCE.md` | Latency / memory baselines |
| `validation/VALIDATION_SUMMARY.md` | This file |
| `validation/perf_raw.json` | Machine-readable perf + case statuses |
| `validation/real_cases/case_*/` | 20 real-case folders |

---

## Final RC1 answers

1. **Architecture Score:** 7.2 / 10  
2. **Code Health:** 7.0 / 10  
3. **Dependency Graph:** See `DEPENDENCY_GRAPH.md` (runtime Pattern→Score; docs stale)  
4. **Performance:** Warm analyze ~282 ms; stages dominated by score/interpretation/narrative; peak ~1.1 MB traced  
5. **Known Issues:** day_master API gap; timezone ignored; legacy duplicates; docs order; storage factory partial wiring; public engines; default JWT  
6. **Recommendations:** Fix P1 serialization + timezone; sync docs; quarantine legacy trees; harden auth/persistence for GA  
7. **Release Ready?** **NO**

RC1 validation artifacts are complete. Pipeline is functionally green for structural E2E, but **not GA / production release ready** until P1 issues are resolved.
