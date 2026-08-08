# 09 — Golden Unit Reference

Version: 1.0  
Status: **WAVE 1.1 EVALUATION — units not modified**  
Date: 2026-08-08  
Units reviewed: KU-ID-001 · KU-ST-001 · KU-WK-001 · KU-UG-001 · KU-RC-001  
Source: `database/20_knowledge/21_knowledge_units.csv` (read-only)  
Status field observed: `awaiting_review`  

---

## 1. Purpose

Evaluate the five Wave 1.1 Knowledge Units against the Golden Knowledge Standard (`06`) and Quality Score (`08`).

**Do not rewrite units in this sprint.**

---

## 2. Pack-level overview

| Attribute | Observation |
|-----------|-------------|
| Count | Exactly 5 |
| Kinds | 4× Analytical + 1× Action |
| Commercial intent | Exec briefing slots + Recommendation core |
| Voice | Consultant VI; non-technical |
| Binding | Placeholders `{day_master_label}`, `{pattern_label}`, `{strength_band_label}`, `{weakness_signal_label}`, `{useful_god_label}` |
| Ethics | `no_guaranteed_returns` on KU-RC-001 |
| Pairing | UG↔RC; WK→RC |
| Runtime | Not wired (expected for this wave) |

---

## 3. Unit evaluations

### 3.1 KU-ID-001 — Identity Core

| Lens | Assessment |
|------|------------|
| **Strengths** | Clear identity framing; Exec/Observation/Conclusion targets; high priority; natural VI; reusable for default Result |
| **Weaknesses** | `required_evidence=grade` is optional for identity (slight over-constraint); condition uses logical flags not yet a frozen Analysis contract |
| **Improvement opportunities** | Soften required_evidence; publish Analysis signal contract doc in wiring epic |
| **Reuse potential** | **Very high** — every default consultation |
| **Risk assessment** | Low content risk; medium wiring-contract risk |
| **Scorecard (0–100)** | Acc 9 · Evq 7 · CV 9 · Act 7 · Nar 9 · Read 9 · Cons 8 · Reuse 10 · Trace 8 · Maint 8 → **84 Strong** |
| **Golden Reference?** | **Yes — Provisional Golden** (Exec identity exemplar) |

### 3.2 KU-ST-001 — Strength Core

| Lens | Assessment |
|------|------------|
| **Strengths** | Conditional on favorable strength; anti-overclaim (“không bảo chứng”); fills strengths slot; good CQ discipline |
| **Weaknesses** | Band enums (`vuong;can;strong_support`) need canonical mapping to engine labels |
| **Improvement opportunities** | Align band vocabulary to Analysis enums in wiring contract |
| **Reuse potential** | **High** when strength favorable |
| **Risk assessment** | Low if drop-on-conflict enforced |
| **Scorecard** | 9 · 8 · 9 · 7 · 9 · 9 · 8 · 9 · 8 · 8 → **84 Strong** |
| **Golden Reference?** | **Yes — Provisional Golden** (strengths language exemplar) |

### 3.3 KU-WK-001 — Weakness Core

| Lens | Assessment |
|------|------------|
| **Strengths** | Calm non-shaming tone; Warning + Exec targets; pairs commercially with recommendation; excellent professional ethics of language |
| **Weaknesses** | `risk_category` populated though kind is Analytical (acceptable but slightly mixed taxonomy); clash condition flag name aspirational |
| **Improvement opportunities** | Later wave: dedicated RK+MT pairs for clash; keep this as weakness framing |
| **Reuse potential** | **High** |
| **Risk assessment** | Low tone risk; medium signal-name risk |
| **Scorecard** | 9 · 7 · 9 · 8 · 9 · 9 · 8 · 9 · 8 · 8 → **84 Strong** |
| **Golden Reference?** | **Yes — Provisional Golden** (weakness/caution exemplar) |

### 3.4 KU-UG-001 — Useful God Core

