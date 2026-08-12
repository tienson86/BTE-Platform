# Implementation Boundary — FROZEN V1.0

| Field | Value |
|-------|-------|
| Document | IMPLEMENTATION_BOUNDARY |
| Status | FROZEN |

---

# 1. Production MAY implement

A future engine (not in this task) MAY:

- Read published Strength Facts
- Build Evidence Layer using frozen evidence states (including `INACTIVE`)
- Load official catalog rows
- Apply gate, relevance levels, salience levels, declared duplicates, conflict actions, budget
- Emit `NarrativePlan` + `ClaimTrace` + Mode A diagnostics
- Hand the plan to a Sentence Composer
- Emit Mode B text **only** from the plan
- Test against CASE-0001 golden **plan shape**

---

# 2. Production MUST NOT

- Recalculate Strength class or scores
- Change Rule Database
- Change Interpretation Standard / Knowledge prose to fit a nicer story
- Change this freeze
- Change CASE-0001 golden plan
- Invent luck, hidden stems, or drain leak
- Use LLM inside reasoning
- Discover duplicate clusters at runtime
- Use `MISSING` for drain inactive
- Print reason codes, scores, Rule IDs, confidence % in Customer Mode
- Flip Strong → Balanced for expert taste
- Implement UI / PDF / Report layout as “interpretation”
- Start Pack 02 by forking a different architecture

---

# 3. Not ready until

1. Official catalog **instances** exist for the golden unit ids
2. Composer exists (later) without violating traces
3. Tests lock CASE-0001 plan shape

This freeze package itself does **not** start that work.

---

END
