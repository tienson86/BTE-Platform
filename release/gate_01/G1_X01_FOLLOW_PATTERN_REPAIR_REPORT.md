# G1-X01 — Follow Pattern Cross-Engine Consistency Repair

**Status:** `G1-X01 CROSS-ENGINE CONSISTENCY: REPAIRED — REFREEZE READY`

**Scope:** Pattern follow eligibility + token SSOT Pattern → Useful God.  
**Not in scope:** Strength weights/thresholds/season/root/drain. G1-05 occurrence distribution. G1-FINAL.

---

## Product-owner invariant (locked)

> Follow / Tòng (cực-nhược family) cannot publish when canonical Strength is `strong`.

Pipeline now:

```text
Canonical Strength
  → Follow eligibility gate
  → Follow rule conditions + ten-god evidence
  → Pattern priority
  → winner
  → follow token published only if winner is a follow rule
  → Useful God consumes the same machine token
```

Ten-god ratio remains evidence. It cannot override Strength.

---

## What changed

| Area | Change |
|------|--------|
| Strength engine / CSV | **Unchanged** |
| Follow detector | Reads canonical `strength_level` / StrengthResult equivalent |
| Follow validation | Rejects weak-follow CSV rows unless Strength is `weak` |
| Tòng Vượng | Separate gate: eligible only when Strength is `strong` (not the cực-nhược rule) |
| `balanced` | Not automatic follow of either family |
| Token SSOT | Machine `tong_tai` · display `Tòng Tài` |
| Useful God builder | Canonicalizes display → token; does not compare Vietnamese labels |
| Follow token publish | Token travels to Useful God **only when the winning pattern is a follow rule** |
| G1-05 Five Elements | **Unchanged** `Mộc3 · Hỏa1 · Thổ4 · Kim3 · Thủy6` |

---

## Vũ Thị Thanh Tuyền

Birth: 1984-07-13 21:01 female, `Asia/Ho_Chi_Minh`  
Chart: **Giáp Tý / Tân Mùi / Mậu Thân / Quý Hợi** · Nhật chủ **Mậu**

| Field | Before (Phase 1 audit) | After (Phase 2 live API) |
|-------|------------------------|---------------------------|
| Strength | **0.66 / strong** (raw 16) | **0.66 / strong** (raw 16) — unchanged |
| Pattern | `tong_tai` / Tòng Tài cách — Nhật chủ cực nhược theo Tài (`fol_ttai_01`) | `kiep_tai` / **Kiếp Tài** (`pat_ktai_01`) |
| `than_vuong_nhuoc` | Thân vượng | Thân vượng |
| `tong_cach` | Tòng Tài (contradiction) | Kiếp Tài |
| Useful God | Thủy · Nhâm · Thiên Tài (`sea_002`) | Thủy · Nhâm · Thiên Tài (`sea_002`) |
| `spc_001` | Did not win (token mismatch) | **Does not win** (no published follow token) |
| “cực nhược” in Pattern / Interpretation / Narrative / Report | Present on Pattern | **Absent** |
| G1-05 FE | Mộc3 · Hỏa1 · Thổ4 · Kim3 · Thủy6 | **Unchanged** |

Replacement Pattern was **not hard-coded**. After the Strength gate rejected `fol_ttai_01`, normal candidate selection published 月令 Kiếp Tài (`pat_ktai_01`, khí chính Mùi **Kỷ**).

### Pattern candidates before / after

CSV still *matches* follow rows on presence of Tài/Sát. Validation now drops them.

| Stage | Before | After |
|-------|--------|-------|
| CSV candidates | `chinh_quan`, `kiep_tai`, `tong_tai`, `tong_sat` | same |
| Validated | `kiep_tai`, `tong_tai` | **`kiep_tai` only** |
| Rejected follow | `fol_tsat_01` `follow_type_mismatch` | `fol_ttai_01` **`follow_strength_incompatible`** · `fol_tsat_01` **`follow_strength_incompatible`** |
| Winner | `fol_ttai_01` | `pat_ktai_01` |

### Useful God candidate trace (canonical priority)

