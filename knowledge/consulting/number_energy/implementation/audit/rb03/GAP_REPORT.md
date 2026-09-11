# RB03 — GAP REPORT FOR MISSING FIELDS

**Stage:** RB03  
**Status:** PASS (gap lock only)  
**Freeze:** `NUMBER_ENERGY_STATIC_UI_V1`  
**Primary case:** `0328278786` / `phone_number`  
**Not a spec.** Does not replace Golden Fixture, Presentation, Knowledge 15, or `04_RUNTIME_BINDING_PLAN.md`.

**Sources:**

- `implementation/04_RUNTIME_BINDING_PLAN.md` §12
- `implementation/audit/rb02/MAPPING_REPORT.md`
- `implementation/audit/rb01/0328278786_phone_number.json`
- `implementation/01_GOLDEN_PHONE_FIXTURE.md`
- `knowledge/15_RUNTIME_BINDING_CONTRACT.md`

**Schema checks (not Golden substitutes):** RB01 `0868271327`, `103`

---

## Owner legend

| Owner | Meaning |
|---|---|
| ENGINE | Canonical object/field is not produced by Number Energy runtime. |
| API | Object is not on `POST /api/v1/number-energy/analyze` `data`. |
| ADAPTER | Format/label map only. No spiritual invention. Contract in RB04; code later. |
| CATALOG | Copy already exists in Knowledge; engine must emit **keys**, adapter resolves text. |
| TEST | Existing assertions will block a correct field until a dedicated engine ticket updates tests. |

A gap may have more than one owner. ENGINE without API exposure still cannot bind.

---

## 1. Gap matrix

| ID | Gap | Slots | Live payload | Primary owner | Also | Next ticket |
|---|---|---|---|---|---|---|
| G01 | score `final_score` | P-S00, P-S08 | absent | ENGINE | API, TEST | RB05-E |
| G02 | grade | P-S00, P-S08 | absent | ENGINE | API, TEST | RB05-E |
| G03 | score breakdown 5 rows | P-S08 | absent | ENGINE | API, CATALOG | RB05-E |
| G04 | score_reasons | P-S08 | absent | ENGINE | API, CATALOG | RB05-E |
| G05 | wealth flow 4 stage | P-S03, P-S09 | absent | ENGINE | API, CATALOG | RB05-C |
| G06 | WealthNode | P-S03 | absent | ENGINE | API | RB05-C |
| G07 | NumberEnergyChain | P-S00, P-S02, P-S09 | absent (`dominant`/`ending` only) | ENGINE | API | RB05-B |
| G08 | triple `canonical_meaning_key` | P-S04 | absent | ENGINE | API, CATALOG | RB05-B |
| G09 | triple `customer_summary_key` | P-S04 | absent | ENGINE | API, CATALOG | RB05-B |
| G10 | domain insights 5 domains | P-S06 | absent | ENGINE | API, CATALOG | RB05-D |
| G11 | NumberEnergyFinding | P-S06, P-S07, P-S10 | absent | ENGINE | API | RB05-D |
| G12 | strengths/cautions 4+2 | P-S07 | 4+4 energy blurbs | ENGINE | CATALOG | RB05-D |
| G13 | final assessment | P-S09 | helper summaries | ENGINE | CATALOG | RB05-F |
| G14 | recommendation state | P-S09 | absent | ENGINE | API, CATALOG | RB05-F |
| G15 | basis / evidence_refs | P-S10 | absent | ENGINE | API | RB05-D |
| G16 | grouped display number | P-S00 | ungrouped `0328278786` | ADAPTER | ENGINE optional | RB04 then bind |
| G17 | pair_summary 7 Cát / 1 Hung | P-S02, P-S10 | `supportive_group_count=3` | ENGINE | API | RB05-A |
| G18 | distribution 8 energy + zeros | P-S05 | `groups[]` 4 present only | ENGINE | API | RB05-A |
| G19 | PairOccurrence strength_label / visual tier | P-S01 | `force_label` / `strength_rank` | ENGINE | ADAPTER, CATALOG | RB05-A |
| G20 | verified_by_runtime | P-S00, P-S08, P-S11 | absent | ENGINE | API | RB05-E |
| G21 | `motorbike_plate` vs `motorcycle_plate` | purpose / P-S00 type | not on phone Golden | API | ADAPTER | RB05 API / RB04 alias |

