# HK-R1 — Dụng / Hỷ / Kỵ semantic & reconciliation audit

**Date:** 2026-08-20  
**Mode:** Audit only. No engine, CSV, presentation, Golden, or G1-FINAL change.  
**Pipeline measured:** production `UsefulGodEngine` V2 (`database/13_useful_god`) after UG-R3F + PAT-R1F.

## Status

**HK-R1: MIXED PRESENTATION + KNOWLEDGE GAP — REVIEW REQUIRED**

---

## 1. Canonical semantic definitions

Searched: `knowledge/` (interpretation domains, concepts, glossary, useful-god packs, governance), `database/13_useful_god`, `engines/interpretation_engine/knowledge/03_terminology`, rule packs, Gate 1 audits. No web theory.

| Concept | Canonical definition (quoted / close paraphrase) | Source | Runtime representation |
|---------|--------------------------------------------------|--------|------------------------|
| Dụng thần / 用神 / Useful God | “Yếu tố Ngũ Hành hoặc Thập Thần được lựa chọn làm **trọng tâm để điều hòa và hoàn thiện** cấu trúc của mệnh cục.” | `engines/interpretation_engine/knowledge/03_terminology/useful_god_terms.json` `dung_than` | `UsefulGodResult.useful_god` → G1-01 `useful_display` (`Element · Stem · Ten God`) |
| Hỷ thần / 喜神 / Favorable God / Xi Shen | “Yếu tố **hỗ trợ hoặc tăng cường hiệu quả của Dụng Thần**.” “mang lại tác động thuận lợi … **sau khi Dụng Thần đã được xác định**.” | same file, `hy_than` | `favorable_gods` / `favorable_display` |
| Kỵ thần / 忌神 / Unfavorable God / Ji Shen | “Yếu tố có xu hướng **làm suy giảm hoặc phá vỡ tác dụng của Dụng Thần**.” | same file, `ky_than` | `unfavorable_gods` / `unfavorable_display` |

Governance glossary **example** of a common misunderstanding: “Many beginners confuse Dụng Thần with Hỷ Thần” (`knowledge/governance/standards/08_GLOSSARY_STANDARD.md` §18). That is a style example, not a full definition, but it treats the two names as distinct terms.

Interpretation domain files (e.g. `thuc_than.json`, `at.json`, `giap.json`) assign **one role per decision**: “Khi được chọn làm Dụng thần … Khi thuộc Hỷ thần … không thay Dụng … ưu tiên thấp hơn Dụng.” Concepts:

- `drain_strong_day_master.json`: Dụng = thoát khí; Hỷ = hỗ trợ kênh thoát, **không tranh vai trò chính**; Kỵ = sinh/kiến thêm vào thân vượng.
- `output_role.json`: Hỷ = “cùng nhóm hỗ trợ kênh thoát, không tranh vai chính.”
- `support_day_master.json`: Dụng = phù trợ; Hỷ = gia cố hướng nâng; Kỵ = **tiết/khắc nhật chủ**.

### Direct answers (no inference beyond sources)

| Question | Evidence |
|----------|----------|
| Is Dụng the primary corrective/balancing force? | **Yes.** Terminology: trọng tâm điều hòa. Domain: “hướng cân bằng chính.” |
| Is Hỷ a supporting/favorable force? | **Yes.** Terminology: hỗ trợ / tăng cường Dụng. Domain: không thay Dụng, ưu tiên thấp hơn. |
| Is Kỵ an aggravating/opposing force? | **Yes.** Terminology: suy giảm / phá tác dụng của Dụng. |

### Does canonical BTE **explicitly** allow `Dụng ∈ Hỷ`?

**Split. Do not collapse to one frozen theory.**

| Layer | Explicit stance |
|-------|-----------------|
| Interpretation terminology + domain role files | Hỷ is defined as a **different role** (support of Dụng). Files describe an entity as Dụng **or** Hỷ **or** Kỵ in a given decision. They do **not** say “print Dụng as the first Hỷ line.” |
| `bz_07_useful_god_priority` | **Yes, as a set-alignment check.** `reinforce_favorable_contains_useful` (“Củng cố khi Hỷ chứa Dụng”). `detect_useful_not_in_favorable` is a **conflict** if Dụng is missing from Hỷ. `detect_useful_in_unfavorable` is a conflict if Dụng is in Kỵ. |
| Production CSV `database/13_useful_god` | Every Overall structural row **authors** `useful_god` as the first member of `favorable_gods`. |
| Analyze runtime | Does **not** execute bz_06/bz_07. Copies the CSV winner row (see §2). |

