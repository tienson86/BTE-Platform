# Foundation Roadmap

| Field | Value |
|-------|-------|
| **Document** | FOUNDATION_ROADMAP |
| **Foundation version** | 1.0.0 |
| **Status** | Canonical |
| **Owner** | BTE Architecture Board |

---

## Standing rule

**Foundation itself remains frozen.**

Phases IV–VI add engines, packages, and (when approved) new catalog entries. They do not reopen Foundation 1.0.0 architecture.

```
Foundation 1.0.0 (frozen)
        ↓
Phase IV — Luck Engine          (extend)
        ↓
Phase V  — Interpretation Engine (extend)
        ↓
Phase VI — Report Engine         (extend)
```

---

## Completed baseline (pre-freeze)

| Phase | Content |
|-------|---------|
| Knowledge | KD-1 … KD-4, Taxonomy, Ontology, Package Spec, Validation, Generator v1.0 |
| Analysis cores | Strength, Seasonal, Temperature, Pattern, Pattern Evaluation |
| Decision cores | Useful God Foundation, Priority, Override |
| Pipelines | AX-1 Analysis 1.0.0, AX-2 Canonical Analysis 2.0.0, AX-3 Canonical Decision 1.0.0 |
| Freeze | F-1 Foundation 1.0.0 |

---

## Phase IV — Luck Engine

**Objective:** Time-cycle analysis (Da Yun / Liu Nian and related luck structures) as a **new engine**, consuming frozen Analysis and Decision published outputs.

In scope:

- New `luck_engine` (or equivalent) public API
- New luck Knowledge / Decision packages (new `package_id`s)
- Optional activation of reserved Luck stages via a **Foundation version bump** if they join a canonical pipeline

Out of scope:

- Editing Strength / Pattern / Useful God sealed packages
- Reordering AX-2 or AX-3 without a Foundation major
- Interpreting or reporting luck in this phase

Foundation remains frozen. Luck is an extension.

---

## Phase V — Interpretation Engine

**Objective:** Narrative / interpretive layer that explains frozen Analysis + Decision (+ Luck if present) without recomputing scores or Useful God.

In scope:

- Interpretation Engine public orchestration
- Interpretation packages bound to published contracts
- Optional reserved Interpretation stage activation (Foundation bump if canonical)

Out of scope:

- Changing `final_useful_god` meaning
- Mixing interpretation text into Rule Engine evaluation
- Report layout / delivery

Foundation remains frozen. Interpretation is an extension.

---

## Phase VI — Report Engine

**Objective:** Format and deliver consultant-grade reports from frozen upstream results.

In scope:

- Report Engine formatting only
- Report templates consuming Canonical Analysis Result + Canonical Decision Result (+ Luck / Interpretation)
- UI remains bound to existing UI Foundation V1.0 (separate freeze)

Out of scope:

- New analytical rules inside Report
- Redesign of Result Page architecture (UI Foundation frozen)
- Mutation of upstream traces

Foundation remains frozen. Report is an extension.

---

## After Phase VI

Future work (schools, languages, AI explainers, plugins) follows `FOUNDATION_EXTENSION_GUIDE.md`.

Any need to change canonical order, schema generation, or checksum rules starts a **new Foundation major** — not an informal patch to 1.0.0.
