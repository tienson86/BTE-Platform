# Runtime Pipeline — PACK-01 Prototype

| Field | Value |
|-------|-------|
| Document | RUNTIME_PIPELINE |
| Pack | PACK-01 Prototype |
| Version | 1.0.0 |

---

# 1. Purpose

Stage-by-stage run of the prototype.

This is a procedure, not production code.

---

# 2. Stages

```text
S0  Receive Strength Facts
S1  Build Evidence Layer
S2  Map interpretation class
S3  Compute Mode A honesty (confidence, alternatives, missing, conflicts)
S4  Select knowledge units
S5  Apply priority
S6  Resolve conflicts (keep/drop units, never flip class)
S7  Remove duplicates
S8  Compose sentences (Mode B) / assemble audit (Mode A)
S9  Insert transitions
S10 Emit DualModeInterpretation
```

Every stage is deterministic and stateless.

---

# 3. S0 — Receive Strength Facts

Accepted fields (logical):

| Field | Required |
|-------|----------|
| `strength_level` | Yes |
| `strength_score` | If published |
| `season_score` / season evidence | If published |
| `root_score` / root evidence | If published |
| `support_score` / support evidence | If published |
| `drain_score` / drain evidence | If published |
| `control_score` / control evidence | If published |
| other component scores | If published |
| `matched_rules` | If published |
| per-rule reason / group / polarity | If published |
| engine `confidence` | If published |
| engine `reasoning` | If published |

Rejected at the door (not Strength Facts):

- Pattern name
- Useful God
- Temperature class
- Ten Gods lectures
- ShenSha lists
- Gender as a customer token
- Luck, unless published as luck×Day-Master interaction

If a field is absent, S1 records `missing`. S0 does not invent it.

---

# 4. S1 — Evidence Layer

For each present fact, emit an evidence item:

- `evidence_id` (deterministic)
- `dimension`
- `source` (engine field and/or rule id)
- `observed_fact`
- `polarity` (`support` / `weaken` / `neutral` / `override` / `classify`)
- `status` (`present` / `inactive` / `missing` / `not_applicable`)
- `leak_class` (`internal_only` or `meaning_ok`)
- `customer_usable`

Group into: activated rules, supporting factors, weakening factors, component scores, classification source, missing fields, conflicts.

See Interpretation Standard `EVIDENCE_LAYER.md`.

---

# 5. S2 — Map class

| Engine `strength_level` | Interpretation class |
|-------------------------|----------------------|
| `very_strong` | `very_strong` |
| `strong` | `strong` |
| `balanced` | `balanced` |
| `weak` | `weak` |
| `very_weak` | `very_weak` |
| unknown / empty | `unmapped` |

Do not upgrade `strong` → `very_strong`.

Do not downgrade to please an expert label. Expert labels are not S0 input.

---

# 6. S3 — Mode A honesty

Using Evidence Layer + Interpretation Standard:

1. Final conclusion = mapped class
2. Confidence = policy over completeness, agreement, conflict, boundary, missing — engine confidence is an **input**, not a silent copy
3. Alternatives = neighbor class if residual plausibility exists, else `none_plausible`
4. Missing data list
5. Conflict objects

---

# 7. S4 — Select knowledge units

See [KNOWLEDGE_SELECTION.md](KNOWLEDGE_SELECTION.md).

Selector reads:

- mapped class
- present dimensions
- missing dimensions
- conflict flags
- luck present? (CASE-0001: no)

Selector does not read biography.

---

# 8. S5–S7 — Priority, conflict, duplicates

See:

- [PRIORITY_MODEL.md](PRIORITY_MODEL.md)
- [CONFLICT_RESOLUTION.md](CONFLICT_RESOLUTION.md)
- [DUPLICATE_REMOVAL.md](DUPLICATE_REMOVAL.md)

---

# 9. S8 — Compose

Mode A: fill seven audit sections from Evidence Layer + S3. Knowledge units are **not** required for Mode A facts; they may add `why_fired` language only when a cause unit is selected.

Mode B: for each required customer section, take surviving units for that topic, one job per sentence, leak-free.

See [SENTENCE_COMPOSER.md](SENTENCE_COMPOSER.md).

---

# 10. S9 — Transitions

See [TRANSITION_ENGINE.md](TRANSITION_ENGINE.md).

Transitions never add analysis.

---

# 11. S10 — Emit

One DualModeInterpretation object.

Same facts → same object.

See [OUTPUT_SPECIFICATION.md](OUTPUT_SPECIFICATION.md).

---

# 12. Failure

| Condition | Result |
|-----------|--------|
| No `strength_level` | Mode A `unmapped`; Mode B Insufficient Data for all class-dependent sections |
| Empty matched rules | Mode A records empty evidence; Mode B Why may be insufficient if no cause dimensions |
| Luck missing | Luck section Insufficient Data; natal sections continue |
| Selector finds zero meaning units for mapped class | Prototype error — knowledge pack gap, not a guessed class |

Partial fake stories are forbidden.

---

END
