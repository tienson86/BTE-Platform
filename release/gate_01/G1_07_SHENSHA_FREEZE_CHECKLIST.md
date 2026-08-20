# G1-07 — ShenSha Freeze Checklist

Canonical production remains:

```text
BaziEngine.build
  → ShenShaService.evaluate (signal_maps)
  → ShenShaDetectionResult
  → calculate() / BaziChart.shensha   # name projection only
  → BaziView.shensha + shensha_matches
  → Orchestrator / API / Portal / Report / PDF / DOCX
```

V1.0 lock: one calculation path; structured evidence; Option A aliases; Hồng Loan ≠ Thiên Hỷ; no Cát/Hung inference; no Deep Interpretation.

| # | Criterion | Status |
|---|-----------|--------|
| 1 | One canonical ShenSha calculation path (`evaluate`) | PASS |
| 2 | Structured evidence on every published match | PASS |
| 3 | Legacy `list[str]` is projection only (`calculate` / `canonical_names`) | PASS |
| 4 | Thiên Ất alias no longer double-publishes | PASS |
| 5 | Thiên Đức alias no longer double-publishes | PASS |
| 6 | Nguyệt Đức alias no longer double-publishes | PASS |
| 7 | Hồng Loan formula independent (`HONG_LUAN_OPPOSITE`) | PASS |
| 8 | Thiên Hỷ formula independent (`TIAN_XI_BRANCH`) | PASS |
| 9 | CASE-0001 false Thiên Hỷ removed (no Mùi) | PASS |
| 10 | Multiple occurrences preserved on one canonical ID | PASS |
| 11 | Alias dedup does not drop positions | PASS |
| 12 | Every published item has source + target + location | PASS |
| 13 | Portal does not recalculate ShenSha | PASS |
| 14 | Report does not use the name as fake evidence | PASS |
| 15 | Unsupported S07 Cát/Hung inference removed | PASS |
| 16 | API / Portal / Report / PDF / DOCX copy the same matches | PASS |
| 17 | Current V1 Golden synchronized | PASS |
| 18 | G1-07 regression tests PASS | PASS |
| 19 | No Deep ShenSha interpretation added | PASS |
| 20 | Không Vong not invented; not in V1.0 natal catalog | PASS |

CASE-0001 freeze facts:

- Pillars: Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần
- Published: **Thiên Ất Quý Nhân**, **Hồng Loan**, **Thiên Đức Quý Nhân**, **Nguyệt Đức Quý Nhân**
- Thiên Ất: Nhật can Canh → Sửu tại trụ Tháng
- Hồng Loan: Niên chi Dần → Sửu tại trụ Tháng
- Thiên Đức Quý Nhân: Nguyệt chi Sửu → Canh tại trụ Ngày (can)
- Nguyệt Đức Quý Nhân: Nguyệt chi Sửu → Canh tại trụ Ngày (can)
- Thiên Hỷ: absent

| Sync | Status |
|------|--------|
| Golden Dataset synchronized | **YES** |
| Remaining canonical ShenSha mismatch | **0** |

Stop: do not start G1-08.

G1-07 STATUS: FROZEN FOR BTE V1.0
