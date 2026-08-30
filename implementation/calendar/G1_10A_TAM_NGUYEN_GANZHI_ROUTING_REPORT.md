# G1-10A — Tam Nguyên Ganzhi Routing

## 1. STATUS

**DONE.**

Year and Month Cung now follow Calendar Tam Nguyên everywhere that publishes Tứ Trụ identity (birth analysis, homepage “Kết quả ngày”, identity header, report adapters). Day and Hour stay on Hạ Nguyên. Personal digit-sum Cung Phi is unchanged from G1-10.

## 2. Root cause

G1-10 published `calendar.tam_nguyen` (1966 → Trung Nguyên) and personal Cung Phi (1966 male → Đoài) but Tứ Trụ Year/Month Cung still called `pillar_contract(ganzhi)` with no Nguyên.

That helper always used `ha_nguyen_cung.csv`. For 1966 **Bính Ngọ**:

- personal Cung Phi (Gregorian digit-sum) → Đoài
- Year Cung via Hạ Nguyên table → Khảm

One analysis therefore mixed Trung Nguyên cycle metadata with Hạ Nguyên pillar palaces. Homepage “Kết quả ngày” used the same unrouted helper. Identity header Can Chi could also fall back to lunar `calendar.year_can_chi` instead of BaZi Lập Xuân stems.

## 3. Previous Year source

Hạ Nguyên (`engines/date_selection/data/ha_nguyen_cung.csv` via `pillar_contract` / `trach_for_date_ganzhi`). No Tam Nguyên argument.

## 4. Previous Month source

Same Hạ Nguyên default as Year.

## 5. New Year source

`calendar.tam_nguyen` of the Gregorian civil year.

Lookup: `cung_for_ganzhi(year_ganzhi, tam_nguyen=calendar.tam_nguyen, reference_year=solar_year)` on the canonical Tam Nguyên 60 Hoa Giáp dataset introduced in G1-10.

Can Chi stems/branches are still Calendar/BaZi algorithms (lunar year label on Calendar; Lập Xuân year on BaZi). Nguyên routing selects the Cung row, not a second stem/branch calculator.

## 6. New Month source

Same Tam Nguyên as Year.

Can Chi remains solar-term Ngũ Hổ Độn (`month_pillar`). Cung uses the year’s Nguyên dataset.

## 7. Day source

**Hạ Nguyên** (unchanged).

Noon JDN day Can Chi + Hạ Nguyên Cung (`HA_NGUYEN` in `ganzhi_routing` / `snapshot_pillar_payloads` / identity Day cell).

## 8. Hour source

**Hạ Nguyên** (unchanged).

Ngũ Thử Độn hour Can Chi + Hạ Nguyên Cung. Date-selection hours still use `trach_for_date_ganzhi`.

Canonical routing:

| Pillar | `source_nguyen` |
| --- | --- |
| Year | `calendar.tam_nguyen` |
| Month | `calendar.tam_nguyen` |
| Day | Hạ Nguyên |
| Hour | Hạ Nguyên |

UI does not choose this. Frontend does not recompute Year/Month.

## 9. Birth chart routing

```
Birth Input
  → CalendarEngine.build (tam_nguyen, cung_phi, ganzhi_routing)
  → BaZi (Lập Xuân year / solar-term month / JDN day / Ngũ Thử hour)
  → identity.four_pillars (BaZi Can Chi + Nguyên-aware Year/Month Cung)
  → Orchestrator stamps bazi.*_pillar.source_nguyen from calendar.ganzhi_routing
  → ResultStore / /result / Report consume those pillars
```

No downstream engine reconstructs Year/Month Cung from the Hạ Nguyên CSV. Strength / Pattern / Luck / ShenSha still receive the same BaZi stems as before.

## 10. Homepage Kết quả ngày routing

`DateSelectionService.inspect_day` still reads Calendar Engine for Can Chi.

`DaySelection.to_dict` / `RankedDate.to_dict` now call `snapshot_pillar_payloads`:

- Year / Month: snapshot `tam_nguyen` (Gregorian year)
- Day: Hạ Nguyên
- Hours: existing Hạ Nguyên hour rows

Frontend `date_selection` / `TuTruPanel` only display API fields. No local 60 Hoa Giáp table.

## 11. /result verification

Identity header `bindPillar` now takes **BaZi stem/branch first**, then identity. Calendar lunar `year_can_chi` is no longer a Can Chi fallback.

BaZi card `bindPillar` uses BaZi stem/branch first.

Invariant covered by `test_case_1966_header_matches_bazi`:

```
identity.year/month/day/hour.can_chi
  == bazi year/month/day/hour stem+branch
```

Live browser click-through of `/result` was not started in this session. Data identity is enforced in adapters + golden tests.

## 12. Report/PDF/DOCX verification

- `ReportInputV1Adapter._build_pillars` copies `analysis.bazi` pillars (no date rebuild).
- `build_customer_report_input` copies stored `data.bazi` pillars (Portal PDF/DOCX).
- Production runner stamps `source_nguyen` on the same serialized BaZi dict used for calendar shaping and consulting.

Portal / PDF / DOCX therefore receive the same four Can Chi after G1-10A.

## 13. 1966 result

Input: male, 24/09/1966, 04:15, Hà Nội.

| Field | Value | Source |
| --- | --- | --- |
| `tam_nguyen` | Trung Nguyên | 180-year cycle |
| `cuu_van` | 6 | 180-year cycle |
| `cung_phi` / `menh_quai` | Đoài | Gregorian digit-sum (personal) |
| `house_group` | Tây Tứ Trạch | palace group |
| Year | Bính Ngọ, Cung Đoài | Trung Nguyên dataset |
| Month | Đinh Dậu, Cung Đoài | Trung Nguyên dataset |
| Day | Bính Tuất, Cung Chấn | Hạ Nguyên |
| Hour | Canh Dần, Cung Cấn | Hạ Nguyên |

