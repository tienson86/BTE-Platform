# DESKTOP_COMPONENT_MAPPING.md

> BTE Design System
>
> Desktop Component Mapping
>
> Version: V1.0
>
> Status: CANONICAL
>
> This document defines the mapping between the canonical desktop layout
> and the React component architecture.
>
> Every section on the Desktop Result Page must map to exactly one root component.

---

# 1. Purpose

This document establishes a one-to-one relationship between:

- Canonical Layout
- React Components
- Business Modules

Its objectives are:

- Prevent duplicated UI
- Improve maintainability
- Standardize component naming
- Allow independent evolution of sections
- Simplify testing

---

# 2. Component Architecture

The Desktop Result Page follows this hierarchy.

```

ResultPage
│
├── ContextHeader (S00)
│
├── LifeDirectionSection
│ ├── LifeProfileCard (S01)
│ ├── OverviewCard (S02)
│ └── BaguaCard (S09)
│
├── AnalysisSection
│ ├── FourPillarsCard (S03)
│ ├── ElementBalanceCard (S04)
│ ├── StrengthCard (S05)
│ └── BoneWeightCard (S10)
│
└── InterpretationSection
├── TenGodCard (S06)
├── ShenShaCard (S07)
├── SummaryCard (S08)
└── FinalReportCard (S11)

3. Canonical Mapping
Section	React Component	Responsibility
S00	ContextHeader	Hồ sơ, thời gian, trạng thái
S01	LifeProfileCard	Thông tin bản mệnh
S02	OverviewCard	Tổng quan & hành động
S03	FourPillarsCard	Tứ Trụ Bát Tự
S04	ElementBalanceCard	Cân bằng Ngũ hành
S05	StrengthCard	Điểm sức mạnh mệnh cục
S06	TenGodCard	Thập thần
S07	ShenShaCard	Thần sát
S08	SummaryCard	Luận giải tổng hợp
S09	BaguaCard	Cung Phi / Quái Mệnh
S10	BoneWeightCard	Cân xương đoán mệnh
S11	FinalReportCard	Báo cáo tổng kết


4. Component Responsibilities
S00 — ContextHeader
Responsibilities
Display profile information
Display chart metadata
Display analysis status
Display sharing action
Must NOT perform calculations.
S01 — LifeProfileCard
Responsibilities
Nhật chủ
Mệnh cục
Định hướng
Điều kiện mệnh
Pure presentation.
S02 — OverviewCard
Responsibilities
Tổng quan
Dụng thần
Kỵ thần
Thể cục
No business logic.
S03 — FourPillarsCard
Responsibilities
Display four pillars
Heavenly stems
Earthly branches
Hidden stems (if enabled)
Uses official Four Pillars template.
S04 — ElementBalanceCard
Responsibilities
Display
Mộc
Hỏa
Thổ
Kim
Thủy
Horizontal bars only.
Forbidden
Radar Chart
Pie Chart
S05 — StrengthCard
Responsibilities
Strength score
Progress bar
Strength summary
Key observations
S06 — TenGodCard
Responsibilities
Display
10 Ten Gods
Each item contains
Icon
Name
Score
Forbidden
Ranking
Top 3
Bottom 3
Summary panel
S07 — ShenShaCard
Responsibilities
Display
Cát tinh
Hung tinh
Grouped lists only.
S08 — SummaryCard
Responsibilities
Display
Executive Summary
Strengths
Weaknesses
Recommendations
No detailed explanation.
S09 — BaguaCard
Responsibilities
Display
Official Bagua
Quái Mệnh
Nhóm Trạch
Mandatory
Use official SVG asset.
Never redraw.
Never regenerate.
S10 — BoneWeightCard
Responsibilities
Display
Bone Weight
Rating
Verse
Summary
S11 — FinalReportCard
Responsibilities
Display
Final conclusion
Highlights
Warnings
Action plan
Official title
BÁO CÁO TỔNG KẾT

5. Component Rules
Every section has one root component.
One section
↓
One component
No shared root component.

6. Component Independence
Every component must be independently testable.
Every component must support loading state.
Every component must support empty state.
Every component must support error state.
7. Data Flow

API

↓

ResultPage

↓

ResultContext

↓

Section Component

↓

Child Components

Components must never fetch API directly.

8. Folder Recommendation

applications/
portal/

components/

result/

ContextHeader/

LifeProfileCard/

OverviewCard/

FourPillarsCard/

ElementBalanceCard/

StrengthCard/

TenGodCard/

ShenShaCard/

SummaryCard/

BaguaCard/

BoneWeightCard/

FinalReportCard/

Each component owns
index.tsx
styles.ts
types.ts
hooks.ts (if needed)
tests/

9. Testing
Each component should have
Unit Tests
Visual Regression
Snapshot Tests
Root page should have
Integration Tests

10. Future Expansion
New sections
S12
S13
...
must become new root components.
Existing mappings must never be reused.

11. Source of Truth
This document is the official mapping specification.
If implementation differs,
this document has higher priority.
Developers must update implementation accordingly.


---

## Mình muốn bổ sung thêm một phần nữa (rất quan trọng cho BTE)

Đây là phần mà nhiều Design System không có, nhưng BTE nên có vì đây là **phần mềm chuyên ngành**.

### **12. Dependency Mapping**

Mỗi component sẽ chỉ rõ nó phụ thuộc vào Engine nào.

Ví dụ:

| Component | Engine |
|-----------|--------|
| ContextHeader | Profile Engine |
| LifeProfileCard | Interpretation Engine |
| OverviewCard | Analysis Engine |
| FourPillarsCard | BaZi Engine |
| ElementBalanceCard | Score Engine |
| StrengthCard | Score Engine |
| TenGodCard | Analysis Engine |
| ShenShaCard | ShenSha Engine |
| SummaryCard | Interpretation Engine |
| BaguaCard | Feng Shui Engine |
| BoneWeightCard | Bone Weight Engine |
| FinalReportCard | Report Engine |

Điều này sẽ giúp kiến trúc của BTE cực kỳ rõ ràng: **UI không chỉ biết hiển thị gì, mà còn biết dữ liệu của mình đến từ Engine nào**, rất hữu ích cho việc bảo trì và mở rộng sau này.

---

### Sau 3 file này

Đến thời điểm này chúng ta sẽ có:

- ✅ `DESKTOP_LAYOUT_SPEC.md`
- ✅ `DESKTOP_GRID_SPEC.md`
- ✅ `DESKTOP_COMPONENT_MAPPING.md`

Đây là **bộ "bản vẽ kỹ thuật" hoàn chỉnh** cho Desktop. Từ đây trở đi, mọi công việc của Cursor, Frontend Developer và QA đều có một đặc tả chung để tuân theo, thay vì mỗi bên tự diễn giải bố cục theo cách riêng.

END OF DOCUMENT

