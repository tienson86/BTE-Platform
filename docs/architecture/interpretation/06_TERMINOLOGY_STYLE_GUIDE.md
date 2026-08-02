# 06 — Terminology Style Guide

| Field | Value |
|-------|--------|
| **Title** | BTE Interpretation System — Official Terminology Style Guide |
| **Document ID** | `ARCH-INT-06` |
| **Version** | `1.0.0` |
| **Status** | **Frozen / Normative** |
| **Owner** | Architecture (Interpretation System) + Domain Editorial |
| **Effective** | 2026-08-02 |

---

## Purpose

This document is the **authoritative lexicon policy** for BTE Interpretation System V1.0.

It defines preferred, discouraged, and forbidden terms, plus professional, educational, and encouraging alternatives.

One concept = one preferred term family. Conflicting synonyms in customer prose create support burden and domain disputes.

---

## Scope

### In scope

- Terminology classes and substitution tables
- Tone-aligned alternatives
- Mapping guidance between classical terms and customer language

### Out of scope

- Section ownership ([02](02_REPORT_SECTION_SPEC.md))
- Narrative length/progression ([03](03_NARRATIVE_GUIDE.md)) — but must obey it
- Sentence ranking ([05](05_SENTENCE_PRIORITY.md))

---

## Audience

Writers, translators, prompt engineers, UI copy authors for interpretation claims, QA linguistic review, domain experts.

---

## Definitions

| Term | Definition |
|------|------------|
| **Preferred term** | Default customer-facing expression |
| **Discouraged term** | Allowed only in Expert/Appendix with definition |
| **Forbidden term** | Must never ship in customer narrative |
| **Professional alternative** | Calm, precise substitute |
| **Educational alternative** | Teaching-oriented substitute |
| **Encouraging alternative** | Supportive without denial of caution |

Canonical architecture terms: [GLOSSARY.md](GLOSSARY.md).

---

## Architecture Notes

```text
Classical / internal label
        │
        ▼
[Terminology Guide mapping]
        │
        ▼
Customer narrative term
```

Internal rule ids and engine enum codes MAY remain technical in logs; customer prose MUST use this guide.

---

## Preferred Terms (core)

| Concept | Preferred (EN) | Preferred (VI guidance) | Notes |
|---------|----------------|-------------------------|-------|
| Day Master | Day Master | Nhật chủ | Not “the person is…” |
| Body Strength | Body Strength / relative strength | Thân vượng / thân nhuợc (as labels) | Pair with soft prose |
| Five Elements | Five Elements | Ngũ hành | |
| Ten Gods | Ten Gods | Thập thần | |
| Pattern | Pattern / structure | Cách cục | |
| Useful God | Useful God | Dụng thần | |
| Helpful God | Helpful / supportive god | Hỷ thần | |
| Unfavorable God | Unfavorable / cautioned direction | Kỵ thần (careful tone) | |
| Luck cycle | Luck cycle | Đại vận / vận hạn (when accurate) | Don’t invent |
| Interpretation | Reading / interpretation | Luận giải | |
| Unavailable | Unavailable / not provided in this result | Chưa có dữ liệu trong kết quả này | Honest empty |

---

## Discouraged Terms

| Discouraged | Why | Prefer instead |
|-------------|-----|----------------|
| “Destiny is sealed” | Absolute | “In this reading framework…” |
| “Good chart / bad chart” | Binary moralizing | Specific structural description |
| “Lucky / unlucky person” | Essentializes person | “More supportive / more demanding phase” |
| Unexplained Sino-classical stacks | Opaque | Define once, then use preferred term |
| Internal rule codes in consumer UI | Leaks internals | Hide or Appendix/Expert only |

---

## Forbidden Terms / phrases

| Forbidden | Replacement direction |
|-----------|----------------------|
| Disaster / catastrophic fate | Potential challenges / additional caution |
| Doomed / cursed | Less supportive in this framework |
| You will die / death predictions | Health should receive greater attention (non-clinical) — or omit health claims |
| Guaranteed rich / bankrupt for sure | No guaranteed financial prediction — use tendency language |
| Disease-as-destiny diagnoses | Omit or non-clinical attention only |
| Racial/gender destiny insults | Never |

Full ban classes: [03_NARRATIVE_GUIDE.md](03_NARRATIVE_GUIDE.md).

---

## Substitution tables

### Severity & evaluation language

