# COMMON_PATTERNS

| Field | Value |
|-------|-------|
| Step | 2 |
| Rule | Fix the pattern once. Do not write CASE_0002-only or P04-only lines. |

---

## P1 — OUTPUT room leaks off-theme

**Pattern:** Recognition, career balance, action suffixes, and UG cooling phrases assume “sản phẩm / vòng ra kết quả” for every adult.

**Why it happens:** EPIC-A taught the OUTPUT room well; the default else-branch reused it. Useful-god hints (Thực Thần → “tạo ra sản phẩm”) fire even when PRIMARY theme is SELF_CARRY or BALANCE.

**Buyer cost:** BALANCE / SELF_CARRY / CONSERVING adults are put in the wrong consulting room.

**Shared fix:** Theme-gate OUTPUT language. Keep it **on** OPERATING_OUTPUT. Rewrite product-dump cooling when theme ≠ OUTPUT.

Maps to **PB-002**.

---

## P2 — Default close is a motivation speech

**Pattern:** Memory / close falls through to “Bạn mạnh hơn khi…”.

**Why it happens:** One fallback served every theme and every capacity band.

**Buyer cost:** Tired / cooling / BALANCE adults are told to get stronger. Conserving week is sold as a pep talk.

**Shared fix:** Conserving rule = `weak` / `very_weak` **or** (`BALANCE_DIRECTION` + balanced/empty). Conserving close = rest + stop-list, not “mạnh hơn”.

Maps to **PB-001**.

---

## P3 — Dual publication collapsed to one label

**Pattern:** Capacity and structure are both published; close and insight keep only the louder theme.

**Why it happens:** Memory builder prefers a single memorable line. Empty structure phrase makes the second story unusable, so it is dropped.

**Buyer cost:** Tension / dual-scope buyers are forced to pick a nametag.

**Shared fix:** If both cues are published, close and insight must keep both. Never “choose one label to erase the other”.

Maps to **PB-003**.

---

## P4 — Structure phrase is not a sentence the buyer can use

**Pattern:** `structure_to_plain` returned empty “khung lá số” or a generic “giữ nhất quán”. Capital “Ấn” missed the “ấn” token.

**Why it happens:** Case-sensitive token match; no lived map for Ấn / Tài / Quan / Thương.

**Buyer cost:** PB-003 cannot land — two stories require two *lived* stories.

**Shared fix:** Case-normalize; map tòng / ấn / tài / quan|sát / thương|thực; never emit empty khung.

Supporting work for **PB-003** (and closes the empty-khung half of **PB-004**).

---

## P5 — Identical avoid lines stacked

**Pattern:** “Đừng kết luận ngoài phạm vi…” repeated.

**Why it happens:** Limitation keys map to the same plain line; no dedupe.

**Buyer cost:** Executive feels like an audit, not a consultant.

**Shared fix:** Dedupe `_avoid_block` by realized text.

Ships with this program (**PB-013**).

---

## What is *not* a common pattern (do not “fix”)

| Observation | Why leave it |
|-------------|--------------|
| 0002 product / output week | Correct room for OPERATING_OUTPUT |
| 0003 Career hidden + parent conserve | Product Context — frozen |
| Section title “Điểm làm tôi mạnh hơn” | CLL heading taxonomy — frozen docs |
| CASE_0001 “nhịp quyết nhanh dưới áp lực” | Published style — Truth |

---

END
