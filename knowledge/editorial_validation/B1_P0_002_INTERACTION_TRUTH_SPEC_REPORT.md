# B1_P0_002_INTERACTION_TRUTH_SPEC_REPORT

| Field | Value |
|-------|-------|
| Issue | B1-P0-002 Interaction Truth Specification |
| Date | 2026-08-17 |
| Type | DESIGN |
| Implementation | **NONE** |

---

## Status

**COMPLETE — READY_FOR_IMPLEMENTATION_DESIGN**

Interaction Truth is specified as a facts-only layer between already-published natal / luck identity and Narrative.

No code.

No runtime.

No tests.

No architecture changes.

---

## Purpose

Narrative cannot truthfully explain the **current life period** until a structured record exists of how **Current Da Yun** meets **Natal Truth**.

That record is Interaction Truth.

It is not a new engine.

It is not Knowledge.

It is not Narrative.

---

## Scope

Defined:

- Purpose
- Ownership
- Inputs (already available only)
- Outputs (minimum Interaction Facts)
- Boundaries
- Consumers
- Professional and Executive section responsibility
- Traceability chain
- Validation of real interaction vs natal copy vs duplicated thesis vs filler
- Non-goals

Not defined:

- Algorithms
- Python types
- Runtime wiring
- Luck Domain
- Life State / Story / Identity engines

---

## Ownership

Interaction Truth owns **interaction facts only**.

It does not own Strength, Pattern, Useful God, Ten Gods, Shen Sha, Temperature, Five Elements, luck calculation, Knowledge, or Narrative.

Natal engines remain source of natal values.

LuckEngine remains source of current period identity (label, years, and already-published stem / branch / element / ten-god / hidden stems).

---

## Interaction Facts

Minimum groups:

- Period identity
- Natal governors in force
- Interaction summary (structured, not prose)
- Helpful factors (list; empty allowed)
- Pressure factors (list; empty allowed)
- Supported direction (natal Useful God / Hỷ still in force, with overlap qualifier)
- Restricted direction (natal Kỵ still in force, with overlap qualifier)
- Confidence (completeness, not fortune)
- Evidence (upstream field paths)
- Status / diagnostics

Helpful / pressure require **identity overlap** between published period tokens and published natal tokens.

Natal Hỷ/Kỵ must not be copied into those lists merely because they exist.

Empty overlap is a valid fact.

---

## Consumers

| Consumer | Interaction Facts |
|----------|-------------------|
| Professional `sec-luck` | Required |
| Professional other pages | Optional overlays; `sec-chart` must never show them |
| Executive current-period briefing | Period identity + summary; no thesis paste |
| Career / Finance / Relationship / Health | Optional overlap overlay only |
| Recommendations | Optional now-only actions tied to overlap |
| Conclusion | Optional one period-true fact |

---

## Validation

| Class | Test |
|-------|------|
| Real interaction | Period + natal governor + evidenced relation; claim changes if the decade name is removed, or explicitly records empty overlap |
| Copied natal truth | Natal sentence with a decade prefix; true without the decade name |
| Duplicated thesis | Thesis / career / risk / corrective slots reused as luck |
| Narrative filler | Generic importance, glossary, or padded natal consultation |

B1-P0-001 Professional luck assembly fails this validation: it expands one natal thesis across seven slots.

---

## Non-goals

- Luck Engine redesign
- Life State Engine
- Story Engine
- Identity Engine
- New framework / runtime
- Knowledge content
- Narrative architecture
- Ten-cycle interpretation
- New analytical calculations

---

## Future implementation candidates

Later implementation design may consider, without changing this spec’s boundaries:

1. Copy already-published LuckEngine period identity fields into interpretation luck facts (stem, branch, element, ten-god, hidden stems) — copy only.
2. An Interaction Facts builder that records identity overlap / empty overlap / governors in force.
3. Narrative consumption of those facts for Current Da Yun.
4. Publisher refusal to fill `sec-luck` from natal thesis when Interaction Facts are missing or empty-overlap.

Not candidates:

- Luck Domain interpreter
- Recalculating Useful God for the decade
- Period five-element scoring
- New engines named in Non-goals

---

## Runtime changes

**NONE**

---

## Architecture changes

**NONE**

Specification documents only:

- `knowledge/interpretation/interaction/README.md`
- `knowledge/interpretation/interaction/INTERACTION_TRUTH_SPEC.md`
- `knowledge/interpretation/interaction/INTERACTION_BOUNDARIES.md`
- `knowledge/interpretation/interaction/INTERACTION_FACTS.md`
- `knowledge/interpretation/interaction/INTERACTION_TRACEABILITY.md`
- `knowledge/interpretation/interaction/INTERACTION_VALIDATION.md`

---

## Final verdict

**READY_FOR_IMPLEMENTATION_DESIGN**

STOP.

No code.

No runtime.

No implementation.
