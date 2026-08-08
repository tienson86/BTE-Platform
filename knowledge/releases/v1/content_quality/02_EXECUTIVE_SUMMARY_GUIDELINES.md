# 02 — Executive Summary Guidelines

Version: 1.0  
Status: **Release B — Content Quality**  
Date: 2026-08-08  
Scope: Quality standards only — no runtime change

---

## 1. Purpose

Executive Summary is the customer’s first consulting briefing.

It must answer, in commercial Vietnamese, who this person is and what matters now — without sounding like a system dump or a rule catalog.

This document extends Pack 05 `05_EXECUTIVE_SUMMARY_SPEC.md` and Sprint C tone (`14_TONE_OF_VOICE.md`) with **commercial quality standards**.

---

## 2. Required answers

Every complete Executive Summary must make these answers visible (as slots, short paragraphs, or clearly labeled lines):

| # | Question | Slot / field guidance |
|---|----------|------------------------|
| 1 | Who is this person? | `identity` — day-master / pattern / strength identity in human language |
| 2 | Core strengths | `strengths` — 1–2 supported strengths |
| 3 | Core weaknesses | `weaknesses` — supported cautions (not shaming) |
| 4 | Primary opportunities | Prefer derived from strengths + useful guidance already in Interpretation; never invent |
| 5 | Primary risks | Prefer aligned with Warning / weakness evidence; never invent |
| 6 | Immediate priority | `priority_recommendation` — one clear priority |
| 7 | Next action | `next_action` — one concrete next step |

### Notes on opportunities / risks

Pack 05 `NarrativeSummary` today formalizes five core slots (identity, strengths, weaknesses, priority, next action). Opportunities and risks are **commercial reading targets**:

- Opportunities may be expressed inside strengths + priority when no separate field exists.  
- Risks may be expressed inside weaknesses when no separate field exists.  
- Do **not** invent new analytical claims to fill empty opportunity/risk language.  
- If evidence is missing → use approved insufficient narrative for that slot — never filler.

---

## 3. Quality standards

### 3.1 Voice

| Attribute | Standard |
|-----------|----------|
| Tone | Briefing, decisive, respectful |
| Perspective | Consultant speaking to the person |
| Length | Short briefing — not a full essay |
| Certainty | Match evidence strength; never upgrade weak evidence |

### 3.2 Must

✓ Answer the commercial questions above (or mark insufficient)  
✓ Preserve analytical meaning (meaning lock)  
✓ Use human language for BaZi concepts (e.g. Nhật chủ, thế mạnh, điểm cần lưu ý)  
✓ Keep one idea per sentence  
✓ Prefer concrete phrasing over abstract scoring talk  
✓ Leave the reader knowing **what to prioritize next**

### 3.3 Must not

✗ Generic wording (“Bạn có tiềm năng phát triển…”) with no chart-specific anchor  
✗ Rule descriptions (“Kích hoạt khi…”, “Áp dụng bảng…”)  
✗ Technical language (`rule_id`, `matched_rules`, `ViewModel`, `PACK_0x`, English UI leftovers)  
✗ Score dumps as personality (“Điểm 51.25 chứng minh…”)  
✗ Invented opportunities, risks, or timelines  
✗ Absolute prophecy (“Bạn chắc chắn sẽ…”)  
✗ Shame (“Bạn kém / mệnh xấu tuyệt đối…”)  
✗ Mock / placeholder / “chờ engine” text

---

## 4. Structure pattern (commercial)

Preferred reading shape (content may be slots or short lines):

1. **Identity** — one clear statement of who they are in this chart  
2. **Strengths** — what is already working  
3. **Weaknesses / risks** — what needs care  
4. **Opportunities** — where energy is best applied (evidence-backed)  
5. **Priority** — the single most important focus  
6. **Next action** — the immediate step

### Example shape (illustrative — not a frozen template)

**GOOD (direction):**

> Nhật chủ và cục diện cho thấy một người thiên về trách nhiệm và ổn định.  
> Thế mạnh nổi bật là khả năng duy trì nhịp làm việc bền.  
> Điểm cần lưu ý là dễ mất cân bằng khi áp lực kéo dài.  
> Ưu tiên hiện tại là phát huy đúng hướng đã được chỉ ra trong luận giải.  
> Bước tiếp theo: chọn một việc quan trọng và giữ nhịp thực hiện ổn định trong giai gian tới.

**BAD:**

> Observation: Critical. Score payload strength_score=51.25. Kích hoạt khi Nhật Chủ cân bằng. (mock)

---

## 5. Slot quality criteria

| Slot | GOOD | REQUIRES IMPROVEMENT |
|------|------|----------------------|
| Identity | Names a recognizable personal pattern in plain language | Restates engine field names or “user profile” |
| Strengths | Specific, evidence-backed capability | “Bạn có nhiều điểm mạnh” |
| Weaknesses | Calm, specific caution | Vague fear or moral judgment |
| Opportunities | Tied to useful guidance already present | Invented career prophecy |
| Risks | Tied to validated caution | Catastrophe language |
| Priority | One clear focus | Laundry list of unrelated tips |
| Next action | Doable next step | Repeat of priority with no action |

---

## 6. Insufficient evidence

When a slot lacks commercial evidence:

- Use the approved line: `Chưa đủ dữ liệu để đưa ra kết luận.`  
- Do not soft-invent with “có thể là…” fillers  
- Do not hide emptiness behind generic optimism  

A partial Executive Summary with honest insufficient slots is better than a fluent false briefing.

---

## 7. Relationship to other components

| Component | Relationship |
|-----------|--------------|
| Observation | Supplies identity / strength anchors |
| Warning | Supplies weakness / risk anchors |
| Recommendation | Supplies priority / next action |
| Impact | May clarify consequence language — do not duplicate full Impact |
| Conclusion | Later synthesis — Executive Summary must stand alone as opening briefing |

Executive Summary may compress and reorder meaning. It must not invert meaning.

---

## 8. Review questions

Before accepting Executive Summary copy:

1. Could a non-technical reader answer “who is this person?” after reading it?  
2. Are strengths and cautions both present or honestly insufficient?  
3. Is there one clear priority and one next action?  
4. Does any sentence sound like a rule engine, score dump, or developer note?  
5. Would an experienced BaZi consultant be comfortable saying this aloud?

If any answer fails → rewrite or mark insufficient. Do not ship generic filler.
