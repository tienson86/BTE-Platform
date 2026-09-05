# P7-IMP-09R DOMAIN SEMANTIC CONTRACT REPAIR REPORT

**Task:** P7-IMP-09R — Domain semantic contract repair (Driver / Support / Bottleneck)  
**Date:** 2026-09-05  
**Status:** PASS

Live CASE-0001: Nguyễn Tiến Sơn, male, 21/01/1987 04:30, Hà Nội.

---

## Status

PASS

Canonical DI-12~DI-17 driver IDs are elected as mechanisms. Customer Vietnamese text is a display label only. Domain Engine architecture, MC-01, Evidence Priority, Luck, Optimization, and Narrative were not changed.

---

## Root cause

`_domain_driver` treated Evidence Priority `customer_label`, MC-01 dimension names, Achievement/Career lists, and Damage copy as Domain Driver.

That happened because driver was filled by `label_of(finding)` and fallbacks such as:

- Vitality → `damage_label("resource_overload")` → “Ấn quá vượng kìm biểu đạt”
- Wealth → retention/creation dimension → “Giữ tài”
- Career → `" · ".join(work_styles)` → three profile strengths
- Authority → `capability_label("authority")` → generic “Quyền hạn”

Those are evidence texts or dimensions, not frozen AuthorityDriver / CareerDriver / WealthDriver / RelationshipDriver / LegacyDriver / VitalityDriver taxonomies.

---

## Authority driver

Canonical ID: `mixed`  
Display label: **Cơ chế hỗn hợp**

Support: Thất Sát  
Bottleneck: Quá tải áp lực quyền hạn  
Risk / caution: Quá tải áp lực quyền hạn

Not `authority` / “Quyền hạn”. Competing mechanisms (Sát→Ấn, Tài sinh Quan, Quan→Ấn, management_structure, professional_authority) are preserved as hybrid/`mixed`, not concatenated labels.

---

## Career driver

Canonical ID: `hybrid`  
Display label: **Cơ chế hỗn hợp**

Support: Thất Sát  
Bottleneck: Ấn quá vượng kìm biểu đạt  
Risk / caution: Ấn quá vượng kìm biểu đạt

Not “Nghiên cứu học thuật · Quản lý · Lãnh đạo”. Academic depth and authority/management compete, so `hybrid`. Component strengths remain on dimensions.

---

## Wealth driver

Canonical ID: `hybrid`  
Display label: **Cơ chế hỗn hợp**

Support: Cứu giải cấu trúc còn hiệu lực  
Bottleneck: Thiên Tài  
Risk / caution: Biến động tài cao

Not “Giữ tài”. Retention / accumulation / volatility stay dimensions. Output chain, management, and entrepreneurship compete, so `hybrid`.

---

## Relationship driver

Canonical ID: `communication`  
Display label: **Giao tiếp**

Support: Cứu giải cấu trúc còn hiệu lực  
Bottleneck: Khe hở giao tiếp  
Risk / caution: Khe hở giao tiếp

Canonical id is `communication` with peer-conflict evidence. Hồng Loan is not Driver.

---

## Legacy driver

Canonical ID: `hybrid`  
Display label: **Cơ chế hỗn hợp**

Support: Thiên Ấn  
Bottleneck: (empty)  
Risk / caution: (empty)

Knowledge legacy and business legacy are both high, so `hybrid` rather than a single “Học thuật” string. Canonical values remain `knowledge` / `business` components under `hybrid`; display is not the engine enum.

---

## Vitality driver

Canonical ID: `resilience`  
Display label: **Bền bỉ**

Support: Sát → Ấn → Thân  
Bottleneck: Ấn quá vượng kìm biểu đạt  
Risk / caution: Quá tải căng thẳng

Damage is bottleneck/risk, not Driver.

---

## Driver / Support / Bottleneck separation

PASS

- Driver is a frozen mechanism id + mapped label.
- Support enables the driver and is rejected when it is the same finding/label as bottleneck or a Damage/risk finding.
- Bottleneck may consume Damage/Risk (Vitality bottleneck is resource_overload).
- Same display string is not used as both driver and bottleneck.
- Wealth no longer repeats Thiên Tài as support and bottleneck.

---

## Domain states changed

NONE

Live CASE-0001 states are unchanged from P7-IMP-09:

| Domain | State |
| --- | --- |
| Authority | conditional |
| Career | conditional |
| Wealth | fragmented |
| Relationship | fragmented |
| Legacy | conditional |
| Vitality | conditional |

---

## Evidence Priority

UNCHANGED

Domain Engine still consumes `EvidencePriorityResult`. No rerank.

---

## MC-01

UNCHANGED

Pattern Chính Ấn, Grade B, ScoreEngine D+ remain distinct. No MC-01 profile rewrite.

---

## Build

PASS — `python tools/build.py`

---

## Type Check

PASS — Pack 07 scoped mypy, 75 files, no issues.

---

## Tests

| Suite | Result |
| --- | --- |
| `tests/detailed_interpretation` | **149 passed** before the final support-label split; **12** P7-IMP-09R tests passed after |
| P7-IMP-09R negatives / metamorphics / CASE-0001 | **12 passed** |
| P7-IMP-09 domains | **15 passed** |
| MC-01 / Evidence Priority / Portal / PDF / DOCX / History | **45 passed** |

No Golden Dataset / snapshot / expected-output edits.

---

## Runtime

PASS

`POST /api/v1/analyze` CASE-0001 returns `driver_id` + Vietnamese `driver` on all six domains. Diagnostics Domains **PASS**. `/result` renders repaired labels. History 200, export path unchanged.

---

## Screenshots

- `implementation/pack_07/screenshots/p7_imp_09r_domain_summary.png`
- `implementation/pack_07/screenshots/p7_imp_09r_authority_expanded.png`
- `implementation/pack_07/screenshots/p7_imp_09r_career_expanded.png`
- `implementation/pack_07/screenshots/p7_imp_09r_wealth_expanded.png`
- `implementation/pack_07/screenshots/p7_imp_09r_relationship_expanded.png`
- `implementation/pack_07/screenshots/p7_imp_09r_legacy_expanded.png`
- `implementation/pack_07/screenshots/p7_imp_09r_vitality_expanded.png`
- `implementation/pack_07/screenshots/p7_imp_09r_diagnostics.png`

Also captured: overview, mobile summary. Proof: `implementation/pack_07/P7-IMP-09R_diagnostics.json`

---

## Regression

PASS

MC-01, Evidence Priority, Portal, PDF, DOCX, and History tests passed. No layout redesign.

---

## Business logic introduced

SEMANTIC CONTRACT REPAIR ONLY

Elect frozen driver taxonomies; map display labels; guard damage/dimension/risk-as-driver; keep support off primary risk. No Luck / Optimization / Narrative.

---

## Next

STOP.

Do not implement Luck automatically.
