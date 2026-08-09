# Action Model — Result Experience V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-1  
Depends on: Visual Language §12 · Product Polish CTA strategy (voice) · this pack’s reading flow

---

## 1. Purpose

Actions support understanding.  
They never interrupt reading.

---

## 2. Action tiers

| Tier | Count | Role |
|------|------:|------|
| **Primary** | Exactly 1 per Result view | Commit to the main next step of this consultation |
| **Secondary** | ≤2 visible | Deepen a milestone or adjacent domain plan |
| **Tertiary** | As needed | Expand, đọc thêm, mở kỹ thuật, jump in-page |

---

## 3. Primary action

| Field | Rule |
|-------|------|
| **Meaning** | Begin acting on the core direction already stated |
| **Lives near** | Định hướng chính |
| **Label language** | Vietnamese · verb-first · specific |
| **Must not** | Sit in Hero as marketing · open a new unexplained product world · outrank Tóm tắt |
| **Visual** | One Primary button style from Design System |

Primary answers: **“Tôi bắt đầu làm theo định hướng chính.”**

Example label intents (not implementation copy-lock beyond language rules):

- **Bắt đầu theo định hướng này**  
- **Lưu định hướng chính**  

Choose one product verb and keep it consistent. Do not invent a new verb per card.

---

## 4. Secondary actions

Support, never compete.

Examples of intent:

- Xem sâu hơn lĩnh vực Sự nghiệp  
- Xem mốc thăng tiến (if that capability is in the session)  

Secondary uses Secondary button style.  
Never equal visual weight to Primary.

---

## 5. Tertiary actions (disclosure and navigation)

| Intent | Example label |
|--------|----------------|
| Expand recommendation | **Xem thêm** / **Thu gọn** |
| Expand analysis | **Xem phân tích chi tiết** |
| Open charts table | **Xem bảng số liệu** |
| Open technical | **Xem chi tiết kỹ thuật** |
| Open knowledge | **Đọc thêm** |
| Jump to recs | **Xem định hướng chính** |

Tertiary = Text Button / quiet control.  
No new routes required by this blueprint.

---

## 6. Actions that do not belong

| Action | Why forbidden in V2 Result |
|--------|----------------------------|
| Hero “Export JSON” | Developer tool |
| “View schema” in first viewport | Technical leakage |
| Multiple Primary CTAs, one per domain | Decision freeze |
| Urgency countdown | Excitement theatre |
| Upsell gallery | Marketing, not consulting |

Export / print / share — if they exist in product chrome — stay in PageChrome or Technical/Appendix, never in Hero.

---

## 7. Action vs reading

```
Read Tóm tắt
  ↓
Read Định hướng
  ↓
Optionally expand one card
  ↓
Take Primary action
  ↓
Optionally inspect charts / technical / knowledge
```

Do not require a click to see Tóm tắt or top recommendations.

---

## 8. Domain cards

Individual recommendation cards do **not** each carry a Primary button.

They carry:

- Việc cần làm (content)  
- Xem thêm (tertiary)  

The page-level Primary remains singular.

---

## 9. Stop line

One Primary. Quiet Secondary. Disclosure as Tertiary. Vietnamese labels only.

END