Locked extras from plan §12: `later_outcome` / hậu vận is inside **G05** stage 04.

---

## 2. Per-gap detail

### G01 — score (`final_score`)

- **Impacted slots:** P-S00 Hero score; P-S08 total.
- **Live status:** no `data.score`, no `PhoneScoreResult`. Envelope `data` keys: occurrences, sequence_state, patterns, narrative, warnings, metadata, reading.
- **Why current cannot be used:** nothing to bind. `strength_rank` / `strongest_rank=2` are not scores. `supportive_group_count` is not 82.
- **Owner:** ENGINE + API + TEST.
- **Minimum field:** `PhoneScoreResult.final_score` (0–100 integer). Customer display `{n} / 100`.
- **If skipped:** UI keeps static 82 (honest fixture) **or** invents a client score (FAIL). Do not silently replace 82 without verification state.
- **Next:** RB05-E (after chain + wealth + domains). Bind UI in RB12.

TEST lock (do not change in RB03):

- `tests/number_energy/test_api.py` — `assert "score" not in data`
- `applications/api/tests/test_number_energy.py` — `assert "score" not in data`

Update those tests only inside the engine ticket that adds score.

---

### G02 — grade

- **Slots:** P-S00, P-S08 `TỐT`.
- **Live:** absent. Same tests assert `"grade" not in data`.
- **Why not:** no grade object. Cannot derive from Cát count.
- **Owner:** ENGINE + API + TEST.
- **Minimum:** `PhoneScoreResult.grade` customer label (Golden: `TỐT`).
- **If skipped:** static fixture only; no runtime grade.
- **Next:** RB05-E → RB12.

---

### G03 — score breakdown 5 rows

- **Slots:** P-S08.
- **Golden:** Cấu trúc 21/25, Dòng tài 22/25, Công việc 17/20, Ổn định 10/15, Năng lượng kết 12/15. Sum 82.
- **Live:** absent.
- **Why not:** no component scores. UI must not reverse-engineer 21/25 from pairs.
- **Owner:** ENGINE + API; row labels CATALOG.
- **Minimum:**

      energy_structure_score
      wealth_flow_score
      career_support_score
      stability_risk_score
      tail_score

  each with earned + max, or equivalent named fields matching Knowledge 15 §39.
- **If skipped:** P-S08 cannot leave fixture. Fake bars FAIL.
- **Next:** RB05-E → RB12.

---

### G04 — score_reasons

- **Slots:** P-S08 four reasons.
- **Live:** absent. `narrative.strengths` are energy blurbs, not score reasons.
- **Why not:** score must not drive narrative truth (Knowledge 15 §40). Reasons come after interpret, as summary keys.
- **Owner:** ENGINE + API + CATALOG (`14_PHONE_SCORE_MODEL` / Golden §44–47).
- **Minimum:** `score_reasons[]` of `{ reason_key }` (adapter → title/copy). Golden keys conceptually: cát-structure, wealth-source, career-axis, họa-hại-use.
- **If skipped:** empty reasons or LLM/copy invention FAIL.
- **Next:** RB05-E → RB12.

---

### G05 — wealth flow 4 stage (+ later_outcome)

- **Slots:** P-S03; story reused in P-S09.
- **Golden stages:** 01 Tài vận / 27·86; 02 Tài từ đâu / 827 Sinh Khí→Thiên Y; 03 Tài đi đâu / 278 Thiên Y→Diên Niên; 04 Hậu vận / 786 Diên Niên→Thiên Y.
- **Live:** no wealth object. `reading.triplets` has digits `827`/`278`/`786` without wealth role or catalog copy. `reading.summary` is not Wealth Flow.
- **Why not:** digits ≠ stage narrative. Plan forbids treating `reading.summary` as wealth. UI must not compose stages from Pair Map.
- **Owner:** ENGINE + API + CATALOG (`13_PHONE_WEALTH_FLOW_RULES`).
- **Minimum:** Phone Wealth Flow result:

      wealth_presence
      wealth_sources
      wealth_destinations
      later_outcome
      four customer stages { id, label_key, headline_key, evidence, interaction_key, narrative_key }

- **If skipped:** P-S03 stays fixture, or illegal React derivation. Risk: financial-guarantee wording if copy is invented.
- **Next:** RB05-C → RB09. Blocked until resolver exists.

---

### G06 — WealthNode

