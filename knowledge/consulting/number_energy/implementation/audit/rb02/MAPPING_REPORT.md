# RB02 — MAP FIXTURE FIELDS ↔ RUNTIME FIELDS

**Stage:** RB02  
**Status:** PASS (mapping only)  
**Freeze:** `NUMBER_ENERGY_STATIC_UI_V1`  
**Primary case:** `0328278786` / `phone_number`  
**Supporting schema checks:** `0868271327`, `103` (same envelope; do not replace Golden)

**Not a spec.** Audit output for Runtime Binding. Does not replace:

- `01_GOLDEN_PHONE_FIXTURE.md`
- `04_RUNTIME_BINDING_PLAN.md`
- `knowledge/15_RUNTIME_BINDING_CONTRACT.md`

**Payload snapshots:**

- `../rb01/0328278786_phone_number.json`
- `../rb01/0868271327_phone_number.json`
- `../rb01/103_phone_number.json`

---

## Verdict legend

| Verdict | Meaning |
|---|---|
| DIRECT | Live field is customer-safe and same meaning. Pass-through after select. |
| ADAPTER | Live field may feed the slot only after format/label map. No new spiritual meaning. |
| ENGINE_MISSING | Canonical runtime object/field is not produced. |
| API_MISSING | Canonical field is not on `POST /api/v1/number-energy/analyze` `data`. |
| UNSAFE | Field exists; raw value must not appear in Customer Mode. |
| DO_NOT_BIND | Forbidden mapping, even if the value looks convenient. |

Canonical source (Knowledge 15 / plan RB02) wins over live `reading` helper.

Live `data.reading` is `build_reading()`, not the Presentation Fixture object.

---

## 1. Slot-by-slot mapping (P-S00 … P-S11)

### P-S00 Result Hero

| UI field (frozen) | Golden fixture source | Canonical runtime | Live candidate | Verdict | Required work | Customer safety |
|---|---|---|---|---|---|---|
| `eyebrow` | §3 `KẾT QUẢ TƯ VẤN NĂNG LƯỢNG SỐ` | chrome / catalog | none | ADAPTER / CATALOG | Keep static chrome or catalog key. Not analyze payload. | Safe chrome. |
| `analysisTypeLabel` = Số điện thoại | §3 Analysis type; `purpose_context=phone_number` | `purpose_context` → customer label | `metadata.purpose_context` = `phone_number` | ADAPTER | Map enum → label. Trap: API `motorbike_plate` vs Presentation `motorcycle_plate`. | Do not show raw enum. |
| `displayValue` = `0328 278 786` | §2 `display_value` | `display_value` grouped | `reading.display_number` / `metadata.input_raw` = `0328278786` | ADAPTER + ENGINE_MISSING | Adapter may group phone display from raw input. Engine/API should eventually emit `display_value`. UI must not parse pairs from digits. | Ungrouped raw is usable as input identity, not as frozen Hero identity. |
| original input (internal) | §2 `original_input` | `original_input` | `metadata.input_raw` | DIRECT | Pass-through for adapter identity. | Customer sees grouped display, not analysis body. |
| analysis body | §2 `analysis_body` = `328278786` | internal / expert | `reading.analyzed_number` / `metadata.analyzed_input` | DO_NOT_BIND (Customer) | Expert/internal only. | Analysis body leak = FAIL. |
| `scoreDisplay` = `82 / 100` | §4 score | `PhoneScoreResult.final_score` | **absent** | ENGINE_MISSING + API_MISSING | Score engine after chain + wealth + domains. Do not keep showing 82 as if verified. | Do not invent client score. Do not map `strength_rank` / `strongest_rank`. |
| `grade` = `TỐT` | §4 grade | `PhoneScoreResult.grade` | **absent** | ENGINE_MISSING + API_MISSING | Same as score. | No percent (`82%`). |
| `primaryEnergy` = Diên Niên | §5 customer label; energy `DIEN_NIEN` | `NumberEnergyChain.primary_energy` → customer label | `reading.dominant.display_name` = Diên Niên | ADAPTER + ENGINE_MISSING | Confirm primary ≠ dominant (Knowledge 15 §30). Need chain object. Live label OK only after that contract. | `energy_id=yan_nian` UNSAFE. Enum `DIEN_NIEN` Expert only. |
| `primaryKeywords` | §5 Công việc · năng lực · trách nhiệm | catalog by energy | **absent** | ENGINE_MISSING / CATALOG | Engine returns energy id or narrative key; adapter resolves customer keywords. | Do not invent keywords in UI. |
| `terminalEnergy` = Thiên Y | §7 customer label; pair 86 | `chain.terminal_energy` → customer label | `reading.ending.display_name` = Thiên Y; `pair_digits=86` | ADAPTER + ENGINE_MISSING | Need chain.terminal_energy / terminal_state. Live ending label coincides on Golden. | `ending.kind=supportive` English UNSAFE. `ending.note` not Hero copy. |
| `terminalKeywords` | §7 Tài vận · tài nguyên · thành quả | catalog | **absent** | ENGINE_MISSING / CATALOG | Same as primary keywords. | — |
| `summary` (short) | §8 short version | composed from chain + wealth keys | `reading.summary` (engine helper copy) | DO_NOT_BIND + ENGINE_MISSING | Compose from approved catalog keys after wealth/chain exist. | Live summary ≠ Golden short. Do not treat as Wealth Flow. |

