# TODO_REVIEW — Uncertain Publication Metadata

**Module:** `knowledge/references`  
**Library version:** 1.0.0  
**Date:** 2026-07-30  

Fields marked `TODO_REVIEW` in `references.json` must not be invented casually. Resolve via Academic Review before promoting any record to `official`.

---

## Per-reference bibliographic TODOs

### REF-000001 — Huang Di Nei Jing

| Field | Status |
|-------|--------|
| author | TODO_REVIEW |
| dynasty | TODO_REVIEW |
| estimated_year | TODO_REVIEW |
| isbn_or_identifier | TODO_REVIEW |
| publisher | TODO_REVIEW |
| edition | TODO_REVIEW |
| volume | TODO_REVIEW |
| chapter_support | empty — need Suwen/Lingshu anchors |

### REF-000002 — Zhou Yi

| Field | Status |
|-------|--------|
| author | TODO_REVIEW |
| dynasty | TODO_REVIEW |
| estimated_year | TODO_REVIEW |
| isbn_or_identifier | TODO_REVIEW |
| publisher | TODO_REVIEW |
| edition | TODO_REVIEW |
| volume | TODO_REVIEW |
| chapter_support | empty |

### REF-000003 — Yuan Hai Zi Ping

| Field | Status |
|-------|--------|
| author | provisional: "Traditional attribution" — confirm |
| dynasty | TODO_REVIEW |
| estimated_year | TODO_REVIEW |
| isbn_or_identifier | TODO_REVIEW |
| publisher | TODO_REVIEW |
| edition | TODO_REVIEW |
| volume | TODO_REVIEW |
| chapter_support | empty |

### REF-000004 — San Ming Tong Hui

| Field | Status |
|-------|--------|
| author | TODO_REVIEW (Wan Minying often cited traditionally — confirm edition) |
| dynasty | TODO_REVIEW |
| estimated_year | TODO_REVIEW |
| isbn_or_identifier | TODO_REVIEW |
| publisher | TODO_REVIEW |
| edition | TODO_REVIEW |
| volume | TODO_REVIEW |
| chapter_support | empty |

### REF-000005 — Di Tian Sui

| Field | Status |
|-------|--------|
| author | TODO_REVIEW (Jingtu / commentary lineages vary) |
| dynasty | TODO_REVIEW |
| estimated_year | TODO_REVIEW |
| isbn_or_identifier | TODO_REVIEW |
| publisher | TODO_REVIEW |
| edition | TODO_REVIEW |
| volume | TODO_REVIEW |
| chapter_support | empty |

### REF-000006 — Zi Ping Zhen Quan

| Field | Status |
|-------|--------|
| author | TODO_REVIEW (Shen Xiaozhan lineage — confirm) |
| dynasty | TODO_REVIEW |
| estimated_year | TODO_REVIEW |
| isbn_or_identifier | TODO_REVIEW |
| publisher | TODO_REVIEW |
| edition | TODO_REVIEW |
| volume | TODO_REVIEW |
| chapter_support | empty |

### REF-000007 — Qiong Tong Bao Jian

| Field | Status |
|-------|--------|
| author | TODO_REVIEW |
| dynasty | TODO_REVIEW |
| estimated_year | TODO_REVIEW |
| isbn_or_identifier | TODO_REVIEW |
| publisher | TODO_REVIEW |
| edition | TODO_REVIEW |
| volume | TODO_REVIEW |
| chapter_support | empty |

---

## Cross-cutting Architect TODOs

1. **ID remapping communication** — announce V1.0 SSOT IDs vs legacy `classics/INDEX.md` placeholders.
2. **Canon citation fix (out of this sprint)** — remap `wood.json` REF IDs to V1.0 meanings (see `REFERENCE_COVERAGE_REPORT.md` §3).
3. **Legacy INDEX sync** — update or deprecate Markdown INDEX after Canon remapping is approved.
4. **Promote statuses** — move records from `draft` → `review` → `official` only after bibliographic TODOs resolve.
5. **Extend seed** — decide whether REF-000008+ should continue legacy classics (Xie Ji Bian Fang Shu, etc.) or restart numbering for non-seed works.

---

## Count

| Item | Count |
|------|-------|
| Seed records | 7 |
| Bibliographic TODO_REVIEW field warnings (validator) | 48 |
| Empty `chapter_support` arrays | 7 |
| Records still `draft` | 7 |
