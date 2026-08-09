# Empty State Guide — Result Experience V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-1

---

## 1. Purpose

Empty is a consulting honesty, not a blank dashboard tile.

Use `CardEmpty`.  
Never fake content to avoid emptiness.

---

## 2. Principles

1. Speak Vietnamese  
2. Explain what is missing in human language  
3. Offer the next useful read  
4. Do not use Danger styling  
5. Do not show English “No data”  
6. Do not leave a silent hole that looks like a bug  

---

## 3. By section

| Section | When empty | Message intent | Next step |
|---------|------------|----------------|-----------|
| Hero | Cannot identify user | Cannot open a consultation without identity | Recover via error pattern (this is not a soft empty) |
| Tóm tắt tư vấn | No summary available | Session cannot lead — escalate to page error | Error State Guide |
| Định hướng chính | No recs | Chưa có định hướng cụ thể trong buổi này | Read domains if any; else error/partial status |
| Lưu ý quan trọng | No qualified warnings | **Không có lưu ý vượt ngưỡng trong buổi này.** | Continue to domains — do not invent fear |
| A life domain | No domain content | **Chưa có luận giải cho [tên lĩnh vực] trong buổi tư vấn này.** | Continue next domain / Định hướng chính |
| Charts | No charts | **Chưa có biểu đồ minh họa.** | Advice still stands without charts |
| Technical | No technical payload | **Chưa có chi tiết kỹ thuật để kiểm tra.** | Stay collapsed; do not block advice |
| Knowledge | No KU | **Chưa có bài đọc thêm cho buổi này.** | Stay collapsed |
| Appendix | Always has at least scope/limits | Should not be empty | Write generic scope close |

---

## 4. Anatomy

```
Title     (Vietnamese, calm)
Body      (one or two sentences)
Next      (tertiary text action, optional)
```

No illustration theatre.  
No giant empty-box icons dominating P1.

---

## 5. Partial consultation

If some domains exist and others do not:

- Keep section order  
- Show empty cards in missing domains  
- Status may be **Tư vấn một phần**  
- Do not hide empty domain sections to “look fuller” — honesty beats collage  

Exception: Lưu ý quan trọng may omit the section entirely when there is truly nothing to warn, replacing it with nothing rather than a fake warning. A single quiet empty line is acceptable if layout needs a stable slot.

---

## 6. Forbidden

- Skeleton forever pretending content will arrive when it will not  
- Random motivational quote  
- Upsell in the empty hole  
- Engine null dumps  

---

## 7. Stop line

Empty states protect trust.

END