No production document says customer Hỷ **must** repeat the full `Element · Stem · Ten God` Dụng line.

---

## 2. Current data model / production path

**Hỷ/Kỵ are copied from the Overall winner CSV row. Not independently calculated. Renderer does not reconstruct gods.**

```
database/13_useful_god/{01_strength,04_flow,06_special}_rules.csv
  columns: useful_god, favorable_gods, unfavorable_gods
        ↓ matcher (conditions only)
UsefulGodEngine.calculate
  overall = PriorityResolver(overall_candidates)
  favorable  = parse(overall["favorable_gods"])     # engine.py
  unfavorable = parse(overall["unfavorable_gods"])
        ↓ enrich_useful_god_result (roles.py)
  G1-01 map each token → stem / element / ten_god
  useful_display / favorable_display / unfavorable_display
        ↓ UsefulGodView / useful_god_truth.py
        ↓ rule_context_bridge overlays pattern.hy_than / ky_than / dung_than
        ↓ ReportInputV1Adapter copies useful.favorable_display
        ↓ Report V1 HTML / PDF / DOCX section 07
        ↓ Portal canonicalUsefulGod.ts copies favorable_display (no derive)
```

| Question | Answer |
|----------|--------|
| A. Independently calculated? | **No** on the Analyze path. |
| B. Copied from winner CSV? | **Yes.** |
| C. Renderer reconstructs? | **No.** Formats tokens already on the result. |
| D. Mixture? | Overlay only: Pattern `hy_than` is **replaced** from UG after merge. Climate Hỷ/Kỵ on `sea_*`/`tmp_*` are **not** copied into Overall Hỷ/Kỵ (UG-R2). Non-winning `flo_*` Hỷ/Kỵ are discarded. |

G1-06 already recorded the same fact: “Hỷ rule? **Not an independent engine.** Copied from winning rule `favorable_gods`.”

bz_06 `candidate_favorable_gods.json` / `candidate_unfavorable_gods.json` exist as a **separate** Hỷ/Kỵ candidate layer. `OrchestratorService` Analyze uses `UsefulGodEngine`, not that pack.

---

## 3. CSV / rule schema (Overall structural)

`favorable_gods` always includes the `useful_god` token for every Overall row that can win.

| Rule | Pri | Dụng token | Hỷ raw | Kỵ raw | Includes Dụng in Hỷ? | 101 winners (PAT-R1F) |
|------|----:|------------|--------|--------|----------------------|----------------------:|
| `str_001` | 80 | Chính Ấn | Chính Ấn, Thiên Ấn, Tỷ Kiên | Chính Tài, Thiên Tài | **Yes** | 1 |
| `str_002` | 78 | Thiên Ấn | Thiên Ấn, Chính Ấn, Kiếp Tài | Chính Tài, Thiên Tài | **Yes** | 15 |
| `str_003` | 82 | Chính Quan | Chính Quan, Thực Thần | Tỷ Kiên, Kiếp Tài | **Yes** | 45 |
| `str_004` | 76 | Thực Thần | Thực Thần, Thương Quan | Tỷ Kiên, Kiếp Tài | **Yes** | 7 |
| `str_005` | 70 | Chính Tài | Chính Tài, Thực Thần | Kiếp Tài | **Yes** | 29 |
| `spc_001` | 95 | Chính Tài | Chính Tài, Thiên Tài | Chính Ấn, Thiên Ấn | **Yes** | 3 |
| `spc_002` | 95 | Chính Quan | Chính Quan, Thất Sát | Tỷ Kiên, Kiếp Tài | **Yes** | 0 |
| `spc_003` | 95 | Thất Sát | Thất Sát, Chính Quan | Tỷ Kiên, Kiếp Tài | **Yes** | 1 |
| `spc_004` | 92 | Thiên Ấn | Thiên Ấn, Chính Ấn | Chính Tài, Thiên Tài | **Yes** | **0** (PAT-R1F suppressed) |
| `flo_001`–`004` | 74 | stem | sibling stems | opposing stems | **Yes** | 0 Overall (candidate only) |

