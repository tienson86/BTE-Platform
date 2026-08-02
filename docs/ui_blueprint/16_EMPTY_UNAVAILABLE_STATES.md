# 16 — EMPTY / UNAVAILABLE STATES (Addendum K)

| Field | Value |
|-------|--------|
| **Document** | `16_EMPTY_UNAVAILABLE_STATES.md` |
| **Addendum** | **K** |
| **Version** | `1.1.0` |
| **Status** | **Normative — Blueprint V1.1 Final** |

---

## Purpose

Freeze every empty / missing / error presentation so implementers never invent “placeholder fake data” or inconsistent empty UI.

---

## 1. State taxonomy

| State ID | When | Visual component |
|----------|------|------------------|
| `PAGE_EMPTY` | No ResultStore payload | EmptyState + CTA Analyze |
| `TIER_PARTIAL` | Tier exists; some slots missing | Tier renders; slots use UNAVAILABLE |
| `SLOT_UNAVAILABLE` | Bound field absent | UnavailableBlock |
| `SLOT_PLACEHOLDER` | Value present but display `--` for empty string | Inline `--` (not a block) |
| `CHART_EMPTY` | Series cannot render | ChartEmpty |
| `LIST_EMPTY` | Array empty but key exists | Caption “—” or i18n empty list — not fake bullets |
| `EXPERT_ERROR` | Discussion API failure | ErrorPanel + Retry |
| `EXPERT_LOADING` | Request in flight | Skeleton in answer pane |
| `SECTION_COLLAPSED_EMPTY` | Chapter/section empty + collapsed | Title visible; body Unavailable when expanded |

---

## 2. Copy contract (VI defaults — see Localization)

| State | Default VI message key | Intent |
|-------|------------------------|--------|
| PAGE_EMPTY | `result.empty` | Guide to Analyze |
| SLOT_UNAVAILABLE | `report.unavailable` | Calm honesty |
| CHART_EMPTY | `report.unavailable` | No fake axes |
| EXPERT_ERROR | `discussion.expert_unavailable` | Retry possible |
| FirstRecommendation missing | `report.unavailable` under “Khuyến nghị đầu tiên” | — |
| Quality missing | Unavailable — never invent “lá số tốt” | — |

Tone: professional, non-fearful, non-blaming.

---

## 3. What must remain visible when empty

| Region | Must still show |
|--------|-----------------|
| NavigationRail | All six tier labels (disabled jumps only if PAGE_EMPTY) |
| Hero structure | Eyebrow + DayMaster area (Unavailable values OK) + metric shells |
| Interpretation TOC | Chapter titles when ≥2 chapters configured |
| Relation matrix | All five row labels (Hợp…Phá) with Unavailable cells |
| Knowledge tier title | Always |

---

## 4. What must never be faked

- Pillar stems/branches  
- Dụng / Hỷ / Kỵ  
- Pattern name  
- Luck decades / Hợp-Xung values  
- Classical book names  
- Confidence numbers  
- Recommendations  
- Gauge numeric value (use text Thân fallback instead)  

---

## 5. Error vs Unavailable

| | Unavailable | Error |
|--|-------------|-------|
| Meaning | Data not in payload | Request/system failed |
| Retry | No | Yes when applicable |
| Color | Neutral dashed | Danger only for system error |

Kỵ thần is **not** an Error state.

---

## 6. Skeleton rules

- First paint: rail + hero outline only  
- No skeleton that looks like real scores  
- Replace atomically when view-model ready  

---

## Version

`1.1.0`