Hero score/grade remain presentation fixture until Score tickets PASS (`verified_by_runtime`).

---

### P-S01 Pair Map

Canonical: ordered `PairOccurrence[]` — digits, energy_label, category Cát/Hung, strength_label Nhẹ/Mạnh.

| UI field | Golden | Canonical runtime | Live candidate | Verdict | Required work | Customer safety |
|---|---|---|---|---|---|---|
| pair order / count = 8 | §9 sequence; 78 twice | overlapping `PairOccurrence[]` | `reading.pairs[]` (8) and `occurrences[]` (8), order `32 28 82 27 78 87 78 86` | ADAPTER (structure) | Bind ordered `reading.pairs` for digits+label only until canonical PairOccurrence is emitted. Verify overlap; do not skip shared digits. | `occurrence_id` / `source_span` DO_NOT_BIND. |
| `digits` | §9–17 | `PairOccurrence.digits` | `reading.pairs[].pair_digits` | DIRECT | Pass-through. | Safe. |
| `energyLabel` | customer labels | `PairOccurrence.energy_label` | `reading.pairs[].display_name` | DIRECT (live label) + ENGINE_MISSING (canonical object) | Prefer canonical energy_label. Live Vietnamese names match Golden on this case. | `energy_id` UNSAFE. |
| `categoryLabel` Cát/Hung | §10–17 HUNG/CAT | pair category from catalog | `reading.pairs[].kind` = `supportive`/`challenging` | ADAPTER + UNSAFE (raw) | Map supportive→Cát, challenging→Hung in adapter. Do not show English. Do not use `classification` / `classification_label`. | Raw `kind` FAIL. |
| `strengthLabel` Nhẹ/Mạnh | T4→Nhẹ, T2→Mạnh | `PairOccurrence.strength_label` from `03_PAIR_STRENGTH_MATRIX` | `force_label` = `lực nhẹ`/`lực mạnh` (`lực rất mạnh` on 086) | ADAPTER + ENGINE_MISSING + UNSAFE | Engine must emit customer `Nhẹ`/`Mạnh` (frozen union). Remap `lực *` is lossy: third value `lực rất mạnh` is not in frozen UI. | `strength_rank` DO_NOT_BIND. `force_level` integer DO_NOT_BIND. T1–T4 Expert only. |
| `strengthDots` ●○○○ / ●●●○ | visual of T4/T2 | from strength tier, not score | **absent** | ADAPTER after canonical strength | Adapter maps Nhẹ/Mạnh (or T-tier expert) → dots. UI must not derive from frequency. | Do not map rank 4 → four filled dots. Rank 4 on 32 is weakest. |
| `keywords` | per pair fixture | catalog | **absent** | ENGINE_MISSING / CATALOG | Lookup by energy, not UI invention. | — |
| customer pair note (32) | §10 note | catalog / finding | `occurrences[].notes` | DO_NOT_BIND | Engine notes are V1 jargon. | Contains combination/control language. |
| `expression` Lặp lại | not a Customer pair field | modifier | `reading.pairs[].expression` | DO_NOT_BIND (Customer pair card) | Modifier belongs Expert or a dedicated customer-safe label later. | 103: `Bị che bởi số 0` + `sequence_state=HIDDEN` UNSAFE. |