- **Slots:** P-S03 evidence (27, 86) and source/destination nodes.
- **Live:** absent. Two Thiên Y pairs exist in `reading.pairs` (27, 86) without node semantics.
- **Why not:** a pair named Thiên Y is not a WealthNode (no source/destination/primary/terminal flags).
- **Owner:** ENGINE + API.
- **Minimum:** `WealthNode[]` per Knowledge 15 §32 (`pair`, `strength`, `position`, `source_energy`, `destination_energy`, `is_primary`, `is_terminal_relevant`, …). Retain **all** Thiên Y nodes.
- **If skipped:** stages collapse two Thiên Y into one, or skip hậu vận.
- **Next:** RB05-C.

---

### G07 — NumberEnergyChain

- **Slots:** P-S00 primary/terminal; P-S02; P-S09 story axis.
- **Live:** `reading.dominant` (Diên Niên) and `reading.ending` (86 Thiên Y). No `NumberEnergyChain`.
- **Why not:** Knowledge 15 §30 dominant ≠ terminal; primary may ≠ dominant. Live labels coincide on Golden only. `energy_id=yan_nian` unsafe.
- **Owner:** ENGINE + API.
- **Minimum:**

      NumberEnergyChain {
        nodes, interactions, modifiers, controls,
        primary_energy, secondary_energy,
        dominant_flow, terminal_energy, terminal_state,
        balance_state
      }

  Customer sees labels only.
- **If skipped:** Hero binds the wrong concept on non-Golden numbers.
- **Next:** RB05-B (after triples, before wealth).

---

### G08 — triple `canonical_meaning_key`

- **Slots:** P-S04 title/narrative; also 328 in P-S02/P-S07.
- **Live:** `reading.triplets[]` = `{ digits, left_name, right_name, left_pair, right_pair }`. Seven digits match Golden order. No keys.
- **Why not:** left+right names yield naïve “Họa Hại xấu + Sinh Khí tốt”. Canonical 328 is khẩu tài (Knowledge 15 §18). Plan: do not map `reading.triplets` to P-S04 copy.
- **Owner:** ENGINE + API + CATALOG (`12_TRIPLE_COMBINATION_CATALOG`).
- **Minimum:** `TripleOccurrence.canonical_meaning_key` (e.g. `HH_TO_SK`). `interpretation_status` including `UNDEFINED`.
- **If skipped:** Customer meaning FAIL on 328 and wealth triples.
- **Next:** RB05-B → RB08.

---

### G09 — triple `customer_summary_key`

- **Slots:** P-S04 customer title/summary.
- **Live:** absent.
- **Why not:** same as G08. Adapter may resolve catalog copy from keys; it must not write new spiritual text.
- **Owner:** ENGINE + API + CATALOG.
- **Minimum:** `TripleOccurrence.customer_summary_key` (+ optional `domains`).
- **If skipped:** titles invented in React/adapter.
- **Next:** RB05-B → RB08.

---

### G10 — domain insights 5 domains

- **Slots:** P-S06.
- **Required:** Tài vận; Công việc & sự nghiệp; Tình cảm & quan hệ; Tính cách & năng lực; Cân bằng trường khí. Optional Giao tiếp is not a 6th required card.
- **Live:** no domain array. `narrative.paragraphs` mix pair lectures + **health/organ** lines.
- **Why not:** paragraphs are expert/health leak, not five domain cards. Wealth domain must not copy Wealth Flow verbatim.
- **Owner:** ENGINE + API + CATALOG.
- **Minimum:** five customer domain records `{ domain, conclusion_key, narrative_key, caution_key?, evidence_refs }` from findings.
- **If skipped:** P-S06 fixture-only, or health leak into Customer Mode.
- **Next:** RB05-D → RB10.

---

### G11 — NumberEnergyFinding

- **Slots:** P-S06, P-S07, P-S10 evidence.
- **Live:** absent.
- **Why not:** no `finding_id` / `semantic_key` / `evidence_refs`. `narrative.strengths` are not findings.
- **Owner:** ENGINE + API.
- **Minimum:** Knowledge 15 §42

      NumberEnergyFinding {
        finding_id, domain, title, semantic_key,
        evidence_refs, prominence,
        favorable_side, caution_side, narrative_keys
      }

  `evidence_refs.length >= 1` unless `GENERIC_CONTEXT`.
- **If skipped:** domains/strengths cannot be traced; basis empty.
- **Next:** RB05-D.

---

