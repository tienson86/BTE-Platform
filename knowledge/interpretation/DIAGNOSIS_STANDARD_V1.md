# DIAGNOSIS_STANDARD_V1.md

| Field | Value |
|-------|-------|
| **Title** | BTE Diagnosis Standard |
| **Document ID** | `DS-V1` |
| **File** | `knowledge/interpretation/DIAGNOSIS_STANDARD_V1.md` |
| **Version** | `1.0.0` |
| **Status** | **Canonical / Normative** |
| **Date** | 2026-08-18 |
| **Owner** | Interpretation Architecture + Product Owner |
| **Audience** | Domain experts · Narrative · Editorial · Knowledge QA · AI agents · Human review |
| **Runtime** | None |
| **Code** | None |

---

# 0. What this document is

This is the canonical Diagnosis Standard of BTE.

It defines **what a diagnosis is**, **what it may answer**, and **what it must refuse**.

Diagnosis is the clinical reading of already-published analytical truth.

It is the bridge between analysis and life guidance.

```text
Analytical Truth
        ↓
Evidence
        ↓
Reasoning
        ↓
Life Strategy
        ↓
Narrative
```

Diagnosis sits on this bridge.

It does not calculate.

It does not compose customer prose.

It does not format a report.

It does not create a new engine.

---

## What this document is not

This standard is not:

- a software specification
- a runtime
- an engine
- a Report section catalogue
- a Narrative composer
- a Knowledge Asset
- a Rule Database
- a UI redesign
- customer-facing copy

It does not authorize:

- a Diagnosis Engine
- a Life State Engine
- a Story Engine
- a second Composer
- a second Analytical Truth owner
- a second Interaction Truth owner

Existing architecture remains the only architecture.

---

# 1. Purpose

BTE exists to turn structured BaZi analysis into understanding, then into action.

Analytical engines publish **what is true**.

Evidence records **what may be cited**.

Reasoning records **why a conclusion holds**.

Life Strategy records **how to live with that conclusion**.

Narrative speaks to **one paying customer**.

Diagnosis is the missing clinical contract among those layers.

Without Diagnosis, Narrative dumps evidence.

Without Diagnosis, Life Strategy becomes generic advice.

Without Diagnosis, Reasoning has no governing question.

A complete diagnosis answers only five questions.

Everything else is Evidence.

---

# 2. Place in existing architecture

This standard uses only frozen BTE layers.

It does not insert a new pipeline stage into runtime.

It names the **clinical obligation** that those layers already imply.

## 2.1 Frozen truth flow

From `beta/BETA0_ANALYTICAL_TRUTH_LOCK.md`:

```text
Calendar
    ↓
BaZi
    ↓
Score / Strength / Temperature / Pattern / Ten Gods
    ↓
Useful God
    ↓
Luck
    ↓
Interpretation Foundation
    ↓
Narrative (copy, do not calculate)
```

Analytical truth is calculated once, upstream.

Diagnosis may only read that truth.

Diagnosis may not recalculate astrology.

## 2.2 Frozen knowledge flow

From `knowledge/interpretation/KNOWLEDGE_ARCHITECTURE.md` and `knowledge/interpretation/README.md`:

```text
Engine Truth
    ↓
Canonical Facts
    ↓
Decision Explanation
    ↓
Concept Layer
    ↓
BaZi Knowledge
    ↓
Narrative
    ↓
Report
```

Diagnosis consumes Canonical Facts, Decision Explanation, and Concept meaning.

It does not replace Knowledge.

It does not replace Narrative.

## 2.3 Frozen narrative flow

From `beta/BETA0_NARRATIVE_LOCK.md`:

```text
Decision
    ↓
State
    ↓
Relationship
    ↓
Knowledge
    ↓
Narrative Composer
    ↓
Published Narrative
    ↓
Professional Publisher
    ↓
PDF
```

Diagnosis is an input obligation for Composer and Publisher.

It is not a second composer.

PDF remains format, not diagnosis.

