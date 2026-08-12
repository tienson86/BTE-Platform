# Reasoning Engine Architecture

| Field | Value |
|-------|-------|
| Document | REASONING_ENGINE_ARCHITECTURE |
| Pack | PACK-01 Strength |
| Version | 1.0.0 |
| Status | DESIGN ONLY |

---

# 1. Position

Target production architecture:

```text
Rule Database
      ↓
Strength Engine
      ↓
Published Facts
      ↓
Evidence Layer
      ↓
Interpretation Knowledge Selection     eligibility only
      ↓
Reasoning Engine                       this pack
      ↓
NarrativePlan
      ↓
Sentence Composer
      ↓
Interpretation Result
        ├── Mode A Validation
        └── Mode B Customer
```

The Reasoning Engine consumes **already published** facts and **already selected-as-eligible** (or candidate) knowledge units.

It does not match rules.

It does not compose Vietnamese/English prose.

---

# 2. Split of labor with the selector

| Stage | Job |
|-------|-----|
| Knowledge Selection | Class match, required-fact presence, forbidden conditions → candidate set |
| Reasoning Engine | Rank, budget, duplicate, conflict, confidence language, mode split, order, emphasis |
| Sentence Composer | Render plan into sentences + transition wording |

If a unit is class-wrong or fact-missing, the Evidence Gate rejects it even if the selector leaked it.

---

# 3. The fourteen questions

| # | Question | Primary module |
|---|----------|----------------|
| 1 | Core conclusion unit? | Priority + purpose = CONCLUSION |
| 2 | Why units? | purpose = WHY + reasoning chain |
| 3 | Highest practical value? | Salience + customer_value |
| 4 | Supporting only? | Relevance without salience |
| 5 | Duplicate? | Duplicate reasoning |
| 6 | Conflict? | Conflict reasoning |
| 7 | Insufficient evidence? | Evidence Gate |
| 8 | Hide from Customer Mode? | mode_visibility + confidence + alternative |
| 9 | Say first? | Narrative priority + domain order |
| 10 | Say later? | Same |
| 11 | Warn? | severity + WARNING purpose |
| 12 | Soften language? | Confidence reasoning |
| 13 | `insufficient_data`? | Missing data policy |
| 14 | Keep Alternative Analysis? | Alternative reasoning (default Validation) |

---

# 4. Internal stages (deterministic)

```text
R0  Validate ReasoningInput
R1  Evidence Gate each candidate
R2  Attach RelevanceScore
R3  Attach Salience
R4  Duplicate clustering + representative
R5  Conflict classify (resolve / qualify / defer / expose)
R6  Confidence-aware claim strength
R7  Alternative handling
R8  Missing-data shells
R9  Apply Narrative Budget + compression
R10 Build reasoning chains
R11 Assign narrative positions + transition intents
R12 Build ExecutiveSummaryPlan
R13 Emit NarrativePlan + ClaimTrace + diagnostics
```

No random. No LLM.

---

# 5. Generic reuse

PACK-01 instantiates `subject = strength`.

Later packs change:

- `subject`
- knowledge prefix
- domain catalog extras
- default domain order (optional override)

They keep:

- `ReasoningInput` / `NarrativePlan`
- Evidence Gate states
- Relevance vs Salience
- three priority kinds
- reason codes
- Mode A / Mode B split

---

# 6. Invariants

1. Primary classification comes from input facts, never from knowledge.
2. Mode B claims ⊆ Mode A traces.
3. Absence of data is not negative evidence.
4. Strength score is not Relevance.
5. Rule priority is not narrative priority.
6. More units ≠ better narrative.

---

END