| Instead of | Use (Professional) | Use (Educational) | Use (Encouraging) |
|------------|--------------------|-------------------|-------------------|
| Very bad | Needs additional attention | This marker signals imbalance that deserves explanation | There is room to strengthen supportive factors |
| Disaster | Potential challenges | A demanding configuration in classical terms | Challenges can be approached with clearer priorities |
| Failure | Higher level of caution is recommended | Outcomes are not fixed; method emphasizes caution here | Caution supports better decisions |
| Death | Health should receive greater attention | This reading does not diagnose; it only flags attention themes | Prioritizing wellbeing is consistent with a careful reading |
| Hopeless | Limited support in this framework | Useful-god support becomes especially important | Focus on supportive directions still available |
| Terrible luck | More demanding luck phase (if data exists) | Timing markers appear less aligned with useful-god | Demanding phases are for planning awareness |
| Perfect / flawless chart | Strong consistency across markers | Multiple structural signals align | Solid foundation for constructive planning |
| Stupid / weak character | Relative Day Master strength is limited | Strength is a technical BaZi measure, not moral worth | Supportive resources matter more in this structure |

### Guidance language

| Instead of | Use |
|------------|-----|
| You must… (absolute) | It is generally more supportive to… |
| Never do X or ruin your life | X-heavy contexts may warrant caution |
| Guaranteed success if you… | Aligning with useful-god direction is generally more supportive |
| This proves you will marry/divorce | Relationship tendencies in this framework suggest… |

### Classical → customer bridges

| Classical | Customer bridge sentence pattern |
|-----------|----------------------------------|
| Dụng thần | “Useful God (primary supportive direction) …” |
| Hỷ thần | “Helpful God (secondary support) …” |
| Kỵ thần | “Unfavorable direction (caution note) …” |
| Thân vượng | “Day Master assessed as relatively strong …” |
| Thân nhuợc | “Day Master assessed as relatively limited …” |
| Cách cục | “Pattern / structure classification …” |

---

## Professional Alternatives

Use in Overview, Pattern, Summary, Appendix method notes:

- “assessed as”
- “in this framework”
- “analysis indicates”
- “section unavailable because input was not provided”

---

## Educational Alternatives

Use in Body Strength, Five Elements, Ten Gods:

- “In BaZi method, this means…”
- “This relates to Useful God because…”
- “Think of this as a balance signal, not a verdict on character”

---

## Encouraging Alternatives

Use in Recommendations and closings:

- “clearer priorities”
- “supportive environments”
- “planning awareness”
- “constructive focus”

Encouraging ≠ denying Unfavorable God content.

---

## Examples

**Bad:** “This chart is very bad. Disaster and failure are coming. Death energy is strong.”  
**Good:** “Several markers need additional attention. Potential challenges appear around unfavorable directions; higher caution is recommended. Health should receive greater attention as a general theme—this is not a medical diagnosis.”  
**Excellent:** Adds useful-god constructive focus and luck Unavailable honesty if timing data missing.

---

## Best Practices

1. Maintain a shared glossary file for translators derived from this guide.
2. Lint customer prose against forbidden list in CI when narrative packs change.
3. In Expert Mode, classical terms OK if defined on first use.
4. UI labels for tabs should match Preferred Terms where possible.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Translating fear idioms literally | Use substitution table |
| Mixing “Useful God” and random synonyms every paragraph | Stick to preferred term |
| Calling Unavailable “error” to customers | Prefer “not provided in this result” |
| Softening so much that Useful God disappears | Keep precise preferred term |

---

## Future Expansion

- Full VI/EN bilingual normative tables
- Domain-specific micro-glossaries (career, finance) inheriting bans
- Machine-checkable term graphs for AI prompts

---

## Cross References

- [01](01_INTERPRETATION_STANDARD.md)  
- [02](02_REPORT_SECTION_SPEC.md)  
- [03](03_NARRATIVE_GUIDE.md)  
- [04](04_EXPLANATION_POLICY.md)  
- [05](05_SENTENCE_PRIORITY.md)  
- [GLOSSARY.md](GLOSSARY.md)  

---

## Version

`1.0.0`

## Status

**Frozen — Terminology Policy**

## Review Checklist

- [ ] Preferred terms cover mandatory sections
- [ ] Forbidden list aligned with Narrative Guide ban classes
- [ ] Substitution tables include required examples from milestone brief
- [ ] No conflicting owner definitions vs GLOSSARY
- [ ] CHANGELOG updated on lexicon breaks
