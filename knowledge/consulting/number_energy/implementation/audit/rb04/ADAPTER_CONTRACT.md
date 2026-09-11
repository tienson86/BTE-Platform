# RB04 — ADAPTER CONTRACT

**Stage:** RB04  
**Status:** PASS (contract only)  
**Freeze:** `NUMBER_ENERGY_STATIC_UI_V1`  
**Adapter name:** `NumberEnergyPresentationAdapter`  
**Output name:** `NumberEnergyPresentationView`  
**Machine types:** `applications/customer_portal/src/features/number_energy/presentationContract.ts`

**Not a Presentation spec. Not Knowledge 15. Not Golden Fixture.**  
Does not replace `04_RUNTIME_BINDING_PLAN.md`.

**Sources:** plan §13, RB03 `GAP_REPORT.md`, RB02 mapping, RB01 `0328278786_phone_number.json`, `01_GOLDEN_PHONE_FIXTURE.md`, Knowledge 15.

**Must not:** import into `NumberEnergyPage` / `ResultSection` / `numberEnergyApp`; implement adapter functions; wire fetch; edit engine/API; start RB05.

Leftover `api.ts`, `types.ts`, `readingTypes.ts`, `ResultView.tsx` describe the **old analyze payload**. They are **not** this contract.

---

## 1. Purpose

One adapter sits between canonical runtime result and frozen Customer slots P-S00…P-S11.

    KNOWLEDGE > ENGINE > API > ADAPTER > UI

    Adapter binds.
    Adapter does not detect pairs.
    Adapter does not resolve triples.
    Adapter does not score.
    Adapter does not invent wealth direction.
    Adapter maps enums → customer labels (approved tables only).
    Adapter omits detailed narrative when interpretation_status = UNDEFINED.
    Adapter never exposes technical fields in Customer Mode.

React sections will later receive `NumberEnergyPresentationView`.  
Until each bind ticket (RB06+), the page **keeps rendering Golden Fixture**. One layout only.

---

## 2. Field status legend

| Status | Meaning |
|---|---|
| PRESENT_FROM_CURRENT_PAYLOAD | Live analyze `data` already has a customer-safe or mappable value. |
| ADAPTER_DERIVED_SAFE | Adapter may format/label without new spiritual meaning. |
| REQUIRES_ENGINE | Canonical object/field not produced yet (RB05). |
| REQUIRES_API | Not on `POST /api/v1/number-energy/analyze` `data`. |
| DO_NOT_BIND | Forbidden in Customer Mode even if present. |

---

## 3. Adapter input contract

Input name: `NumberEnergyAdapterInput`

Always required:

- `locale` (Customer default `vi`)
- `mode` = `customer` (Expert is not default)
- `purpose_context`
- `identity.original_input`

Canonical runtime objects are **nullable**. Missing → `RUNTIME_GAP` + that slot stays Golden Fixture. Adapter must not invent them.

### 3.1 `purpose_context`

| Item | Status |
|---|---|
| `phone_number` | PRESENT_FROM_CURRENT_PAYLOAD |
| `car_plate` | PRESENT_FROM_CURRENT_PAYLOAD (API) |
| Presentation `motorcycle_plate` | ADAPTER_DERIVED_SAFE alias (G21) |
| API `motorbike_plate` | ADAPTER_DERIVED_SAFE alias → same customer label until API aligns (RB05) |

Customer labels (chrome, not spiritual copy):

- `phone_number` → Số điện thoại
- `car_plate` → Biển số ô tô
- `motorcycle_plate` / `motorbike_plate` → Biển số xe máy

Raw enum is DO_NOT_BIND.

### 3.2 Identity / `input_raw`

| Field | Status | Notes |
|---|---|---|
| `identity.original_input` / `metadata.input_raw` | PRESENT_FROM_CURRENT_PAYLOAD | Golden `0328278786` |
| `identity.display_value` grouped | ADAPTER_DERIVED_SAFE | `0328278786` → `0328 278 786` (G16). UI must not parse pairs from this string. |
| `reading.display_number` ungrouped | PRESENT_FROM_CURRENT_PAYLOAD | Same as raw; not Hero identity until grouped |
| `identity.analysis_body` | DO_NOT_BIND (Customer) | `328278786` Expert/internal only |

### 3.3 `pair_occurrences`

Canonical `PairOccurrence[]` (Knowledge 15 §12): digits, energy_label, category, strength_label, strength_level, position_zone, distance_to_tail.

