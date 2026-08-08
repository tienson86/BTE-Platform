# 02 — Pipeline Integration

Version: 1.0  
Status: **EPIC 4 · SPRINT A**  
Date: 2026-08-08  
Depends on: `01_RETRIEVAL_CONTRACT.md`, V1 Architecture Freeze  

---

## 1. Purpose

Document the production integration pipeline:

```
Knowledge Unit (corpus)
        ↓
Retrieval
        ↓
Commercial Bundle
        ↓
Narrative Runtime
        ↓
Narrative Composer
        ↓
Narrative Result
        ↓
Portal
```

For every stage: **Input · Output · Responsibilities · Failure handling**.

---

## 2. Stage 0 — Knowledge Unit corpus

| Aspect | Definition |
|--------|------------|
| **Input** | Authored KUs in `database/20_knowledge/21_knowledge_units.csv` (and future rows) |
| **Output** | Readable corpus for Adapter |
| **Responsibilities** | Store advisory SSOT; version; status |
| **Failure handling** | Corrupt/unreadable row → skip + log; never crash analysis |

**Constraint:** Sprint A does not modify corpus.

---

## 3. Stage 1 — Retrieval

| Aspect | Definition |
|--------|------------|
| **Input** | Analysis signals, scenario, allow-list, optional interpretation hints |
| **Output** | Candidate KU set (pre-bundle) |
| **Responsibilities** | Filter by contract (`01`); evaluate conditions; apply confidence gates |
| **Failure handling** | No matches → empty candidates; invalid signal map → treat as empty + trace error |

---

## 4. Stage 2 — Commercial Bundle

| Aspect | Definition |
|--------|------------|
| **Input** | Candidate KUs |
| **Output** | `CommercialKnowledgeBundle` + `NarrativeKnowledgePayload` |
| **Responsibilities** | Rank, dedupe, conflict-resolve, bind placeholders, emit trace (`03` Adapter) |
| **Failure handling** | Bind failure → drop unit; conflict → resolution policy; partial bundle allowed |

---

## 5. Stage 3 — Narrative Runtime

| Aspect | Definition |
|--------|------------|
| **Input** | Existing Narrative inputs **plus** NarrativeKnowledgePayload (additive) |
| **Output** | NarrativeTree (unchanged model) |
| **Responsibilities** | Build tree from evidence including commercial evidence kinds |
| **Failure handling** | Missing commercial payload → legacy behavior (insufficient/thin); must not invent |

**Constraint:** No Narrative redesign. Payload must fit **existing** evidence kind consumption.

**Phase B placement:** Prefer **Orchestrator-level merge** into the object/dict Narrative already accepts — avoid editing Interpretation Engine; avoid Pack 05 grammar changes.

---

## 6. Stage 4 — Narrative Composer

| Aspect | Definition |
|--------|------------|
| **Input** | NarrativeTree |
| **Output** | NarrativeResult sections |
| **Responsibilities** | Compose Exec / Rec / … in official order; keep trace refs on paragraphs |
| **Failure handling** | Underfilled slots → approved insufficient copy |

---

## 7. Stage 5 — Narrative Result

| Aspect | Definition |
|--------|------------|
| **Input** | Composer output |
| **Output** | `NarrativeResult` (`complete` / `partial_insufficient` / `failed`) |
| **Responsibilities** | Stable commercial prose contract for Portal |
| **Failure handling** | `failed` only on hard pipeline errors; thin commercial → partial_insufficient |

---

## 8. Stage 6 — Portal

| Aspect | Definition |
|--------|------------|
| **Input** | `data.narrative_result` |
| **Output** | Result Page presentation |
| **Responsibilities** | Prefer NarrativeResult; no inventing advice |
| **Failure handling** | Existing fallbacks when NarrativeResult absent |

**Constraint:** No Portal UI changes in this epic.

---

## 9. End-to-end failure matrix

| Failure | Pipeline behavior |
|---------|-------------------|
| Units awaiting_review only | Empty commercial bundle (allow-list) |
| Analysis missing useful_god | No UG/RC units |
| Strength not favorable | No ST unit |
| Placeholder unbound | Drop that unit |
| All commercial dropped | Narrative baseline (pre-CK) honesty path |
| Adapter exception | Log; continue without CK (degrade gracefully) |

---

## 10. Analytical meaning preservation

| Rule | Detail |
|------|--------|
| Analysis SSOT | Scores/patterns/gods unchanged |
| Adapter | Selects text; does not recompute |
| Narrative | Composes; does not invent claims |
| Portal | Displays; does not author analysis |

---

## 11. Stop line

Pipeline integration documented. No runtime.

---

END
