# Reasoning Chain

| Field | Value |
|-------|-------|
| Document | REASONING_CHAIN |
| Version | 1.0.0 |

---

# 1. Chain shape

Every Customer Mode recommendation and every major implication should be traceable as:

```text
FACT
  ↓
INTERPRETATION
  ↓
IMPLICATION
  ↓
ACTION
```

---

# 2. Schema

```text
ReasoningChain
├── chain_id
├── fact_ids[]
├── interpretation_unit_ids[]     WHY / MEANING
├── implication_unit_ids[]        ADVANTAGE / CHALLENGE / domain
├── action_unit_ids[]             RECOMMENDATION / WARNING
└── broken                        true if ACTION without IMPLICATION
```

Example (structure only):

```text
FACT:            season support present
INTERPRETATION:  Day Master is fed by climate
IMPLICATION:     internal capacity is more stable
ACTION:          recommendations focus on brake / pacing, not on adding support
```

---

# 3. Rules

1. ACTION without IMPLICATION → drop ACTION from Customer Mode (`REJECTED_NO_CHAIN`).
2. IMPLICATION without FACT → should have failed Evidence Gate.
3. Multiple facts may feed one interpretation (CASE-0001 Why).
4. One implication may feed at most a small set of actions (budget).
5. Chains are Mode A visible. Customer Mode sees only rendered sentences.

---

# 4. CASE-0001 sketch (not production copy)

```text
FACT: season + root_thin + support + special + control
INTERPRETATION: Strong with real feed and a sitting pressure
IMPLICATION: can carry load; endurance may be mistaken for correctness
ACTION: rest on calendar; allow one reviser; do not collect difficulty as identity
```

Luck chain: **broken / not built** — luck MISSING.

---

END
