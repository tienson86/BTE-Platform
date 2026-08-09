# CTA Specification

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2  
Aligns with: PX-1 ACTION_MODEL

---

## 1. Counts

| Tier | Count | Control |
|------|------:|---------|
| Primary | **1** | Primary button |
| Secondary | **0 or 1** | Secondary button |
| Text buttons | as needed | jump / next |
| Expand buttons | as needed | disclosure |

No duplicated primary action.

---

## 2. Bindings

| Concern | Path |
|---------|------|
| Primary label | `i18n.cta.primary` → **Bắt đầu theo định hướng này** |
| Primary enabled | `report.cta.primary.enabled` |
| Secondary label | `i18n.cta.secondary` → **Xem sâu sự nghiệp** |
| Secondary enabled | `report.cta.secondary.enabled` |
| Expand | `i18n.expand.*` |

CTA **meaning** (what happens after click) is a product-shell concern. PX-2 only specifies enablement + labels + placement. Adapter does not invent a second Primary if `enabled=false`.

---

## 3. Placement

- Primary + Secondary: Recommendation region only  
- Text: Summary jump, empty next, error retry  
- Expand: cards / technical / knowledge  

Hero has no CTA.

---

## 4. Disabled behavior

| Condition | Primary | Secondary |
|-----------|---------|-----------|
| `page.state == loading` | disabled | disabled |
| `page.state == error` | hidden | hidden |
| `page.state == empty` | hidden | hidden |
| `page.state == printing \| exporting` | disabled | disabled |
| `primary.enabled == false` | disabled, still visible on ready/partial | — |
| `secondary.enabled == false` or null label | hidden | — |

Disabled Primary: visible, not activatable, no replacement control.

---

## 5. Loading behavior

While loading: CTA disabled.  
Do not swap label to English `Loading`.  
Optional chrome: `i18n.cta.loading` → **Đang xử lý** if a spinner label is required.

---

## 6. Expand buttons

Not CTAs. Tertiary.  
Hidden when target detail is null.  
Labels: **Xem thêm** / **Thu gọn** / technical & knowledge variants (i18n).

---

## 7. Stop line

One Primary. Optional Secondary. Disclosure is not a CTA.

END
