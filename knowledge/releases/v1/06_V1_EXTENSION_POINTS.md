# 06 — BTE V1 Extension Points

Version: 1.0  
Status: **CANONICAL** — Release Candidate A  
Date: 2026-08-08  
Scope: Documentation only

---

## 1. Purpose

Define what **may** be extended after the V1 architecture freeze, and what **must never change** without a new architecture release.

---

## 2. What Can Be Extended

### 2.1 Rule Database

- Add new rule rows / files following schema rules.  
- Add columns **additively** (never rename/delete existing columns silently).  
- Version database when changes are material.

### 2.2 New analytical engines (behind Score / peers)

- New calculators that publish **new Result objects**.  
- Wire into Orchestrator as a new stage **only** with architecture review.  
- Must not break RuleContext immutability rules.

### 2.3 Interpretation evidence richness

- More matched rules / higher-quality section evidence.  
- New interpreters behind Interpretation Public API.  
- Must continue to feed Narrative as evidence, not as Portal prose authority.

### 2.4 Narrative quality (future epic)

- Better SourceBundle coverage.  
- Richer Pack 05 paragraphs **without** inventing facts.  
- New optional NarrativeResult fields (**additive**).  
- Must keep `compose_narrative_result` as the facade.

### 2.5 Portal presentation

- New cards **inside** existing Result Page zone architecture.  
- Prefer NarrativeResult fields over new scraping.  
- Localization / copy polish that respects Brand Language.  
- Must not invent Design System tokens.

### 2.6 New Packs

Future packs should:

1. Declare input Result object(s).  
2. Declare output Result object.  
3. Depend only **downstream** in the pipeline.  
4. Export a single facade.  
5. Document Public API + tests + architecture pack folder.

### 2.7 Report Engine redesign (future epic)

- Consume **NarrativeResult** as primary commercial input.  
- Keep delivery field BC via wrappers if renaming `narrative`.

### 2.8 API

- Additive JSON fields on `/analyze`.  
- New versioned routes (`/v2/...`) if breaking changes are required.  
- OpenAPI documentation improvements.

---

## 3. What Must Never Change (V1 Freeze)

| Frozen item | Reason |
|-------------|--------|
| Layer direction | Prevents architectural collapse |
| Foundation V1.0 content | Product law |
| Design System structure & tokens as published | Visual consistency |
| Result Page Zones → Rows → Grid → Cards | Analysis Experience |
| Score / Interpretation / Narrative public facade names | BC |
| Pack 05 `contract: pack05_narrative_result_v1` meaning | Portal/API contract |
| Database write prohibition for engines | Integrity |
| Golden Dataset mutation to force green tests | Trust |
| Portal importing engine internals | Boundary |
| Narrative inventing analytical facts | Consultant integrity |
| Replacing NarrativeResult with Interpretation scraping in Portal | Product Integration V1 |

---

## 4. How Future Packs Integrate

### 4.1 Recommended template

```
knowledge/architecture/pack_NN_<name>/
  00_INDEX.md
  01_ARCHITECTURE.md
  02_PIPELINE.md
  03_MODELS.md
  04_PUBLIC_API.md
  …

engines/<name>_engine/
  engine.py
  service.py
  models.py
  …

tests/<name>_engine/
```

### 4.2 Integration checklist

1. Read Foundation + owning upstream pack Public API.  
2. Define Result object (dataclass).  
3. Implement engine facade only.  
4. Wire Orchestrator stage **after** dependencies, **before** dependents.  
5. Publish payload field with `*_source` fingerprint.  
6. If commercial prose: extend Narrative SourceBundle — do **not** bypass Narrative for Portal.  
7. Add module tests; do not edit golden expected outputs to hide bugs.  
8. Update `knowledge/releases/` notes in the next release doc set.

### 4.3 Pack that produces UI copy

```
New analytical facts
        ↓
Interpretation evidence (if needed)
        ↓
NarrativeResult (official prose)
        ↓
API
        ↓
Portal adapters
```

Skipping Narrative for user-facing consulting prose is **not** an approved extension pattern for V1+.

---

## 5. Extension Anti-Patterns

1. Editing Foundation markdown to unlock a UI shortcut.  
2. Adding `if/else` business rules in Portal adapters.  
3. Duplicating Score logic inside Narrative.  
4. Creating a second “official” commercial prose object beside NarrativeResult.  
5. Cross-importing engines “just this once.”  
6. Deleting deprecated APIs without wrappers and a deprecation window.

---

## 6. Compatibility Promise for Extenders

- Additive > breaking.  
- Wrapper > rename.  
- Document > silent behavior change.  
- Architecture review required for pipeline order changes.

---

END
