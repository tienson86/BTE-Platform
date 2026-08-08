# 07 — Versioning Policy

Version: 1.0.0  
Status: **OFFICIAL**  
Date: 2026-08-08  
Owner: BTE Product  

---

## 1. Purpose

Define how BTE versions **Commercial** trains, **Capabilities**, and **Knowledge**.

---

## 2. Commercial version (product train)

Format: `Commercial MAJOR.MINOR` or `Commercial MAJOR` with patch notes.

| Bump | When |
|------|------|
| **Major** (e.g. V1 → V2) | Breakthrough product scope; multiple new Domains/Capabilities; breaking customer journey expectations |
| **Minor** (e.g. V1 → V1.1) | New Capability or significant polish train inside same architecture era |
| **Patch** (e.g. V1.0.x notes) | Bug fix / hotfix / small quality revision without new Capability |

RC labels: `Commercial V1 RC1`, `RC2`, … until Product GO.

**Commercial V1 is not Released until Product sign-off** — RC labels are not Releases.

---

## 3. Capability version

Format: semver `MAJOR.MINOR.PATCH` on Capability Registry entries.

| Bump | When |
|------|------|
| **1.0.0** | First Production Capability release |
| **MINOR** | Customer-visible enrichment of the same Capability |
| **PATCH** | Wording / binding / non-breaking fix |
| **MAJOR** | Breaking change to customer outcome model |

Aligns with `knowledge/product/02_CAPABILITY_RELEASE_POLICY.md`.

---

## 4. Knowledge version

| Layer | Versioning |
|-------|------------|
| Knowledge Unit `version` field | Per-unit semver / dotted version in CSV |
| Domain corpus wave id | e.g. `W-D01-C-SEL`, `W-D01-E-PRO` |
| Database changelog | `database/20_knowledge/CHANGELOG.md` |

Knowledge bumps that change customer advice require Golden Case Gate and appropriate Capability patch/minor.

---

## 5. Coexistence rules

| Rule | Detail |
|------|--------|
| Capability Released ≠ Commercial Released | Both tracked separately |
| Multiple Capabilities may share one Commercial train | e.g. SEL + PRO in Commercial V1 |
| Hotfix patches Commercial notes and affected Capability PATCH | Keep Registry truthful |

---

## 6. Examples

| Event | Commercial | Capability | Knowledge |
|-------|------------|------------|-----------|
| Career Selection first production | V1 RC… | CAP-CAREER-SEL-001 `1.0.0` | SEL units + wave |
| Promotion first production | still V1 RC… | CAP-CAREER-PRO-001 `1.0.0` | PRO units + wave |
| Product GO for Commercial V1 | **V1 Released** | unchanged unless bump needed | — |
| Exec wording hotfix | V1 patch note | possibly PATCH | unit PATCH or presentation-only |
| Leadership Assessment ships | V1.1 or V2 (Product) | new `1.0.0` | new wave |

---

## 7. Stop line

Do not advertise a Commercial version as Released based only on Capability Registry status.

---

END
