# 02 — Label Language Standard

Version: 1.0  
Status: **OFFICIAL — Commercial Label Language Standard**  
Date: 2026-08-08  
Depends on: `01_P0_IMPROVEMENT_PLAN.md` · Brand Language (consultant, not calculator)  
Scope: Documentation only — defines wording; no runtime yet  

---

## 1. Purpose

Replace technical / romanized Analysis tokens in **customer-facing** commercial text with consistent consultant language.

Applies to Wave 1.1 bound prose and any future unit that exposes the same placeholders.

---

## 2. Principles

1. **Customer never sees engine tokens** (`vuong`, `nhuoc`, `can`, `matched rules`, `kích hoạt khi`, raw enums).  
2. **One concept → one commercial phrase** (stable across Identity / Strength / Weakness).  
3. **Labels describe posture, not grades** — no fake precision.  
4. **Bind from Analysis truth** — commercial labels are a presentation map, not new facts.  
5. **Vietnamese commercial default** for Result.

---

## 3. Strength band commercial map

| Analysis token / signal (examples) | Forbidden in customer text | Official commercial label (`strength_band_label`) |
|------------------------------------|----------------------------|---------------------------------------------------|
| `vuong`, `vượng`, strong_support, score ≥ ~55 favorable | `vuong`, `vượng` as bare token | **được nâng đỡ / đang vững** |
| `can`, `cân`, balanced mid | `can` as bare token | **đang cân bằng** |
| `nhuoc`, `nhược`, weak, overtaxed, score thin | `nhuoc`, `nhược` as bare token | **đang mỏng lực / cần giữ mực** |
| unknown / empty | inventing a band | **chưa xác định rõ** (rare; prefer omit clause) |

### Preferred full phrases (for KU authors)

| Context | Preferred phrase |
|---------|------------------|
| Identity (KU-ID-001) | `Ở mức thân được nâng đỡ` / `Ở mức thân đang cân bằng` / `Ở mức thân đang mỏng lực` |
| Strength (KU-ST-001) | `cấu trúc đang được nâng đỡ` / `nhịp đang cân bằng` |
| Weakness when thân thin (KU-WK-001 frame A) | `lực cấu trúc đang mỏng` |
| Weakness when enemy on strong (frame B) | **do not** say mỏng; see `03` |

Authors may keep placeholder `{strength_band_label}` **only if** the projection contract guarantees commercial labels above.

---

## 4. Other commercial labels

| Signal | Forbidden | Commercial form |
|--------|-----------|-----------------|
| Day master | Raw dump as sole Exec | `Nhật chủ {day_master_label}` inside full sentence |
| Pattern | Engine code alone | `cấu trúc {pattern_label}` (human pattern name already OK if Vietnamese) |
| Useful god | Token-only Rec (`Thủy`) | `Dụng thần {useful_god_label}` inside action/reason sentences |
| Enemy / ky | Duplicated raw list | Single caution noun phrase — see `03` |
| Grade / score | Leading with grade letters | Optional side evidence only — not Exec hero |

---

## 5. Technical wording denylist (customer text)

Never ship in bound `modern_interpretation`:

- `kích hoạt`, `matched rules`, `matched_rules`, `(mock)`, `placeholder`  
- Bare romanizations: `vuong`, `nhuoc`, `can` (as band)  
- English engine crumbs (`strong_support`, `overtaxed`) unless wrapped in approved Vietnamese commercial label  

Classical short citations in `classical_text` remain internal / scholar side — not Exec hero copy.

---

## 6. Consistency rules across units

| Rule | Detail |
|------|--------|
| Same band → same label | ID and ST must not disagree on thân posture |
| ST present ⇒ not “mỏng lực” in WK frame A | Conflict = drop or switch to frame B |
| UG/RC | Do not restate band tokens; defer to ID/ST/WK |

---

## 7. Implementation note (not this sprint)

Projection layer should map Analysis → commercial labels **before** bind.  
Until then, KU revision may inline preferred phrases and narrow placeholder use.

**This sprint does not modify runtime.**

---

## 8. Stop line

Label Language Standard defined for IA-P0-01. Apply via Wave 1.1 update plan after Product approval.

---

END
