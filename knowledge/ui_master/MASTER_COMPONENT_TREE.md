# BTE Platform

# MASTER_COMPONENT_TREE

---

Version

1.0.0

Status

MASTER

Module

UI_MASTER

Document

MASTER_COMPONENT_TREE

Owner

Product Owner

Purpose

Canonical Component Hierarchy for the entire BTE Desktop Portal.

---

# 1. Purpose

MASTER_COMPONENT_TREE định nghĩa toàn bộ cây Component chuẩn của BTE Platform.

Đây là tài liệu kết nối giữa:

Business

↓

Information Architecture

↓

Master Layout

↓

React Component Tree

Tài liệu này không định nghĩa giao diện.

Không định nghĩa CSS.

Không định nghĩa Tailwind.

Chỉ định nghĩa:

- Component Hierarchy
- Component Ownership
- Component Responsibility
- Component Dependency

---

# 2. Design Philosophy

Một Component chỉ có:

- một trách nhiệm
- một vị trí
- một vai trò

Không có Component đa mục đích.

Không có Component "God Component".

---

# 3. Canonical Component Tree

```
PortalPage

├── PortalHeader
│
├── PortalSidebar
│
├── PortalContent
│   │
│   ├── S00ContextHeader
│   │
│   ├── S01IdentityDecisionPanel
│   │
│   ├── S02OverviewActions
│   │
│   ├── S03FourPillars
│   │
│   ├── S04ElementBalance
│   │
│   ├── S05Strength
│   │
│   ├── S06TenGods
│   │
│   ├── S07ShenSha
│   │
│   ├── S08Interpretation
│   │
│   └── LearningPanel
│
└── PortalFooter
```

Đây là cây chuẩn.

Không thay đổi.

---

# 4. Root Component

Root luôn là:

```
PortalPage
```

PortalPage chỉ có trách nhiệm:

- tạo bố cục
- điều phối Section

Không chứa Business Logic.

Không chứa API Logic.

---

# 5. Header Component

```
PortalHeader

├── Logo

├── MainNavigation

├── UserMenu
```

Không thêm Component khác.

---

# 6. Sidebar Component

```
PortalSidebar

├── SidebarTitle

├── NavigationTree

├── UtilityLinks

└── VersionInfo
```

Sidebar không hiển thị dữ liệu lá số.

---

# 7. Portal Content

```
PortalContent

↓

Section Components
```

PortalContent không chứa Card.

Không chứa Metric.

Không chứa Badge.

Chỉ chứa các Section.

---

# 8. S00 Context Header

```
S00ContextHeader

├── ContextIdentity

├── ContextMetadata

├── ContextStatus

└── ContextActions
```

Không hiển thị:

- Hero
- Decision
- Strength

---

# 9. S01 Identity & Decision

```
S01IdentityDecisionPanel

├── IdentityCard

├── ConditionCard

├── DecisionPanel
```

DecisionPanel gồm:

```
DecisionPanel

├── WhatCard

├── WhyCard

└── NextCard
```

Không Component nào vượt DecisionPanel.

---

# 10. S02 Overview

```
S02OverviewActions

├── SummaryCards

├── QuickActions

└── ExportActions
```

Overview không chứa phân tích.

---

# 11. S03 Four Pillars

```
S03FourPillars

├── YearPillarCard

├── MonthPillarCard

├── DayPillarCard

└── HourPillarCard
```

DayPillarCard luôn là Component trung tâm.

---

# 12. S04 Element Balance

```
S04ElementBalance

├── ElementChart

├── BalanceSummary

└── BalanceLegend
```

Legend luôn phụ thuộc Chart.

---

# 13. S05 Strength

```
S05Strength

├── StrengthScore

├── StrengthEvidence

└── RecommendationCard
```

Recommendation không được đứng trước Evidence.

---

# 14. S06 Ten Gods

```
S06TenGods

├── TenGodGrid

│   └── TenGodCard

└── TenGodSummary
```