### G12 — strengths / cautions canonical 4+2

- **Slots:** P-S07.
- **Golden:** 4 strengths (827, 787/878, 786, 328) + 2 cautions (32 Họa Hại; educational Cát-count).
- **Live:** `narrative.strengths` length 4 and `watchouts` length 4 — catalog-by-energy (Họa Hại, Sinh Khí, Thiên Y, Diên Niên), not Golden cards.
- **Why not:** count 4+4 ≠ 4+2; copy mismatch; `groups[].strength` duplicates meaning.
- **Owner:** ENGINE + CATALOG (`10_CUSTOMER_NARRATIVE_CATALOG`). API must expose finding/narrative keys (not raw expert_notes).
- **Minimum:** ordered customer finding keys for 4 strengths + 2 cautions, with evidence refs.
- **If skipped:** wrong story (treats Họa Hại as a “strength” blurb).
- **Next:** RB05-D → RB11.

---

### G13 — final assessment

- **Slots:** P-S09 full story + QUÝ NHÂN → TÀI → SỰ NGHIỆP → TÀI.
- **Live:** `reading.summary` / `narrative.summary` / `narrative.paragraphs` ≠ Golden §48.
- **Why not:** helper prose is not composed from wealth + chain + catalog. Forbidden: LLM; forbidden: score→story.
- **Owner:** ENGINE + CATALOG.
- **Minimum:** `assessment.story_key` or composed paragraph keys after wealth+chain exist. Not free-form engine dump.
- **If skipped:** P-S09 stays fixture; live bind would show the wrong story.
- **Next:** RB05-F → RB13.

---

### G14 — recommendation state

- **Slots:** P-S09 `PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG` + recommendation copy §49.
- **Live:** `reading.purpose_note` is generic “không phải sim nào nhiều cát…”. No state enum.
- **Why not:** fixture state is not a runtime rule yet. Purpose note ≠ recommendation.
- **Owner:** ENGINE + API + CATALOG.
- **Minimum:** `recommendation.state` (customer-safe enum) + `copy_key`. Golden expected: continue-to-use. No “đổi số ngay”.
- **If skipped:** sales/replace wording risk; or static-only.
- **Next:** RB05-F → RB13.

---

### G15 — basis / evidence_refs

- **Slots:** P-S10.
- **Golden:** compact groups — nổi bật Diên Niên·Thiên Y·Sinh Khí; triples 827/278/786; terminal 86; totals 8/7/1.
- **Live:** no `evidence_refs`. `metadata.knowledge_version` / `engine_version` must not appear.
- **Why not:** cannot dump occurrences. Customer basis is grouped, enum-free.
- **Owner:** ENGINE + API; helper sentences CATALOG.
- **Minimum:** `evidence_refs[]` pointing at PairOccurrence / TripleOccurrence / WealthNode / TerminalState / ChainSegment, plus customer grouping keys.
- **If skipped:** P-S10 fixture-only, or metadata leak.
- **Next:** RB05-D (emit refs) → RB14 (bind).

---

### G16 — grouped display number

- **Slots:** P-S00 `0328 278 786`.
- **Live:** `reading.display_number` = `0328278786`; `metadata.input_raw` same.
- **Why not:** ungrouped string is original_input, not frozen Hero identity. UI must not parse that string into Pair Map.
- **Owner:** ADAPTER (group VN phone display from raw). Optional ENGINE/API `display_value` later.
- **Minimum for adapter input:** `original_input` + `purpose_context`. Output: `hero.displayValue`.
- **If skipped:** Hero identity regresses vs freeze.
- **Next:** specify in RB04; apply when P-S00 identity binds. No engine blocker for phone grouping.

---

### G17 — pair_summary 7 Cát / 1 Hung

- **Slots:** P-S02, P-S10 Cát/Hung totals.
- **Live:** `supportive_group_count=3`, `challenging_group_count=1`. Unique **groups**, not **pairs**.
- **Why not:** Golden is 7 cặp / 1 cặp. Binding 3 FAIL. 086: two hung pairs (`71`, `32`) still `challenging_group_count=1`. Counting `kind` in React is forbidden (UI must not calculate spiritual totals as a substitute for runtime pair_summary).
- **Owner:** ENGINE + API.
- **Minimum:**

      pair_summary {
        pair_count
        favorable_count   // Cát cặp
        challenging_count // Hung cặp
      }

  Golden: 8 / 7 / 1.
