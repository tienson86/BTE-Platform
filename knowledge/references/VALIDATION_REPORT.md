# Reference Library Validation Report

**Module:** `knowledge/references`  
**Library version:** 1.0.0  
**Date:** 2026-07-30  
**Validator:** `validate_references.py`

---

## Summary

| Metric | Value |
|--------|-------|
| Records checked | 7 |
| Index entries | 7 |
| Errors | **0** |
| Warnings (`TODO_REVIEW` metadata) | 48 |
| Result | **PASS** |

---

## Checks executed

| Rule | Result |
|------|--------|
| No duplicated `reference_id` | PASS |
| Unique `title_english` | PASS |
| Valid `category` enum | PASS |
| Valid `source_type` enum | PASS |
| Valid `canonical_status` enum | PASS |
| Required metadata fields present | PASS |
| Index ↔ catalog consistency | PASS |

---

## Seed inventory validated

| ID | title_english | category | status |
|----|---------------|----------|--------|
| REF-000001 | Huang Di Nei Jing | classic | draft |
| REF-000002 | Zhou Yi | classic | draft |
| REF-000003 | Yuan Hai Zi Ping | classic | draft |
| REF-000004 | San Ming Tong Hui | classic | draft |
| REF-000005 | Di Tian Sui | classic | draft |
| REF-000006 | Zi Ping Zhen Quan | classic | draft |
| REF-000007 | Qiong Tong Bao Jian | classic | draft |

---

## Warnings

All warnings are intentional `TODO_REVIEW` placeholders for uncertain bibliographic scalars (author, dynasty, year, ISBN, publisher, edition, volume). See `TODO_REVIEW.md`.

---

## Command

```bash
python knowledge/references/validate_references.py
```

Output: `ok=True`, `error_count=0`.
