# Error State Guide — Result Experience V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-1

---

## 1. Purpose

Errors are part of the consultation contract: honest, calm, recoverable.

Use `CardError` for section failures.  
Use a page-level error only when the consultation cannot start.

---

## 2. Principles

1. Vietnamese only  
2. Say what failed in human terms  
3. Say what the user can do next  
4. Do not dump stack traces, schema, or pipeline names  
5. Danger role is for blocking issues — not for every warning  
6. Preserve any successful P1 content when a lower section fails  

---

## 3. Levels

| Level | When | Behavior |
|-------|------|----------|
| **Page** | Hero + Tóm tắt cannot be formed | Full-page error · no fake report |
| **Region** | Định hướng chính fails but summary exists | Show summary · error card in rec region |
| **Section** | One domain / charts / technical / knowledge fails | Local error card · rest of page remains |
| **Inline** | Single expand payload fails | Error inside expand · parent card stays |

A chart error must never hide Tóm tắt or Định hướng.

---

## 4. Anatomy

```
Status     (short · Vietnamese)
Explanation
Recovery action
Optional note
```

Example intent:

**Không thể hiển thị phần tài chính.**  
Phần còn lại của buổi tư vấn vẫn đọc được.  
**Thử tải lại phần này** · hoặc **Quay lại tóm tắt tư vấn**.

---

## 5. Recovery actions

| Situation | Recovery intent |
|-----------|-----------------|
| Transient section failure | Thử lại phần này |
| Page failure | Thử tải lại buổi tư vấn |
| Partial capability missing | Đọc các phần sẵn có |
| Technical panel failure | Ẩn kỹ thuật · advice still valid |
| Knowledge failure | Bỏ qua đọc thêm |

Recovery labels are Tertiary or Secondary — not a second Primary that competes with consulting CTA when advice is still available.

---

## 6. Mapping vs empty

| Symptom | Pattern |
|---------|---------|
| Capability not in this session | Empty |
| Capability should exist but call failed | Error |
| User not entitled | Empty or limited status — not a red crash |
| Identity missing | Page error |

---

## 7. Screen reader and focus

- Error is announced when it appears  
- Focus moves to page error on full failure  
- Section error does not steal focus from P1 on first load unless it blocks the only content  

---

## 8. Forbidden

- `500 Internal Server Error` as the only copy  
- English exception class names  
- Retry loops without explanation  
- Replacing the whole page because one chart failed  
- Blaming the user  

---

## 9. Stop line

Errors keep the consultant trustworthy under failure.

END