- **If skipped:** Quick Structure lies; users read 3 Cát.
- **Next:** RB05-A → RB07.

---

### G18 — distribution 8 energy including zeros

- **Slots:** P-S05.
- **Golden order/counts:** Sinh Khí 2, Thiên Y 2, Diên Niên 3, Phục Vị 0, Họa Hại 1, Ngũ Quỷ 0, Lục Sát 0, Tuyệt Mệnh 0.
- **Live:** `reading.groups[]` four present energies only. No zero rows. `energy_id` unsafe.
- **Why not:** omitting zeros hides catalog completeness. Count is not a score. UI must not fill catalog from local enum lists as a spiritual guess — engine/API should emit the 8-vector; adapter may map id→label.
- **Owner:** ENGINE + API; labels CATALOG (`02_EIGHT_ENERGY_CATALOG`).
- **Minimum:** `energy_distribution` map of eight canonical ids → count, plus primary/secondary marks from chain.
- **If skipped:** P-S05 incomplete; zeros disappear.
- **Next:** RB05-A → RB07.

---

### G19 — PairOccurrence canonical strength_label / visual tier

- **Slots:** P-S01 Nhẹ/Mạnh + dots.
- **Golden:** 32 T4 → Nhẹ ●○○○; 78/87/86 T2 → Mạnh ●●●○. Frozen union: `"Nhẹ" | "Mạnh"`. T-tier Expert only.
- **Live:** `force_label` `lực nhẹ`/`lực mạnh`; 086/103 also `lực rất mạnh`. `force_level` 1/3/4. `occurrences[].strength_rank` **inverted** (32 Họa Hại rank **4** = weakest).
- **Why not:** remapping `lực *` is lossy (third value). Mapping `strength_rank` → dots would fill four dots on Nhẹ. Knowledge 15: strength from `03_PAIR_STRENGTH_MATRIX`, not frequency.
- **Owner:** ENGINE (emit `strength_label` + `strength_level`/tier). ADAPTER maps tier → dots only after that. CATALOG matrix. Raw rank UNSAFE.
- **Minimum:** canonical `PairOccurrence` with `digits`, `energy_label`, customer category, `strength_level`, `strength_label` (`Nhẹ`/`Mạnh` for Customer). T1–T4 stay expert.
- **If skipped:** wrong intensity; rank leak; 086 cannot fit frozen union.
- **Next:** RB05-A → RB06.

Also missing on live vs Knowledge 15 pair object: `position_zone`, `distance_to_tail` (expert/score inputs; not Customer pair card).

---

### G20 — verified_by_runtime

- **Slots:** P-S00/P-S08 honesty; Expert trace. Customer MUST NOT show the flag text (checklist blacklist).
- **Live:** absent. Golden internal `score_verified_by_runtime = false`.
- **Why not:** without the flag, binding 82 looks like a live score. Adapter uses the flag to keep static honesty or a “chưa đối chiếu” state — not to render `verified_by_runtime` in DOM.
- **Owner:** ENGINE + API.
- **Minimum:** `score.verified_by_runtime: boolean` (and later per-section flags if needed). Default false until RB05-E PASSes Golden comparison.
- **If skipped:** silent false-runtime score.
- **Next:** RB05-E; Customer leak check RB15.

---

### G21 — purpose naming `motorbike_plate` vs `motorcycle_plate`

- **Slots:** analysis type label (P-S00) when vehicle context is used. Not on Golden phone case.
- **Live:** request enum includes API `motorbike_plate` (RB00/RB01). Presentation uses `motorcycle_plate`.
- **Why not:** adapter/label map will miss or dual-key. Phone `phone_number` is aligned.
- **Owner:** API (canonical name) + ADAPTER (accept alias until API aligns). Do not edit Presentation in this ticket.
- **Minimum:** one public enum; adapter alias table in RB04.
- **If skipped:** vehicle results mislabeled or rejected.
- **Next:** RB04 alias + RB05 API schema. Not a phone Golden blocker.

---

## 3. Must-not-derive rules (UI / adapter / Cursor)

Do **not** close a gap by:

