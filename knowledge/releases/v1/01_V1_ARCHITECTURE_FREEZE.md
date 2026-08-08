# 01 — BTE V1 Architecture Freeze

Version: 1.0  
Status: **FROZEN** — Release Candidate A  
Date: 2026-08-08  
Scope: Documentation only (no runtime change)

---

## 1. Purpose

This document freezes the **official BTE V1 architecture**.

From this release forward:

- V1 layers, engines, pipeline order, and ownership are **canonical**.
- Changes that alter frozen boundaries require an explicit architecture review and a new release note.
- Feature work (Narrative Quality, UI Polish, Report Engine redesign) must **not** begin until this freeze is approved.

---

## 2. Official Layers

```
┌─────────────────────────────────────────────────────────────┐
│  Presentation                                                │
│  Portal · Result Page · ViewModels · Adapters                │
├─────────────────────────────────────────────────────────────┤
│  Application                                                 │
│  API · Orchestrator · Serialization · Auth / Cases           │
├─────────────────────────────────────────────────────────────┤
│  Narrative (Pack 05)                                         │
│  Narrative Runtime → NarrativeTree → Composer → NarrativeResult │
├─────────────────────────────────────────────────────────────┤
│  Interpretation (Pack 04)                                    │
│  Interpretation Engine → InterpretationResult                │
├─────────────────────────────────────────────────────────────┤
│  Analysis                                                    │
│  Score · Pattern · Strength · Useful God · Luck · …          │
│  → AnalysisResult / orchestrator payload slices              │
├─────────────────────────────────────────────────────────────┤
│  Chart                                                       │
│  Calendar Engine · BaZi Engine                               │
├─────────────────────────────────────────────────────────────┤
│  Knowledge                                                   │
│  Rule Database (CSV-first) · Knowledge packs                 │
├─────────────────────────────────────────────────────────────┤
│  Foundation (UI) — FROZEN V1.0                               │
│  Product Manifesto → Experience → Brand → Visual → DS        │
└─────────────────────────────────────────────────────────────┘
```

Higher layers consume lower layers through **Public APIs / Result objects** only.  
UI layers must not import engine internals. Engines must not import Portal.

---

## 3. Official Engines (V1)

| Engine | Pack / location | V1 status | Responsibility |
|--------|-----------------|-----------|----------------|
| Calendar Engine | Pack 01 | Active · Frozen contract | Solar/lunar / tiết khí calendar |
| BaZi Engine | Pack 02 | Active · Frozen contract | Chart / pillars / day master |
| Score Engine | Pack 03 | Active · Complete | Analysis scoring → AnalysisResult |
| Interpretation Engine | Pack 04 | Active · Complete | Analysis → InterpretationResult |
| Narrative Engine | Pack 05 (Narrative) | Active · Complete | Tree + NarrativeResult composition |
| Report Engine | Pack 05 (Report docs) / `engines/report_engine` | Active delivery path · **Not redesigned** | Format / markdown delivery (BC) |
| Pattern / Strength / Temperature / Useful God / Luck / Feng Shui / Context | Supporting engines | Active | Feed Analysis / RuleContext |

**One Engine · One Responsibility** remains a V1 principle.

---

## 4. Official Product Pipeline (Commercial Narrative Path)

The **official commercial path** for Result Page prose is:

```
Knowledge / Rule Database
        ↓
Score Engine (+ analysis stages)
        ↓
AnalysisResult (facts)
        ↓
Interpretation Engine
        ↓
InterpretationResult (evidence / sections)
        ↓
Narrative Runtime (D1)
        ↓
NarrativeTree
        ↓
Narrative Composer (D2)
        ↓
NarrativeResult
        ↓
Application API (`data.narrative_result`)
        ↓
Portal Adapter (Canonical Desktop)
        ↓
Result Page ViewModel
        ↓
Result Page UI
```

Full orchestrator stage list is documented in `02_V1_PIPELINE_REFERENCE.md`.

---

## 5. Official Ownership