Climate `sea_*` / `tmp_*` also include Dụng-in-Hỷ, but they must not win Overall (UG-R2). Their lists never become customer Hỷ/Kỵ.

**Count:** 9/9 Overall structural families author Dụng inside Hỷ. **101/101** live winners inherit that.

`str_004` specifically: Dụng = Thực Thần; Hỷ = `[Thực Thần, Thương Quan]`. Thực Thần **is** in Hỷ because the CSV list starts with the Dụng token, then the sibling Output.

---

## 4–5. 101-case duplication (after UG-R3F + PAT-R1F)

n=101. Incomplete=0.

| Relationship | Cases | % |
|--------------|------:|--:|
| A. Exact Dụng repeated in Hỷ (same element **and** stem **and** ten god) | **101** | **100%** |
| of which exact + at least one other Hỷ entry | 101 | 100% |
| of which Hỷ is **only** the Dụng line | **0** | 0% |
| B. Same element, different stem/ten god (in addition to A) | 27 | 26.7% |
| C. Dụng not repeated | **0** | 0% |

Cross-tab by winning rule: every rule is `exact_plus_others` for all of its winners (`str_003` 45, `str_005` 29, `str_002` 15, `str_004` 7, `spc_001` 3, `str_001` 1, `spc_003` 1).

Duplication is **systemic**, not a Dũng-only display bug.

Levels must stay separate:

- Dũng `Thủy · Nhâm · Thực Thần` vs `Thủy · Quý · Thương Quan` = same **element**, different stem, different ten god → **not** exact duplication.
- Dũng first Hỷ line `Thủy · Nhâm · Thực Thần` = **exact** duplication of Dụng.

---

## 6. Ngô Đắc Dũng

Canonical (live Analyze, PAT-R1F): Ất Sửu / Ất Dậu / Canh Thân / Canh Thìn · Canh · **1.00 strong** · `gia_sac` LEVEL-1 override false.

| Field | Value |
|-------|--------|
| Overall | `str_004` Thủy · Nhâm · Thực Thần |
| Hỷ | Thủy · Nhâm · Thực Thần / Thủy · Quý · Thương Quan |
| Kỵ | Kim · Canh · Tỷ Kiên / Kim · Tân · Kiếp Tài |
| Điều hậu | `sea_004` Hỏa · Đinh · Chính Quan |

**Why Hỷ contains Nhâm · Thực Thần and Quý · Thương Quan**

Not because the engine computed “Dụng is also favorable.”  
Because `str_004.favorable_gods = ["Thực Thần","Thương Quan"]` is a **static sibling Output pair**. G1-01 maps:

- Canh × Thực Thần → Nhâm / Thủy
- Canh × Thương Quan → Quý / Thủy

Nhâm is in Hỷ **because it is the Dụng token**, listed first in CSV. Quý is the paired Output, not a second calculated support of Nhâm.

Climate Hỏa is **not** merged into Hỷ (UG-R2). `flo_003` (Kim quá thịnh → Hỏa) is an Overall **candidate** on this chart class in other dumps; it does not donate Hỷ/Kỵ unless it wins (priority 60 < strength 80).

---

## 7. Vũ Thị Thanh Tuyền

Birth used in G1-X01 / UG-R3F: **1984-07-13 21:01** female. Chart Giáp Tý / Tân Mùi / Mậu Thân / Quý Hợi · Mậu · **0.66 strong** · Pattern `kiep_tai` (follow gated).

| Field | Live |
|-------|------|
| Overall | `str_003` Mộc · Ất · Chính Quan |
| Hỷ | Mộc · Ất · Chính Quan / Kim · Canh · Thực Thần |
| Kỵ | Thổ · Mậu · Tỷ Kiên / Thổ · Kỷ · Kiếp Tài |
| Điều hậu | `sea_002` Thủy · Nhâm · Thiên Tài |

**Does Hỷ repeat Ất · Chính Quan?** **Yes** — first Hỷ line is exact Dụng (`str_003.favorable_gods` starts with Chính Quan).

**Does Hỷ then add Canh / Thực Thần?** **Yes** — second CSV token. For Mậu, Thực Thần = Canh / Kim.

Rule semantics: `str_003` = strong + Chính Quan reachable → Dụng = Chế (Quan); Hỷ list = Quan + Output (Chế **and** Tiết as a **set**). That set matches unused pack `cand_fav_officer_set` (“Hỷ thần khi thân vượng: Quan + Thực”), which also **includes** Chính Quan when Dụng is Chính Quan.

