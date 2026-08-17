# Interaction Facts

Version: 1.0  
Status: SPECIFICATION  
Issue: B1-P0-002

Facts only. Not prose. No algorithms.

---

## 1. Minimum output

Interaction Truth must be able to publish the following fact groups, or explicitly mark them missing.

| Fact group | Required? | Meaning |
|------------|-----------|---------|
| Period identity | Required | Which Da Yun is being lived |
| Natal governors in force | Required when natal facts exist | Chart decisions LuckEngine did not replace |
| Interaction summary | Required | Structured relation record, not a paragraph |
| Helpful factors | Required as a list (may be empty) | Period tokens that overlap natal support |
| Pressure factors | Required as a list (may be empty) | Period tokens that overlap natal restriction |
| Supported direction | Required when Useful God exists | Natal operating direction still in force |
| Restricted direction | Required when Kỵ exists; else empty | Natal restriction still in force |
| Confidence | Required | Completeness of upstream evidence |
| Evidence | Required | Traceable natal + luck field refs |
| Status | Required | `AVAILABLE` / `PARTIAL` / `MISSING` |
| Diagnostics | Required as a list (may be empty) | Missing inputs, empty overlap, unused domains |

No other fact group is required by this spec.

---

## 2. Common field rules

Every Interaction Fact has:

| Field | Rule |
|-------|------|
| `fact_id` | Stable id inside one chart run |
| `kind` | Closed vocabulary in §3 |
| `period_ref` | LuckEngine field + published value, or empty if not applicable |
| `natal_ref` | Natal owner + field + published value, or empty if not applicable |
| `polarity` | `context` / `support` / `restrict` / `helpful` / `pressure` / `none` |
| `evidence_ids` | Upstream field paths only |
| `confidence` | Copied from the weaker upstream confidence, or `unknown` if none |

Values inside `period_ref` and `natal_ref` are **copied identities**.

They are not newly calculated labels.

---

## 3. Closed fact kinds

Do not add kinds without a later specification.

| Kind | What it records | What it is not |
|------|-----------------|----------------|
| `period_identity` | Current Da Yun label, years, optional stem/branch/element/ten-god/hidden stems | A luck reading |
| `next_period_not_current` | Next cycle label exists and is not the living decade | Interpretation of the next decade |
| `natal_governor_in_force` | Pattern, Strength, Useful God, Hỷ, or Kỵ still owned by natal engines | Proof that the decade causes those values |
| `identity_overlap` | The same published token appears on both period and natal sides | A score, a prediction, or a new Useful God |
| `no_identity_overlap` | Compared sides have no shared published identity | A claim that the decade is empty or irrelevant |
| `supported_direction` | Natal Useful God / Hỷ remain the operating direction | A new selected Useful God |
| `restricted_direction` | Natal Kỵ remain the restriction | A new Kỵ list |

`identity_overlap` is allowed only for identities already published on both sides.

Example of a valid overlap: current luck stem `Đinh` equals natal Useful God `Đinh`.

Example of a valid non-overlap: current luck stem `Ất` is not among natal Useful God / Hỷ / Kỵ identities `Thực Thần`, `Thương Quan`, `Tỷ Kiên`, `Kiếp Tài`.

This spec does not define how to infer that `Ất` “supports” `Thực Thần`. That would be new analytical data.

---

## 4. Period identity

Copied from LuckEngine. Not recomputed.

Minimum:

- `gan_zhi`
- `year_start`
- `year_end`
- `is_current = true`

Copy when already published:

- `stem`
- `branch`
- `element`
- `yin_yang`
- `ten_god` (LuckEngine period ten-god vs day master)
- `hidden_stems`
- `age_start` / `age_end`
- `index`
- `direction`

Next cycle:

- `next_gan_zhi` as `next_period_not_current` only

Do not expand the other eight cycles into Interaction Facts.

---

## 5. Natal governors in force

Copy references, do not restamp as period effects.

Minimum governors when each domain is available:

| Governor | Natal source |
|----------|--------------|
| Pattern | `selected` / `label` |
| Strength | `level` / `label` |
| Useful God | `selected` + `selected_entity_type` |
| Hỷ | `favorable_gods` + types |
| Kỵ | `unfavorable_gods` + types |

Optional governors, only if already available and later needed by a consumer:

| Governor | Natal source |
|----------|--------------|
| Ten Gods | visible names / stems |
| Shen Sha | matched names |
| Temperature | `level` / `label` |
| Five Elements | dominant / missing |
| Day Master | stem / element |