## 2.4 Canonical diagnosis bridge

```text
Analytical Truth          existing engine owners
        ↓
Evidence                  typed, published, citable facts
        ↓
Reasoning                 why those facts justify a conclusion
        ↓
Diagnosis                 this standard — five questions only
        ↓
Life Strategy             how to live with the diagnosis
        ↓
Narrative                 customer prose under Editorial Standard
```

Evidence and Reasoning precede Diagnosis because Diagnosis may not invent missing facts.

Life Strategy and Narrative follow Diagnosis because they may not diagnose a second time.

---

# 3. Definition

**Diagnosis** is the structured clinical synthesis of published Analytical Truth into five governing answers.

It answers:

```text
What imbalance governs this life, what corrects it,
whether the living decade helps that correction,
and what repeats if the person does not change.
```

It does not answer:

- What every engine calculated
- What the knowledge library contains
- How lucky the decade is in general
- What events will happen
- Who the person is as a catalogue of gods
- What sentence the customer should read

Those belong to Evidence, Knowledge, Interaction Truth, Editorial, or Narrative.

---

# 4. The five questions

Diagnosis must answer **only** these questions.

The questions are ordered.

Later answers depend on earlier answers.

A later answer may not rewrite an earlier owner.

| # | Question | Clinical job |
|---|---------|--------------|
| 1 | What is excessive? | Name the governing surplus |
| 2 | What is lacking? | Name the governing deficit |
| 3 | What is Useful God correcting? | Name the selected correction function |
| 4 | Is the current Da Yun helping the correction? | Name whether this living decade helps that correction |
| 5 | If nothing changes, what repeats? | Name the natal operating loop that continues |

These five answers are the diagnosis.

They are one reading.

They are not five encyclopedias.

---

# 5. Ownership

Diagnosis has **no new analytical owner**.

It reads existing owners. It does not become them.

| Object | Existing owner | Diagnosis may | Diagnosis must not |
|--------|----------------|---------------|--------------------|
| Calendar / pillars | Calendar Engine · BaZi Engine | Cite as Evidence | Recalculate pillars |
| Day Master | BaZi Engine | Use as identity frame | Invent a second Day Master |
| Strength | Strength Engine | Read surplus / deficit class | Reclassify strength |
| Temperature | Temperature Engine | Read climate imbalance | Recompute climate |
| Five Elements | Score Engine / published wuxing facts | Read dominant / missing counts already published | Invent a new Wuxing engine |
| Pattern | Pattern Engine | Read selected pattern as governing form | Reselect or tournament patterns |
| Ten Gods | Ten Gods Engine | Read published role concentration or absence | Catalogue Ten Gods into diagnosis |
| Useful God / Hỷ / Kỵ | Useful God Engine | Read selected Yong / Xi / Ji | Reselect Dụng / Hỷ / Kỵ |
| Current Da Yun identity | Luck Engine | Read already-selected current cycle | Compute sequence, ages, or all ten cycles |
| Period × natal relation | Interaction Truth | Read helpful / pressure / supported / restricted | Invent overlap by wording |
| Concept meaning | Interpretation Concept Layer | Use approved correction concepts | Invent a new concept family |
| Expert meaning | BaZi Knowledge System | Use meaning of already-selected keys | Author a new canon |
| Evidence graph | Narrative Composer V2 Evidence · Evidence Standard | Require published evidence | Infer unpublished facts |
| Reasoning path | Reasoning Framework · Reasoning component | Require a why-chain | Run Rule Engine again |
| Life Strategy | Commercial Knowledge kind `ST` · Recommendation / Warning | Feed the five answers | Become a second diagnosis |
| Customer prose | Narrative Composer · Editorial Standard | Supply the clinical answers | Write paragraphs |
| Report pages | Report Engine · Professional Publisher | Be represented | Choose edition layout |
| Score totals / grades | Score Engine | Never use as diagnosis | Treat grade as imbalance |

One owner per truth remains frozen.