| Field | Status |
|---|---|
| Ordered overlapping pairs (8; `78` twice) | PRESENT_FROM_CURRENT_PAYLOAD via `reading.pairs[]` |
| `pair_digits` | PRESENT_FROM_CURRENT_PAYLOAD |
| `display_name` / energy_label | PRESENT_FROM_CURRENT_PAYLOAD (live label) |
| Customer category Cát/Hung | ADAPTER_DERIVED_SAFE **only** via approved `kind` map **or** canonical category (preferred, REQUIRES_ENGINE G19) |
| `strength_label` Nhẹ/Mạnh + dots | REQUIRES_ENGINE (G19) |
| `occurrence_id`, `source_span`, `energy_id`, `strength_rank`, `classification*`, `state` | DO_NOT_BIND |

Do not detect pairs from `original_input`.

### 3.4 `pair_summary`

| Field | Status |
|---|---|
| `{ pair_count, favorable_count, challenging_count }` | REQUIRES_ENGINE + REQUIRES_API (G17) |
| Golden phone: 8 / 7 / 1 | expected after RB05-A |
| `reading.supportive_group_count` / `challenging_group_count` | DO_NOT_BIND |

### 3.5 `energy_distribution`

Eight catalog ids including zeros: Sinh Khí, Thiên Y, Diên Niên, Phục Vị, Họa Hại, Ngũ Quỷ, Lục Sát, Tuyệt Mệnh.

| Field | Status |
|---|---|
| Complete 8-count object | REQUIRES_ENGINE + REQUIRES_API (G18) |
| `reading.groups[]` present-only | DO_NOT_BIND as distribution |
| Fill zeros from local catalog without runtime counts | **Forbidden** |

Adapter may list zero-count rows **only** when runtime sends a complete distribution object (or an explicit catalog-safe count object with all eight keys).

### 3.6 `triple_occurrences`

Canonical `TripleOccurrence[]` with `canonical_meaning_key`, `customer_summary_key`, `interpretation_status`.

| Field | Status |
|---|---|
| Ordered `digits` (328…786) | PRESENT_FROM_CURRENT_PAYLOAD structure |
| `left_name` / `right_name` as energy labels | PRESENT_FROM_CURRENT_PAYLOAD labels only |
| Meaning keys / titles / narratives | REQUIRES_ENGINE (G08, G09) |
| Compose meaning from left+right | DO_NOT_BIND |

If `interpretation_status = UNDEFINED`: omit detailed narrative; do not guess.

### 3.7 `chain`

`NumberEnergyChain`: primary_energy, secondary_energy, terminal_energy, terminal_state, …

| Field | Status |
|---|---|
| Canonical chain | REQUIRES_ENGINE + REQUIRES_API (G07) |
| `reading.dominant` as primary | DO_NOT_BIND (dominant ≠ primary) |
| `reading.ending` as terminal | DO_NOT_BIND until chain exists |

### 3.8 `wealth_flow`

Phone Wealth Flow Resolver output: four customer stages + `later_outcome`. Not raw `WealthNode[]` dump.

| Field | Status |
|---|---|
| 4 stages + story keys | REQUIRES_ENGINE + REQUIRES_API (G05, G06) |
| Derive from Pair Map or triple digits 827/278/786 | DO_NOT_BIND |
| `reading.summary` as wealth | DO_NOT_BIND |

### 3.9 `findings`

`NumberEnergyFinding[]` with `semantic_key`, `evidence_refs`, narrative keys.

| Field | Status |
|---|---|
| Canonical findings | REQUIRES_ENGINE + REQUIRES_API (G11) |
| 5 customer domains | REQUIRES_ENGINE (G10) |
| 4+2 strengths/cautions keys | REQUIRES_ENGINE (G12) |
| `narrative.strengths` / `watchouts` / `paragraphs` | DO_NOT_BIND |

### 3.10 `score`

`PhoneScoreResult` + `verified_by_runtime`.

| Field | Status |
|---|---|
| final_score, grade, 5 components, score_reasons | REQUIRES_ENGINE + REQUIRES_API + TEST (G01–G04, G20) |
| Client-side score/grade | DO_NOT_BIND |
| Show `verified_by_runtime` text in Customer DOM | DO_NOT_BIND (blacklist). Adapter **uses** the flag internally so 82 is not presented as live until true. |

### 3.11 `recommendation`

| Field | Status |
|---|---|
| `state` + copy keys | REQUIRES_ENGINE + REQUIRES_API (G13, G14) |
| Derive from score | DO_NOT_BIND |
| `reading.purpose_note` as recommendation | DO_NOT_BIND |