**Forbidden:** map `occurrences[].state` HIDDEN/AMPLIFIED/REPEATED to customer; map `strength_rank` to Hero score or dots.

---

### P-S02 Quick Structure

| UI field | Golden | Canonical runtime | Live candidate | Verdict | Required work | Customer safety |
|---|---|---|---|---|---|---|
| `favorableValue` = 7 cặp | §18; fixture `favorable_count=7` | `pair_summary` pair counts | `reading.supportive_group_count` = **3** | DO_NOT_BIND (group count) + ENGINE_MISSING (`pair_summary`) | Engine/API must emit pair counts (7/1), not unique-group counts. | Binding 3 would FAIL Golden. |
| `challengingValue` = 1 cặp | §18 `challenging_count=1` | `pair_summary` | `reading.challenging_group_count` = 1 | DO_NOT_BIND | Coincidentally 1 on Golden; still group semantics. 086 has 2 hung pairs but `challenging_group_count=1`. | Trap. |
| `primaryValue` | §18 Diên Niên | `chain.primary_energy` label | `reading.dominant.display_name` | ADAPTER + ENGINE_MISSING | Same as Hero primary. | No enum. |
| `terminalValue` | §18 Thiên Y | `chain.terminal_energy` label | `reading.ending.display_name` | ADAPTER + ENGINE_MISSING | Same as Hero terminal. | No English kind. |
| `summary` | §18 supporting summary | catalog compose from 328 + chain | `reading.summary` / `narrative.purpose_focus` | DO_NOT_BIND + ENGINE_MISSING | Catalog key after triple 328 exists. | Counts are not scores. No `7/8=87.5`. |

Counting `reading.pairs[].kind` would yield 7/1 on Golden only. That is **not** the approved source (UI must not calculate; group_count is the known trap). RB03: `pair_summary` = ENGINE_MISSING.

---

### P-S03 Wealth Flow

Canonical: Phone Wealth Flow Resolver → four customer stages, not raw `WealthNode` dump.

| UI field | Golden | Canonical runtime | Live candidate | Verdict | Required work | Customer safety |
|---|---|---|---|---|---|---|
| Stage 01 Tài vận / Có Thiên Y / 27 · 86 | §29 | `wealth_presence` + wealth nodes 27, 86 | **absent** | ENGINE_MISSING + API_MISSING | Invoke Phone Wealth Flow Resolver. | No “rất giàu”. |
| Stage 02 Tài từ đâu / 827 Sinh Khí → Thiên Y | §30 | `wealth_sources` / source interaction | `reading.triplets` row `827` digits only | DO_NOT_BIND (as wealth) + ENGINE_MISSING | Triple digits ≠ wealth stage copy. | — |
| Stage 03 Tài đi đâu / 278 Thiên Y → Diên Niên | §31 | `wealth_destinations` | triple `278` digits only | DO_NOT_BIND + ENGINE_MISSING | Same. | — |
| Stage 04 Hậu vận / 786 Diên Niên → Thiên Y | §32 | `later_outcome` / terminal wealth | triple `786` digits only | DO_NOT_BIND + ENGINE_MISSING | Hậu vận ≠ lifetime destiny. | No “về già chắc chắn”. |
| Story QUÝ NHÂN → TÀI → SỰ NGHIỆP → TÀI | §33 | composed wealth story keys | `reading.summary` | DO_NOT_BIND | Plan: do not treat `reading.summary` as Wealth Flow. | — |
| Signal summary | §34 | wealth synthesis | **absent** | ENGINE_MISSING | — | No financial guarantee. |

---

### P-S04 Triple Story

Canonical: ordered `TripleOccurrence[]` with `canonical_meaning_key` + `customer_summary_key`.