---

## 8. Cao Xuân Trường

Live reconstruct matching the stated Current (weak Nhâm, Dụng Kim · Tân · Chính Ấn): **1989-07-21 15:45** male · Kỷ Tỵ / Tân Mùi / Nhâm Ngọ / Mậu Thân · Nhâm · **0.34 weak** · Pattern `quan_an`.

| Field | BTE |
|-------|-----|
| Overall | `str_001` Kim · Tân · Chính Ấn |
| Hỷ | Kim · Tân · Chính Ấn / Kim · Canh · Thiên Ấn / Thủy · Nhâm · Tỷ Kiên |
| Kỵ | Hỏa · Đinh · Chính Tài / Hỏa · Bính · Thiên Tài |
| Điều hậu | `sea_002` Thủy · Nhâm · Tỷ Kiên |
| G1-05 | Mộc1 · Hỏa5 EXCESS · Thổ7 EXCESS · Kim4 EXCESS · Thủy2 |

Reference (not oracle): Dụng Kim, Hỷ Thủy, Kỵ Hỏa + Thổ.

**Kỵ is winner-row-only.** `str_001.unfavorable_gods = [Chính Tài, Thiên Tài]` → Fire for Nhâm. Officer/Killings for Nhâm are **Earth** (khắc nhật chủ). Earth EXCESS 7 never enters Kỵ.

Interpretation concept `support_day_master.json` Kỵ = “Tiết/khắc nhật chủ.” Production weak Kỵ pack (`cand_unfav_weak_wealth` and CSV) lists **Tài only**, not Quan/Sát and not Output. So BTE **omits** the Earth officer force that would further weaken an already weak Nhâm. That is a **knowledge-completeness** limit of the static row, not a chart-specific calculation.

Hỷ includes Tỷ Kiên = the day master stem Nhâm (CSV third token), plus duplicated Dụng Kim.

---

## 9. Lưu Hoàng Sơn

Live reconstruct matching Current (balanced Canh, Dụng Mộc · Ất · Chính Tài, Điều hậu Hỏa / Cần ôn ấm): **1996-11-29 17:20** male · Bính Tý / Kỷ Hợi / Canh Ngọ / Ất Dậu · Canh · **0.51 balanced**.

| Field | BTE |
|-------|-----|
| Overall | `str_005` Mộc · Ất · Chính Tài |
| Hỷ | Mộc · Ất · Chính Tài / Thủy · Nhâm · Thực Thần |
| Kỵ | Kim · Tân · Kiếp Tài |
| Điều hậu | `sea_001` Hỏa · Bính · Thất Sát |
| G1-05 | Thủy **4 EXCESS** (dominant water), Hỏa 3 EXCESS, Kim 3 EXCESS |

Reference (not oracle): Water excessive.

**BTE has no production mechanism that adds an element to Kỵ from whole-chart excess/pressure.** Five Elements publishes `status=EXCESS` / `dominant=water` with an explicit disclaimer that count is **not** Dụng. Useful God does not read those statuses. Flow `flo_*` can match “element key present” (G1-06: even count=1 is labeled quá thịnh) but **never wins Overall**, so its Hỷ/Kỵ never publish. Kỵ here is exactly `str_005` → `[Kiếp Tài]` (peer Metal). Water is absent from Kỵ.

---

## 10. Phạm Thị Huyền

Live reconstruct matching Current (strong Kỷ, Overall Kim · Tân · Thực Thần): **1987-09-07 02:00** female · Đinh Mão / Mậu Thân / Kỷ Mùi / Ất Sửu · Kỷ · **0.74 strong**.

| Field | BTE |
|-------|-----|
| Overall | `str_004` Kim · Tân · Thực Thần |
| Hỷ | Kim · Tân · Thực Thần / Kim · Canh · Thương Quan |
| Kỵ | Thổ · Kỷ · Tỷ Kiên / Thổ · Mậu · Kiếp Tài |
| Điều hậu | `sea_004` Hỏa · Đinh · Thiên Ấn |
| G1-05 | Thổ 7 EXCESS, Mộc 4 EXCESS, Hỏa 2 STRONG (Resource for Kỷ) |

