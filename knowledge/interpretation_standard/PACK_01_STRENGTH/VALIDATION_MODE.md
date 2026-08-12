# Validation Mode (Mode A)

| Field | Value |
|-------|-------|
| Document | VALIDATION_MODE |
| Pack | PACK-01 Strength |
| Audience | Developers, auditors, expert reviewers |
| Customer visibility | Never |
| Version | 1.0.0 |
| Status | DESIGN ONLY |

---

# 1. Purpose

Validation Mode is the complete explainability surface for Strength interpretation.

It exists so a developer or reviewer can answer:

- What did the system conclude?
- Which rules and factors produced that conclusion?
- Why did each rule fire?
- How confident is the conclusion?
- What else could it have been?
- What data is missing?
- Where do rules disagree?

Customers never see this mode.

---

# 2. Position

```text
Evidence Layer
      ↓
Validation Mode
      ↓
Developer audit view / QC / expert review
```

Validation Mode is not a report.

Validation Mode is not a UI layout.

Validation Mode is the audit projection of the same evidence that Customer Mode narrates.

---

# 3. Required Sections

Validation Mode contains exactly these seven sections, in this order.

---

## 3.1 Final Conclusion

The single Strength interpretation class.

Allowed values:

- Very Strong
- Strong
- Balanced
- Weak
- Very Weak

Plus the canonical ID and Vietnamese label.

Example (illustrative, not a runtime template):

```text
Class: Strong
ID: strong
Label VI: Thân Vượng
Source: Strength Engine strength_level mapped without alteration
```

Rules:

- One primary class only.
- Must match Customer Mode conclusion.
- Must not be softened or upgraded for narrative convenience.
- If mapping is impossible because the engine class is unknown, Final Conclusion is `unmapped` and Customer Mode must use Insufficient Data — not a guessed class.

---

## 3.2 Evidence

List every activated strength factor and rule that contributed.

Evidence must be grouped, not dumped as a flat mystery list.

Required groups when data exists:

| Group | Shows |
|-------|-------|
| Activated rules | Rule ID, category, polarity, contribution |
| Supporting factors | Season, root, stems, hidden stems, generation, growth stage, special support |
| Weakening factors | Drain, control, restriction, clash/harm/punishment/void as strength-weakening, special drain |
| Component scores | Season, root, support, drain, control, combination, special, total / normalized |
| Structural facts | Day Master, month command, rooting class, growth stage, Đắc Lệnh / Đắc Địa / Đắc Thế flags when published |
| Unused but relevant | Factors inspected and found inactive |

Every evidence item MUST include:

- `evidence_id`
- `rule_id` when a rule produced it
- `dimension`
- `polarity` (`support` / `weaken` / `neutral` / `override`)
- `observed_fact`
- `why_it_matters` (analytical, not customer prose)
- `score_or_weight` when published
- `present` / `missing`

Never invent an evidence item to fill a group.

If a group has no data, mark the group `missing` or `not_applicable`.

---

## 3.3 Rule Trace

For every activated rule, explain WHY it fired.

See [RULE_TRACE.md](RULE_TRACE.md).

Minimum per rule:

1. Rule ID
2. Rule name / category
3. Matched conditions
4. Chart facts that satisfied those conditions
5. Declared action / contribution
6. Priority class
7. Whether it supports, weakens, or overrides the final class

Inactive candidate rules that almost fired belong in Alternative Analysis or Conflicts, not as fake activations.

---

## 3.4 Confidence

A numeric confidence for the primary class, plus an explanation.

Example shape:

```text
Primary: Strong  92%
Explanation: High because season, root, and stem support agree; no special override; one mild drain remains.
```

See [CONFIDENCE_MODEL.md](CONFIDENCE_MODEL.md).

Confidence is Validation Mode only.

Customer Mode never prints the percentage.

---

## 3.5 Alternative Analysis

Show the next plausible class or classes.

Example shape:

```text
Strong     92%
Balanced    8%
```

Explain why the alternative did not win.

