# Analysis Dependency Map

| Field | Value |
|-------|-------|
| **Document** | ANALYSIS_DEPENDENCY_MAP |
| **Version** | 1.0.0 |
| **Sprint** | KX-2B |
| **Status** | Canonical reference for Analysis Engine |
| **Scope** | Knowledge / analytical dependency order — no engine code |

This is the canonical dependency reference for how analytical knowledge packages relate. Engines consume **released package outputs** in this order. They must not import reverse.

---

## 1. Canonical pipeline

```
Calendar
  ↓
Four Pillars (BaZi chart)
  ↓
Seasonal
  ↓
Strength
  ↓
Temperature
  ↓
Pattern
  ↓
Useful God
  ↓
Luck Cycle
  ↓
Interpretation
  ↓
Report
```

Calendar and Four Pillars are **engine / chart construction** stages. From Seasonal onward, each stage is (or will be) a Knowledge Package plus an engine that reads it.

---

## 2. Package map

| Stage | Package (when present) | Domain |
|-------|------------------------|--------|
| Calendar | (engine + calendar knowledge; no KX core package yet) | DOM-CALENDAR |
| Four Pillars | (Bazi engine / chart objects) | DOM-BAZI |
| Seasonal | `bz_02_seasonal_core` | DOM-SEASONAL |
| Strength | `bz_01_strength_core` | DOM-STRENGTH |
| Temperature | `bz_03_temperature_core` | DOM-TEMPERATURE |
| Pattern | future `bz_04_pattern_core` | DOM-PATTERN |
| Useful God | future useful-god package | DOM-USEFUL_GOD |
| Luck Cycle | future luck-cycle package | DOM-LUCK_CYCLE |
| Interpretation | future interpretation package | DOM-INTERPRETATION |
| Report | future report package | DOM-REPORT |

V1 Rule Database modules remain dual-read: `02_season_rules`, `01_strength_rules`, `03_temperature_rules`, etc.

---

## 3. Stage contracts

### 3.1 Calendar

| | |
|--|--|
| **Direct dependencies** | Civil datetime, timezone, solar-term tables |
| **Produces** | Normalized datetime, solar term, lunar month index |
| **Consumes** | None (pipeline root) |
| **Downstream** | Four Pillars |

### 3.2 Four Pillars

| | |
|--|--|
| **Direct dependencies** | Calendar outputs |
| **Produces** | Four pillars, day master, hidden stems, ten gods (chart facts) |
| **Consumes** | Calendar datetime / solar term |
| **Downstream** | Seasonal, Strength, Temperature, Pattern, Useful God, Luck Cycle |

### 3.3 Seasonal — `bz_02_seasonal_core`

| | |
|--|--|
| **Direct dependencies** | Four Pillars (`month_branch`, lunar month); conceptual Calendar solar terms |
| **Produces** | `season`, `season_phase`, `seasonal_qi_phase` (Vượng/Tướng/Hưu/Tù/Tử), `season_score`, seasonal influence band (strong/balanced/weak **seasonal qi**, not DM strength) |
| **Consumes** | Month branch / lunar month / solar term ids |
| **Downstream** | Strength (month-command facts), Temperature (seasonal climate adjustment), Pattern, Useful God, Luck Cycle |
| **Must not** | Write `strength_score` or select Useful God |

### 3.4 Strength — `bz_01_strength_core`

| | |
|--|--|
| **Direct dependencies** | Four Pillars; Seasonal month-command / 旺相休囚死 **as chart facts** (V1 CSV or SEC signals) |
| **Produces** | `strength_score`, `strength_level` (strong / weak / balanced Day Master), root/support/control contributions |
| **Consumes** | Pillars, ten gods, `month_status` / seasonal command intensity |
| **Downstream** | Temperature (intensity context), Pattern, Useful God, Luck Cycle, Interpretation |
| **Must not** | Redefine month→season mapping; write `temperature_score` |

### 3.5 Temperature — `bz_03_temperature_core`

| | |
|--|--|
| **Direct dependencies** | Four Pillars; **Seasonal** (`season`, `season_phase`); **Strength** (`strength_level` as context) |
| **Produces** | `temperature_score`, `temperature_level` (`cold` \| `cool` \| `warm` \| `hot`), dryness/humidity flags, tiao hou correction vectors |
| **Consumes** | Season + phase; element counts; DM element; optional strength band |
| **Downstream** | Pattern, Useful God, Interpretation |
| **Must not** | Duplicate SEC season classification or SKC strength weights |

### 3.6 Pattern (future)

| | |
|--|--|
| **Direct dependencies** | Four Pillars, Seasonal, Strength, Temperature |
| **Produces** | Pattern eligibility / names / quality |
| **Consumes** | Structure facts, strength, temperature type |
| **Downstream** | Useful God, Interpretation |

### 3.7 Useful God (future)

| | |
|--|--|
| **Direct dependencies** | Strength, Temperature, Pattern, Seasonal |
| **Produces** | Yong Shen / Xi Shen / Ji Shen classification |
| **Consumes** | `strength_level`, `temperature_type`, pattern, seasonal command |
| **Downstream** | Luck Cycle evaluation, Interpretation |

### 3.8 Luck Cycle (future)

| | |
|--|--|
| **Direct dependencies** | Four Pillars, Seasonal, Strength, Temperature, Useful God |
| **Produces** | Da Yun / Liu Nian evaluation vs useful gods and climate |
| **Consumes** | Chart + prior analytical outputs |
| **Downstream** | Interpretation |

### 3.9 Interpretation

| | |
|--|--|
| **Direct dependencies** | All prior analytical packages (read-only results) |
| **Produces** | Narrative sections / sentence bindings |
| **Consumes** | Result objects, not raw engine internals |
| **Downstream** | Report |

### 3.10 Report

| | |
|--|--|
| **Direct dependencies** | Interpretation (+ layout knowledge) |
| **Produces** | Report blocks / section order |
| **Consumes** | Interpretation units |
| **Downstream** | Portal / API presentation |

---

## 4. Knowledge package load vs pipeline order

Package **load** dependencies may be optional so each package stays independently deployable.

**Analytical execution order** is still mandatory:

Seasonal → Strength → Temperature → Pattern → Useful God → Luck Cycle

Temperature Core lists Seasonal and Strength as **optional** package dependencies with declared `signals`. Engines that run the full pipeline MUST supply those signals (from packages or V1 dual-read) before Temperature rules.

Circular **required** package dependencies are prohibited.

---

## 5. Signal names (stable)

| Signal | Owner | Consumers |
|--------|-------|-----------|
| `month_branch`, pillars, day master | Four Pillars | All later stages |
| `season`, `season_phase`, `season_score` | Seasonal | Strength, Temperature, Pattern, UG, Luck |
| `strength_score`, `strength_level` | Strength | Temperature, Pattern, UG, Luck, Interpretation |
| `temperature_score`, `temperature_level` | Temperature | Pattern, UG, Interpretation |
| pattern ids / quality | Pattern | UG, Interpretation |
| useful/favorable/unfavorable gods | Useful God | Luck, Interpretation |
| luck evaluations | Luck Cycle | Interpretation |
| sections / sentences | Interpretation | Report |

---

## 6. Compatibility

- V1 modules remain valid dual-read sources for the same signals.
- This map does not authorize engine refactors in KX-2B.
- Future packages MUST declare `domain_id` and optional upstream `signals` consistently with this document.