### 3.12 `evidence`

| Field | Status |
|---|---|
| `evidence_refs` customer groups | REQUIRES_ENGINE + REQUIRES_API (G15) |
| `metadata.knowledge_version` / engine ids | DO_NOT_BIND |

### 3.13 Expert trace (optional)

`expert_trace` may exist on input. **Never Customer default.** P-S11 stays `hidden` + `aria-hidden`. No `?expert=true` in this contract.

---

## 4. Presentation view contract (`NumberEnergyPresentationView`)

Customer-safe. Field names aligned with frozen Golden UI modules (`goldenHero.ts`, …).

| View key | Slot | Golden source |
|---|---|---|
| `hero` | P-S00 | `GOLDEN_PHONE_HERO` |
| `pairs` | P-S01 | `GOLDEN_PHONE_PAIRS` |
| `quick_structure` | P-S02 | `GOLDEN_QUICK_STRUCTURE` |
| `wealth_flow` | P-S03 | `GOLDEN_WEALTH_STAGES` + story + synthesis |
| `triples` | P-S04 | `GOLDEN_PHONE_TRIPLES` |
| `distribution` | P-S05 | `GOLDEN_ENERGY_DISTRIBUTION` |
| `domains` | P-S06 | `GOLDEN_DOMAIN_INSIGHTS` (5 required) |
| `findings` | P-S07 | `GOLDEN_STRENGTHS` (4) + `GOLDEN_CAUTIONS` (2) |
| `score` | P-S08 | `GOLDEN_SCORE_*` |
| `assessment` | P-S09 | `GOLDEN_ASSESSMENT_*` + recommendation |
| `basis` | P-S10 | `GOLDEN_BASIS_*` |
| `expert_seam` | P-S11 | hidden placeholder |

Envelope (not shown in Customer DOM):

    NumberEnergyAdapterResult {
      freezeLabel: NUMBER_ENERGY_STATIC_UI_V1
      view: NumberEnergyPresentationView
      slotSource: Record<P-S00…P-S11, GOLDEN_FIXTURE | RUNTIME>
      gaps: RuntimeGap[]   // G01…G21
    }

`hero` customer fields: eyebrow, analysisTypeLabel, displayValue, scoreDisplay, grade, primaryEnergy, primaryKeywords, terminalEnergy, terminalKeywords, summary.  
No enums, no analysis_body, no percent, no fixture_id.

`pairs[]`: digits, energyLabel, categoryLabel `Cát|Hung`, strengthLabel `Nhẹ|Mạnh`, strengthDots `[4]`, keywords.

`quick_structure`: favorableValue / challengingValue as **cặp counts**, not scores.

`wealth_flow.stages` length 4, ids WF-01…WF-04.

`triples[]`: digits, sourceLabel, targetLabel, title, narrative, domains, priority. Title/narrative only from catalog keys.

`distribution[]`: eight rows, zeros allowed only from complete runtime object.

`domains[]`: exactly the five required titles. Optional Giao tiếp is not required.

`findings`: strengths[4], cautions[2].

`score`: total display, grade, five breakdown rows, four reasons, honest note until `verified_by_runtime`.

`assessment`: story, flow QUÝ NHÂN → TÀI → SỰ NGHIỆP → TÀI, recommendation state + copy.

`basis`: helper, principles, highlights, evidence groups — customer wording only.

`expert_seam`: `{ visible: false, hidden: true, ariaHidden: true }` in Customer Mode.

---

## 5. Allowed adapter transforms

1. Group VN phone display from `original_input` / `input_raw` (`0328278786` → `0328 278 786`).
2. `purpose_context` → customer analysis-type label, including `motorbike_plate` ↔ `motorcycle_plate` alias.
3. Pass `reading.pairs[].pair_digits` + `display_name` **preserving order** (including duplicate 78).
4. `kind` `supportive` → `Cát`, `challenging` → `Hung` **only** via the approved table, and **never** show English `kind`. Prefer canonical category when RB05-A emits it.
5. Include zero-count distribution rows **only** when runtime provides a complete 8-key count object.
6. Look up **catalog copy from engine keys** (`canonical_meaning_key`, finding keys, score_reason keys). Lookup ≠ writing new copy.
7. Map canonical `strength_label` Nhẹ/Mạnh → `strengthDots` **after** RB05-A emits that label. Not from `strength_rank`.
8. Omit UNDEFINED triple narrative.
9. Keep P-S11 hidden.
10. Record `RUNTIME_GAP` on `NumberEnergyAdapterResult.gaps`.