1. Computing **score** in React (no 7/8=87.5, no rank→82).
2. Deriving **Wealth Flow** from Pair Map or from triple digits 827/278/786 in React.
3. Deriving **Triple meaning** from `left_name` / `right_name` (328 khẩu tài rule).
4. Using **`supportive_group_count` as 7 Cát** (or `challenging_group_count` as Hung cặp).
5. Showing **metadata / enum / rank** (`energy_id`, `strength_rank`, `classification`, `sequence_state`, `knowledge_version`, `analyzed_input`, …).
6. **Editing Golden Fixture** because live runtime differs. Report RUNTIME GAP; keep freeze copy.
7. Deleting a UI section because the API lacks the field.
8. Filling copy with Cursor-written spiritual prose or LLM.
9. Importing leftover `api.ts` / `readingTypes.ts` as the adapter.
10. Mapping `occurrence.state` HIDDEN/AMPLIFIED/REPEATED to Customer chips.
11. Treating `reading.summary` as Hero short, Wealth Flow, or Final Assessment.
12. Binding `narrative.paragraphs` (health/organ leak).

Until a slot is bound under later RB tickets, the page **keeps rendering Golden Fixture**.

---

## 4. Required runtime objects

Engine must produce (Knowledge 15), then API expose:

| Object | Required for | RB05 slice |
|---|---|---|
| Canonical `PairOccurrence[]` (overlap, strength_label, category) | P-S01, pair_summary, distribution | RB05-A |
| `pair_summary` | P-S02, P-S10 | RB05-A |
| `energy_distribution` (8 keys) | P-S05 | RB05-A |
| `TripleOccurrence[]` + meaning keys + status | P-S04 | RB05-B |
| `NumberEnergyChain` | P-S00, P-S02, P-S09 | RB05-B |
| `WealthNode[]` + Phone Wealth Flow 4 stages + `later_outcome` | P-S03 | RB05-C |
| `NumberEnergyFinding[]` + 5 domains + 4+2 keys | P-S06, P-S07 | RB05-D |
| `evidence_refs` grouped | P-S10 | RB05-D |
| Assessment compose + `recommendation.state` | P-S09 | RB05-F |
| `PhoneScoreResult` + `verified_by_runtime` | P-S00, P-S08 | RB05-E **after** interpret |

Live `reading` / `occurrences` / `narrative` remain **legacy helpers**, not Customer contract.

---

## 5. API exposure needs

`POST /api/v1/number-energy/analyze` `data` today:

    occurrences, sequence_state, patterns, narrative, warnings, metadata, reading

Needs a **customer-adapter input** (names to lock in RB04), conceptually:

    identity { original_input, display_value?, purpose_context, analysis_body? }
    pair_occurrences[]
    pair_summary
    energy_distribution
    triple_occurrences[]
    chain
    wealth_flow
    findings[]
    score { ... PhoneScoreResult, verified_by_runtime }
    recommendation
    evidence

Rules:

- Do not make Customer payload = raw `occurrences` + `metadata.summary`.
- Keep unsafe fields out of Customer view (Expert/P-S11 later).
- Adding `score` **requires** updating TEST assertions in the same engine ticket (`"score" not in data` / `"grade" not in data`).
- Align or alias `motorbike_plate` / `motorcycle_plate`.
- Do not change BaZi / Good Date / Marriage APIs.

---

## 6. Adapter contract inputs for RB04

RB04 writes the contract only (no code in RB03). Proposed names from plan: `NumberEnergyPresentationAdapter` → `NumberEnergyPresentationView`.

### 6.1 Adapter must receive (canonical; wait if missing)

From ENGINE/API (RB05+). Adapter **fails closed** (keep fixture / unsupported) rather than invent:

- `purpose_context`, `original_input`
- `PairOccurrence[]` or interim `reading.pairs` **only** for digits + `display_name` until RB05-A
- `pair_summary` (not group counts)
- `energy_distribution` (8)
- `TripleOccurrence[]` with keys (digits/order may be interim)
- `NumberEnergyChain` (primary/terminal labels)
- `wealth_flow` 4 stages (not raw WealthNode dump)
- `NumberEnergyFinding[]` filtered to customer domains
- approved 4+2 narrative keys
- `PhoneScoreResult` + `verified_by_runtime`
- `recommendation.state`
- `evidence_refs` customer groups
- `interpretation_status` per triple

### 6.2 Adapter may specify now from **current** payload (still no wiring)