| Lens | Assessment |
|------|------------|
| **Strengths** | Converts useful god into life-priority question; blocks technical residue; strong Reasoning/Rec support; paired to RC |
| **Weaknesses** | Kind Analytical with `action_category` set (minor taxonomy blur); classical text is paraphrase (honest, but not quotable scholarship yet) |
| **Improvement opportunities** | Knowledge Review to upgrade classical_support quality later without changing modern body |
| **Reuse potential** | **Very high** across CA/MD/LT/default |
| **Risk assessment** | Low if useful_god absent → unit drops |
| **Scorecard** | 9 · 8 · 10 · 8 · 9 · 9 · 9 · 10 · 9 · 8 → **89 Strong** (near Golden) |
| **Golden Reference?** | **Yes — Provisional Golden** (explanation→action bridge exemplar) |

### 3.5 KU-RC-001 — Core Recommendation

| Lens | Assessment |
|------|------------|
| **Strengths** | Explicit Action/Reason/Next-step shape; prepare posture (safe); useful-god bound; ethics flag; Exec+Recommendation targets |
| **Weaknesses** | Still somewhat template-generic until placeholders bind; Advance not supported (by design — OK for Wave 1.1) |
| **Improvement opportunities** | Later Opportunity units to unlock Advance; scenario-specific Action variants in P1 |
| **Reuse potential** | **Very high** for default Rec |
| **Risk assessment** | Low overclaim risk; medium “generic feel” until wired |
| **Scorecard** | 9 · 8 · 10 · 9 · 10 · 9 · 9 · 9 · 9 · 8 → **90 Golden** |
| **Golden Reference?** | **Yes — Golden Reference** (Recommendation exemplar) |

---

## 4. Pack score summary

| Unit | Total | Band | Golden Reference |
|------|------:|------|------------------|
| KU-ID-001 | 84 | Strong | Provisional Golden |
| KU-ST-001 | 84 | Strong | Provisional Golden |
| KU-WK-001 | 84 | Strong | Provisional Golden |
| KU-UG-001 | 89 | Strong | Provisional Golden |
| KU-RC-001 | 90 | Golden | **Golden Reference** |
| **Pack average** | **86.2** | Strong | Pack qualifies as Wave 1.1 reference set |

---

## 5. Shared strengths (pack)

1. Customer-first consultation framing (not academic folders)  
2. Clear evidence_kind → Narrative slot mapping  
3. Commercial VI without rule jargon  
4. Placeholder honesty + drop-on-conflict notes  
5. Minimal, atomic set covering Exec + Recommendation spine  
6. Ethics awareness on recommendation  

---

## 6. Shared weaknesses / risks (pack)

| Issue | Blocking for content Approve? | Blocking for Publish? |
|-------|-------------------------------|------------------------|
| Analysis signal names not frozen contract | No | **Yes** until wiring contract exists *or* Product accepts HOLD |
| Id scheme ≠ catalog `KU-AN-ID-000001` pattern | No (alias policy) | No if Product accepts aliases |
| Classical paraphrases not verbatim | No | No |
| No RK/MT Warning pairs yet | No (out of Wave 1.1 scope) | No for this wave’s goal |
| Runtime not wired | N/A to unit text | Live quality gain blocked until wiring epic |

---

## 7. Reuse potential (pack)

| Consumer | Ready as content SSOT? |
|----------|------------------------|
| Narrative Exec / Rec | Yes (content) |
| Portal via NarrativeResult | After wiring |
| Report | After NarrativeResult consumption |
| AI Assistant / Search | Yes as retrieval corpus once Published |

---

## 8. Golden Reference determination

| Verdict | Detail |
|---------|--------|
| **Pack** | **Qualifies as Wave 1.1 Golden Reference Set (Provisional)** |
| **Individual Golden (≥90)** | KU-RC-001 |
| **Provisional Golden (Strong 80–89 + exemplar role)** | KU-ID-001, KU-ST-001, KU-WK-001, KU-UG-001 |
| **Rewrite required?** | **No** for Golden Review purposes |

Promotion from Provisional → full Golden may occur after live wiring + Product confirmation.

---

## 9. Stop line

Evaluation complete. Units **not** modified.

---

END