| Rule | Group | Payload | Group priority | Why it matched |
|------|-------|---------|----------------|----------------|
| `str_004` | strength | Thực Thần / Canh | 80 | Strength `strong` → tiết khí |
| `sea_002` | season | Nhâm / Thiên Tài | **90** | Summer + `hot` |
| `tmp_002` | temperature | Quý / Chính Tài | 70 | `hot` overlay |
| `flo_004` | flow | Mậu / Tỷ Kiên | 60 | Engine dist unique-max **Thủy** (see below) |
| `spc_001` | special | — | 100 | **Not a candidate** — Pattern did not publish `tong_tai` |

**Winner: `sea_002`** because season group (90) beats strength (80), temperature (70), and flow (60).  
Do **not** force Mộc / Thủy / Nhâm / Chính Tài. Nhâm remains the V1.0 winner on this legitimate seasonal path. The old ChatGPT Mộc reference is a different theory path; not an oracle.

`spc_001` must not win for Tuyền merely because tokens were normalized. It does not: Tuyền is strong, Tòng Tài is invalid, no follow token is published.

---

## `flo_004` check

Engine `element_distribution` for this chart (stems + hidden, **not** the G1-05 customer card):

`Mộc 3 · Kim 2 · Thổ 3 · Thủy 4 · Hỏa 1`

G1-06 `contains` on a mapping is **unique maximum**, not key presence. Thủy 4 > max(others 3) → `flo_004` is legitimate.  
G1-05 customer occurrence **Mộc3 · Hỏa1 · Thổ4 · Kim3 · Thủy6** is a separate presentation model and was not used as an element-strength score. **No `flo_004` repair.**

---

## Token SSOT

| Layer | Value |
|-------|--------|
| Canonical token | `tong_tai` |
| Display | `Tòng Tài` |
| Pattern → UG field | `follow_pattern` / `follow_type` = token |
| `spc_001` condition | `follow_pattern == tong_tai` |

Vietnamese labels are never compared to machine tokens. `build_useful_god_context` canonicalizes both. Direct `UsefulGodContext(follow_pattern="Tòng Tài")` does **not** match `spc_001`.

Legitimate weak + Tòng Tài winner still fires `spc_001` (synthetic contract test).

---

## Follow-pattern inventory

All rows: `database/14_pattern/03_follow_pattern.csv`.  
Eligibility is **code** (Strength gate + detector). CSV still has no `strength_level` column; that is intentional — the gate is the SSOT so Tuyền is not hard-coded.

| Rule | Token | Display | Required Strength | Structural (CSV) | Detector evidence | Useful God |
|------|-------|---------|-------------------|------------------|-------------------|------------|
| `fol_tv_01` | `tong_vuong` | Tòng Vượng | **`strong` only** | `ten_gods_list` not_contains Quan / Sát / Tài | support ratio ≥ 0.70 | none |
| `fol_ttai_01` | `tong_tai` | Tòng Tài | **`weak` only** | contains Chính Tài | support ratio ≤ 0.25 + wealth dominance | `spc_001` → Chính Tài |
| `fol_tsat_01` | `tong_sat` | Tòng Sát | **`weak` only** | contains Thất Sát | same + sát dominance | `spc_003` → Thất Sát |
| `fol_tquan_01` | `tong_quan` | Tòng Quan | **`weak` only** | contains Chính Quan | same + quan dominance | `spc_002` → Chính Quan |
| `fol_tnhi_01` | `tong_nhi` | Tòng Nhi | **`weak` only** | contains Thực Thần | same + output dominance | none |
| `fol_tan_01` | `tong_an` | Tòng Ấn | **`weak` only** | contains Chính Ấn | same + resource dominance | none |

No `fol_*` row remains disconnected from Strength.

`balanced`: may not publish weak-follow or Tòng Vượng. Weak + Tài present is eligible, not automatic Tòng.

Follow token is published to Useful God **only if the winning Pattern rule is that follow rule**. Combination/main winners (example: Đặng Thị Dung `sat_an`) do not leak a detector-only `tong_tai` into `spc_001`.

---

## Matrix (tests)

