# 01 — Population Workflow

Version: 1.0  
Status: **EPIC 3 · SPRINT A — Population Framework**  
Date: 2026-08-08  
Depends on: `00_POPULATION_INDEX.md`, EPIC 2 `14`/`15`/`16`  

---

## 1. Purpose

Define the official end-to-end workflow for populating Knowledge Units:

```
Catalog pick → Author Draft → Reviews → Approved → Published → (Revise | Deprecate)
```

This is **process design only**. No units are authored in this sprint.

---

## 2. Preconditions (before any content sprint)

| Gate | Requirement |
|------|-------------|
| G0 | EPIC 2 model + catalog frozen (done) |
| G1 | This Population Framework approved |
| G2 | Content sprint authorized (explicit product/architecture approval) |
| G3 | Wave selected from `05_WAVE_EXECUTION_PLAN.md` |
| G4 | Physical store mapping decided in implementation epic **or** authoring proceeds in approved staging format that maps 1:1 to logical schema `12` |

**G2 is mandatory.** Framework approval ≠ license to write production bodies.

---

## 3. Master workflow

```
1. Select wave + catalog rows (16)
        ↓
2. Reserve / confirm KU ids
        ↓
3. Author Draft (schema + body + metadata)
        ↓
4. Author self-check (03 validation checklist)
        ↓
5. Technical Review
        ↓
6. Knowledge Review
        ↓
7. Commercial Review
        ↓
8. Narrative Review
        ↓
9. Approval (Release / Ops)
        ↓
10. Publish (production-eligible)
        ↓
11. Wave exit validation (composition / sample suite)
        ↓
12. Maintain: Revise or Deprecate as needed
```

Any fail at steps 5–8 → return to **Draft** with recorded findings.

---

## 4. Author workflow (detail)

### 4.1 Select work item

| Step | Action |
|------|--------|
| 1 | Open wave list (`05`) |
| 2 | Pick next catalog row (`16`) — prefer Required before Optional |
| 3 | Confirm id unused; RK+MT always queued as a pair |
| 4 | Note primary_usage and Narrative components from catalog/matrix |

### 4.2 Draft

| Step | Action |
|------|--------|
| 1 | Fill logical fields per EPIC 2 `12` |
| 2 | Write commercial VI `body` (consultant voice) |
| 3 | Set `applicable_conditions` to Analysis signals (no invented signals) |
| 4 | Set `evidence_kind`, domains, scenarios, usage, ethics |
| 5 | Link `paired_unit_ids` for Risk/Mitigation |
| 6 | Set version + `review_status=draft` |
| 7 | Run self-checklist (`03`) |

### 4.3 Submit

Author submits package:

- KU Draft  
- Self-check results  
- Related pair Draft (if RK/MT)  
- Notes on sample signals to test  

---

## 5. Review workflow (summary)

| Order | Review | Blocks publish if fail |
|------:|--------|------------------------|
| 1 | Technical | Yes |
| 2 | Knowledge | Yes |
| 3 | Commercial | Yes |
| 4 | Narrative | Yes |

Full checklists: `02_REVIEW_PROCESS.md`.

**Narrative Review** is an EPIC 3 population gate in addition to EPIC 2 lifecycle stages. It ensures Content Quality / Pack 05 fitness before Approval.

---

## 6. Approval process

| Step | Owner | Action |
|------|-------|--------|
| 1 | Release / Knowledge Ops | Verify all four reviews recorded Pass |
| 2 | Ops | Verify wave membership + catalog id |
| 3 | Ops | Set `review_status=approved` |
| 4 | Ops | Bundle into release candidate (wave batch preferred) |
| 5 | Ops | Publish → `review_status=published` + timestamps |
| 6 | Ops | Update wave progress register (future ops artifact) |

**Approved ≠ Published.** Only Published may feed production Narrative.

---

## 7. Quality gates (workflow-level)

| Gate | When | Pass condition |
|------|------|----------------|
| QG-Author | Before submit | Checklist `03` § Author |
| QG-Tech | Technical Review | Schema + no Rule DB dup + conditions |
| QG-Know | Knowledge Review | Meaning + ethics |
| QG-Comm | Commercial Review | Value + brand + priority |
| QG-Narr | Narrative Review | Component/evidence/CQ fit |
| QG-Approve | Approval | All reviews Pass |
| QG-Publish | Publish | Manifest + pair integrity |
| QG-Wave | Wave exit | `05` exit criteria |

---

## 8. Parallelization rules

| Allowed in parallel | Not allowed |
|---------------------|-------------|
| Different KU ids by different authors | Same id by two authors |
| AN wave track vs AC track (different owners) | Publishing unpaired RK |
| Reviews of different units | Skipping Narrative Review for P0 Exec/Rec/Warning units |

---

## 9. Exception paths

| Case | Process |
|------|---------|
| Typo-only on Published | Patch version; Technical confirms no semantic change; may fast-track Commercial + Narrative skim (`04`) |
| Meaning change | Full review path on new version |
| Catalog gap discovered | Amend catalog (`16`) via Architect before new id |
| Ethics dispute | Hold; escalate Architect + Commercial; do not Publish |
| Analysis signal missing | Do not invent; backlog signal or rewrite condition |

---

## 10. Out of scope for this workflow

- Implementing retrieval/composition runtime  
- Editing Score / Interpretation / Narrative engines  
- Portal copy as a substitute for KUs  
- Golden Dataset / snapshot mutation  

---

## 11. Stop line

Population workflow defined.  
No units created in this sprint.

---

END
