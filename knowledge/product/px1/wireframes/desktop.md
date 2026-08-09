# Wireframe — Desktop

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-1  
Breakpoint: Desktop · 12-column · page padding 32px

No implementation. Structural sketch only.

---

## First viewport

```
┌──────────────────────────────────────────────────────────────────────────┐
│  [Product chrome]                                                         │
│  Đến nội dung tư vấn                                                      │
├────────────┬─────────────────────────────────────────────────────────────┤
│ TOC (opt.) │  HERO                                                       │
│            │  Danh tính                                                  │
│ Tóm tắt    │  Tiêu đề tư vấn                                             │
│ Định hướng │  Một câu tóm tắt                                            │
│ Lưu ý      │  Trạng thái tư vấn                                          │
│ Sự nghiệp  │                                                             │
│ Tài chính  ├─────────────────────────────────────────────────────────────┤
│ Quan hệ    │  TÓM TẮT TƯ VẤN                                             │
│ Sức khỏe   │  • (câu 1)                                                  │
│ Vận trình  │  • (câu 2)                                                  │
│ Biểu đồ    │  • (câu 3)                                                  │
│ Kỹ thuật   │  • (câu 4)                                                  │
│ Kiến thức  │  • (câu 5)                                                  │
│ Phụ lục    │                                                             │
└────────────┴─────────────────────────────────────────────────────────────┘
```

TOC is optional. If present, labels match section titles. Hero is not titled “Hero”.

---

## Below fold (continues same column)

```
┌──────────────────────────────────────────────────────────────────────────┐
│  ĐỊNH HƯỚNG CHÍNH                          [ Primary CTA ]               │
│                                                                          │
│  Sự nghiệp              Tài chính               Quan hệ                  │
│  ┌────────────────┐    ┌────────────────┐    ┌────────────────┐         │
│  │ Vì sao         │    │ Vì sao         │    │ Vì sao         │         │
│  │ Kết quả kỳ vọng│    │ Kết quả kỳ vọng│    │ Kết quả kỳ vọng│         │
│  │ Việc cần làm   │    │ Việc cần làm   │    │ Việc cần làm   │         │
│  │ Xem thêm       │    │ Xem thêm       │    │ Xem thêm       │         │
│  └────────────────┘    └────────────────┘    └────────────────┘         │
│  Sức khỏe               Vận trình                                        │
│  ┌────────────────┐    ┌────────────────┐                               │
│  │ …              │    │ …              │                               │
│  └────────────────┘    └────────────────┘                               │
├──────────────────────────────────────────────────────────────────────────┤
│  LƯU Ý QUAN TRỌNG                                                        │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ Cảnh báo · giảm nhẹ · Xem thêm                                     │  │
│  └────────────────────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────────────────────┤
│  SỰ NGHIỆP     (full width domain chapter)                               │
│  TÀI CHÍNH                                                               │
│  QUAN HỆ                                                                 │
│  SỨC KHỎE                                                                │
│  VẬN TRÌNH                                                               │
├──────────────────────────────────────────────────────────────────────────┤
│  BIỂU ĐỒ MINH HỌA                                                        │
│  ┌───────────────────────────┐  ┌───────────────────────────┐           │
│  │ Figure + chú thích VI     │  │ Figure + chú thích VI     │           │
│  └───────────────────────────┘  └───────────────────────────┘           │
├──────────────────────────────────────────────────────────────────────────┤
│  ▶ Chi tiết kỹ thuật          (collapsed)                                │
│  ▶ Kiến thức bổ sung          (collapsed)                                │
│  PHỤ LỤC                                                                 │
│  Footer                                                                  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Desktop rules

- Max content width centered (1600px / 1800px ultra-wide)  
- Summary is one reading column — not three equal hero tiles  
- Rec *groups* may wrap 2–3 columns; group order unchanged  
- Domains are sequential full-width chapters  
- Charts appear only after domains  
- No metadata ribbon in Hero  

---

END
