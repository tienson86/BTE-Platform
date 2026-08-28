# 05 — Evidence Classification

| Field | Value |
|-------|--------|
| Document | INT-02B.1 Evidence Classification |
| Version | 1.0.0 |
| Status | Canonical |

---

## Purpose

Evidence Classification sits between published engine evidence and narrative blocks.

```
Engine Result
        ↓
Topic Evidence (copy only)
        ↓
Evidence Classification
        ↓
Observation → Reasoning → Impact → Recommendation → Summary
```

It does not score. It does not judge fortune. It labels how a published fact contributes to the **analytical target**.

---

## Semantic meaning

Classification is **target-relative**.

For Strength, the target is Day Master strength.

| Value | Meaning for Strength |
|-------|----------------------|
| `positive` | Supports / increases Day Master strength |
| `negative` | Restrains / weakens Day Master strength |
| `neutral` | No clear directional contribution, or unpublished |

`positive` is not auspicious. `negative` is not inauspicious.

Do not emit `good_score`, `bad_score`, `auspicious_score`, or `risk_score`.

---

## Canonical item

`NarrativeEvidenceItem`: id, topic, component, value, display_value, classification, reason, source_path, confidence, metadata.

Reasons and polarity must come from published evidence (signed component scores, compact phrases, explicit effect fields). Missing evidence is `neutral` with reason `Chưa có dữ liệu`.

---

## Traceability

Each item keeps a canonical `source_path` such as `strength.season_score`.

Narrative remains auditable back to the engine payload.

---

## Reuse

The item contract is topic-agnostic.

Future topics (Useful God, Pattern, Five Elements, Ten Gods, Luck) may reuse it with their own target semantics.

INT-02B.1 implements Strength only.

---

END
