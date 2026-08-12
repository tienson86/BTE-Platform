# Interpretation Standard

| Field | Value |
|-------|-------|
| Document | INTERPRETATION_STANDARD |
| Pack | PACK-01 Strength (first instance) |
| Scope | Platform-wide interpretation architecture |
| Version | 1.0.0 |
| Status | DESIGN ONLY |
| Runtime | None |

---

# 1. Purpose

This document is the canonical Interpretation Standard for the BTE Platform.

PACK-01 Strength is the first domain that instantiates it.

Every later interpretation domain must reuse this architecture without inventing a parallel model.

---

# 2. Governing Conversion

Interpretation is the conversion of analytical facts into consultant reasoning.

```text
FACTS
  ↓
EVIDENCE
  ↓
REASONING
  ↓
CONCLUSION
  ↓
PRACTICAL ADVICE
```

A system that stops at FACTS has not interpreted.

A system that gives ADVICE without REASONING has not interpreted.

A system that explains a dictionary term instead of this person has not interpreted.

---

# 3. Dual-Mode Architecture

One Evidence Layer.

Two projections.

```text
                    StrengthResult / AnalysisResult
                                │
                                ▼
                         EVIDENCE LAYER
                     (shared, immutable facts)
                                │
              ┌─────────────────┴─────────────────┐
              ▼                                   ▼
     MODE A — VALIDATION                 MODE B — CUSTOMER
     Developer / auditor                 Paying customer
              │                                   │
              ▼                                   ▼
     Validation Interpretation           Customer Interpretation
```

Rules:

1. Mode B may only claim what Mode A can trace.
2. Mode A may never be shown to the customer.
3. Mode B may never leak Mode A internals.
4. If evidence is missing, both modes must say so in their own language. Neither may invent data.

---

# 4. Mode Responsibilities

## Mode A — Validation Mode

Visible only to developers and audit surfaces.

Must contain:

1. Final Conclusion
2. Evidence
3. Rule Trace
4. Confidence
5. Alternative Analysis
6. Missing Data
7. Conflicts

See [VALIDATION_MODE.md](VALIDATION_MODE.md).

## Mode B — Customer Mode

This is the commercial report.

Must contain only:

1. Conclusion
2. Why
3. Meaning
4. Advantages
5. Challenges
6. Influence
7. Influence during Luck Cycles
8. Recommendations
9. Executive Summary

See [CUSTOMER_MODE.md](CUSTOMER_MODE.md).

Customers never see Rule IDs, evidence dumps, internal scores, confidence percentages, or developer information.

---

# 5. Layer Ownership

| Layer | Owns | Must not |
|-------|------|----------|
| Strength Knowledge | What strength evaluation knows | Execute rules |
| Strength Engine | Compute StrengthResult | Write customer prose |
| Evidence Layer | Normalize facts for interpretation | Recalculate scores |
| Mode A | Explainability for humans who audit | Appear in customer report |
| Mode B | Consultant narrative for the customer | Leak internals or invent facts |
| Report Engine | Layout, theme, export | Author interpretation |
| Portal | Presentation | Invent interpretation |

---

# 6. Pipeline Position

```text
BirthRequest
  → Calendar Engine
  → BaZi Engine
  → Strength Engine          ← FACTS (unchanged)
  → (other analytical engines)
  → AnalysisResult
  → Interpretation Standard  ← THIS PACK
        Mode A + Mode B
  → Report Engine / Portal
```

Interpretation consumes published analytical results.

Interpretation never imports reverse.

Interpretation never writes the Rule Database.

---

# 7. Logical Result Contract

Future implementation SHALL produce one dual-mode result per domain.

Logical aggregate (not code):

```text
DualModeInterpretation
├── domain                  e.g. strength
├── version
├── locale
├── evidence                Evidence Layer
├── validation              Mode A
└── customer                Mode B
```

Invariants:

- `validation.final_conclusion` and `customer.conclusion` refer to the same classification.
- Every customer paragraph has at least one evidence reference in Mode A metadata.
- Evidence references are hidden from Mode B text.
- The result is deterministic: same AnalysisResult → same DualModeInterpretation.

---

# 8. Strength Classification Set

PACK-01 uses five canonical interpretation classes.

| ID | English | Vietnamese | Meaning for interpretation |
|----|---------|------------|----------------------------|
| `very_strong` | Very Strong | Thân Cực Vượng | Day Master is strongly over-supported |
| `strong` | Strong | Thân Vượng | Day Master is supported enough to act from surplus |
| `balanced` | Balanced | Trung Hòa | Day Master is near equilibrium |
| `weak` | Weak | Thân Nhược | Day Master lacks sufficient support |
| `very_weak` | Very Weak | Thân Cực Nhược | Day Master is severely under-supported |

These are **interpretation classes**.

They are mapped from Strength Engine output. They are not a new scoring system.

Mapping policy:

