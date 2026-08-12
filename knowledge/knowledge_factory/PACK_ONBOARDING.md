# Pack Onboarding — V1.0

| Field | Value |
|-------|-------|
| Document | PACK_ONBOARDING |
| Version | 1.0.0 |
| Section | 15 — Pack Onboarding |

---

# 15.1 Rule

**Pack 02, Pack 03, … enter the same factory.**

No pack defines its own production pipeline.

Packs may define **constraints** and **schema**. Factory defines **process**.

---

# 15.2 Onboarding checklist

```text
□ QG0 — Charter approved (Chief Reviewer)
□ Domain and fact boundaries documented
□ Interpretation Standard alignment confirmed
□ Topic/chapter list frozen
□ Pack folder created:
    knowledge/interpretation_knowledge/PACK_XX_<DOMAIN>/
    knowledge/knowledge_catalog/PACK_XX_<DOMAIN>/
    knowledge/knowledge_qa/PACK_XX_<DOMAIN>/
□ Reasoning FREEZE folder planned (may follow catalog)
□ Id policy defined (e.g. IK-PAT-MEAN-0001)
□ CATALOG_SCHEMA drafted
□ Factory CHECKLISTS assigned to roles
□ Metrics baseline recorded
```

---

# 15.3 Folder structure (required)

```text
knowledge/
  interpretation_knowledge/
    PACK_XX_<DOMAIN>/
      README.md
      KNOWLEDGE_INDEX.md
      KNOWLEDGE_ARCHITECTURE.md
      <chapters>.md
  knowledge_catalog/
    PACK_XX_<DOMAIN>/
      README.md
      CATALOG_ARCHITECTURE.md
      CATALOG_SCHEMA.md
      CATALOG_INDEX.md
      catalog/<topics>/
  knowledge_qa/
    PACK_XX_<DOMAIN>/
      PHASE_NN_<TOPIC>_REVIEW.md
      VALIDATION_RECORD.md (at validation)
  reasoning_engine/
    PACK_XX_<DOMAIN>/
      FREEZE/ (when Reasoning scope begins)
```

---

# 15.4 What new packs must reference

| System | Action |
|--------|--------|
| Knowledge Factory | Follow this pipeline |
| Knowledge QA Standard | Do not redefine QA |
| Interpretation Standard | Read; do not edit without governance |
| Rule Database | Read facts; do not edit without governance |
| PACK-01 | Reference implementation only |

---

# 15.5 Pack 02 example (hypothetical Pattern)

| Step | Action |
|------|--------|
| 1 | Charter: Pattern interpretation knowledge |
| 2 | Library: pattern names, meanings, life effects |
| 3 | Catalog: units gated on pattern facts from Rule DB |
| 4 | QA: same twelve criteria |
| 5 | Validation: Pattern golden cases |
| 6 | Cross-pack: declare Strength+Pattern dependencies in limitations |
| 7 | Freeze + Release: independent or bundled platform release |

Cross-pack dependencies registered at QG2 catalog time.

Reference: `knowledge/knowledge_qa/STANDARD/CROSS_PACK_POLICY.md`

---

# 15.6 Pack numbering

| Convention | Example |
|------------|---------|
| Folder | `PACK_02_PATTERN`, `PACK_03_TEN_GODS` |
| Catalog id prefix | `IK-PAT-`, `IK-TG-` |
| QA folder | `knowledge_qa/PACK_02_PATTERN/` |

Governance assigns pack number at QG0.

---

# 15.7 Exit from onboarding

Pack exits onboarding when:

- QG0 complete
- Folder structure created
- Roles assigned
- First Library chapter in Draft

Pack enters **production track** at first QG1 pass.

---

# 15.8 PACK-01 as template

Use PACK-01 Strength as structural reference:

- 13 library chapters
- 13 catalog topic folders
- Phased QA by topic
- Golden CASE-0001 in Reasoning FREEZE

New packs adapt topic list; factory gates unchanged.

Detail: [PIPELINE_EXAMPLES.md](PIPELINE_EXAMPLES.md).

---

END
