# Component Property Guide

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2

---

## 1. Property classes

| Class | Source | Mutable in UI |
|-------|--------|---------------|
| Content | `report.*` via adapter | No |
| Chrome | `i18n.*` resolved | No |
| View state | local: expanded, collapsed | Yes |
| Token | UI token catalog | No |

---

## 2. Naming

Props use camelCase in API docs.  
`ui_id` uses Component.field.  
`contract_path` uses report/i18n dotted paths.

Do not expose `contract_path` as a React prop.

---

## 3. Required vs nullable

- Required content missing after bind → parent Empty or page Error (see state machines)  
- Nullable null → omit slot, do not render `"null"`  
- Arrays default `[]`  
- Booleans default explicit false  

---

## 4. IDs

`Recommendation.id` is opaque.  
Use only for expand keys and domain references.  
Never display. Never construct from engine ids in the adapter beyond envelope value.

---

## 5. Labels

Field labels (Vì sao, Kết quả kỳ vọng, Việc cần làm) are chrome props, not report fields.

Do not bind `reason` into the label slot.

---

## 6. CTA props

Only Recommendation region receives `cta`.  
Cards do not receive `primaryEnabled`.

Disabled: `primary_enabled=false` → control visible, not activatable, no second Primary invented.

Loading: page `loading` → CTA disabled.

---

## 7. Children vs slots

Slots name composition holes.  
Children name owned subcomponents.  
Do not pass unnamed leftover report dicts through slots.

---

## 8. Forbidden props

- `analysisResult`  
- `decisionResult`  
- `luckResult`  
- `interpretation`  
- `moduleId`  
- `sourceRefs`  
- `artifactContent`  
- `trace` / `audit`  

---

## 9. Stop line

Properties are the contract surface. Keep them boring and owned.

END
