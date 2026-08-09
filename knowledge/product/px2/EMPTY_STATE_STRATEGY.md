# Empty State Strategy

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2  
Aligns with: PX-1 EMPTY_STATE_GUIDE · SECTION_VISIBILITY_RULES

---

## 1. Distinction

| Pattern | Use |
|---------|-----|
| Hidden | Warnings, charts, knowledge, appendix when arrays/fields empty |
| Empty card | Recommendation region; each missing life domain |
| Page error | Missing Hero or Summary |
| Page empty | Result success but presentation envelope entirely absent and no identity |

Never blank cards.

---

## 2. Bindings (chrome)

| Situation | i18n key | Intent |
|-----------|----------|--------|
| Rec region empty | `i18n.empty.recommendations` | Chưa có định hướng cụ thể trong buổi này |
| Domain empty | `i18n.empty.domain` | Chưa có luận giải cho {domain} trong buổi tư vấn này |
| Page empty | `i18n.empty.page` | Chưa có dữ liệu tư vấn để hiển thị |

`{domain}` is chrome interpolation from `i18n.domain.*` — not invented copy.

---

## 3. Component state

Empty unit → `empty`.  
Optional `onNext` toward Summary or Recommendation if those are ready.

---

## 4. Adapter

`available=false` or empty arrays → empty/hidden per rules.  
Adapter does not fill lorem or reuse another domain’s text.

---

## 5. Stop line

Honesty over collage.

END
