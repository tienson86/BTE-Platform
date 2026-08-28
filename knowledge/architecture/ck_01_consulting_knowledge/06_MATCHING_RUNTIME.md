# 06 — Matching Runtime

| Field | Value |
|-------|--------|
| Document | CK-01C Knowledge Matching Runtime |
| Version | 1.0.0 |
| Status | Canonical for CK-01C |
| Runtime id | `bte.consulting.knowledge.matching.v1` |

---

## 1. Purpose

Run deterministic matching against the frozen CK-01B catalog.

The runtime copies published signals. It does not calculate, infer, or generate wording.

---

## 2. Public entry

`match_published_knowledge(analysis_result, identity, integrated_narrative)`

Output: `ConsultingKnowledgePack`

---

## 3. Match order

```
Canonical Analysis Result
Identity
Integrated Narrative
        ↓
Signal projection (copy only)
        ↓
Condition equality / membership
        ↓
Applicable scope filter
        ↓
Catalog units in stored order
        ↓
ConsultingKnowledgePack
```

Same published inputs + same catalog → same pack.

---

## 4. Fail-closed

No matching unit → pack status `insufficient`. Empty copy: `Chưa có dữ liệu`.

Do not fill the pack with generated consulting text.

---

## 5. Forbidden

- LLM / AI
- arithmetic, ranking, prediction
- calling Calendar, Bazi, Identity, Narrative engines
- rewriting catalog wording
- Report / Workspace / PDF / DOCX wire

---

END