Optional governors must not be required to publish Interaction Truth.

If unused, they stay unused. They must not be dumped into the Current Da Yun page “because they exist”.

---

## 6. Interaction summary

Not a sentence.

A structured bundle:

```text
period:           current gan_zhi + years
governors:        pattern, strength, useful god
overlap:          list of identity_overlap facts
no_overlap:       list of no_identity_overlap facts, or a single empty-overlap flag
supported:        useful god + Hỷ references
restricted:       Kỵ references
status:           AVAILABLE | PARTIAL | MISSING
```

The summary is the object Narrative reads first.

If overlap is empty, the summary must still be publishable.

An empty-overlap summary is true.

A natal thesis copied into this object is false.

---

## 7. Helpful factors

A helpful factor is an `identity_overlap` whose natal side is:

- Useful God, or
- Hỷ, or
- another natal token already classified as supportive by its owning engine (not by Interaction Truth)

Each item must carry:

- natal identity
- natal owner
- period identity that matched
- luck field that supplied the period identity
- evidence_ids

The list may be empty.

Natal Hỷ must not be copied into this list merely because Hỷ exists.

---

## 8. Pressure factors

A pressure factor is an `identity_overlap` whose natal side is:

- Kỵ, or
- another natal token already classified as restricting by its owning engine

Same item shape as helpful factors.

The list may be empty.

Natal Kỵ must not be copied into this list merely because Kỵ exists.

---

## 9. Supported direction

This is not a new Useful God.

It is the natal operating direction still in force during the current period:

- Useful God identity + entity type
- Hỷ identities + types

Qualify with overlap status:

| Overlap status | What the fact may say |
|----------------|----------------------|
| One or more helpful overlaps | Natal direction in force **and** period identity overlaps it |
| No overlap | Natal direction in force **without** evidenced period overlap |

The second row is still Interaction Truth.

It is not permission to narrate Hỷ as “this decade’s opportunity”.

---

## 10. Restricted direction

Natal Kỵ identities + types, with the same overlap qualifier as §9.

If Kỵ is unpublished, the list is empty and status notes `ky_missing` only when Useful God is otherwise available.

---

## 11. Confidence

Confidence is completeness, not fortune.

| Value | When |
|-------|------|
| `high` | Period identity present; Pattern, Strength, Useful God present; overlap comparison performed (including empty overlap) |
| `medium` | Period identity present; at least Useful God present; one natal governor missing |
| `low` | Period identity present; natal governors incomplete enough that overlap cannot be classified against Dụng/Hỷ/Kỵ |
| `unknown` | Period identity missing, or Interaction Truth itself missing |

Do not invent a numeric luck score.

Do not reuse ScoreEngine.

---

## 12. Evidence

Every Interaction Fact must point at upstream fields.

Allowed evidence forms:

```text
LuckEngine.current_dayun.gan_zhi
LuckEngine.current_dayun.heavenly_stem
LuckEngine.current_dayun.earthly_branch
LuckEngine.current_dayun.ten_god
LuckEngine.current_dayun.hidden_stems
UsefulGodEngine.selected
UsefulGodEngine.favorable_gods
UsefulGodEngine.unfavorable_gods
PatternEngine.selected
StrengthEngine.level
TenGodsEngine.visible
ShenShaService.matched
TemperatureEngine.level
RuleContext.wuxing.dominant
```

Forbidden evidence forms:

- Narrative thesis title
- Career implication prose
- Knowledge meaning text
- PDF paragraph ids
- Score totals

---

## 13. Status and diagnostics

| Status | Meaning |
|--------|---------|
| `AVAILABLE` | Period identity present; natal Useful God present; overlap comparison recorded (lists may be empty) |
| `PARTIAL` | Period identity present; some natal governors or luck identity fields missing |
| `MISSING` | No current Da Yun identity, so the current life period cannot be explained |

Suggested diagnostic codes (names only, not runtime):

- `current_period_missing`
- `next_period_missing`
- `useful_god_missing`
- `hy_missing`
- `ky_missing`
- `pattern_missing`
- `strength_missing`
- `period_stem_unpublished`
- `period_branch_unpublished`
- `empty_identity_overlap`
- `optional_domain_unused`

Diagnostics are facts about completeness.

They are not customer warnings until Narrative chooses to say so.

---

## 14. What this document does not define

- Matching code
- Token normalization beyond “use published identity strings”
- Weights, scores, deltas
- Dataclasses or Python modules
- How Narrative sentences are written

Those belong to a later implementation-design issue.
