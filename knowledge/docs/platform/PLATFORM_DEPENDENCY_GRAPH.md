# Platform Dependency Graph

| Field | Value |
|-------|-------|
| **Document** | PLATFORM_DEPENDENCY_GRAPH |
| **Platform version** | 1.0.0 |
| **Status** | Canonical |
| **Owner** | BTE Architecture Board |

---

## Engine dependency direction

```
Knowledge Packages / Rule Database
        ↑ read only
Rule Engine
        ↑
Calendar Engine → Bazi Engine → Score / Pattern
        ↓
Analysis Engine
        ↓
Decision Engine
        ↓
Luck Engine
        ↓
Interpretation Engine
        ↓
Report Engine
        ↓
API / Portal
```

Arrows mean “may depend on / consume results of”. Reverse arrows are forbidden.

---

## Canonical execution order

```
User Request
  → Calendar
  → Four Pillars (Bazi)
  → Seasonal → Strength → Temperature → Pattern → Pattern Evaluation → Useful God (analysis signal)
  → Useful God Foundation → Priority → Override (decision)
  → Luck Timeline → Luck Analysis → Luck Decision
  → Interpretation Foundation → Knowledge Selection → Composition
  → Report Foundation → Layout → Rendering
  → Canonical Report Artifact
```

Analysis Knowledge order inside AX-2:

```
calendar → four_pillars → seasonal → strength → temperature
  → pattern → pattern_evaluation → useful_god
```

Reserved inside AX-2 (inactive): `luck_cycle`, `interpretation`, `report`.

---

## Pipeline-to-pipeline contracts

| From | To | Payload |
|------|----|---------|
| Analysis 2.0.0 | Decision 1.0.0 | Published analytical scores / pattern quality |
| Analysis + Decision | Luck 1.0.0 | Canonical snapshots; natal chart facts |
| Analysis + Decision + Luck | Interpretation 1.0.0 | Immutable dict snapshots |
| Interpretation | Report 1.0.0 | Interpretation result + upstream snapshots |
| Report | API | `CanonicalReportResult` / artifact mime envelope |

---

## Package graph (released)

```
bz_02 seasonal
   ↓
bz_01 strength
   ↓
bz_03 temperature
   ↓
bz_04 pattern core
   ↓
bz_05 pattern evaluation
   ↓
bz_06 useful god foundation
   ↓
bz_07 useful god priority
   ↓
bz_08 useful god override

bz_09 luck foundation  →  Luck Timeline stage
   (consumes chart / analysis / decision snapshots; does not redefine Useful God)
```

---

## Intra-engine component graphs

| Engine | Internal order |
|--------|----------------|
| Luck | timeline → analysis → decision |
| Interpretation | foundation → knowledge_selection → composition |
| Report | foundation → layout → rendering |

Future stages stay registered and disabled: Interpretation `report` / `ai_rewrite`; Report `publisher` / `delivery` / `print`.

---

## Isolation rules

1. One engine, one responsibility.
2. Public API only between engines.
3. No circular imports.
4. Optional package peers do not create load-time hard edges unless declared required.