| Receive | Emit | Notes |
|---|---|---|
| `metadata.input_raw` | `hero.displayValue` grouped | G16 |
| `metadata.purpose_context` | `hero.analysisTypeLabel` | G21 alias later |
| `reading.pairs[].pair_digits` | `pairs[].digits` | order only |
| `reading.pairs[].display_name` | `pairs[].energyLabel` | until energy_label canonical |
| `reading.dominant.display_name` | **do not** treat as chain.primary | wait G07 |
| `reading.ending.*` | **do not** treat as chain.terminal | wait G07 |
| `reading.triplets[].digits` | `triples[].digits` structure | no title/narrative |
| `kind` | Cát/Hung | never show English |
| `force_label` / `strength_rank` | **do not** map to Nhẹ/dots | wait G19 |

### 6.3 Adapter must emit `NumberEnergyPresentationView`

Match frozen slots (plan §13):

    hero
    pairs
    quick_structure
    wealth_flow
    triples
    distribution
    domains
    findings
    score
    assessment
    basis
    expert_seam          // still hidden

Customer Mode: no technical fields. Expert seam remains hidden until a dedicated ticket.

### 6.4 Must wait for RB05 Engine/API before bind

All of G01–G15, G17–G20. G16 grouping can be specified in RB04 without engine. G21 alias in RB04.

**Static compatibility:** until each bind ticket (RB06+), React keeps Golden Fixture in that slot. One layout only.

---

## 7. Priority order

Knowledge 15: DETECT → RESOLVE → MATCH → BIND → COMPOSE → PRESENT. Score last.

| Order | Work | Gaps | Bind UI |
|---|---|---|---|
| 0 | **RB04** Adapter Contract (types only) | view shape, do-not-bind, G16/G21 | none |
| 1 | **RB05-A** PairOccurrence + pair_summary + distribution 8 + strength_label | G17, G18, G19 | later RB06/RB07 |
| 2 | **RB05-B** TripleOccurrence + meaning keys + NumberEnergyChain | G07, G08, G09 | later RB08 |
| 3 | **RB05-C** WealthNode + 4-stage wealth + later_outcome | G05, G06 | later RB09 |
| 4 | **RB05-D** Findings + 5 domains + 4+2 + evidence_refs | G10, G11, G12, G15 | later RB10/RB11/RB14 |
| 5 | **RB05-F** Assessment compose + recommendation state | G13, G14 | later RB13 |
| 6 | **RB05-E** PhoneScoreResult + verified_by_runtime + **TEST update** | G01–G04, G20 | later RB12 |
| 7 | API purpose alias | G21 | with RB04/RB05 |
| 8 | RB06…RB16 bind + leak + visual | — | per slot |

Do not ship all of RB05 in one mixed PR if it cannot be reviewed. Do not start RB05 inside RB04. Do not bind fetch before adapter contract.

---

## 8. Risks / residual gaps

- **Group-count trap** on every non-Golden number (086 already proves hung pair ≠ hung group).
- **Dominant vs primary** on numbers where they diverge.
- **328 naïve triple** if anyone binds names as copy before G08/G09.
- **Inverted strength_rank** vs customer Nhẹ.
- **`lực rất mạnh`** vs frozen two-value strength.
- **TEST wall** on score/grade until RB05-E explicitly updates tests (do not weaken asserts in this ticket).
- **103** accepted as `phone_number` with `HIDDEN` — input-contract gap; not a Golden fix.
- **Health paragraphs** if narrative is reused as domains.
- Leftover portal `api.ts` / `types.ts` / `readingTypes.ts` must not become the adapter.
- Catalog files already exist; the gap is **keys on the payload**, not missing markdown copy.

Out of RB03 scope (report only): CCCD layer (`cccd_note`), Expert Mode content, nav, other products.

---

## 9. What was intentionally NOT changed

- Frontend / NumberEnergyPage / CSS / freeze marker
- Backend, engine, API schema
- Tests (including `"score" not in data`)
- Golden Fixture, Golden Dataset, snapshots, expected output
- Knowledge / Presentation / `04_RUNTIME_BINDING_PLAN.md`
- No adapter code, no fetch, no `api.ts` import, no nav
- BaZi, Good Date, Marriage
- RB04 not started (input prepared only)

---

## 10. Next allowed stage

**RB04 — ADAPTER CONTRACT**

Write `NumberEnergyPresentationAdapter` / `NumberEnergyPresentationView` types and rules.  
No UI wiring. No engine rewrite. Freeze unchanged.

RB05 may be **scheduled** after this report; it must not start in the RB04 ticket unless explicitly requested as a separate task.