Orchestration may sequence results.

Orchestration may not become a second source of truth.

---

# 6. Inputs

Use only facts that are already published.

Absence of evidence is not negative evidence.

If a required input is missing, that diagnosis question is **Unavailable**.

It is not guessed.

## 6.1 Analytical Truth required when present

| Input | Already owned by | Used by question |
|-------|------------------|------------------|
| Day Master | BaZi Engine | 1, 2, 3, 5 |
| Strength class / label | Strength Engine | 1, 2, 3, 5 |
| Temperature class / label | Temperature Engine | 1, 2, 3 |
| Published five-element dominant / missing | Score / published wuxing facts | 1, 2 |
| Selected Pattern | Pattern Engine | 1, 2, 3, 5 |
| Selected Useful God, Hỷ, Kỵ | Useful God Engine | 3, 4, 5 |
| Published Ten God positions / visible roles | Ten Gods Engine | Evidence for 1, 2; not a catalogue |
| Current Da Yun identity | Luck Engine | 4 |
| Interaction Facts | Interaction Truth | 4 |

## 6.2 Reasoning required when present

From `knowledge/reasoning/REASONING_FRAMEWORK.md` and Pack 05 Reasoning:

```text
Observation → Evidence → Inference → Intermediate → Final
```

Diagnosis Q1–Q3 must be justifiable by that path.

If Reasoning is Insufficient Evidence, Diagnosis may not invent the missing why.

## 6.3 Inputs that must not be used as diagnosis

| Input | Reason |
|-------|--------|
| Score totals / grades | Score is not Analytical Truth for diagnosis |
| Unused Useful God candidates | Candidate tournaments are Evidence, not diagnosis |
| All ten Da Yun cycles | Professional diagnosis uses the current living decade only |
| Liu Nian / Liu Yue / Liu Ri | Out of scope for this standard’s Q4 |
| Shen Sha matched-name lists | Evidence; not governing imbalance unless already selected as a natal governor |
| Glossary / encyclopedia units | Knowledge library content is not diagnosis |
| Narrative thesis / cover class | Downstream; using them as diagnosis is circular |
| Confidence numbers | QA / engine metadata, not clinical answers |
| Unpublished luck interaction | Luck interaction must be published — not inferred |

---

# 7. The Evidence remainder

**Everything that is not one of the five answers is Evidence.**

Evidence is necessary.

Evidence is not diagnosis.

From existing Evidence architecture:

- Evidence does not compose paragraphs.
- Evidence does not invent facts.
- Evidence does not decide the governing reading.
- Absence of evidence is not negative evidence.

## 7.1 What remains Evidence

The following stay Evidence unless they directly answer one of the five questions:

- Four Pillars as listed structure
- Hidden stems as inventory
- Ten Gods as a role catalogue
- Shen Sha as a matched-name list
- Five-element counts as a table
- Strength numeric score
- Temperature internal dumps
- Pattern candidates not selected
- Useful God candidates not selected
- Hỷ / Kỵ lists used as catalogues rather than correction support / opposition
- Ten Da Yun identities
- Next-cycle label except as a non-current marker
- Rule ids, matched-rule lists, confidence
- Knowledge definitions of unused keys
- Commercial extras that do not change Q1–Q5

These may support Reasoning.

They may appear in Appendix, Professional evidence panels, or unpublished truth.

They must not be presented as the diagnosis.

## 7.2 Evidence vs Diagnosis

| Test | Evidence | Diagnosis |
|------|----------|-----------|
| Can it be listed without changing the reading? | Yes | No |
| Does removing it leave the five answers intact? | Then it is Evidence | Then it was not Diagnosis |
| Does it answer Q1–Q5? | No | Yes |
| May Narrative print it in Executive Summary as the briefing? | No | Yes, under Editorial Standard |

Unpublished truth is allowed.

Unread diagnosis is a product failure.

Dumped evidence is also a product failure.

---

# 8. Question contracts

