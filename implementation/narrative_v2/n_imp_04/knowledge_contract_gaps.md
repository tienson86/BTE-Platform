# N-IMP-04 Knowledge Contract Gaps

Sprint: N-IMP-04
Purpose: input for later Knowledge Expansion. Do not fill these gaps in this sprint.

---

## strength

| Gap | Notes |
|-----|--------|
| No Narrative V2 record keyed to `core.pattern_context` / `core.useful_god_context` | Resolver uses parent entity `knowledge.strength.strong` via evidence `strength.level` |
| No `customer_meaning` field on Strength entities | `customer_meaning_candidate` remains None. Rewrite owns customer language. |

## pattern

| Gap | Notes |
|-----|--------|
| No record keyed to `core.pattern_context` | Parent entity `knowledge.pattern.chinh_an` used via `pattern.primary=chinh_an` |
| `pattern.cach_cuc=Chính Ấn` is not an exact Pattern `key` | Not aliased. `chinh_an` already matches. Do not invent label↔key maps beyond id suffix. |
| No `customer_meaning` field | Candidate remains None |

## useful_god

| Gap | Notes |
|-----|--------|
| No record keyed to `core.useful_god_context` | Parent entity `knowledge.useful_god.chinh_quan` used via `useful_god.primary` |
| Element `Hỏa` has no UsefulGod entity | Not resolved. Must not become “Nên dùng màu đỏ.” |
| Stem `Đinh` exists (`knowledge.useful_god.dinh`) but is not in this sprint’s lookup evidence ids | Left unused. Do not infer stem from element. |

## temperature

| Gap | Notes |
|-----|--------|
| `knowledge/interpretation/domains/temperature/` has 0 entities | `core.temperature_balancing_context` is UNRESOLVED (`no_approved_knowledge`) |
| Concept `warming_cold_chart` is approved but not an exact key for `warming` / `cold` | Not used. Guessing forbidden. |

## ten_gods

| Gap | Notes |
|-----|--------|
| No record keyed to `core.pattern_ten_gods_relation` | Parent entities resolved from visible labels + pattern primary |
| Hidden ten gods not in this sprint’s lookup | Visible labels only |

## shensha

| Gap | Notes |
|-----|--------|
| N-IMP-03 boundary `approved_rule_unavailable` | N-IMP-04 resolved approved ShenSha entities by exact name. Boundary is traced, not dropped. |
| No romance/career outcome fields used | `applications` rejected. Do not derive “Tình duyên thuận lợi.” |
| Coverage markdown says EXPERT_READY | JSON `metadata.status` is `approved`. Quality token is not the eligibility contract. |

## luck

| Gap | Notes |
|-----|--------|
| `knowledge/interpretation/domains/luck/` has 0 entities | `core.luck_temporal_context` is UNRESOLVED (`no_approved_knowledge`) |
| Current cycle `Ất Tỵ` has no luck-quality knowledge | Must not become “Giai đoạn thuận lợi để mở rộng.” |

## commercial

| Gap | Notes |
|-----|--------|
| CK-01 catalog is frozen architecture, not per-item approved JSON with `metadata.status` | Not indexed. Do not create Action Plan. |
| No consulting units keyed to N-IMP-03 semantic keys | Unresolved for commercial merge (out of sprint) |
| `customer_meaning` is not published on interpretation entities | Commercial Rewrite remains the owner of final customer language |
