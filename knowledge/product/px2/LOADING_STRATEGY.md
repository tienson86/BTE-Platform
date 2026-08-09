# Loading Strategy

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2

---

## 1. Page loading

`report.page.state == loading` until adapter emits a terminal page state.

UI:

- No fake identity  
- No placeholder recommendations that look real  
- Vietnamese status: **Đang chuẩn bị tư vấn** (`i18n.page.loading`)  
- CTA disabled  

---

## 2. Section loading

PX-2 default: **page-level bind**. Sections do not independently fetch engines.

If a later sprint streams sections:

- Section `loading` only when parent is `partial_ready` and that slice is pending  
- Do not block Hero/Summary already `ready`  

Until then: no per-section skeleton that implies engine access.

---

## 3. Expand loading

Forbidden to load new Report truth on expand.  
Detail is already on the model or it is null.

---

## 4. Printing / exporting

Reserved page states. Treat controls as loading-equivalent (disabled).  
Do not change reading order.

---

## 5. Offline

Reserved. Do not implement. If encountered, page `offline` + `i18n.page.offline`.

---

## 6. Stop line

Loading is a page state, not a dashboard of pulsing widgets.

END
