# PACK_02_STRUCTURE.md

> **Pack:** 02 — Analytical Knowledge
>
> **Document Version:** 0.0.0
>
> **Status:** Initialized (Structure Only)
>
> **Depends On:** Pack 01 Architecture principles

---

## 1. Directory Layout

```text
knowledge/pack_02_analytical_knowledge/
├── README.md
├── PACK_02_ARCHITECTURE.md
├── PACK_02_STRUCTURE.md
├── PACK_02_MODULE_INDEX.md
├── PACK_02_REGISTRY_INDEX.md
├── PACK_02_VALIDATION.md
├── PACK_02_COMPILER_SPEC.md
├── PACK_02_RELEASE_NOTES.md
├── PACK_02_CHANGELOG.md
├── PACK_02_FREEZE_DECLARATION.md
├── 01_strength_analysis/
├── 02_pattern_analysis/
├── 03_temperature_analysis/
├── 04_useful_god_analysis/
├── 05_ten_gods_analysis/
├── 06_combination_analysis/
├── 07_shensha_analysis/
├── 08_dayun_analysis/
├── 09_liunian_analysis/
├── 10_liuyue_analysis/
├── 11_scoring/
├── 12_conflict_resolution/
└── 13_analysis_pipeline/
```

Each module:

```text
module/
├── README.md
├── VERSION
├── CHANGELOG.md
├── SPEC.md
├── examples/
├── schemas/
└── validation/
```

---

## 2. Module Responsibilities (Skeleton)

| Module | Owns | Does Not Own |
|--------|------|--------------|
| `01_strength_analysis` | Strength analysis knowledge contracts | Fundamental theory (Pack 01), scoring runtime |
| `02_pattern_analysis` | Pattern analysis knowledge contracts | Pattern engine implementation |
| `03_temperature_analysis` | Temperature analysis knowledge contracts | Climate fundamental definitions (Pack 01) |
| `04_useful_god_analysis` | Useful God analysis knowledge contracts | Useful God engine runtime |
| `05_ten_gods_analysis` | Ten Gods analysis knowledge contracts | Ten Gods fundamental definitions (Pack 01) |
| `06_combination_analysis` | Combination analysis knowledge contracts | Combination fundamental system (Pack 01) |
| `07_shensha_analysis` | Shen Sha analysis knowledge contracts | Shen Sha fundamental system (Pack 01) |
| `08_dayun_analysis` | Dayun analysis knowledge contracts | Calendar computation |
| `09_liunian_analysis` | Liunian analysis knowledge contracts | Calendar computation |
| `10_liuyue_analysis` | Liuyue analysis knowledge contracts | Calendar computation |
| `11_scoring` | Scoring knowledge contracts / weight references | Score calculation engines |
| `12_conflict_resolution` | Conflict resolution knowledge contracts | Priority engine runtime |
| `13_analysis_pipeline` | Pipeline stage contracts / sequencing knowledge | Orchestrator service code |

---

## 3. Dependencies

### 3.1 Pack Dependency

```text
Pack 02 Analytical Knowledge
        │
        ▼
Pack 01 Fundamental Theory / Knowledge Infrastructure
```

Forbidden:

```text
Pack 01 → Pack 02
```

### 3.2 Internal Module Order (Logical)

```text
01_strength_analysis
02_pattern_analysis
03_temperature_analysis
04_useful_god_analysis
05_ten_gods_analysis
06_combination_analysis
07_shensha_analysis
08_dayun_analysis
09_liunian_analysis
10_liuyue_analysis
11_scoring
12_conflict_resolution
13_analysis_pipeline
```

Rules:

- Lower-number modules MUST NOT depend on higher-number modules unless explicitly approved later.
- `13_analysis_pipeline` may reference prior modules as pipeline stages.
- `12_conflict_resolution` may reference analysis outputs from modules 01–11.
- No circular dependencies.

### 3.3 Platform Compatibility

Pack 02 modules MUST be consumable through:

- Registry
- Validation
- Compiler

without duplicating Pack 01 Dictionary / Schema / Registry infrastructure.

---

## 4. Separation From Pack 01

Pack 02 MUST NOT contain:

- Yin/Yang, Wu Xing, Stem/Branch fundamental definitions
- Pack 01 Knowledge Records (KR-000001–KR-000015)
- Infrastructure module trees owned by Pack 01 governance

Pack 02 MAY reference Pack 01 identifiers only.

---

## 5. Initialization Status

Structure created. Specifications are empty skeletons. No analysis rules authored.