Each question has one job.

Each question has existing sources.

Each question has a refusal.

## 8.1 Q1 — What is excessive?

### Job

Name the **governing surplus**.

Not every surplus.

The surplus that actually leans this chart.

### Existing sources

Read, do not recompute:

- Strength surplus / strong standing
- Temperature hot / dry excess when published
- Published dominant five-element fact
- Selected Pattern when it concentrates one force
- Kỵ / Ji Shen as the unfavorable excess direction **after** Useful God is selected
- Approved concepts such as `control_excess` and `drain_strong_day_master`

### Synthesis rule

Pattern, Strength, and climate may describe the same surplus.

Diagnosis states **one governing excess**.

Supporting excesses remain Evidence.

### Refusal

- Do not list every strong Ten God.
- Do not treat a high score as excess.
- Do not call Kỵ “excessive” before Useful God is selected.
- Do not invent excess from missing data.

### Unavailable

If Strength, Pattern, Temperature, and published wuxing surplus facts are all missing, Q1 is Unavailable.

---

## 8.2 Q2 — What is lacking?

### Job

Name the **governing deficit**.

Not every absence.

The lack that the correction must feed, drain toward, warm, cool, or restore.

### Existing sources

Read, do not recompute:

- Strength deficit / weak standing
- Temperature cold / damp lack when published
- Published missing five-element fact
- Selected Pattern when it starves one needed function
- The support direction implied by selected Useful God / Hỷ
- Approved concepts such as `generate_support`, `cooling_hot_chart`, `moistening_dry_chart`, `strength_balance`

### Synthesis rule

Q2 is the counterpart of Q1.

If the chart is strong, the lack is often a usable outlet, not more force.

If the chart is weak, the lack is often support, not more drain.

Diagnosis states **one governing lack**.

A missing Ten God role may support this answer only when that absence is already published and already relevant to the selected correction.

Absence of a catalogue entry is not a lack.

### Refusal

- Do not treat unpublished facts as “lacking”.
- Do not inventory unused stems as deficits.
- Do not say the person lacks a god because the library has more gods.
- Do not invert Q1 into a generic “needs balance”.

### Unavailable

If no published deficit, missing-element, climate lack, or selected Useful God support-direction exists, Q2 is Unavailable.

---

## 8.3 Q3 — What is Useful God correcting?

### Job

Name the **selected correction function**.

Not the identity of a stem as a dictionary entry.

Not a hypothetical Useful God.

### Existing sources

Read, do not recompute:

- Useful God Engine: selected Yong Shen (Dụng thần), Hỷ, Kỵ
- Decision Explanation for Useful God
- Concept Layer correction functions already approved:
  - `control_excess` — chế ngự thái quá
  - `drain_strong_day_master` — tiết thân vượng
  - `generate_support` — sinh phù hỗ trợ
  - `cooling_hot_chart` — giảm nhiệt
  - `moistening_dry_chart` — tư nhuận
  - `strength_balance` — thế cân
- Editorial rule: Pattern, Strength, and Useful God must be **one interpretation**, not three labels

### Correction rule

Useful God is the selected answer to Q1 and Q2.

It corrects the governing excess.

It supplies or protects the governing lack.

Hỷ assists that correction.

Kỵ opposes or burdens that correction.

Chou / idle roles remain Evidence.

### Existing prohibition

Supportive luck is **not** Useful God.

Unfavorable luck is **not** a curse.

Useful God is not re-selected by Luck, Report, Narrative, or Diagnosis.

### Refusal

- Do not hold a candidate tournament.
- Do not say “if this unused stem were Useful God”.
- Do not reduce Q3 to a god name with no correction function.
- Do not let Pattern or Strength silently replace Useful God.

### Unavailable

If Useful God is not published, Q3 is Unavailable.

PACK-01 and sibling packs may describe a needed direction only as already-published fact.

They may not name an unpublished Useful God.

If Q3 is Unavailable, Q4 cannot claim that Da Yun helps “the correction”.