---

## 6. Forbidden adapter transforms

1. Calculate score or grade (no 7/8=87.5, no rank→82).
2. Derive Wealth Flow from Pair Map or from triple digits.
3. Derive Triple meaning from left/right labels (328 khẩu tài rule).
4. Derive 7 Cát / 1 Hung from `supportive_group_count` / `challenging_group_count`.
5. Count `kind` in the adapter as a substitute for `pair_summary` (UI/adapter must not replace runtime pair_summary).
6. Map `strength_rank` / `force_level` / `lực rất mạnh` directly to customer strength or dots.
7. Treat `reading.dominant` as `chain.primary_energy`.
8. Treat `reading.ending` as `chain.terminal_energy` before chain exists.
9. Create final recommendation from score.
10. Write new spiritual/customer copy or LLM text.
11. Remove UI sections because API lacks fields.
12. Expose metadata, enum, rank, raw state, `source_span`, `occurrence_id`, health paragraphs, `analyzed_input`, `request_id`, `cccd_note`, raw warnings/patterns.
13. Use `narrative.paragraphs` in Customer Mode.
14. Show `verified_by_runtime` / `fixture_id` / `knowledge_version` in Customer DOM.
15. Enable Expert Mode by default or bind P-S11.
16. Parse input digits into Pair Map / Triple Story.
17. Resume leftover `api.ts` types as this contract.

---

## 7. Fallback policy

1. If a slot’s canonical runtime field is missing: **keep Static Golden Fixture** for that slot until its RB05 slice **and** bind ticket (RB06+) pass.
2. Missing field → `RUNTIME_GAP` (G01…G21). Not a UI workaround. Not a Golden Fixture edit.
3. Freeze marker stays `data-static-freeze="NUMBER_ENERGY_STATIC_UI_V1"` / `data-static-phase="sb16"`.
4. Fail closed: incomplete view fields are not filled with guessed copy.
5. When `verified_by_runtime !== true`, score/grade stay fixture (or an honest “chưa đối chiếu” state defined later in RB12 — still not a computed score).
6. Golden `0328278786` remains the regression expected value after a slot is bound.
7. Tests that assert current API has no `score` / `grade` stay until RB05-E.

---

## 8. Customer safety

Never in Customer Mode:

`occurrence_id` · `source_span` · `energy_id` · `strength_rank` · `classification*` · `state` / `sequence_state` · `metadata.*` technical · `narrative.paragraphs` · health/organ wording · `analyzed_input` · `force_level` · English `kind` · `request_id` · `cccd_note` · raw `warnings`/`patterns` · `DIEN_NIEN` / `HIDDEN` / `AMPLIFIED` as visible text · `verified_by_runtime` label · `fixture_id`

Expert P-S11: present in DOM, `hidden`, `aria-hidden`, inert. Not in customer navigation.

---

## 9. Runtime / API requirements for RB05

Do not implement in RB04. Schedule only:

| Slice | Must emit | Gaps |
|---|---|---|
| RB05-A | Canonical `PairOccurrence[]`, `pair_summary`, complete `energy_distribution` (8), `strength_label` | G17, G18, G19 |
| RB05-B | `TripleOccurrence[]` + meaning keys + `NumberEnergyChain` | G07, G08, G09 |
| RB05-C | `WealthNode[]` + 4-stage `wealth_flow` + `later_outcome` | G05, G06 |
| RB05-D | `NumberEnergyFinding[]`, 5 domains, 4+2 keys, `evidence_refs` | G10–G12, G15 |
| RB05-F | Assessment compose + `recommendation.state` | G13, G14 |
| RB05-E | `PhoneScoreResult` + `verified_by_runtime`; **update** `"score" not in data` tests in that ticket | G01–G04, G20 |
| API | Expose adapter input objects; alias/align `motorbike_plate` | G21 |

Current `data` shape (`occurrences`, `reading`, `narrative`, `metadata`, …) is **legacy**, not Customer contract.

---

## 10. UI rule (later bind tickets)

Sections receive the view object. They MUST NOT call NumberEnergyEngine, fetch-then-recompute, count pairs into a score, or reconstruct 827/278/786 meaning.

This ticket does **not** import the contract into the page.

---

## 11. Intentionally not changed

Frontend rendering, freeze marker, nav, `api.ts` import, fetch, engine, API behavior, Golden Fixture, tests that assert missing score, BaZi / Good Date / Marriage. RB05 not started. No adapter implementation function.