See [ALTERNATIVE_ANALYSIS.md](ALTERNATIVE_ANALYSIS.md).

---

## 3.6 Missing Data

List every runtime field that interpretation wanted and did not receive.

Examples of missing fields (only if actually absent):

- Hour pillar
- True solar time / timezone
- Month branch / season
- Hidden stems
- Luck cycle set
- Temperature result
- Special-exception inputs
- Gender only when a downstream rule requires it — still never leaked to Customer Mode as a raw token

Policy:

- Never invent the missing field.
- Never silently assume a default that changes class.
- If a default is declared by Strength Engine, Validation Mode must show that a default was used.
- Customer Mode may only say that some life-domain advice cannot be given, in natural language, without naming internal fields.

---

## 3.7 Conflicts

If multiple rules or dimensions disagree, show them.

Examples:

- Season supports Strong; roots support Weak.
- Special exception wants an override; ordinary scoring wants Balanced.
- Drain and support are both large, leaving a boundary class.

Each conflict record MUST include:

- Conflicting parties (rule IDs or dimensions)
- What each side claims
- How Strength Engine resolved it (priority / special override / level rule)
- Residual uncertainty after resolution
- Effect on confidence

If there are no conflicts, the section still exists and states `none`.

Silent conflict resolution is forbidden.

---

# 4. Completeness Rule

All seven sections are mandatory shells.

A section may be empty of content only when:

- Missing Data explains why, or
- Conflicts = none, or
- Alternative Analysis has no runner-up because confidence is canonical and no competing class is plausible

“Not generated” is not allowed.

---

# 5. Tone of Validation Mode

Validation Mode is precise, technical, and complete.

It may use:

- Rule IDs
- Scores
- Enums
- Priority values
- Confidence percentages
- Internal field names

It must still be readable by a human auditor.

It must not be a raw Python repr dump without structure.

---

# 6. Forbidden in Validation Mode

Validation Mode must not:

- Rewrite the Strength Engine class
- Hide losing rules
- Drop missing fields
- Mix Customer Mode prose as a substitute for trace
- Claim 100% confidence when data is incomplete or rules conflict

---

# 7. Traceability to Customer Mode

Every Customer Mode paragraph maps to Validation Mode evidence.

Logical link (hidden from customer):

```text
customer.paragraph_id  →  evidence_ids[]  →  rule_ids[]
```

If a customer sentence cannot be linked, it is illegal and must not be emitted in a future implementation.

---

# 8. Strength-Specific Validation Checklist

- [ ] Final class is one of the five canonical classes or explicit unmapped
- [ ] Supporting and weakening factors are both listed when present
- [ ] Season, root, and stem/hidden-stem dimensions are accounted for (present, missing, or not applicable)
- [ ] Special exceptions are shown when activated
- [ ] Component scores are shown when published by the engine
- [ ] Rule Trace covers every activated rule
- [ ] Confidence has a numeric value and a why
- [ ] At least one alternative is shown when the case is near a boundary
- [ ] Missing Data is honest
- [ ] Conflicts are explicit

---

# 9. Example Skeleton (Not Production Output)

```text
PACK-01 STRENGTH — VALIDATION MODE
Case: <case_id>

1. FINAL CONCLUSION
   Strong / Thân Vượng

2. EVIDENCE
   Activated: STR-000001, STR-000007, STR-000012, …
   Support: season command, two roots, peer stem
   Weaken: one drain branch
   Scores: season … root … support … drain … total …

3. RULE TRACE
   STR-000001 fired because month command = prosperous for Day Master
   …

4. CONFIDENCE
   92% — agreement across season + root + stem; mild drain only

5. ALTERNATIVE ANALYSIS
   Strong 92% / Balanced 8%
   Balanced would require treating the drain as equal to root support

6. MISSING DATA
   none | hour pillar | luck set | …

7. CONFLICTS
   none | season vs drain | special vs ordinary | …
```

This skeleton is an audit layout.

It is not Customer Mode.

It is not a UI mock.

---

END