---

## 8.4 Q4 — Is the current Da Yun helping the correction?

### Job

Answer **yes / no / mixed / unavailable** against **Q3**, not against general fortune.

The question is not:

```text
Is this a lucky decade?
```

The question is:

```text
Does the already-selected current Da Yun help the already-selected Useful God correction?
```

### Existing sources

Read, do not recompute:

- Luck Engine: already-selected current Da Yun identity
- Interaction Truth: helpful factors, pressure factors, supported direction, restricted direction
- Natal governors remaining in force
- PACK-01 luck picture only when luck facts are published:
  - natal surplus + luck that feeds → overdrive
  - natal surplus + luck that empties → correction, not identity loss
  - natal deficit + luck that feeds → growth window
  - natal deficit + luck that empties → conservation window

### Interaction Truth rule

Prefixing a natal sentence with a Da Yun label is not interaction.

It is not diagnosis of Q4.

Q4 may be answered only from Interaction Facts plus current Da Yun identity.

Empty helpful / pressure lists are valid.

Empty lists mean “no evidenced period overlap”.

They do not mean “copy natal Hỷ / Kỵ onto this decade”.

### Scope of current period

Current life period means:

- the already-selected current Da Yun
- plus already-published identity fields
- plus next-cycle **label** as a non-current marker only

It does not mean Liu Nian, Liu Yue, Liu Ri, all ten cycles, or a life-stage engine.

### Allowed answers

| Answer | When |
|--------|------|
| Helping | Published overlap supports the Useful God correction / supported direction |
| Not helping | Published overlap pressures the correction / restricted direction |
| Mixed | Published facts show both support and pressure on the correction |
| Unavailable | Current Da Yun missing, Interaction Truth `MISSING`, or Q3 Unavailable |

### Refusal

- Do not interpret all ten cycles.
- Do not derive a new Useful God for the decade.
- Do not derive a new Strength for the decade.
- Do not compute new five-element math on the luck pillar.
- Do not use ScoreEngine as luck.
- Do not equate “decade named” with “decade helping”.

### Unavailable

If Current Luck Facts are missing, Q4 is Unavailable.

Narrative may name the decade as a frame.

Narrative must not claim that the decade helps or pressures the correction.

That refusal is correct.

Inventing overlap is not.

---

## 8.5 Q5 — If nothing changes, what repeats?

### Job

Name the **natal operating loop**.

What this life keeps doing if the person keeps feeding the excess, starving the lack, and ignoring the correction.

This is not prophecy.

This is structural repetition.

### Existing sources

Read, do not invent:

- Selected Pattern as the repeating form of life
- Strength standing as the repeating budget of force
- Q1 excess as the habit that overgrows
- Q2 lack as the function that stays starved
- Q3 correction as the unused or opposed medicine
- Q4 only as whether this decade eases or tightens that loop
- Weakness Presentation Standard:
  - Weakness → Risk → Mitigation → Opportunity
  - Risk = what goes wrong **if ignored**
- Editorial Impact / Recommendation / Warning: meaning, first action, what to stop
- Life Strategy knowledge kind `ST` as downstream carrier, not as a second diagnosis

### Repeat rule

The repeat is the same mechanism running again.

Examples of belonging, when already evidenced:

- surplus keeps taking every load
- deficit keeps over-promising then emptying
- Kỵ direction keeps being fed
- Useful God direction keeps being postponed
- a decade that feeds surplus repeats overdrive
- a decade that empties surplus repeats the same identity at a higher price

### Refusal

- Do not predict events, titles, marriages, diagnoses, or wealth outcomes.
- Do not use fear language or absolute prediction.
- Do not treat “nothing changes” as fate.
- Do not invent a persona, plot, or life-state engine.
- Do not reprint Q1–Q4 as four new stories.

Q5 is one loop.

Mitigation and Opportunity belong to Life Strategy after this loop is named.

### Unavailable