| UI field | Golden | Canonical runtime | Live candidate | Verdict | Required work | Customer safety |
|---|---|---|---|---|---|---|
| `digits` order 328…786 | §20 | `TripleOccurrence.digits` | `reading.triplets[].digits` | ADAPTER (structure only) | Preserve order. Do not reorder by score. | Safe digits. |
| `sourceLabel` / `targetLabel` | §21–28 | source/target energy labels | `left_name` / `right_name` | ADAPTER (labels only) | Labels OK; **not** meaning. | Do not concatenate as “Hung + Cát = mixed”. |
| `title` / `narrative` | canonical meanings (328 = khẩu tài) | `canonical_meaning_key` → catalog | **absent** (only names) | ENGINE_MISSING + DO_NOT_BIND (naive copy) | Engine must attach catalog keys. Adapter resolves copy. Plan: do not map `reading.triplets` directly to P-S04 copy. | 328 naïve bind = FAIL Knowledge 15 §18. |
| `domains` | per triple | `TripleOccurrence.domains` | **absent** | ENGINE_MISSING | — | — |
| `priority` featured/standard/compact | 827/278/786 featured | presentation from wealth/chain flags | **absent** | ENGINE_MISSING / ADAPTER later | Do not infer from Cát/Hung. | — |

---

### P-S05 Energy Distribution

| UI field | Golden | Canonical runtime | Live candidate | Verdict | Required work | Customer safety |
|---|---|---|---|---|---|---|
| 8 energies catalog order | §19 | `energy_distribution` all 8 keys | `reading.groups[]` only present 4 | ENGINE_MISSING + API_MISSING | Emit 8-count vector including zeros. Adapter must not invent catalog order in UI; engine/adapter contract may fill zeros from catalog. | Count is not a score. |
| counts Sinh Khí 2, Thiên Y 2, Diên Niên 3, Họa Hại 1, four zeros | §19 / fixture object | pair energy counts | group `pairs[]` lengths happen to match present energies | ADAPTER (risky derive) + ENGINE_MISSING | Approved field is distribution object. Deriving from groups drops zeros. | `energy_id` UNSAFE. |
| role primary/secondary | Diên Niên chủ đạo | chain primary/secondary | `reading.dominant` | ADAPTER + ENGINE_MISSING | Mark from chain, not from max count in UI. | — |

---

### P-S06 Domain Insights

Required five: Tài vận, Công việc & sự nghiệp, Tình cảm & quan hệ, Tính cách & năng lực, Cân bằng trường khí. Optional Giao tiếp is not a 6th required card.

| UI field | Golden | Canonical runtime | Live candidate | Verdict | Required work | Customer safety |
|---|---|---|---|---|---|---|
| 5 domain cards | §35–39 | `NumberEnergyFinding[]` filtered | **absent** | ENGINE_MISSING + API_MISSING | Domain resolver after evidence. | Wealth domain ≠ Wealth Flow verbatim. |
| conclusion / narrative / caution | fixture copy | `narrative_keys` + catalog | `narrative.paragraphs` / health lines | DO_NOT_BIND | Catalog keys only. | Health/organ wording UNSAFE. No cam kết tài chính. No marriage prediction. |

---

### P-S07 Strengths & Cautions

| UI field | Golden | Canonical runtime | Live candidate | Verdict | Required work | Customer safety |
|---|---|---|---|---|---|---|
| 4 strengths | §41 titles + evidence 827/787-878/786/328 | approved narrative keys | `narrative.strengths` (4 energy blurbs) | DO_NOT_BIND + ENGINE_MISSING | Findings/narrative keys, not `expert_notes`. | Live 4 items are catalog-by-energy, not Golden cards. |
| 2 cautions | §42 | approved keys | `narrative.watchouts` (4 items) | DO_NOT_BIND + ENGINE_MISSING | Count 4≠2. Copy mismatch. | Not traffic-light red. |
| `groups[].strength` / `watchout` | — | — | same engine blurbs | DO_NOT_BIND | — | — |

---

### P-S08 Score Breakdown

| UI field | Golden | Canonical runtime | Live candidate | Verdict | Required work | Customer safety |
|---|---|---|---|---|---|---|
| `82 / 100` | §43 | `PhoneScoreResult.final_score` | **absent** | ENGINE_MISSING + API_MISSING | Score after interpret. Current tests assert no `score` in data. | Static note stays until verified. |
| `TỐT` | §43 | `grade` | **absent** | ENGINE_MISSING + API_MISSING | — | No percent. |
| 5 rows 21/25 … 12/15 | §43 | component scores | **absent** | ENGINE_MISSING + API_MISSING | `energy_structure_score`, `wealth_flow_score`, `career_support_score`, `stability_risk_score`, `tail_score` | Do not reverse-engineer from fixture. |
| 4 reasons | §44–47 | `score_reasons` | **absent** | ENGINE_MISSING + API_MISSING | Keys → catalog copy. | Score must not drive narrative truth. |

