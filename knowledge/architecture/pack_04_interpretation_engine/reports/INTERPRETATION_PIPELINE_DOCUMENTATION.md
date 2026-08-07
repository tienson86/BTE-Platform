# INTERPRETATION_PIPELINE_DOCUMENTATION.md

Version: 1.0  
Date: 2026-08-07  
Pack: 04  
Status: OFFICIAL (Pack 04 narrative path)

---

## 1. Purpose

Document the implemented Interpretation Engine pipeline for Core Intelligence.

---

## 2. Canonical Pack 04 Flow

```
AnalysisResult          (Score Engine Pack 03 aggregate)
        ↓
Narrative Context       placeholders + facts
        ↓
Evidence                evidence_id list from AnalysisResult.evidence
        ↓
Rule Matching           narrative_rules.json → section winners
        ↓
Sentence Selection      sentences.json by sentence_id
        ↓
Placeholder Binding     {overall_score}, {strength_value}, …
        ↓
Interpretation Builder  section aggregate
        ↓
EngineResult
  └── NarrativeInterpretationResult
```

---

## 3. How to Call

```python
from engines.score_engine import ScoreEngine
from engines.interpretation_engine import InterpretationEngine

analysis = ScoreEngine().analyze(rule_context)
result = InterpretationEngine().interpret_from_analysis(analysis)

assert result.success
narrative = result.value
print(narrative.overview.text)
print(narrative.strength.text)
print(narrative.to_dict())
```

---

## 4. Stage Details

### 4.1 Narrative Context

Builds:

- Placeholder map (scores, grades, names)
- Fact map for rule predicates (`strength.value`, …)
- Analysis id from metadata

### 4.2 Evidence

Reads `AnalysisResult.evidence.items[*].evidence_id` only.  
No analytical recalculation.

### 4.3 Rule Matching

Loads `pack04/library/narrative_rules.json`.

Supported `when.op`:

| op | Meaning |
|----|---------|
| `always` | Always match |
| `eq` | Field equals value |
| `in` | Field in values |
| `gte` | Numeric ≥ |
| `evidence_min` | Evidence count ≥ |

One winning rule per section (highest priority).

### 4.4 Sentence Selection

Resolves `sentence_id` → template text + `template_id` from `sentences.json`.

### 4.5 Placeholder Binding

Replaces `{token}` using NarrativeContext placeholders.  
Records used placeholder values on each sentence.

### 4.6 Interpretation Builder

Assembles sections:

`overview`, `strength`, `pattern`, `useful_god`, `ten_gods`,  
`five_elements`, `season`, `temperature`, `summary`

Attaches metadata (`interpretation_id`, timestamps, duration).

---

## 5. Production Path (Unchanged)

```
RuleContext
  → Rule Loader / Matcher / Scoring / Priority
  → legacy_builder.InterpretationResult
  → SentenceGenerator
  → Portal via to_portal_dict()
```

Do not replace orchestrator wiring in this epic.

---

## 6. Trace Example

```
narrative_context
evidence:N
rule_matching:9
sentence_selection:9
placeholder_binding:9
interpretation_builder
```

Available on `EngineResult.trace`.

---

## 7. Extending Content

1. Add sentence entries to `pack04/library/sentences.json`
2. Add matching rules to `pack04/library/narrative_rules.json`
3. Keep placeholders in sync with `NarrativeContextBuilder` keys

No Score Engine changes required.