If Pattern and Strength are both missing, and no published operating caution exists, Q5 is Unavailable.

Do not fill with generic “keep balance”.

---

# 9. Completeness

A diagnosis is complete only when each of the five questions is either:

- answered from published Analytical Truth, Evidence, Reasoning, and Interaction Truth, or
- explicitly Unavailable with the missing owner named

Partial diagnosis is honest.

Invented completeness is a defect.

## 9.1 One reading

The five answers must not contradict each other.

Q3 must correct Q1 and Q2.

Q4 must judge Q3, not a different Useful God.

Q5 must be the loop of Q1–Q4, not a new chart.

If Pattern, Strength, and Useful God cannot be spoken as one interpretation, Diagnosis is not finished.

## 9.2 Honesty gates

From Interpretation Standard and Evidence Standard:

| Gate | Rule |
|------|------|
| Prefer empty over false | Unavailable beats fabricated surplus, Useful God, or decade help |
| Facts before prose | Narrative cannot precede validated diagnosis inputs |
| No unpublished luck interaction | Q4 requires published Interaction Truth |
| No silent scoring | Confidence is not a sixth diagnosis answer |
| Fail closed | Missing required owner → that question Unavailable |

## 9.3 Product test

A reviewer must be able to retell the diagnosis as:

```text
What is too much.
What is not enough.
What Dụng thần is correcting.
Whether this Đại vận helps that correction.
What repeats if nothing changes.
```

If the reviewer instead recites pillars, god lists, scores, or ten cycles, the artifact is Evidence, not Diagnosis.

This matches the Editorial Standard customer test, but Diagnosis is the clinical content of that test, not the prose.

---

# 10. Downstream layers

Diagnosis does not speak to the customer by itself.

Downstream layers already exist. This standard does not replace them.

## 10.1 Life Strategy

Existing carriers:

- Commercial Knowledge kind `ST` (Life Strategy)
- Recommendation / Warning composition
- Weakness → Risk → Mitigation → Opportunity
- Actionability chain: Published Fact → Interpretation → Action

Life Strategy consumes Diagnosis.

It answers **what to do / protect / stop / wait for**.

It must not:

- reselect Useful God
- reclassify Strength
- invent a luck verdict
- skip Q1–Q5 and jump to generic advice

Understanding precedes recommendation.

Recommendation precedes repetition of the same advice.

If Q5 is named and Life Strategy does not steer against that loop, Life Strategy has failed.

If Life Strategy steers without Q1–Q5, it is not strategy. It is filler.

## 10.2 Narrative

Existing carriers:

- Narrative Composer V2
- Pack 05 component grammar: Observation → Reasoning → Impact → Recommendation → Warning → Conclusion
- Consulting Conversation Model
- Editorial Standard

Narrative copies Diagnosis.

It does not diagnose.

Observation may show the facts behind Q1–Q3.

Reasoning may explain why those answers hold.

Impact / Recommendation / Warning may carry Q5 and Life Strategy.

Executive Summary may brief the five answers in 4–6 sentences.

Narrative may not dump Evidence in place of Diagnosis.

## 10.3 Editorial

Editorial Standard decides:

```text
May this sentence reach a paying customer?
```

Diagnosis Standard decides:

```text
Is this the clinical reading?
```

A sentence may be true Evidence and still fail Diagnosis.

A sentence may be diagnostically correct and still fail Editorial.

Both gates are required for customer publication.

## 10.4 Report

Report Engine and Professional Publisher remain format and edition.

They may present Diagnosis.

They may not become Diagnosis.

Executive and Professional editions may show different Evidence depth.

They must not show two different diagnoses.

---

# 11. Forbidden

Diagnosis V1.0 forbids:

