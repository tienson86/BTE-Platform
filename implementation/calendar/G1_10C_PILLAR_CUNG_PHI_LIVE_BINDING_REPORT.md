# G1-10C — Tứ Trụ Cung Phi live binding repair

## 1. STATUS

**DONE.**

Can Chi is unchanged (Bính Ngọ / Đinh Dậu / Bính Tuất / Canh Dần).

The Tứ Trụ Cung Phi column now binds published BaZi `cung_phi` (copied from Calendar routing), then routing, then identity. Year/Month use birth Tam Nguyên palaces. Day/Hour stay Hạ Nguyên.

Stale ResultStore payloads with `calendar_rule_version = G1-10B` are dropped. Submit a **new Analyze**.

## 2. Live symptom

Top TỨ TRỤ rendered Hạ Nguyên palaces from `ha_nguyen_cung.csv`:

| Trụ | Can Chi | Live Cung | Expected |
| --- | --- | --- | --- |
| Năm | Bính Ngọ | Khảm | Đoài |
| Tháng | Đinh Dậu | Khảm | Đoài |
| Ngày | Bính Tuất | Chấn | Chấn |
| Giờ | Canh Dần | Cấn | Cấn |

That Khảm/Khảm pair is exactly the Hạ Nguyên date table for Bính Ngọ and Đinh Dậu. It is not personal Cung Phi (1966 male = Đoài).

## 3. API Year Cung value

After G1-10C Analyze (24/09/1966 04:15 male):

```
bazi.year_pillar.cung_phi = Đoài
identity.four_pillars.year.cung_phi = Đoài
calendar.ganzhi_routing.year.cung_phi = Đoài
source_nguyen = Trung Nguyên
ganzhi = Bính Ngọ
```

## 4. API Month Cung value

```
bazi.month_pillar.cung_phi = Đoài
identity.four_pillars.month.cung_phi = Đoài
calendar.ganzhi_routing.month.cung_phi = Đoài
source_nguyen = Trung Nguyên
ganzhi = Đinh Dậu
```

Day = Chấn (Hạ Nguyên). Hour = Cấn (Hạ Nguyên). `tam_nguyen = Trung Nguyên`. `calendar_rule_version = G1-10C`.

Before this change, BaZi pillars had **no** `cung_phi` field (`None`). Identity already had Đoài in current source; the live header still followed leftover Hạ Nguyên identity / identity-only binding.

## 5. ResultStore Year Cung value

`bte_last_result.data.bazi.year_pillar.cung_phi` is now **Đoài** on a new Analyze.

G1-10B stored records are incompatible (`calendar_rule_version !== G1-10C`) and `loadCurrent()` returns null.

## 6. ResultStore Month Cung value

`bte_last_result.data.bazi.month_pillar.cung_phi` is now **Đoài** on a new Analyze.

## 7. Previous UI property path

DOM `TuTruRow` → `pillar.cungPhi`

`FourPillars.toTuTruPillar` → `pillars.year.cungPhi`

`adaptIdentityHeader` / `bindPillar`:

```
cungPhi: firstText(cell.cung_phi)
```

`cell` = `identity.four_pillars.year` (and month).

Year Khảm came from identity Year `cung_phi` when that cell still held the Hạ Nguyên table value. Month Khảm came from identity Month `cung_phi` the same way.

BaZi `cung_phi` was not published, so the header could not bind canonical routing Cung.

## 8. New UI property path

```
cungPhi: firstText(
  bazi.{year|month|day|hour}_pillar.cung_phi,
  calendar.ganzhi_routing.{pillar}.cung_phi,
  identity.four_pillars.{pillar}.cung_phi,
)
```

No frontend Ganzhi→palace lookup. No personal `calendar.cung_phi` on pillar rows.

## 9. Legacy fallback removed