**Why Kỵ includes Thổ but not Hỏa/Resource:** `str_004.unfavorable_gods = [Tỷ Kiên, Kiếp Tài]` always. For Kỷ those are Earth peers. Resource for Kỷ is Fire. The row never lists Ấn. Generation does **not** read Strength support sources, Resource, Peer lists, season, or element state — only winner-row labels.

Same Hỷ/Kỵ template as Lương Văn Mạnh (`str_004`). Chart-specific Resource Fire never appears.

---

## 11. Lương Văn Mạnh

Chart: Đinh Mão / Đinh Mùi / Kỷ Dậu / Đinh Mão · Kỷ · **1.00 strong** · `jia_wang` LEVEL-1. Live birth **1987-06-29 06:00** male matches those pillars.

| Field | BTE |
|-------|-----|
| Overall | `str_004` Kim · Tân · Thực Thần |
| Hỷ | Kim · Tân · Thực Thần / Kim · Canh · Thương Quan |
| Kỵ | Thổ · Kỷ · Tỷ Kiên / Thổ · Mậu · Kiếp Tài |
| Điều hậu | `sea_002` Thủy · Nhâm · Chính Tài |
| Overall candidates | `str_004`, `flo_002` (Hỏa quá thịnh → Thủy) — flow does not win |

**Can current Hỷ express “Kim supports the Dụng path” without duplicating Dụng?**

Internally: Hỷ = `[Thực Thần, Thương Quan]` → Tân (Dụng) + Canh (sibling Output), **same element Kim**.

If the exact Dụng line is dropped, remaining customer Hỷ = **Kim · Canh · Thương Quan**. That still says “Kim / Output supports the Tiết path” without repeating Tân · Thực Thần. No new rule is required for that remainder. Hao/Tài is out of scope (UG-R4).

---

## 12. Dụng vs Hỷ semantic model

**MODEL C (knowledge inconsistent) plus production MODEL A (set copy), with unused independent Hỷ packs.** Closest single architecture label: **C + A at runtime, B in customer glossary.**

| Evidence | Model |
|----------|--------|
| CSV + Analyze copy | **A:** Dụng is a member of the favorable **set** |
| bz_07 `favorable_contains_useful` | **A:** missing Dụng-in-Hỷ is a **defect** |
| Terminology + domain “không thay Dụng” | **B:** distinct roles |
| Glossary example “beginners confuse Dụng with Hỷ” | **B** |
| bz_06 `cand_fav_*` as a **separate** publish of `favorable_gods` | Intended independent Hỷ candidates — **not loaded** by Analyze |
| `roles.py` only formats the copied list | **D** only in the weak sense that display concatenates Dụng and Hỷ into parallel lines from one set |

Not a single intended frozen theory. Product Owner’s “should not automatically be identical concepts” matches **B (glossary)** and contradicts **CSV/A** as presented.

---

## 13. Hỷ generation

**Hỷ = static CSV list on the Overall winner row**, then G1-01 token mapping.

It is **not**:

- computed as “elements that generate/support Dụng”;
- “all favorable Ten Gods on the chart”;
- climate-aware;
- bz_06 `cand_fav_*` (those files exist, Analyze ignores them).

Sibling pattern is authoring convention: Output pair, Resource pair, Wealth pair, Officer pair.

---

## 14. Kỵ generation

**Kỵ = static CSV list on the same winner row**, then G1-01 mapping.

| Hypothesis | Production? |
|------------|-------------|
| Opposite of Dụng (five-element) | No (not computed) |
| Strength-based beyond the row that `strength_level` selected | No |
| Winner-row static list | **Yes** |
| Whole-chart excess | **No** |
| Pattern-derived | No (Pattern hy/ky overwritten from UG) |
| Independently reconciled (bz_07) | **No** on Analyze |

Weak template: Kỵ = Tài. Strong template: Kỵ = Tỷ/Kiếp. Balanced: Kỵ = Kiếp Tài only. Follow Tài: Kỵ = Ấn.

---

## 15. Whole-chart reconciliation matrix

