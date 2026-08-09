# Error State Strategy

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2  
Aligns with: PX-1 ERROR_STATE_GUIDE

---

## 1. Levels

| Level | Trigger | UI |
|-------|---------|-----|
| Page | Adapter fail; `success=false` without Hero; missing Hero/Summary | Full-page ErrorStateCard |
| Section | Slice invalid while page partial_ready | Local ErrorStateCard |
| Inline | Expand target corrupt | Inline error, parent stays |

Chart error must not remove Tóm tắt / Định hướng.

---

## 2. Contract fields

| Field | Path |
|-------|------|
| Page error message | `report.page.error_message` (Vietnamese, user-safe) |
| Page error code | `report.page.error_code` (internal; not displayed unless technical opened) |

If envelope lacks user-safe message, chrome: `i18n.error.page` → **Không thể hiển thị buổi tư vấn.**

Never display `CanonicalReportResult.errors` raw strings if they contain engine codes — adapter maps to user-safe message or generic chrome. Mapping codes → generic Vietnamese is **formatting**, not new diagnosis logic. Unknown code → generic message.

---

## 3. Recovery

| Scope | Event | Label |
|-------|-------|-------|
| Page | `onRetry { scope: page }` | `i18n.error.retry` → **Thử tải lại buổi tư vấn** |
| Section | `onRetry { scope: section }` | **Thử lại phần này** |
| Fallback nav | `onNavigate Summary` | **Quay lại tóm tắt tư vấn** |

---

## 4. States

Error unit → `error`.  
CTA Primary hidden on page error.  
Retry is Secondary/Tertiary, not a second Primary consultation CTA.

---

## 5. Stop line

Errors stay consultant-grade Vietnamese. No stack traces.

END
