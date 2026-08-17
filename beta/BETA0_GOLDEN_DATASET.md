# BETA0 Golden Dataset

| Field | Value |
|-------|-------|
| Document | BETA0_GOLDEN_DATASET |
| Date | 2026-08-17 |
| Status | **FROZEN** |
| Rule | No synthetic cases. No invented birth data. Placeholders are not cases. |
| Sources | `knowledge/validation/GOLDEN_DATASET_V1/` · `knowledge/editorial_validation/` |

This freeze records the current production case set.
It does not add charts.
It does not bind placeholders.
It does not make READY_FOR_CUSTOMERS = YES.

Each frozen case must retain:

- birth data
- engine truth
- golden / production PDF
- editorial review
- commercial score (where published)

---

## 1. Laboratory GOLDEN_DATASET_V1

Index: `knowledge/validation/GOLDEN_DATASET_V1/CASE_INDEX.md`

| CASE | Person | Status | Birth (solar) | Commercial score | Notes |
|------|--------|--------|---------------|------------------|-------|
| CASE_0001 | Nguyễn Tiến Sơn | **FROZEN / GOLDEN** | 1987-01-21 04:30 | **8.0** (full journey) | Production fixture. Do not rewrite. |
| CASE_0002 | Hoàng Thị Thu Phương | ACTIVE / NOT GOLDEN | 1997-07-01 14:24 | **~6.7** | Bound; not golden. |
| CASE_0003 | Unnamed female child | STRESS / NOT GOLDEN | 2015-02-15 05:30 | **4.2** | No invented name. Pillar mismatch ISS-C3-001. |
| CASE_0004 … CASE_0010 | — | PLACEHOLDER | — | — | **Not cases. Do not bind in this freeze.** |

CASE_0001 is the only laboratory golden.
CASE_0002 and CASE_0003 remain in the freeze set as bound real charts, not as golden.

---

## 2. Production editorial cases (all remaining validated named charts)

Editorial IDs EV-0001 … EV-0010 avoid CASE-0002 / CASE-0003 collisions across pilot, production, and validation folders.

Manifest: `knowledge/editorial_validation/GOLDEN_DATASET_MANIFEST.json`

| EV | Person | Repo id | Birth | TZ | Place | Editorial overall | Commercial / journey | READY_FOR_CUSTOMERS |
|----|--------|---------|-------|----|-------|-------------------|----------------------|---------------------|
| EV-0001 | Nguyễn Tiến Sơn | CASE-0001 | 1987-01-21 04:30 | Asia/Bangkok | Hà Tây | 56 | 8.0 journey | NO |
| EV-0002 | Lương Ngọc Huỳnh | HUYNH | 1966-09-24 04:15 | Asia/Bangkok | Hà Nội | 59 | (editorial case; not laboratory golden) | NO |
| EV-0003 | Ngô Đặng Minh Tân | TAN | 2008-03-17 06:20 | Asia/Bangkok | Hà Nội | 53 | (editorial case; not laboratory golden) | NO |
| EV-0004 | Đinh Thành Trung | PILOT-0002 | 1977-02-18 06:30 | Asia/Ho_Chi_Minh | Hải Phòng | 49 | Pilot CASE-0002 ≠ production CASE-0002 | NO |
| EV-0005 | Nguyễn Tiến Khang (child) | PILOT-0003 | 2015-08-14 07:20 | Asia/Ho_Chi_Minh | Hà Nội | 22 | — | NO |
| EV-0006 | Nguyễn Tiến Minh (child) | PILOT-0004 | 2013-08-20 13:40 | Asia/Ho_Chi_Minh | Hà Nội | 24 | — | NO |
| EV-0007 | Nguyễn Thị Hương Mai | PILOT-0006 | 1988-06-07 20:45 | Asia/Ho_Chi_Minh | Hải Phòng | 50 | — | NO |
| EV-0008 | Vũ Thị Thanh Tuyền | PILOT-0007 | 1984-07-13 21:01 | Asia/Ho_Chi_Minh | Quảng Ninh | 28 | — | NO |
| EV-0009 | Hoàng Thị Thu Phương | CASE-0002 | 1997-07-01 14:24 | Asia/Ho_Chi_Minh | Quảng Ninh | 26 | ~6.7 CLL | NO |
| EV-0010 | CASE-0003 Extreme Subject | CASE-0003 | 2015-02-15 05:30 | Asia/Ho_Chi_Minh | Hà Nội | 39 | 4.2 | NO |

Known production anchors named in this freeze mission:

- Nguyễn Tiến Sơn
- Lương Ngọc Huỳnh
- Ngô Đặng Minh Tân

Plus all remaining validated named cases EV-0004 … EV-0010.

---

## 3. Required artifacts per case

| Artifact | Where |
|----------|--------|
| Birth data | `knowledge/editorial_validation/cases/EV-00xx/INPUT.md` |
| Engine truth | `cases/EV-00xx/ANALYTICAL_TRUTH.md` |
| Production PDF | `knowledge/editorial_validation/exports/` |
| Editorial review | `PRODUCT_REVIEW.md` · `FINDINGS.md` · `SCORECARD.json` |
| Commercial score | CASE_INDEX / commercial reviews where published |

PUBLISH01 dual-edition PDFs (2026-08-17) for anchors:

`knowledge/editorial_validation/exports/publish01/executive/`  
`knowledge/editorial_validation/exports/publish01/professional/`

| Chart | Executive | Professional |
|-------|-----------|--------------|
| Nguyễn Tiến Sơn | 4 pages | 11 pages |
| Lương Ngọc Huỳnh | 4 pages | 11 pages |
| Ngô Đặng Minh Tân | 4 pages | 11 pages |

---

## 4. Excluded (not golden, not frozen as product cases)

| Id | Reason |
|----|--------|
| `validation/real_cases/case_01`–`case_20` | Anonymous fixtures. No consulting identity. |
| Pilot CASE-0008 | No birth datetime. |
| Pilot CASE-0009 | No verified birth/pillar source. |
| Synthetic Readiness Subject | Explicitly synthetic. |
| GOLDEN_DATASET placeholders CASE_0004–CASE_0010 | Unbound. Not people. |

Do not promote these during Beta without Product Owner binding of a **real** chart.

---

## 5. Immutability

Golden Dataset contents, snapshots, and expected outputs are not to be edited to make tests pass.

Regeneration of PDFs for a Beta release is required by the release checklist.
Regeneration does not authorize rewriting birth data, engine truth, or editorial history.

---

## Official status

**Current Golden Dataset and all remaining validated production cases are frozen for Beta 0.**
Synthetic cases: **NONE**.