| Input | Dụng selection | Hỷ | Kỵ |
|-------|----------------|----|----|
| StrengthResult `strength_level` | YES (chooses str_*) | NO (except via which row wins) | NO (same) |
| Strength score / roots / drain / control ledger | NO | NO | NO |
| PatternResult winner / follow / special | YES if override-eligible follow | NO | NO |
| Five Elements G1-05 counts / EXCESS | NO (disclaimer: not Dụng) | NO | NO |
| Ten Gods visible | Indirect (`officer_elements` for `str_003`) | NO | NO |
| Ten Gods hidden | Indirect (UG-R3F hidden Chính Quan) | NO | NO |
| Climate / Điều hậu | NO (UG-R2) | NO | NO |
| Overall Dụng token | YES | Copied into Hỷ list | Must not appear (CSV disjoint; bz_07 would conflict) |
| Candidate provenance of losers | NO | Discarded | Discarded |
| Root/support/drain as Hỷ/Kỵ drivers | NO | NO | NO |

---

## 16. G1-05

Occurrence counts **must not** become strength or auto Hỷ/Kỵ. Production already disclaims this.

**Is there another canonical element-state source that may identify excess/deficiency for Hỷ/Kỵ?**

- G1-05 `status=EXCESS` / `MISSING` / `dominant` exist on the Five Elements payload and are **not** consumed by Useful God.
- Flow rules claim “quá thịnh” but match on key **presence**, not count, and never win Overall (G1-06).
- Legacy “tăng hành thiếu” rows are **not** loaded by UG V2 (UG-R4).

**Limitation:** V1.0 has **no** production Hỷ/Kỵ path from element-state. Do not invent one here.

---

## 17. Climate relation

UG-R2: Điều hậu ≠ Overall Dụng. Climate `favorable_gods` stay on the climate row and are **not** merged.

Dũng: Overall Thủy, climate Hỏa. **Should Hỏa appear as Overall Hỷ?** Canonical production knowledge **does not** say yes. Terminology splits Hàn thần / Điều hậu from Dụng/Hỷ. Do not change it.

Trường coincidence: climate display `Thủy · Nhâm · Tỷ Kiên` equals the third Hỷ token because `str_001` already lists Tỷ Kiên and `sea_002` token is stem Nhâm. That is **not** a merge.

---

## 18. Winner-row inheritance

Hỷ/Kỵ **flip wholesale** with the Overall winner. No residual from the previous row.

Observed recently (conceptual counts, Golden not updated):

| Repair | Winner change | Hỷ/Kỵ effect |
|--------|---------------|--------------|
| UG-R2 | `sea_*`/`tmp_*` leave Overall | Climate Hỷ/Kỵ no longer shown as Overall |
| UG-R3F | Tuyền `str_004` → `str_003` | Thực/Thương + Tỷ/Kiếp → Quan+Thực + Tỷ/Kiếp |
| PAT-R1F | 8× `spc_004` → `str_003` or `str_004` | Ấn/Tài pair → either Quan+Thực or Thực+Thương / Tỷ-Kiếp |

101 live Hỷ sets = **7** unique (exactly the 7 winning rule templates). Kỵ sets = **4** unique.

---

## 19. Exact-duplicate customer UX

**Engine semantics (CSV/A):** Dụng belongs to the favorable **set**.

**Customer presentation:** showing

```
Dụng: Thủy · Nhâm · Thực Thần
Hỷ:   Thủy · Nhâm · Thực Thần / Thủy · Quý · Thương Quan
```

is redundant and reads as if Dụng and Hỷ were the same concept. Glossary treats that confusion as a beginner error. Commercial UX is **not** forced by the SET model.

Separate ENGINE SEMANTICS from CUSTOMER PRESENTATION.

---

## 20. Safe presentation-only option (not implemented)

Keep internal `favorable_gods` unchanged (preserves bz_07 “Hỷ chứa Dụng” if that pack is ever wired).

Customer Hỷ display = favorable roles **minus the exact Dụng triple** (element+stem+ten god).

Dũng would become: Dụng = Nhâm/Thực Thần; Hỷ = Quý/Thương Quan.

**101/101 already have a remainder** (`exact_only` = 0). No chart would lose all Hỷ.

Meaning preserved: Dụng remains the primary; remaining Hỷ is the sibling/helper. Does **not** fix Kỵ completeness or whole-chart excess.

---

## 21. Kỵ completeness vs display

This is **not** display-only.

| Case | Static Kỵ | Canonical pressure not represented |
|------|-----------|-------------------------------------|
| Trường (weak Nhâm) | Fire Tài | Earth Officer/Killings (concept: khắc nhật chủ); Thổ EXCESS 7 unused |
| Lưu Hoàng Sơn (balanced Canh) | Kiếp Tài only | Water EXCESS unused |
| Huyền / Mạnh (strong Kỷ) | Earth peers | Fire Resource unused; G1-05 Thổ/Hỏa unused |