Year/Month Can Chi strings are not hardcoded in production code. Tests read expected Cung from `cung_for_ganzhi(..., tam_nguyen=tam_nguyen_for_year(year))`.

Personal Cung Phi (Đoài) and Year Cung (Đoài) now agree for this chart. They remain separate algorithms.

## 14. Boundary tests

`test_boundary_year_month_source_follows_tam_nguyen`:

| Year | Year/Month source | Day/Hour source |
| --- | --- | --- |
| 1923 | Thượng Nguyên | Hạ Nguyên |
| 1924 | Trung Nguyên | Hạ Nguyên |
| 1983 | Trung Nguyên | Hạ Nguyên |
| 1984 | Hạ Nguyên | Hạ Nguyên |
| 2043 | Hạ Nguyên | Hạ Nguyên |
| 2044 | Thượng Nguyên | Hạ Nguyên |

## 15. 180-year regression

`test_180_year_cycle_source_nguyen_property` loops `1864 … 2043` (one full cycle) on `routing_table`:

- `year.source_nguyen == tam_nguyen_for_year(year)`
- `month.source_nguyen == tam_nguyen_for_year(year)`
- `day.source_nguyen == Hạ Nguyên`
- `hour.source_nguyen == Hạ Nguyên`

## 16. Legacy Hạ Nguyên paths retained

| Path | Why kept |
| --- | --- |
| `engines/date_selection/cung_phi.py` `cung_for_date_ganzhi` / `trach_for_date_ganzhi` | Day/Hour palace + hour windows |
| `engines/date_selection/data/ha_nguyen_cung.csv` | Canonical Hạ Nguyên 60-row table |
| `pillar_contract(ganzhi)` with no `tam_nguyen` | Day/Hour identity; backward-compatible 3-key cell |
| `ganzhi_routing.resolve_day_ganzhi` / `resolve_hour_ganzhi` | Explicit `HA_NGUYEN` |
| `ha_nguyen_cung_for_ganzhi` | Explicit Hạ Nguyên helper (no implicit default) |
| HourSelection `hoa_giap_view(..., trach_for_date_ganzhi)` | Homepage hour Cung |

BaZi Day/Hour Can Chi algorithms were already Hạ-Nguyên-period civil math (JDN / Ngũ Thử Độn) and are unchanged.

## 17. Legacy paths removed/bypassed

| Path | Change |
| --- | --- |
| Birth Year Cung via default `pillar_contract()` | Now `pillar_contract(..., tam_nguyen=calendar.tam_nguyen)` |
| Birth Month Cung via default `pillar_contract()` | Same |
| Homepage Year/Month via default `pillar_contract()` | `snapshot_pillar_payloads` routes by snapshot Tam Nguyên |
| Identity header Can Chi fallback to `calendar.year_can_chi` | Removed; BaZi pillar is SSOT |
| Implicit “everything is Hạ Nguyên” in Tứ Trụ Year/Month | Bypassed |

No Hạ Nguyên CSV rows were deleted. Day/Hour still use that table.

## 18. Tests

Executed (module scope, not full pytest):

```
pytest tests/calendar tests/identity tests/date_selection applications/api/tests/test_production_readiness.py -q
```

- `tests/calendar` + `tests/identity` + `tests/date_selection`: **261 passed**
- `applications/api/tests/test_production_readiness.py`: **3 passed** (1987 male Cung Phi expectation **Khôn → Tốn**)

New: `tests/calendar/test_g1_10a_ganzhi_routing.py`

- 1966 golden (cycle + Nguyên-aware Year/Month Cung from dataset)
- header == BaZi Can Chi
- 1923/1924, 1983/1984, 2043/2044
- 180-year property
- homepage / BaZi / report Can Chi consistency for 24/09/1966 04:15

**Remaining failures:** none in the modules run.

## 19. Files changed

| File | Role |
| --- | --- |
| `engines/calendar_engine/ganzhi_routing.py` | Canonical Year/Month/Day/Hour source routing + `stamp_bazi_source_nguyen` |
| `engines/calendar_engine/engine.py` | `CalendarResult.ganzhi_routing` |
| `engines/calendar_engine/cung_phi.py` | `ganzhi_label_for_year` (G1-10 dataset helper) |
| `engines/calendar_engine/tam_nguyen.py` | Unchanged G1-10 cycle (consumed) |
| `engines/date_selection/identity.py` | Nguyên-aware `pillar_contract` + `snapshot_pillar_payloads` |
| `engines/date_selection/models.py` | Snapshot `tam_nguyen`; homepage payloads use routed cells |
| `engines/date_selection/calendar_adapter.py` | Copy Calendar Tam Nguyên onto snapshot |
| `engines/identity/four_pillars.py` | Year/Month Cung from Calendar Tam Nguyên |
| `engines/identity/assemble.py` | Pass `tam_nguyen` + solar year into four pillars |
| `applications/api/services/orchestrator.py` | Stamp `source_nguyen` on serialized BaZi pillars |
| `applications/production/engine_runner.py` | Same stamp on production BaZi payload |
| `applications/customer_portal/src/screens/commercial_dashboard/adapter.ts` | Header binds BaZi Can Chi (same object as Bát Tự) |
| `applications/customer_portal/src/screens/commercial_dashboard/baziAdapter.ts` | BaZi stem/branch first |
| `applications/api/tests/test_production_readiness.py` | 1987 male Cung Phi = Tốn |
| `tests/calendar/test_g1_10a_ganzhi_routing.py` | Golden / boundary / 180-year / consistency |

G1-10A stops here. No further feature started.
