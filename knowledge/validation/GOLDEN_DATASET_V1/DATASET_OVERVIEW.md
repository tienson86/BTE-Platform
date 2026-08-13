# DATASET_OVERVIEW

| Field | Value |
|-------|-------|
| Document | DATASET_OVERVIEW |
| Dataset | GOLDEN_DATASET_V1 |
| Date | 2026-08-13 |
| Status | Official laboratory inventory |

---

## Current dataset

GOLDEN_DATASET_V1 reserves **10 case slots**.

| Band | Cases | Role |
|------|-------|------|
| Populated | CASE_0001, CASE_0002, CASE_0003 | Existing validation artifacts, indexed only |
| Placeholder | CASE_0004–CASE_0010 | Structure only; no chart bound |

No new chart content was authored for this laboratory.

### CASE_0001 — Golden commercial reference

| Field | Value |
|-------|-------|
| Subject | Nguyễn Tiến Sơn |
| Role | Frozen commercial / regression reference |
| Chart | Strong adult male · self-carry · Chính Ấn |
| Source tree | Scattered existing artifacts (pilot, master interpretations, feature samples, customer review) |
| Laboratory folder | [CASE_0001/](CASE_0001/README.md) |

### CASE_0002 — Generalization / follow-output

| Field | Value |
|-------|-------|
| Subject | Hoàng Thị Thu Phương |
| Role | Adult female balanced + Tòng Nhi + output-led |
| Source tree | `knowledge/validation/CASE_0002/` |
| Laboratory folder | [CASE_0002/](CASE_0002/README.md) |

### CASE_0003 — Extreme weak child stress

| Field | Value |
|-------|-------|
| Subject | Female child (2015) · Hà Nội |
| Role | Extreme weak + minor packaging stress |
| Source tree | `knowledge/validation/CASE_0003/` |
| Laboratory folder | [CASE_0003/](CASE_0003/README.md) |

---

## Coverage

| Dimension | Present | Missing |
|-----------|---------|---------|
| Strong adult | CASE_0001 | — |
| Balanced / follow-output adult | CASE_0002 | — |
| Extreme weak | CASE_0003 | Adult weak (non-child) |
| Child / minor packaging | CASE_0003 | Additional ages |
| Male | CASE_0001 | Additional males |
| Female | CASE_0002, CASE_0003 | — |
| Self-carry / over-responsibility | CASE_0001 | — |
| Output / Thương Quan led | CASE_0002, CASE_0003 | — |
| Special pattern | — | CASE slot open |
| Mixed / tension (non-follow) | Partial in 0002/0003 | Dedicated mixed adult |
| No useful god (control) | — | CASE slot open |
| Thin evidence (control) | — | CASE slot open |
| Business / marriage / health / wealth intent | — | Intent cases not bound |
| Geographic diversity | Hà Nội, Quảng Ninh | Other regions |

Structural methodology already defined in:

`knowledge/real_case_validation/01_GOLDEN_CASE_SELECTION.md`

That set (12 consultation profiles) is **methodology**. GOLDEN_DATASET_V1 is the **bound laboratory**. Only three profiles are bound today.

---

## Known gaps

1. **Seven unbound slots** (CASE_0004–CASE_0010).
2. **One Golden only.** Commercial V1.0 cannot rest on a single shippable chart type.
3. **CASE_0002** is improved vs baseline but below commercial KPI floor (latest published overall ~6.7 / 10 after CLL V1.2).
4. **CASE_0003** fails commercial fitness for a minor + weak chart (overall 4.2 / 10). Engine detection of weakness is not the gap; packaging and language bias are.
5. **Calendar / stated-pillar dispute** on CASE_0003 remains an open S1 (`ISS-C3-001`).
6. **Master Consulting** remains policy-NOT_AVAILABLE on non-golden generic runs.
7. **Luck / full DaYun timeline** is a known commercial thin spot on CASE_0001 Part 06 (accepted with packaging conditions, not solved).
8. **Intent diversity** (business, marriage, health, wealth) is not bound to laboratory cases.
9. This laboratory does **not** replace `tests/golden_dataset/` analytical fixtures. Engine-level golden coverage is a separate system.

---

## Roadmap

| Stage | Target | Exit |
|-------|--------|------|
| **Lab V1.0** (this package) | Registry + protocol + 3 populated + 7 placeholders | Laboratory usable |
| **RC1** | CASE_0001 frozen; protocol obeyed; 0002/0003 registered | See [RELEASE_CRITERIA.md](RELEASE_CRITERIA.md) |
| **RC2** | 0001 remains Golden; 0002 reaches commercial floor **or** is formally classified STRESS/GAP; 0003 packaging policy decided | Two adult types + one stress case governed |
| **Bind 0004–0010** | Fill gaps: adult weak, special pattern, mixed, no UG, thin evidence, intent cases | Coverage matrix complete |
| **Commercial V1.0** | Designated commercial set passes KPIs + 100% Golden regression | Product sign-off |

Binding a placeholder requires Product + Domain approval per [GOVERNANCE.md](GOVERNANCE.md). Do not fill slots by copying CASE_0001 prose.

---

END