---

### P-S09 Final Assessment & Recommendation

| UI field | Golden | Canonical runtime | Live candidate | Verdict | Required work | Customer safety |
|---|---|---|---|---|---|---|
| assessment story | §48 full version | compose wealth + chain + catalog | `reading.summary` / `narrative.summary` / paragraphs | DO_NOT_BIND + ENGINE_MISSING | No LLM. Catalog compose. | Health paragraphs UNSAFE. |
| recommendation copy | §49 | catalog after recommendation rule | `reading.purpose_note` | DO_NOT_BIND + ENGINE_MISSING | Not yet a runtime rule. | No “đổi số ngay”. |
| state `PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG` | §50 | recommendation state enum | **absent** | ENGINE_MISSING + API_MISSING | Explicit state field. | Fixture until rule exists. |

---

### P-S10 Basis of Assessment

| UI field | Golden | Canonical runtime | Live candidate | Verdict | Required work | Customer safety |
|---|---|---|---|---|---|---|
| helper + principles | §52 | catalog | **absent** | ENGINE_MISSING / CATALOG | — | No raw enums. |
| highlights (Diên Niên · pairs 827/278/786 · 86 · 8/7/1) | §51 | `evidence_refs` grouped customer-safe | scattered pairs/triples/counts | ENGINE_MISSING + DO_NOT_BIND (raw metadata) | Group evidence_refs. Do not dump `knowledge_version`. | `verified_by_runtime` / `fixture_id` / `knowledge_version` must not show. |
| evidence groups | §51 | evidence_refs | **absent** | ENGINE_MISSING + API_MISSING | — | — |

---

### P-S11 Expert seam

| UI field | Golden | Canonical runtime | Live candidate | Verdict | Required work | Customer safety |
|---|---|---|---|---|---|---|
| hidden seam | §53; DOM hidden | remaining trace | entire `occurrences` / `metadata` / `narrative.paragraphs` | DO_NOT_BIND into Customer Mode | Keep hidden. No `?expert=true`. Later Expert may consume UNSAFE trace. | Freeze: still placeholder, not live runtime. |

---

## 2. Group maps (explicit)

### Identity / display number

| Item | Verdict |
|---|---|
| `metadata.input_raw` → original_input | DIRECT |
| `reading.display_number` → grouped Hero identity | ADAPTER (needs grouping) |
| Canonical `display_value` field | ENGINE_MISSING / API_MISSING |
| `analyzed_input` / `analyzed_number` | DO_NOT_BIND Customer |

### Analysis type / purpose context

| Item | Verdict |
|---|---|
| `metadata.purpose_context` | ADAPTER → “Số điện thoại” |
| raw enum on screen | DO_NOT_BIND |
| `motorbike_plate` vs `motorcycle_plate` | API/Presentation gap (RB03) |

### Pair sequence

| Item | Verdict |
|---|---|
| `reading.pairs[].pair_digits` ordered | DIRECT (structure) |
| `occurrences[]` same order | ADAPTER verify; fields UNSAFE |
| UI parse digits into pairs | DO_NOT_BIND |

### Pair category Cát/Hung

| Item | Verdict |
|---|---|
| `kind` supportive/challenging | ADAPTER remap; raw UNSAFE |
| `classification*` | DO_NOT_BIND |
| Canonical category on PairOccurrence | ENGINE_MISSING |

### Pair strength Nhẹ/Mạnh + visual

| Item | Verdict |
|---|---|
| `force_label` lực nhẹ/mạnh | ADAPTER (lossy); 086 `lực rất mạnh` not in frozen union |
| `force_level` | DO_NOT_BIND |
| `strength_rank` | DO_NOT_BIND (inverted vs customer) |
| T1–T4 | Expert only |
| `strength_label` + dots from matrix | ENGINE_MISSING |

### Primary / terminal energy

| Item | Verdict |
|---|---|
| `reading.dominant.display_name` | ADAPTER candidate (label) |
| `reading.ending.display_name` / `pair_digits` | ADAPTER candidate (label) |
| `NumberEnergyChain.primary_energy` / `terminal_energy` | ENGINE_MISSING + API_MISSING |
| `energy_id` / `dominant_energy_ids` | UNSAFE / DO_NOT_BIND |