TenGodCard là Component lặp.

---

# 15. S07 ShenSha

```
S07ShenSha

├── ShenShaCategory

│   └── ShenShaCard

└── ShenShaSummary
```

Không hiển thị toàn bộ ShenSha trong một Card.

---

# 16. S08 Interpretation

```
S08Interpretation

├── InterpretationHeader

├── InterpretationContent

├── InterpretationEvidence

└── InterpretationActions
```

InterpretationContent là vùng đọc chính.

---

# 17. Learning Panel

```
LearningPanel

├── LearningNavigation

├── KnowledgeArticle

├── RelatedTopics

└── CloseAction
```

Learning không phụ thuộc vào Reading Flow chính.

---

# 18. Shared Components

Các Component dùng chung.

```
SectionHeader

Card

InfoCard

MetricCard

EvidenceCard

Badge

Chip

ScoreBar

ProgressBar

ActionBar

Accordion

Drawer

Tooltip

EmptyState

LoadingState

ErrorState
```

Không tạo phiên bản riêng cho từng Section nếu Pattern đã tồn tại.

---

# 19. Dependency Rules

Dependency chỉ theo chiều từ trên xuống.

```
PortalPage

↓

Section

↓

Container

↓

Card

↓

Element
```

Không được:

Card

↓

Section

Không Circular Dependency.

---

# 20. Cursor Implementation Rules

Cursor phải:

- tạo Component đúng cây này.
- không gộp nhiều Section.
- không chia nhỏ Component ngoài Specification.
- không tạo Component "helper" làm thay đổi Hierarchy.

Nếu cần Component mới:

STOP.

Chờ Product Owner Approval.

---

# 21. Product Owner Checklist

□ Root đúng.

□ Header đúng.

□ Sidebar đúng.

□ PortalContent đúng.

□ S00 đúng.

□ S01 đúng.

□ S02 đúng.

□ S03 đúng.

□ S04 đúng.

□ S05 đúng.

□ S06 đúng.

□ S07 đúng.

□ S08 đúng.

□ Learning đúng.

□ Shared Components đúng.

□ Dependency đúng.

PASS khi toàn bộ Component Tree khớp với Master UI.

---

# Appendix A — Complete Component Hierarchy

```
PortalPage

├── PortalHeader
│   ├── Logo
│   ├── MainNavigation
│   └── UserMenu
│
├── PortalSidebar
│   ├── SidebarTitle
│   ├── NavigationTree
│   ├── UtilityLinks
│   └── VersionInfo
│
├── PortalContent
│   ├── S00ContextHeader
│   ├── S01IdentityDecisionPanel
│   ├── S02OverviewActions
│   ├── S03FourPillars
│   ├── S04ElementBalance
│   ├── S05Strength
│   ├── S06TenGods
│   ├── S07ShenSha
│   ├── S08Interpretation
│   └── LearningPanel
│
└── PortalFooter
```

---

# Appendix B — Component Ownership Matrix

| Component | Responsibility |
|-----------|----------------|
| PortalPage | Layout |
| Header | Navigation |
| Sidebar | Navigation |
| S00 | Context |
| S01 | Identity + Decision |
| S02 | Overview |
| S03 | Structure |
| S04 | Balance |
| S05 | Strength |
| S06 | Ten Gods |
| S07 | ShenSha |
| S08 | Interpretation |
| Learning | Knowledge |

Mỗi Component chỉ có một trách nhiệm.

---

# Appendix C — Golden Rules

1. Một Component chỉ có một trách nhiệm.
2. Không Component đa mục đích.
3. Shared Components được ưu tiên tái sử dụng.
4. Không tạo Component trùng chức năng.
5. Không phá vỡ Component Hierarchy.
6. Không Circular Dependency.
7. Business Logic không nằm trong Layout Component.
8. Section không biết Section khác.
9. Component Tree luôn phản ánh Information Architecture.
10. React phải triển khai đúng cây Component này.

---

# Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | MASTER | Initial Master Component Tree |