# Navigation States

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-2

---

## 1. Nav model

`NavModel.items[]`: `{ target_ui_id, label, visible, current? }`

Labels = i18n section/domain titles.  
`visible` mirrors `SECTION_VISIBILITY_RULES.md`.

---

## 2. States

| Nav state | Meaning |
|-----------|---------|
| `idle` | User scrolling |
| `jumping` | In-page navigate in progress |
| `settled` | Current section updated |

No route change. Hash optional later; visible label stays Vietnamese.

---

## 3. Current section

`current` follows scroll/focus in PX-1 reading order among **visible** items only.

Hidden sections cannot be `current`.

---

## 4. Targets

| target_ui_id | Label |
|--------------|-------|
| Summary | Tóm tắt tư vấn |
| Recommendation | Định hướng chính |
| Warnings | Lưu ý quan trọng |
| DomainCareer | Sự nghiệp |
| DomainWealth | Tài chính |
| DomainRelationship | Quan hệ |
| DomainHealth | Sức khỏe |
| DomainLuck | Vận trình |
| Charts | Biểu đồ minh họa |
| Technical | Chi tiết kỹ thuật |
| Knowledge | Kiến thức bổ sung |
| Appendix | Phụ lục |

Skip link: `i18n.nav.skip` → main / Hero.

---

## 5. Collapsed targets

Jump to Technical/Knowledge lands on the **header**. Section stays collapsed until user toggles.

---

## 6. Disabled nav

Page `loading` | `error` | `empty` | `offline`: nav hidden or non-interactive.

---

## 7. Stop line

Navigation tracks visibility. It does not reorder IA.

END
