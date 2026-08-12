# Authoring Pipeline — V1.0

| Field | Value |
|-------|-------|
| Document | AUTHORING_PIPELINE |
| Version | 1.0.0 |
| Section | 5 — Authoring |

---

# 5.1 Purpose

Create **Interpretation Knowledge** (Knowledge Library) — consulting-grade prose that defines **what to say** for a domain pack.

Location: `knowledge/interpretation_knowledge/PACK_XX_<DOMAIN>/`

---

# 5.2 Prerequisites

| Prerequisite | Gate |
|--------------|------|
| Pack charter approved | QG0 |
| Rule Database scope known | Facts the pack may reference |
| Interpretation Standard read | Modes, bans, Customer Mode |
| Topic list frozen | Chapter plan |

---

# 5.3 Authoring workflow

```text
Charter approved
  ↓
Outline chapters (KNOWLEDGE_INDEX)
  ↓
Draft prose per topic
  ↓
Self-check (professional, no rule dump)
  ↓
Domain Reviewer read
  ↓
Library version bump
  ↓
QG1 pass → Catalog may begin
```

---

# 5.4 Chapter structure (PACK-01 reference)

| Chapter | Topic |
|---------|-------|
| 01 | Meanings |
| 02 | Causes |
| 03 | Advantages |
| 04 | Challenges |
| 05 | Personality |
| 06 | Career |
| 07 | Wealth |
| 08 | Marriage |
| 09 | Health |
| 10 | Luck |
| 11 | Recommendations |
| 12 | Edge cases |
| 13 | Examples (Validation) |

New packs define their own chapter list at QG0. Structure may vary; factory pipeline does not.

---

# 5.5 Authoring rules

| Rule | Detail |
|------|--------|
| Knowledge only | No engine, no Reasoning, no Report |
| No Rule Database edit | Reference facts; do not redefine |
| No Interpretation Standard edit | Follow existing modes |
| Class coverage | All professional classes in domain |
| Commercial voice | Consultant, not textbook |
| Examples chapter | Validation / teaching; not Customer headline |
| KNOWLEDGE_INDEX | Every chapter indexed |

---

# 5.6 Cursor role in authoring

Cursor may:

- Draft prose from outlines (human edits required)
- Check consistency across chapters
- Flag cross-pack bleed

Cursor may not:

- Publish Library without Domain Reviewer
- Invent doctrine not approved by domain

---

# 5.7 Library versioning

Increment **Knowledge Version** when:

- Any chapter content changes
- New chapter added
- Professional correction applied

See [VERSIONING.md](VERSIONING.md).

---

# 5.8 Exit criteria (QG1)

- All chapters complete
- Domain Reviewer sign-off
- KNOWLEDGE_INDEX and README current
- No open professional disputes

---

END
