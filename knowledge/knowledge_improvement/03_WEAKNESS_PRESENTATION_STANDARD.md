# 03 — Weakness Presentation Standard

Version: 1.0  
Status: **OFFICIAL — Weakness Presentation Standard**  
Date: 2026-08-08  
Depends on: `01`, `02` · KU-WK-001 · KU-RC-001 pairing  
Scope: Documentation only  

---

## 1. Purpose

Define how BTE presents structural caution so consultation **never stops at weakness**.

Official arc:

```
Weakness
    ↓
Risk
    ↓
Mitigation
    ↓
Opportunity
```

Wave 1.1 has no separate Risk / Mitigation / Opportunity unit ids.  
This sprint **revises existing** KU-WK-001 and KU-RC-001 to carry the arc in commercial prose — **no new units**.

---

## 2. Arc definitions

| Stage | Customer meaning | Wave 1.1 carrier |
|-------|------------------|------------------|
| **Weakness** | Name the limit calmly | KU-WK-001 opening |
| **Risk** | What goes wrong if ignored | KU-WK-001 middle (1 sentence) |
| **Mitigation** | What to do first (usually giảm tải / giữ mực) | KU-WK-001 close + **KU-RC-001 lead when WK selected** |
| **Opportunity** | What becomes possible after mitigation (align to Dụng thần) | KU-RC-001 / KU-UG-001 — only after mitigation when caution present |

Never end Exec/Warning on shame or fate. Never invent medical/legal doom.

---

## 3. Two weakness frames (same unit KU-WK-001)

### Frame A — Thin / overloaded thân

| When | Signals |
|------|---------|
| Use | thân nhược / mỏng lực / overtaxed band |

| Stage | Required content |
|-------|------------------|
| Weakness | Lực cấu trúc đang mỏng hoặc dễ bị kéo quá mức |
| Risk | Dễ lệch nhịp nếu mở rộng khi chưa giữ mực |
| Mitigation | Giảm tải / giữ nhịp trước |
| Opportunity | Sau khi ổn định, mới nuôi đúng Dụng thần |

### Frame B — Strong structure with enemy / clash caution

| When | Signals |
|------|---------|
| Use | thân favorable **and** enemy/ky/clash caution |

| Stage | Required content |
|-------|------------------|
| Weakness | Có điểm đối nghịch / dễ bị kéo lệch (name unique caution) — **not** “cấu trúc mỏng” |
| Risk | Nếu chạy theo phần kỵ, dễ mất lợi thế đang có |
| Mitigation | Giữ biên / giảm việc nuôi phần kỵ |
| Opportunity | Bảo toàn thế mạnh; ưu tiên việc nuôi Dụng thần |

**IA-P0-03** is satisfied by Frame B.  
Authoring may use mutually exclusive paragraphs selected by condition notes in `author_notes` / future dual-bind fields — still **one unit id**.

---

## 4. Signal contract for `{weakness_signal_label}`

| Rule | Requirement |
|------|-------------|
| Uniqueness | Each distinct enemy/caution appears **once** |
| Order | Prefer human labels; drop duplicate ky_than if already in unfavorable list |
| Length | One short phrase (≤ ~40 chars ideal) or “A; B” with unique items only |
| Empty | If no label, omit colon clause rather than printing empty |

Example:

| Bad | Good |
|-----|------|
| `Hỏa; Hỏa; mức thân nhuoc` | `Hỏa (điểm cần giữ)` or `Hỏa; thân đang mỏng lực` |
| `Thủy; Thủy; mức thân vuong` | `Thủy (phần dễ lệch)` — Frame B |

---

## 5. Pairing with Core Recommendation (IA-P0-04)

When KU-WK-001 is selected **and** KU-RC-001 is selected:

| Order | Content |
|------:|---------|
| 1 | Mitigation-first sentence (giảm tải / giữ biên) |
| 2 | Then useful-god alignment action |
| 3 | Next step must not contradict mitigation |

When WK is **not** selected, RC may lead with useful-god priority as today (still consultant prose per `02`).

KU-UG-001 remains the **reason** layer — do not turn it into aggressive “advance now” when WK is active.

---

## 6. Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| Stop at “bạn yếu” | Always add Risk + Mitigation |
| “Mỏng” on strong+enemy | Use Frame B |
| Duplicate labels / paragraphs | Signal contract + single WK statement |
| Expand-first on weak chart | RC mitigation-first |
| Opportunity that denies weakness | Opportunity only **after** mitigation |

---

## 7. Exec / Warning placement

| Surface | Guidance |
|---------|----------|
| Exec weaknesses | One Frame A or B paragraph (full mini-arc compressed) |
| Warning | Risk + Mitigation (may shorten Opportunity) |
| Recommendation | Mitigation-first when WK present |

Rhythm details: `04_EXECUTIVE_SUMMARY_REFINEMENT.md`.

---

## 8. Stop line

Weakness Presentation Standard defined for IA-P0-02, IA-P0-03, IA-P0-04.  
No new Risk/Mitigation/Opportunity unit ids in P0.

---

END