1. Prefer the engine’s published `strength_level` when it already matches a class.
2. Intensity (`very_strong` / `very_weak`) is used only when engine evidence supports extremity (special override, extreme score band, or explicit level rule).
3. If the engine publishes only `strong` / `weak` / `balanced`, interpretation MUST NOT invent `very_strong` or `very_weak`.
4. Interpretation NEVER changes the engine class to make a nicer story.

---

# 9. Strength Evidence Dimensions

Mode A must be able to show, when present:

- Season support (Đắc Lệnh / seasonal command)
- Month branch influence
- Root support (Thông Căn / Đắc Địa)
- Visible stem support (Đắc Thế)
- Hidden stem support
- Five-element generation
- Five-element restriction / drain / control
- Growth stage (Trường Sinh cycle contribution)
- Combination / clash / harm / punishment / void influence as strength factors
- Temperature adjustment influence when published upstream
- Special exceptions
- Supporting factors vs weakening factors
- Component scores (Validation Mode only)

Mode B may use the **meaning** of these dimensions in natural language.

Mode B may never name Rule IDs, score fields, or raw enums.

---

# 10. Reusable Architecture for All Future Packs

Every future pack MUST implement the same skeleton.

```text
PACK_XX_<DOMAIN>
├── Mode A
│   ├── Final Conclusion
│   ├── Evidence
│   ├── Rule Trace
│   ├── Confidence
│   ├── Alternative Analysis
│   ├── Missing Data
│   └── Conflicts
└── Mode B
    ├── Conclusion
    ├── Why
    ├── Meaning
    ├── Advantages
    ├── Challenges
    ├── Influence
    ├── Influence during Luck Cycles
    ├── Recommendations
    └── Executive Summary
```

Domain-specific content changes.

Architecture does not.

Examples of domain-specific content:

| Pack | Conclusion example | Must still answer |
|------|--------------------|-------------------|
| Strength | Strong | Why, so what, life effect, do, avoid |
| Pattern | Follow-use structure | Why, so what, life effect, do, avoid |
| Useful God | Wood is the useful direction | Why, so what, life effect, do, avoid |
| Ten Gods | Direct Wealth is prominent | Why, so what, life effect, do, avoid |
| ShenSha | Peach Blossom is active | Why, so what, life effect, do, avoid |

A later pack that outputs only a name has failed this standard.

---

# 11. Mandatory Frameworks

Every interpretation, in every pack, must satisfy:

1. [QUESTION_FRAMEWORK.md](QUESTION_FRAMEWORK.md)
2. [VALUE_FRAMEWORK.md](VALUE_FRAMEWORK.md)
3. [SENTENCE_STANDARD.md](SENTENCE_STANDARD.md)

If a paragraph does not answer a customer question, it is not interpretation.

If a paragraph repeats a previous paragraph, it has no value.

If a sentence cannot survive “So what?”, it must be rewritten or removed.

---

# 12. Honesty Rules

1. Never invent runtime fields.
2. Never hide missing data.
3. Never silently pick a winner when rules conflict.
4. Never present a boundary case as if it were certain.
5. Never use Customer Mode to paper over Validation Mode uncertainty.
6. Never use Validation Mode dumps as Customer Mode text.

---

# 13. Leakage Boundary

Customer Mode MUST NOT contain:

- Rule IDs (`STR-000001`, `STR-018`, …)
- Confidence percentages
- Internal scores (`strength_score`, `season_score`, …)
- Raw runtime tokens (`male`, `strong`, `success`, `hot`)
- Python / JSON dumps (`{'name': '...', 'index': 23}`)
- Engine / pack names
- Developer traces
- Matcher / priority internals

Validation Mode MUST contain those internals when they exist.

The boundary is absolute.

---

# 14. Determinism

Given the same AnalysisResult, locale, and standard version:

- Evidence Layer is identical
- Mode A is identical
- Mode B is identical

Interpretation is stateless.

No hidden model weights.

No free-form AI rewrite that can change meaning.

---

# 15. Localization

Supported commercial languages: Vietnamese, English, then future locales.

Localization changes wording only.

Classification, evidence, and advice meaning remain identical.

Vietnamese is the primary commercial language for V1.

---

# 16. What Implementation Must Not Do Later

When implementation is authorized, it still must not:

- Recalculate Strength
- Read Rule Database inside Customer Mode generation as if it were scoring
- Mix Pattern / Useful God determination into Strength interpretation
- Skip Mode A because “the customer will not see it”
- Generate Mode B from templates that ignore evidence
- Use AI to invent life events, dates, or guarantees

---

# 17. Acceptance of This Standard

This architecture is accepted when:

- Dual-mode split is unambiguous
- Shared Evidence Layer is defined
- Strength classes and mapping policy are defined
- Future-pack reuse contract is defined
- Question, Value, and Sentence frameworks are defined
- No production code has been written for this pack

---

END
