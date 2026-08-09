# Language Binding

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2  
Aligns with: PX-1 LANGUAGE_GUIDE

---

## 1. Law

Everything the user sees is Vietnamese.

Content strings come from `report.*` and must already be Vietnamese when published.  
Adapter does **not** translate consulting prose.  
Adapter does **not** mix English labels.

Chrome strings come from `i18n.*` (this pack).

---

## 2. Split

```
report.*     → case-specific Vietnamese (name, bullets, why, action…)
i18n.*       → stable UI Vietnamese (section titles, Vì sao, CTA, empty/error)
```

If `report.*` arrives in English, adapter does not auto-translate. It still binds (formatting only). Language QA is a Report publication duty. UI review fails mixed labels on chrome.

---

## 3. Forbidden on screen

- English section titles  
- Engine terms as labels (`decision`, `pipeline`, `schema` as heading)  
- Internal ids in P1/P2  
- Dual labels (`Why / Vì sao`)  

Technical values (Can Chi symbols, timezone offsets) may appear under Vietnamese headings inside collapsed Technical.

---

## 4. Status / domain enums

| Enum value | i18n path | Visible |
|------------|-----------|---------|
| consultation ready | i18n.status.ready | Sẵn sàng tư vấn |
| partial | i18n.status.partial | Tư vấn một phần |
| in_progress | i18n.status.in_progress | Đang hoàn thiện |
| error | i18n.status.error | Không thể hiển thị phần này |
| career | i18n.domain.career | Sự nghiệp |
| wealth | i18n.domain.wealth | Tài chính |
| relationship | i18n.domain.relationship | Quan hệ |
| health | i18n.domain.health | Sức khỏe |
| luck | i18n.domain.luck | Vận trình |

---

## 5. Stop line

Chrome is i18n. Content is Report. Both Vietnamese on screen.

END