Classify: **KNOWLEDGE COMPLETENESS ISSUE** (static row), plus **DISPLAY ISSUE** on Hỷ duplication.

Do not author new Kỵ rules in V1.0.

---

## 22. 101 distribution

| Metric | Value |
|--------|------:|
| Exact Dụng-in-Hỷ | 101 / 101 |
| Same-element extra Hỷ | 27 / 101 |
| Average Hỷ entries | **2.16** |
| Average Kỵ entries | **1.71** |
| Unique Hỷ token-sets | **7** |
| Unique Kỵ token-sets | **4** |

Outputs are **templated by winning rule**, not chart-specific reconciliation.

---

## 23. Reference comparison (conceptual; not oracle)

| Case | Old Dụng | Old Hỷ | Old Kỵ | BTE Dụng | BTE Hỷ | BTE Kỵ | Difference type |
|------|----------|--------|--------|----------|--------|--------|-----------------|
| Dũng | (pre-PAT-R1F) Thổ · Mậu · Thiên Ấn via `spc_004` | Ấn pair | Tài pair | Thủy · Nhâm · Thực Thần | Dụng + Quý Thương Quan | Canh/Tân Tỷ Kiếp | BTE duplication + winner-row inheritance |
| Tuyền | (pre-UG-R3F) Kim · Canh · Thực Thần | Thực+Thương | Tỷ/Kiếp | Mộc · Ất · Chính Quan | Dụng + Canh Thực Thần | Mậu/Kỷ Tỷ Kiếp | BTE duplication; Chế vs Tiết theory shift |
| Trường | Kim | Thủy | Hỏa + Thổ | Kim · Tân · Chính Ấn | Dụng + Canh Thiên Ấn + Nhâm Tỷ Kiên | Hỏa Tài only | different theory on Hỷ; **BTE completeness** on Earth Kỵ |
| Lưu Hoàng Sơn | (ref) Water excess as problem | — | Thủy | Mộc · Ất · Chính Tài | Dụng + Nhâm Thực Thần | Tân Kiếp Tài | different theory; **BTE completeness** (no excess Kỵ) |
| Huyền | Kim/Tân/Thực | (dup) | Thổ peers | Kim · Tân · Thực Thần | Dụng + Canh Thương Quan | Thổ Tỷ/Kiếp | BTE duplication; completeness (no Resource Kỵ) |
| Mạnh | Thủy | Kim | Hỏa / Thổ | Kim · Tân · Thực Thần | Dụng + Canh Thương Quan | Thổ Tỷ/Kiếp | different theory (UG-R4 Hao gap); duplication on Hỷ |

---

## 24. Defect classification

**HK-R1: MIXED PRESENTATION + KNOWLEDGE GAP — REVIEW REQUIRED**

Not A: glossary and CSV disagree; 100% Dụng-in-Hỷ is not a documented customer rule.  
Not B only: Kỵ is statically incomplete vs interpretation concepts and vs G1-05 excess (unused).  
Not C only: exact Hỷ duplication is also a commercial presentation defect with a safe remainder.  
Not D as a V1.0 engine bug: Analyze is faithfully copying CSV; it is not secretly merging two computed Hỷ engines.

---

## 25. Minimum V1.0 recommendation (audit only — do not implement here)

1. **Do not** change Overall winners, Strength, Pattern, climate, CSV tokens, or Golden.
2. If Product Owner wants a freeze polish: **presentation-only** omit the exact Dụng triple from customer Hỷ (internal set unchanged). Safe on 101/101.
3. **Do not** invent excess-element Kỵ, Officer-on-weak Kỵ, or Resource-on-strong Kỵ in V1.0.
4. V1.1 backlog: independent Hỷ/Kỵ reconciliation (wire or retire bz_06 `cand_fav_*` / bz_07 set checks), decide SET vs distinct-role SSOT, Kỵ completeness vs winner-row templates.
5. Do **not** start G1-FINAL on this audit.

---

**HK-R1: MIXED PRESENTATION + KNOWLEDGE GAP — REVIEW REQUIRED**

STOP. No repair. No Golden. No G1-FINAL.
