# 01 — Golden Case Selection

Version: 1.0  
Status: **OFFICIAL — Golden Case Set (methodology)**  
Date: 2026-08-08  
Epic: EPIC 6 · Sprint A  
Depends on: EPIC 5 Case Review Workflow · Consultation Scenarios (CS-*)  
Scope: Case selection only — no Knowledge creation  

---

## 1. Purpose

Define the official **Golden Case** set for consulting-quality validation.

Golden Cases are **consultation profiles**, not Golden Dataset analytical regression fixtures.  
They must span structural diversity and customer-intent diversity.

---

## 2. Selection principles

1. **Cover structure** — strong, weak, follow, special, mixed.  
2. **Cover intent** — business, career, marriage, health, wealth (+ default identity).  
3. **Cover failure modes** — missing useful god, thin evidence, conflicting strength/risk.  
4. **Wave 1.1 honest** — do not require domain depth Wave 1.1 cannot provide; record gaps instead.  
5. **Reproducible** — each case has stable id, expected signals, scenario affinity.  
6. **No PII in docs** — use labels / synthetic profiles; Product may attach private birth data offline.

---

## 3. Official Golden Case set (Sprint A)

### 3.1 Structural cases

| Case id | Profile | Expected Analysis signals (min) | Scenario affinity | Wave 1.1 expected KUs |
|---------|---------|----------------------------------|-------------------|------------------------|
| **GC-STRONG-FOLLOW** | Strong chart · Follow Pattern | thân vượng/cân; follow-style cách cục; useful god present | CS-ID, default | ID, ST, UG, RC |
| **GC-WEAK-ENEMY** | Weak chart · enemy caution | thân nhược; ky/enemy present; useful god present | CS-ID, CS-MD | ID, WK, UG, RC |
| **GC-FOLLOW-PATTERN** | Follow Pattern emphasis | follow / thuận cục signal; useful god | CS-ID, CS-PG | ID, ST or WK, UG, RC |
| **GC-SPECIAL-PATTERN** | Special Pattern | named special cách (e.g. từ quý / hóa khí class); useful god | CS-ID | ID, ST/WK, UG, RC — **no special-pattern KU yet** |
| **GC-MIXED** | Mixed / tension chart | strength favorable **and** enemy/clash caution | CS-ID, CS-MD | ID, ST, WK, UG, RC |

### 3.2 Intent-oriented cases

| Case id | Profile | Customer question (intent) | Scenario | Wave 1.1 coverage |
|---------|---------|----------------------------|----------|-------------------|
| **GC-BUSINESS** | Business-oriented | “Có nên mở rộng / khởi sự không?” | CS-BU / CS-MD | Core only — **domain gap** |
| **GC-CAREER** | Career-oriented | “Hướng nghề / vai trò nào phù hợp?” | CS-CA | Core only — **domain gap** |
| **GC-MARRIAGE** | Marriage-oriented | “Quan hệ / hôn nhân cần giữ gì?” | CS-RL / CS-MA | Core only — **domain gap** |
| **GC-HEALTH** | Health-oriented | “Nhịp sống / sức khỏe cấu trúc?” | CS-HE | Core only — **domain gap** (ethics: no medical diagnosis) |
| **GC-WEALTH** | Wealth-oriented | “Tiền bạc / đầu tư ưu tiên gì?” | CS-FI / CS-IV | Core only — **domain gap** |

### 3.3 Control / honesty cases

| Case id | Profile | Purpose |
|---------|---------|---------|
| **GC-NO-USEFUL-GOD** | Useful god absent | Confirm UG/RC omitted; no invention |
| **GC-THIN-EVIDENCE** | Sparse pattern/strength | Trustworthiness / insufficient honesty |

**Sprint A official count:** 12 Golden Case slots (5 structural + 5 intent + 2 control).

---

## 4. Mapping to EPIC 5 review

Every Golden Case review must complete:

- Consulting Scorecard (`knowledge/consulting_quality/04`)  
- Case Review Template (`02` in this folder)  

Commercial acceptance still governed by EPIC 5 `05_ACCEPTANCE_CRITERIA.md`.

---

## 5. Binding real BaZi charts (Product)

| Step | Rule |
|------|------|
| 1 | Product/Consultant picks anonymized real chart matching profile |
| 2 | Record Analysis signals actually produced (do not invent) |
| 3 | Generate NarrativeResult via frozen pipeline |
| 4 | Score with template; log gaps in `04` |

If a real chart does not match the profile, **reclassify** — do not force signals.

Sprint A evaluation (`03`) used **synthetic analysis bags** representing each structural/control profile; intent cases evaluated for **coverage gap** (no domain KU) without fabricating domain advice.

---

## 6. Out of scope for case selection

- Creating Knowledge Units to “fill” intent cases  
- Editing Golden Dataset expected JSON  
- Portal scenario UX  

---

## 7. Stop line

Golden Case set defined. Reviews use `02`; findings in `03`–`05`.

---

END