| Case | Result |
|------|--------|
| Strong + Tài present | Must not become Tòng Tài |
| Balanced + Tài present | Must not become Tòng Tài solely because Tài exists |
| Weak + Tài present, no dominance | Eligible, not automatic Tòng |
| Weak + Tài dominance + CSV Chính Tài | May become Tòng Tài; token `tong_tai`; `spc_001` may win |
| Equivalent officer / sát / nhi families | Same Strength gate |
| Strong + peer/resource dominance | May become Tòng Vượng |
| Weak + peer dominance | Must not become Tòng Vượng |

Semantic contract:

- Impossible: `strength=strong` + customer-facing Pattern/Interpretation/Narrative/Report contains `cực nhược`
- Impossible: `strength=weak` + `cực vượng` / `tong_vuong`
- Impossible: `spc_001` unless canonical Pattern is `tong_tai` (same for `spc_002` / `spc_003`)

---

## Regression five cases

Strength unchanged on all five. Pattern changed **only** Tuyền (invalid follow). Useful God changed only where Pattern no longer published a follow token that would have been a false `spc_001` after token repair (Dung stays non-follow `sea_002`).

| Case | Strength | Pattern | Useful God | Follow leak |
|------|----------|---------|------------|-------------|
| Nguyễn Tiến Sơn | 0.87 strong raw 37 | `chinh_an` `pat_ca_01` — unchanged | `sea_001` Hỏa · Bính · Thất Sát | none |
| Lương Ngọc Huỳnh | 0.64 balanced raw 14 | `chinh_tai` `pat_ct_01` — unchanged | `sea_004` Hỏa · Đinh · Kiếp Tài | none |
| Đặng Thị Dung | 0.24 weak raw −26 | `sat_an` `com_san_01` — unchanged | `sea_002` Thủy · Nhâm · Chính Ấn (not `spc_001`) | detector may see hidden wealth; token **not published** |
| Đoàn Quang Hưng | 0.61 balanced raw 11 | `thuc_than` `pat_tht_01` — unchanged | `sea_004` Hỏa · Đinh · Thiên Ấn | `tong_*` CSV hits rejected (`balanced`) |
| Vũ Thị Thanh Tuyền | 0.66 strong raw 16 | **`kiep_tai` `pat_ktai_01`** (was `tong_tai`) | `sea_002` Thủy · Nhâm · Thiên Tài — same winner | `fol_ttai_01` rejected |

---

## Live runtime

- API restarted from current repo (`127.0.0.1:8000`).
- Fresh `POST /api/v1/analyze` for Tuyền (no ResultStore reuse).
- Portal rebuild **not required**: PatternView / UsefulGodView contracts unchanged; `cach_cuc` is data.

Live HTTP 200:

- Strength `0.66 / strong / raw 16`
- Pattern `kiep_tai` / Kiếp Tài / `pat_ktai_01`
- Useful God `sea_002` / Thủy · Nhâm · Thiên Tài
- Five Elements counts wood 3 · fire 1 · earth 4 · metal 3 · water 6
- No `cực nhược` in pattern, interpretation, narrative, or report

---

## Tests executed

```text
pytest tests/pattern tests/useful_god -q
48 passed
```

New contract tests:

- `tests/pattern/test_g1_x01_follow_strength_gate.py`
- `tests/useful_god/test_g1_x01_follow_token_normalization.py`

Golden Dataset / snapshots / expected output: **not edited**. Strength CSV: **not edited**.

---

## Files changed

| File | Reason |
|------|--------|
| `engines/pattern_engine/follow_tokens.py` | Canonical token / Strength eligibility SSOT |
| `engines/pattern_engine/calculators/follow_pattern.py` | Consume Strength; emit tokens |
| `engines/pattern_engine/calculator.py` | Strength gate + publish token only on follow winner |
| `engines/pattern_engine/labels.py` | Display labels for `tong_*` |
| `engines/pattern_engine/rule_context_bridge.py` | `tong_cach` uses display, not token |
| `engines/useful_god_engine/utils/context_builder.py` | Normalize follow token for `spc_*` |
| `tests/pattern/test_g1_x01_follow_strength_gate.py` | Matrix + Tuyền + semantic contract |
| `tests/useful_god/test_g1_x01_follow_token_normalization.py` | Token vs label + `spc_001` guard |

---

## Remaining failures

None in `tests/pattern` or `tests/useful_god`.

---

## Stop

Do **not** start G1-FINAL.