- Header no longer uses identity Cung alone.
- Identity four-pillars Cung is overwritten from Calendar routing before publish.
- BaZi pillars receive `cung_phi` + `ganzhi` from routing (stems/Nạp âm untouched).
- ResultStore rejects G1-10B current results.

## 10. 1966 rendered result

Adapter + TuTruPanel DOM (vitest):

```
Năm    Bính Ngọ   Đoài
Tháng  Đinh Dậu   Đoài
Ngày   Bính Tuất  Chấn
Giờ    Canh Dần   Cấn
```

Regression: identity Year/Month still Khảm, BaZi/routing Đoài → DOM still Đoài.

## 11. Homepage Kết quả ngày result

`DateSelectionService.inspect_day(1966, 9, 24)`:

```
year  Bính Ngọ / Đoài / Trung Nguyên
month Đinh Dậu / Đoài / Trung Nguyên
day   Bính Tuất / Chấn / Hạ Nguyên
hour  Canh Dần / Cấn   (Hạ Nguyên, Dần window)
```

## 12. DOM test

`applications/customer_portal/tests/js/g1_10c_tutru_cung_phi.test.tsx`

2 passed.

## 13. Backend tests

```
pytest tests/calendar/test_g1_10c_pillar_cung_phi.py
       tests/calendar/test_g1_10a_ganzhi_routing.py
       tests/calendar/test_g1_10b_actual_ganzhi.py
       tests/identity/test_four_pillar_identity.py -q
```

**34 passed.** Remaining failures in that set: none.

## 14. Frontend tests

```
vitest run g1_10c_tutru_cung_phi ui03r1_tutru_bazi
           result_workspace_identity_consumers tu_tru_panel
```

**29 passed.**

## 15. Live screenshot evidence

API TestClient (new Analyze):

```
tam_nguyen = Trung Nguyên
calendar_rule_version = G1-10C
Year  Bính Ngọ  Cung=Đoài  (identity = bazi = routing)
Month Đinh Dậu  Cung=Đoài
Day   Bính Tuất Cung=Chấn
Hour  Canh Dần  Cung=Cấn
```

Header DOM from `CommercialDashboardPage` + `TuTruPanel` (`data-pillar` rows): Năm→Đoài, Tháng→Đoài, Ngày→Chấn, Giờ→Cấn.

`static/dist/result.js` rebuilt.

A live browser PNG of `/result` was not captured here. After restart, clear old `bte_last_result` (G1-10C gate does this) and submit 24/09/1966 04:15 male Hà Nội.

## 16. Files changed

| File | Role |
| --- | --- |
| `engines/calendar_engine/ganzhi_routing.py` | Stamp BaZi + identity Cung from routing |
| `engines/calendar_engine/tam_nguyen_dataset.py` | `calendar_rule_version = G1-10C` |
| `applications/api/services/orchestrator.py` | Apply identity Cung stamp |
| `applications/customer_portal/src/screens/commercial_dashboard/adapter.ts` | Bind BaZi/routing Cung first |
| `applications/customer_portal/src/features/result_workspace/adapter/baziWorkspaceAdapter.ts` | Same BaZi-first Cung |
| `applications/customer_portal/src/components/canonical/TuTruPanel.tsx` | `data-pillar` rows |
| `applications/customer_portal/static/js/canonical/tu_tru_panel.js` | Same row attribute |
| `applications/customer_portal/src/models/dto.ts` | Pillar `cung_phi` |
| `applications/customer_portal/src/resultState/currentResult.ts` | Invalidate ≠ G1-10C |
| `applications/customer_portal/static/js/result_store.js` | Same |
| `applications/customer_portal/static/dist/result.js` | Rebuilt bundle |
| `tests/calendar/test_g1_10c_pillar_cung_phi.py` | API + homepage values |
| `applications/customer_portal/tests/js/g1_10c_tutru_cung_phi.test.tsx` | Header DOM |

Tam Nguyên definitions, personal Cung Phi formula, and 1966 Can Chi values were not changed.

G1-10C stops here.