1. Creating a Diagnosis Engine, Story Engine, Case Identity Engine, or Life State Engine
2. Recalculating any Analytical Truth owner
3. Answering a sixth clinical question as if it were Diagnosis
4. Treating Evidence catalogues as Diagnosis
5. Treating Score as imbalance
6. Treating Shen Sha lists as governing surplus or lack
7. Useful God candidate tournaments
8. Hypothetical Useful Gods
9. Claiming current Da Yun helps the correction without Interaction Truth
10. Interpreting all ten Da Yun cycles as Q4
11. Equating luck support with Useful God
12. Event prediction, medical / legal / guaranteed-finance claims
13. Fear, curse, or fate framing of Q5
14. Circular use of Narrative thesis as Analytical Truth
15. Dual calculation of any owner listed in the Analytical Truth Lock

---

# 12. Relationship to existing standards

Higher layers win conflicts of purpose.

This standard wins conflicts of **what counts as diagnosis**.

| Document | Relation |
|----------|----------|
| `knowledge/product/BTE_PRODUCT_MANIFESTO.md` | Purpose: explain before recommending |
| `beta/BETA0_ANALYTICAL_TRUTH_LOCK.md` | Owners of truth; Diagnosis only reads |
| `beta/BETA0_NARRATIVE_LOCK.md` | Composer remains the only customer-sentence composer |
| `docs/architecture/interpretation/01_INTERPRETATION_STANDARD.md` | Completeness of interpretation product |
| `docs/architecture/interpretation/03_NARRATIVE_GUIDE.md` | How Diagnosis may be spoken |
| `knowledge/editorial/BTE_EDITORIAL_STANDARD_V1.md` | Whether a diagnosis sentence may ship |
| `knowledge/knowledge_qa/STANDARD/EVIDENCE_STANDARD.md` | What may be cited |
| `knowledge/reasoning/REASONING_FRAMEWORK.md` | Why-chain required before diagnosis synthesis |
| `knowledge/architecture/pack_05_narrative_engine/02_NARRATIVE_PIPELINE.md` | Evidence → Composer |
| `knowledge/architecture/pack_05_narrative_engine/07_REASONING_COMPONENT.md` | Reasoning explains; does not act |
| `knowledge/architecture/pack_05_narrative_engine/20_CONSULTING_CONVERSATION_MODEL.md` | Conversation order after diagnosis exists |
| `knowledge/interpretation/interaction/INTERACTION_TRUTH_SPEC.md` | Only lawful source for Q4 relation |
| `knowledge/05_useful_god_knowledge/` | Yong / Xi / Ji terminology and selection knowledge |
| `knowledge/09_luck_knowledge/` | Da Yun layer terminology |
| `knowledge/knowledge_improvement/03_WEAKNESS_PRESENTATION_STANDARD.md` | Risk if ignored; Opportunity after mitigation |
| `knowledge/knowledge_enhancement/model/16_KNOWLEDGE_CATALOG.md` | Life Strategy kind `ST` as downstream carrier |
| `knowledge/knowledge_qa/STANDARD/ACTIONABILITY_STANDARD.md` | Life Strategy must steer after diagnosis |

This document does not freeze or unfreeze those documents.

It forbids implementing Diagnosis by bypassing them.

---

# 13. Acceptance

Diagnosis V1.0 is satisfied when:

1. The five questions are the only clinical answers.
2. Each answer traces to an existing owner listed in this standard.
3. Everything else is classified as Evidence.
4. Q3 is the selected Useful God correction of Q1 and Q2.
5. Q4 judges that correction against current Da Yun via Interaction Truth, or is Unavailable.
6. Q5 names the repeating loop, not an event.
7. No new engine, runtime, report, or narrative system was required to hold the standard.
8. Narrative, Life Strategy, Editorial, and Report can consume the five answers without recalculating astrology.

If a deliverable cannot answer the five questions, it is not a BTE diagnosis.

If a deliverable answers more than the five questions as if they were diagnosis, it has collapsed back into Evidence.

---

# 14. Official status

**Diagnosis Standard V1.0 is canonical.**

It is documentation only.

It does not modify runtime.

It does not modify report.

It does not modify engines.

Implementation, if later authorized, must use existing BTE architecture only.

---

END
