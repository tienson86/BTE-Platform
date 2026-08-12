# Test Strategy

| Field | Value |
|-------|-------|
| Document | TEST_STRATEGY |
| Pack | PACK-01 Strength |
| Version | 1.0.0 |
| Status | DESIGN ONLY |
| Runtime tests | None in this pack |

---

# 1. Purpose

This document defines how a future implementation of PACK-01 will be tested.

It does not implement tests.

It does not modify existing tests.

It does not modify Golden Dataset.

---

# 2. Testing Philosophy

Interpretation tests verify **conversion quality**, not Strength scoring.

Strength Engine tests remain the authority for class correctness.

PACK-01 tests ask:

- Did we explain the published class without changing it?
- Did Mode A contain the seven audit sections?
- Did Mode B contain the nine customer sections?
- Did every customer sentence pass So What, leak ban, and value rules?
- Did missing data stay missing?

---

# 3. What Is Not Tested Here

- Calendar correctness
- BaZi chart construction
- Strength score formulas
- Rule Database content edits
- PDF/DOCX layout
- UI

If a Strength class is wrong, that is a Strength Engine defect.

Interpretation must still explain the published class honestly, or refuse if unmapped.

---

# 4. Test Layers (Future Implementation)

```text
L1  Contract tests          Dual-mode schema / required sections
L2  Leak tests              Customer Mode forbidden tokens
L3  Fidelity tests          Mode B conclusion == Mode A class == engine class
L4  Trace tests             Every activated rule has why_fired
L5  Confidence tests        Numeric + explanation; hidden from Mode B
L6  Alternative tests       Runner-up or none_plausible
L7  Missing-data tests      No invention
L8  Conflict tests          Disagreement is visible in Mode A
L9  Question tests          Five questions answered
L10 Value tests             No duplicate information budget
L11 Sentence tests          So What / dictionary / mega-sentence bans
L12 Luck-interaction tests  Support vs weaken narratives; missing luck
L13 Localization tests      VI/EN meaning lock
L14 Determinism tests       Same input → same DualModeInterpretation
L15 Golden interpretation   Frozen customer+validation fixtures (future; do not edit current golden analysis datasets)
```

---

# 5. Layer Details

## L1 Contract

Assert Mode A shells 1–7 and Mode B shells 1–9 exist.

Empty illegal. Insufficient Data legal.

## L2 Leak

Customer Mode text must not match:

- `STR-` rule IDs
- `%` confidence
- `confidence`
- `strength_score` and sibling score fields
- raw enums as standalone tokens: `male`, `success`, `hot`
- dict-like dumps `{...}`
- engine/pack names

Natural language “Thân Vượng” / “Strong category” is allowed.

A dedicated token `strong` as a raw code dump is not allowed.

## L3 Fidelity

```text
engine.strength_level  →  mapped class
mapped class           →  Mode A Final Conclusion
Mode A Final Conclusion → Mode B Conclusion (same class, different wording)
```

Any rewrite of class fails.

## L4 Trace

For each matched rule ID in the Evidence Layer, a Rule Trace item exists with matched conditions and why_fired.

## L5 Confidence

Mode A has percent + why.

Mode B has neither the number nor the word confidence.

Boundary cases have lower confidence than deep-in-class twins, all else equal.

## L6 Alternative

Near-threshold fixtures must show a neighbor class.

Deep fixtures may be `none_plausible` with a why.

## L7 Missing Data

Fixtures with no hour, no luck, or empty matches:

- Mode A lists the field
- Mode B does not guess
- Luck section insufficient when luck missing

## L8 Conflicts

Season-vs-root fixture:

- Mode A conflict object present
- Mode B does not emit two classes

## L9 Question Framework

Reviewer or automated rubric checks that Why/Meaning/Influence/Do/Avoid are non-empty or explicitly insufficient.

## L10 Value Framework

Duplicate-n-gram / section-swap tests:

If Career paragraph == Leadership paragraph, fail.

If Why paragraph is copied into Meaning, fail.

## L11 Sentence Standard

Fail on dictionary openings (“X means Y”), rule-engine openings (“Kích hoạt khi”), and prophecy (“chắc chắn sẽ”).

## L12 Luck

Four natal×luck polarities from EDGE_CASES must produce distinct Mode B luck paragraphs.

## L13 Localization

VI and EN share class, evidence IDs, and advice meaning.

Only wording changes.

## L14 Determinism

Run twice. Byte-stable or canonical-JSON-stable DualModeInterpretation.

## L15 Golden interpretation

When implementation is authorized, create a **new** interpretation golden set.

Do not edit existing Strength / analysis Golden Dataset to make interpretation tests pass.

---

# 6. Fixtures (Design)

Future fixtures should include at least:

| Fixture | Intent |
|---------|--------|
| Deep Strong, complete data | Clean Mode B, high confidence, none_plausible or tiny alt |
| Boundary Strong/Balanced | Alternative + qualifier |
| Deep Weak | Non-shaming Mode B |
| Very Strong override | Override trace |
| Season vs root conflict | Conflict record |
| Empty matches | Insufficient Data |
| Missing hour | Partial natal OK / luck blocked as applicable |
| Missing luck | Section 7 insufficient |
| Leak-contaminated upstream text | Mode B stripped |
| VI and EN pair | Meaning lock |

Use synthetic or already-published cases.

Do not alter Golden Dataset expected analysis outputs.

---

# 7. Manual Review Gates

Automated tests cannot fully score consulting quality.

Human review still checks:

- So What
- consultant voice
- no shame / no hype
- domain distinctness
- recommendations follow from meaning

A future QC rubric should be binary per checklist item in [ACCEPTANCE_CHECKLIST.md](ACCEPTANCE_CHECKLIST.md).

---

# 8. Module Boundary for Later Pytest

When implementation exists, run only the interpretation-standard / interpretation-engine module tests.

Do not run the full project suite unless requested.

Do not change Strength Engine tests to expect customer prose.

---

# 9. Exit Criteria for a Future Implementation Sprint

Implementation of PACK-01 may be called test-complete when:

- L1–L14 have automated coverage for the fixtures above
- L15 interpretation goldens exist as a new set
- existing Golden Dataset is untouched
- existing Strength Engine tests still own scoring
- remaining failures are listed, not hidden

This pack itself ships **zero** tests, because it ships **zero** code.

---

END
