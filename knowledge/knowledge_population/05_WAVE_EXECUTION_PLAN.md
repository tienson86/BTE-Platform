# 05 — Wave Execution Plan

Version: 1.0  
Status: **EPIC 3 · SPRINT A — Population Framework**  
Date: 2026-08-08  
Depends on: EPIC 2 `16`/`19`/`20`, this folder `01`–`04`  
Scope: Planning only — **no authoring in this sprint**  

---

## 1. Purpose

Define **wave planning** for Knowledge Population: ordered batches of catalog units that move through the population workflow together.

Waves implement EPIC 2 Phases without creating content yet.

---

## 2. Wave principles

| Principle | Detail |
|-----------|--------|
| Catalog-bound | Every wave item is a `16` KU id |
| Risk pairs | RK+MT always same wave |
| P0 first | No P2 before P0 exit without Architect exception |
| Narrative-first | Early waves unlock Exec/Rec/Warning |
| Exit gates | Wave not done until `03` QG-Wave Pass |
| No engine scope | Waves are content+review only |

---

## 3. Phase ↔ Wave map

| Phase (EPIC 2 `20`) | Waves | Catalog scope |
|---------------------|-------|---------------|
| Phase 1 Foundation | W-P0-1.1 … W-P0-1.5 | P0 (~42) |
| Phase 2 Depth | W-P1-2.1 … W-P1-2.n | P1 (~48) |
| Phase 3 Sensitive | W-P2-3.1 … W-P2-3.n | P2 (~36) |

---

## 4. Phase 1 waves (detailed)

### W-P0-1.1 — Identity & observation

| Attribute | Plan |
|-----------|------|
| **Units** | KU-AN-ID-000001…000008; KU-AN-XX-000001 |
| **Unlock** | Exec identity, Observation, Conclusion settle |
| **Exit** | All Published; Narrative Review Pass on identity pack |

### W-P0-1.2 — Decision actions

| Attribute | Plan |
|-----------|------|
| **Units** | KU-AC-DM-000001…000007 |
| **Unlock** | Recommendation postures (Wait/Prepare/Advance/Protect/Reassess) |
| **Exit** | All Published; posture vocabulary consistent |

### W-P0-1.3 — Structural risk pairs

| Attribute | Plan |
|-----------|------|
| **Units** | KU-RK/MT-XX-000001…000004 |
| **Unlock** | Warning + mitigation for default/LT/MD |
| **Exit** | Pair integrity 100%; Warning CQ spot-check |

### W-P0-1.4 — Luck & practical

| Attribute | Plan |
|-----------|------|
| **Units** | KU-CN-LU-000001; KU-AC-LU-000001; KU-OP-LU-000001; KU-PG-XX-000001; KU-PG-LS-000001; KU-ST-PG-000001; KU-OP-XX-000001 |
| **Unlock** | Timing + practical guidance |
| **Exit** | CS-LT light profile satisfiable |

### W-P0-1.5 — Impact & career light + remaining P0

| Attribute | Plan |
|-----------|------|
| **Units** | KU-CN-XX-000001; KU-CN-CA-000001; KU-AC-CA-000001; KU-CN-PE-000001; KU-AN-XX-000002/000003; any remaining P0 from `16` |
| **Unlock** | Minimum Narrative pack complete (`19` §7) |
| **Exit** | **Phase 1 exit criteria** (`20`): P0 Published; sample insufficient rate expectation documented |

---

## 5. Phase 2 waves (outline)

| Wave | Focus | Example unit families |
|------|-------|------------------------|
| W-P1-2.1 | Career change / promotion | CA/LE RK-MT-AC-OP |
| W-P1-2.2 | Finance / investment / property | FI RK-MT-AC-CN-PG |
| W-P1-2.3 | Business / startup / entrepreneurship | BU RK-MT-AC-OP-ST |
| W-P1-2.4 | Luck depth / education / growth | LU/ED/PG |
| W-P1-2.5 | Relocation + curated shensha | EN + XX shensha pairs |

Exact id lists = remaining P1 rows in `16`. Wave lead splits for parallel owners.

**Phase 2 exit:** Domain Required sets for CA/FI/BU/LE/ED/PG/EN per `17`.

---

## 6. Phase 3 waves (outline)

| Wave | Focus | Notes |
|------|-------|-------|
| W-P2-3.1 | Marriage / dating | Ethics-mandatory |
| W-P2-3.2 | Children / parents | Ethics-mandatory |
| W-P2-3.3 | Health lifestyle | Non-medical gate |
| W-P2-3.4 | Environment / travel / retirement | Adjacent |
| W-P2-3.5 | Knowledge Panel + low-CV depth | Glossary / special |

**Phase 3 exit:** ≥85% of 126 planned Published; ethics sign-off; re-audit.

---

## 7. Wave execution checklist (each wave)

### Start

- [ ] Framework + content sprint authorized  
- [ ] Wave id assigned; owner named  
- [ ] Unit id list frozen from catalog  
- [ ] Reviewers booked (Tech/Know/Comm/Narr)  
- [ ] Pair list verified  

### During

- [ ] Authors follow `01` workflow  
- [ ] Reviews recorded per `02`  
- [ ] Validation HF clean per `03`  
- [ ] Versions per `04`  

### Exit

- [ ] QG-Wave Pass  
- [ ] Publish manifest updated  
- [ ] Wave exit report filed  
- [ ] Next wave go/no-go  

---

## 8. Staffing model (indicative)

| Role | Phase 1 need |
|------|----------------|
| Authors | 1–3 parallel tracks (AN / AC / RK-MT) |
| Technical Reviewer | Shared |
| Knowledge Reviewer | Shared |
| Commercial Reviewer | Shared |
| Narrative Reviewer | Shared (critical on 1.1–1.3) |
| Ops / Wave lead | 1 |

Sizing finalized at content kickoff — not in this sprint.

---

## 9. Tracking metrics

| Metric | Track per wave |
|--------|----------------|
| Planned vs Published count | |
| Days in each review stage | |
| Fail/rework rate | |
| Open HF/SF counts | |
| Pair integrity % | |
| Narrative CQ spot-check Pass % | |

---

## 10. Explicit non-starts

Until this Sprint A framework is approved **and** a content sprint is authorized:

- Do not start W-P0-1.1 authoring  
- Do not create CSV/JSON bodies  
- Do not Publish anything  
- Do not wire runtime “because wave planning exists”  

---

## 11. Stop line

Wave execution plan complete.

**EPIC 3 Sprint A complete.**  
Wait for review.  
**No Knowledge Units. No database population. No implementation.**

---

END