### Quick Structure 7/1

| Item | Verdict |
|---|---|
| `supportive_group_count` / `challenging_group_count` | DO_NOT_BIND |
| `pair_summary` pair counts | ENGINE_MISSING + API_MISSING |

### Wealth Flow 4 stage

ENGINE_MISSING + API_MISSING. DO_NOT_BIND `reading.summary` and raw triples as stages.

### Triple Story + canonical meaning keys

| Item | Verdict |
|---|---|
| `reading.triplets[].digits` | ADAPTER structure only |
| `left_name` / `right_name` | ADAPTER labels only |
| `canonical_meaning_key` / `customer_summary_key` | ENGINE_MISSING + API_MISSING |
| Direct copy from left+right names | DO_NOT_BIND |

### Distribution 8 energy counts

ENGINE_MISSING + API_MISSING as object. Groups omit zeros. energy_id UNSAFE.

### 5 Domain Insights / findings

ENGINE_MISSING + API_MISSING. `narrative.paragraphs` DO_NOT_BIND.

### Strengths / Cautions

ENGINE_MISSING approved keys. Live `narrative.strengths` / `watchouts` DO_NOT_BIND.

### Score / grade / breakdown / reasons

ENGINE_MISSING + API_MISSING entire `PhoneScoreResult`.

### Final Assessment / Recommendation

ENGINE_MISSING compose + recommendation state. Live summaries DO_NOT_BIND.

### Basis evidence

ENGINE_MISSING `evidence_refs`. metadata versions DO_NOT_BIND.

### P-S11 Expert seam

DO_NOT_BIND to Customer. Keep hidden. Remaining trace stays expert.

---

## 3. Adapter-candidate fields (after RB04; not bind today)

Allowed as **inputs to a future adapter**, not Customer DOM:

| Live field | Future slot | Adapter duty |
|---|---|---|
| `reading.pairs[].pair_digits` | P-S01 digits | Identity pass-through. Keep order including duplicate 78. |
| `reading.pairs[].display_name` | P-S01 energyLabel | Pass-through Vietnamese label until canonical energy_label exists. |
| `reading.dominant.display_name` | P-S00 / P-S02 primary | Label only, after primary≡dominant is proven by chain. |
| `reading.ending.display_name` | P-S00 / P-S02 terminal | Label only. |
| `reading.ending.pair_digits` | terminal pair 86 | Pass-through. |
| `reading.triplets[].digits` | P-S04 structure | Order only. No copy. |
| `metadata.input_raw` | original_input | Pass-through. |
| `metadata.purpose_context` | analysis type | Enum → customer label. |
| `reading.display_number` | identity | Grouping only; do not parse pairs. |

Not adapter-candidate for Customer: group counts, `narrative.*` prose, `occurrences` technical fields, `force_level`, English `kind` as visible text.

---

## 4. Do-not-bind fields (Customer Mode)

Never render raw:

- `occurrence_id`
- `source_span`
- `energy_id` (`yan_nian`, `tian_yi`, `huo_hai`, `sheng_qi`, …)
- `strength_rank`
- `classification` / `classification_label`
- `state` / `sequence_state` (`NORMAL`, `REPEATED`, `HIDDEN`)
- `via_modifier`
- `occurrences[].notes`
- `metadata.*` technical (`engine`, `engine_version`, `knowledge_version`, `raw_digits`, `sequence_states`, `summary.*_ids`, `fu_wei_supported`, `approved_supportive_chain`, `strongest_rank`, `pattern_labels`)
- `narrative.paragraphs` (span, rank, health/organ)
- health/organ wording anywhere
- `analyzed_input` / `reading.analyzed_number`
- `force_level`
- English `kind` (`supportive` / `challenging`)
- `request_id`
- `reading.cccd_note`
- `reading.layout` / `version` / `incomplete`
- raw `warnings[]` / `patterns[]`
- `fixture_id` / `presentation_fixture` / `verified_by_runtime` if they appear later

Supporting cases:

- **0868271327:** `force_label=lực rất mạnh`; hung pairs 71+32 but `challenging_group_count=1`.
- **103:** `sequence_state=HIDDEN`; `expression=Bị che bởi số 0`; no triplets; 3-digit `phone_number`.

---

## 5. Missing field groups for RB03

