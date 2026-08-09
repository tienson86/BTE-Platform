# Commercial Experience

Version: 1.0.0  
Sprint: PX-6

---

## Principle

BTE sells **clarity and a next conversation**, not a dashboard seat.

Commercial actions exist to keep the consultation useful after the first read.

---

## Action catalog (presentation)

| Action | Label (VI) | When | Implementation this sprint |
|--------|------------|------|----------------------------|
| Save report | Lưu báo cáo | After Result ready | Local success state + toast |
| Download PDF | Tải bản PDF | After Result ready | UX mode + print dialog hint |
| Print | In tư vấn | After Result ready | `window.print` / print mode class |
| Share | Chia sẻ | After Result ready | Share sheet UX, no backend |
| Continue reading | Tiếp tục đọc | Result + Knowledge | Navigate Knowledge |
| Related knowledge | Bài liên quan | Beside recommendation | Article then return |
| Book consultation | Đặt tư vấn chuyên sâu | After first report | Placeholder screen, no payment |

One primary commercial CTA on Result: **Lưu báo cáo**.  
Others are secondary / text.

---

## What is not commercial

- Engine scores  
- Schema / IDs  
- Admin metrics  
- Fake urgency countdown  

---

END
