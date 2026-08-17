# Interaction Truth Boundaries

Version: 1.0  
Status: SPECIFICATION  
Issue: B1-P0-002

---

## 1. What Interaction Truth owns

Only **interaction facts**.

That means:

- Period identity references copied from LuckEngine
- Natal governor references copied from natal engines
- Evidenced relations between those references
- Classification of those relations as helpful, pressure, supported, or restricted
- Confidence and evidence for those relations
- Diagnostics when a required input is missing

It owns the **relation record**.

It does not own either side of the relation.

---

## 2. What Interaction Truth must not own

| Domain | Owner | Interaction Truth must not |
|--------|-------|----------------------------|
| Strength | StrengthEngine | Reclassify strong / balanced / weak |
| Pattern | PatternEngine | Reselect or relabel the pattern |
| Useful God | UsefulGodEngine | Reselect Dụng / Hỷ / Kỵ or change entity type |
| Ten Gods | TenGodsEngine | Rebuild natal positions |
| Shen Sha | ShenShaService | Add or drop natal stars |
| Temperature | TemperatureEngine | Recompute climate |
| Five Elements | RuleContext.wuxing | Recount natal wuxing |
| Luck calculation | LuckEngine | Compute Da Yun sequence, ages, stems, branches, hidden stems, period ten-god |
| Knowledge | Knowledge System | Author expert meaning of stems, roles, patterns, or stars |
| Narrative | Narrative Composer / Publisher | Write customer paragraphs |
| Report | Report / edition publisher | Choose Executive vs Professional pages |
| Score | ScoreEngine | Use totals as interaction evidence |
| Identity / story | — does not exist | Invent persona, life-state, or plot |

If a value needs to change, the owning engine or layer changes it.

Interaction Truth only rereads.

---

## 3. Hard separations

### 3.1 Natal Truth ≠ Interaction Truth

Natal Truth answers: what is this chart.

Interaction Truth answers: how this living decade meets this chart.

A natal fact remains natal even when the customer is living a decade.

### 3.2 Luck identity ≠ Luck interpretation

LuckEngine may already publish the current pillar’s stem, branch, element, ten-god, and hidden stems.

Those are **identity facts**.

Using them as references is allowed.

Building a Luck Domain, scoring the decade, or interpreting all ten cycles is not allowed in this spec.

### 3.3 Knowledge ≠ Interaction

Knowledge explains what `Thực Thần` or `Đinh` means.

It does not decide whether the current Da Yun overlaps that key.

### 3.4 Narrative ≠ Interaction

Narrative may say:

> In Ất Tỵ, no published period token overlaps natal Hỷ.

only if that Interaction Fact exists.

Narrative may not create the overlap by wording.

---

## 4. Allowed copy vs forbidden invention

| Action | Allowed? |
|--------|----------|
| Copy current `gan_zhi`, years, stem, branch from LuckEngine | Yes |
| Copy natal Useful God, Hỷ, Kỵ, Pattern, Strength | Yes |
| Record that a copied period token is the same published identity as a natal token | Yes — this is an interaction fact |
| Record that no such identity overlap exists | Yes — empty overlap is a fact |
| Record that natal Useful God still governs because LuckEngine does not reselect it | Yes — `natal_governor_in_force` |
| Prefix natal thesis with the decade name | No — that is copied natal truth |
| Derive a new Useful God for the decade | No |
| Derive a new Strength for the decade | No |
| Compute a new five-element balance from the luck pillar | No |
| Use ScoreEngine as climate or luck | No |
| Fill helpful factors with natal Hỷ because Hỷ exists | No — that is natal, not period overlap |

---

## 5. Scope of the current life period

In this specification, **current life period** means:

- the already-selected **current Da Yun**
- plus its already-published identity fields
- plus the already-published next-cycle **label** as a non-current marker

It does not mean:

- Liu Nian
- Liu Yue
- Liu Ri
- a life-stage engine (child / adult / elder)
- a career-phase engine
- the full ten-cycle story

---

## 6. Failure boundary

If Current Luck Facts are missing, Interaction Truth status is `MISSING`.

If natal governors are missing, Interaction Truth status is `PARTIAL` or `MISSING` according to `INTERACTION_FACTS.md`.

If period identity exists but no evidenced overlap exists, status may be `AVAILABLE` with empty helpful/pressure lists.

Narrative then:

- may name the decade
- may state that natal governors remain in force
- must not claim that the decade helps or pressures specific natal factors

That refusal is correct.

Inventing overlap is not.