Do not start RB03 in this ticket. Input list only.

### ENGINE

- `PhoneScoreResult`: `final_score`, `grade`, five component scores, `score_reasons`
- Phone Wealth Flow Resolver: 4 stages, `wealth_presence`, `wealth_sources`, `wealth_destinations`, `later_outcome`, `WealthNode[]`
- `NumberEnergyChain` (`primary_energy`, `secondary_energy`, `terminal_energy`, `terminal_state`)
- `TripleOccurrence.canonical_meaning_key` / `customer_summary_key` / `interaction_id` / domains
- `NumberEnergyFinding[]` + five required domains
- Approved strength/caution narrative keys (4+2)
- Final assessment compose + recommendation **state**
- `evidence_refs` / basis groups
- Canonical `PairOccurrence` (`strength_label`, `position_zone`, `distance_to_tail`, customer category)
- `pair_summary` (pair counts 7/1, not groups)
- `energy_distribution` 8 keys including zeros
- `verified_by_runtime`
- Grouped `display_value` (if not left to adapter-only)

### API

- Expose the engine objects above on `data` (not only `reading` helper)
- Today `data` has no `score`, `grade`, `wealth_flow`, `findings`, `chain`, `evidence`
- Align `motorbike_plate` vs `motorcycle_plate` naming
- Do not add Customer-unsafe fields as the public customer contract

### ADAPTER (after RB04; no code now)

- Group phone display `0328278786` → `0328 278 786`
- `purpose_context` → analysis type label
- `kind` → Cát/Hung (never show English)
- `force_label` → Nhẹ/Mạnh **only if** engine contract guarantees the frozen two-value set (currently does not)
- Triple **digits/order** only until meaning keys exist
- Catalog key → frozen customer copy
- Keep P-S11 hidden

### CATALOG (already in Knowledge; engine must return keys, not UI guess)

- Pair keywords / energy short meanings (`02`, `10`)
- Triple titles/narratives (`12_TRIPLE_COMBINATION_CATALOG`)
- Wealth stage copy (`13_PHONE_WEALTH_FLOW_RULES`)
- Domain / finding copy
- Score reason copy (`14_PHONE_SCORE_MODEL`)
- Hero short / Final Assessment full / recommendation copy
- Strength dots from strength matrix (`03_PAIR_STRENGTH_MATRIX`)

### Locked RB03 gaps (must appear)

- score
- grade
- score breakdown
- score reasons
- wealth flow 4 stage
- triple canonical meaning key
- domain insights
- findings
- recommendation
- basis/evidence
- grouped display
- pair_summary counts
- distribution 8 energy

---

## 6. Risks / gaps

1. **Group count trap:** `supportive_group_count=3` vs Golden 7 cặp. 086: two hung pairs, still `challenging_group_count=1`.
2. **Dominant ≠ primary:** live Hero-looking label comes from `reading.dominant`, not `chain.primary_energy`.
3. **Triple naïve meaning:** binding `left_name`+`right_name` as P-S04 copy violates khẩu tài rule for 328.
4. **Inverted rank:** `strength_rank=4` on 32 Họa Hại is Nhẹ. Mapping rank to dots or Hero score FAIL.
5. **Third strength wording:** `lực rất mạnh` (086, 103) vs frozen `Nhẹ | Mạnh`.
6. **Score absence is current API truth;** tests assert no score. Do not fake 82 as runtime.
7. **103 as phone_number:** short input + interior zero `HIDDEN` — product/input-contract gap, not a Golden substitute.
8. **Health prose** in `narrative.paragraphs` would leak into any “use narrative” shortcut.
9. Leftover portal `types.ts` / `readingTypes.ts` / `api.ts` describe this old payload. Do not resume them as the adapter.

---

## 7. Intentionally not changed

- Frontend, backend, engine, tests
- Golden Fixture, snapshots, expected outputs
- Knowledge / Presentation specs (`01`, `03`, `04`, `15` unread-only)
- No adapter code, no fetch, no `api.ts` import into NumberEnergyPage
- No nav, no Expert Mode, no P-S11 bind
- BaZi, Good Date, Marriage untouched
- RB03/RB04 not started

---

## 8. Next allowed stage

**RB03 — GAP REPORT FOR MISSING FIELDS**

Use this mapping + the locked missing list. Do not write adapter code. Do not start RB05.