| Concern | Owner | Must not own |
|---------|-------|--------------|
| Rule data | Rule Database / Loaders | Hard-coded if/else rules in engines |
| Chart facts | Calendar + BaZi | Portal |
| Analytical scores / matches | Score (+ pattern/strength/…) | Narrative / UI |
| Rule prose / section evidence | Interpretation | Portal adapters inventing analysis |
| Commercial consulting narrative | Narrative Engine (Pack 05) | Report Engine scraping Interpretation |
| HTTP / orchestration | Application API | Engine business rules in routes |
| ViewModels / cards | Portal adapters + Result screens | Engine models in React |
| Spacing / type / color / layout patterns | Foundation + Design System | Ad-hoc UI invention |
| Layout Patterns LP-00x Result Page | Foundation / Result architecture | Redesign in feature epics |

---

## 6. Frozen Boundaries

### 6.1 Must not change without architecture review

1. Layer direction (Knowledge → Analysis → Interpretation → Narrative → API → Portal).
2. Public API symbols of Score / Interpretation / Narrative engines (additive wrappers only).
3. Pack 05 NarrativeResult contract (`pack05_narrative_result_v1`) field semantics.
4. Foundation V1.0 documents and Design System packs.
5. Result Page zone architecture (Zones → Rows → Grid → Cards).
6. Database schema stability rules (no silent column renames / deletes).
7. Golden Dataset / snapshot immutability rules.

### 6.2 Explicit non-goals of V1 freeze

- Does **not** freeze Narrative prose quality (known limitation).
- Does **not** freeze Report Engine redesign (future epic).
- Does **not** delete deprecated Portal screens (documented in `07_V1_DEPRECATION_STATUS.md`).
- Does **not** claim OpenAPI field `narrative` equals Pack 05 `narrative_result`.

---

## 7. Architecture Principles (V1)

1. **Stability > Features** when boundaries conflict.  
2. **One Engine · One Responsibility.**  
3. **Result objects** over tuples / ad-hoc dicts at engine boundaries.  
4. **Database First** for business rules; engines read only.  
5. **Public API only** across module boundaries.  
6. **Backward compatibility** — wrap, do not delete.  
7. **Minimal change** — no drive-by refactors across engines.  
8. **Consultant product**, not calculator widget (Brand / Experience).  
9. **NarrativeResult is the official commercial prose source** for Portal Result Page.  
10. **Foundation is frozen** — presentation follows Design System; does not invent tokens.

---

## 8. Future Compatibility Policy

| Change type | Allowed in V1 patch? | Process |
|-------------|----------------------|---------|
| Bug fix inside an engine (no API rename) | Yes | Module tests only; report impact |
| Additive Public API / optional DTO fields | Yes | Document in release notes |
| Rename / remove Public API | No | Wrapper + deprecation window + major note |
| New Pack consuming NarrativeResult | Yes | Follow extension points (`06`) |
| Redesign Result Page layout patterns | No | Architecture review |
| Edit Foundation / Design System content | No | Separate Foundation release |
| Report Engine rewrite to consume NarrativeResult | Future epic | After freeze approval |
| Narrative Quality enrichment | Future epic | After freeze approval |

**Compatibility promise:** Existing `/analyze` consumers that read `interpretation` and delivery `narrative` continue to work. Official new consumers must prefer `narrative_result`.

---

## 9. Related Freeze Documents

| File | Content |
|------|---------|
| `02_V1_PIPELINE_REFERENCE.md` | Stage interfaces |
| `03_V1_MODULE_MAP.md` | Module ownership |
| `04_V1_DEPENDENCY_GRAPH.md` | Dependencies |
| `05_V1_PUBLIC_API.md` | Public surfaces |
| `06_V1_EXTENSION_POINTS.md` | What may grow |
| `07_V1_DEPRECATION_STATUS.md` | Legacy inventory |
| `08_V1_RELEASE_NOTES.md` | V1 summary |

---

## 10. Approval Gate

Release A stops here.

Do **not** begin:

- Narrative Quality  
- UI Polish  
- Report Engine redesign  

until architecture review approves this freeze set.

## Change Control

Any modification affecting:

- public APIs
- production pipeline
- module responsibilities
- architectural boundaries
- engine interactions

must be accompanied by an Architecture Decision Record (ADR).

Minor implementation improvements that do not change architecture do not require an ADR.

---

END
