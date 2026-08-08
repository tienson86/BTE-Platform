# 06 — Priority Expansion Plan

Version: 1.0  
Status: **AUDIT COMPLETE — Awaiting review**  
Date: 2026-08-08  
Epic: Knowledge Coverage Audit (EPIC 1)  
Depends on: `01`–`05` reports  

---

## 1. Purpose

Rank future knowledge work by **commercial value** for BaZi consultation.

Priorities:

| Tier | Meaning |
|------|---------|
| **P0** | Blocks consultant-grade product copy; highest ROI |
| **P1** | Materially expands consultation value; next after P0 |
| **P2** | Completeness / academic depth / secondary domains |

**Constraints:** No architecture change. No engine redesign. Content and wiring decisions only (wiring = future implementation epic after approval).

---

## 2. Ranking criteria

| Criterion | Weight |
|-----------|-------:|
| Impact on Pack 05 commercial richness (G6/CQ-1) | 35% |
| Impact on trust (explanations, citations) | 20% |
| Impact on actionable advice (Rec / Warning) | 20% |
| Reuse across charts (structural frequency) | 15% |
| Effort / risk (ethics, medical, orphan cleanup) | 10% |

---

## 3. P0 — Must do first

| ID | Work item | Why commercial | Primary artifacts |
|----|-----------|----------------|-------------------|
| P0-1 | **Commercial evidence / sentence units** for identity, strength, weakness, action, risk, implication (structural domains) | Directly reduces `partial_insufficient`; fills Exec/Rec/Warning | Pack 04 library and/or approved sentence corpus; Analysis-keyed |
| P0-2 | **Useful God practical guidance** (do / avoid / prioritize) | Best action source for Recommendation | `20_knowledge/08_useful_god` seed + evidence actions |
| P0-3 | **Strength + Pattern commercial explanations** (non-technical) | Feeds Observation / Reasoning / Exec | `09_strength`, `07_patterns` + Pack 04 explanations |
| P0-4 | **Risk + mitigation pairs** (clash, kỳ thần, key shensha) | Fixes CQ-5 Warning quality | Warning templates bound to signals |
| P0-5 | **Seed `database/20_knowledge`** for: Five Elements, Ten Gods, Useful God, Strength, Patterns | Creates citeable classical + modern layer | 5 CSV files, curated rows + REF-* |

**P0 success metric:** Material drop in insufficient Narrative on representative charts; Exec Summary meets Content Quality briefing bar more often.

---

## 4. P1 — High commercial value next

| ID | Work item | Why commercial | Primary artifacts |
|----|-----------|----------------|-------------------|
| P1-1 | **Luck cycle guidance language** (đại vận / lưu niên) | Timing is core consultation value | `18_luck_cycles` + action evidence |
| P1-2 | **Ten Gods relationship narratives** | Personality / dynamics without new architecture | `03_ten_gods` + ten gods evidence |
| P1-3 | **Orphan rule triage** for Career / Wealth / Marriage | Unlocks ~1,200+ existing rows OR retires debt | Decision: wire / migrate / archive `08–10` + interp rules |
| P1-4 | **Career + Wealth explainable seeds** (after triage) | Life-domain product differentiation | `12_career`, `13_wealth` + ethics pass |
| P1-5 | **Temperature / Season balance guidance** | Complements Useful God advice | `10_temperature` + practical tips |
| P1-6 | **Knowledge Canon expansion** (stems, branches, ten gods) + **REF remapping** | Governance / citation correctness | Canon JSON + Wood fix |
| P1-7 | **Shensha caution catalog** (top commercial stars only) | Warning enrichment | `11_shensha` curated subset |

**P1 success metric:** Career/wealth/luck appear as trustworthy consultation themes (even if still under structural Narrative sections).

---

## 5. P2 — Completeness and depth

| ID | Work item | Why later |
|----|-----------|-----------|
| P2-1 | Marriage / Children knowledge (ethics-first) | Sensitive; needs policy + careful language |
| P2-2 | Health lifestyle hints (non-medical) | Liability / safety review |
| P2-3 | Parents domain (greenfield) | Lower frequency than career/wealth |
| P2-4 | Education domain (greenfield) | New module end-to-end |
| P2-5 | Personality pack (explicit) | Partially covered via ten gods / day master |
| P2-6 | Transformations doctrine + framework rules | Niche / special charts |
| P2-7 | Na Yin / Growth stage deep narratives | Lower commercial priority |
| P2-8 | Feng Shui product scope decision + content | May stay out of core Narrative |
| P2-9 | Classic chapter support + more REF seeds | Academic depth |
| P2-10 | Sentence Library framework ↔ Pack 04 consolidation | Hygiene after volume exists |
| P2-11 | Full BaZi academic JSON promotion (modules 02–14) | Long-running scholarly program |

---

## 6. Explicit deprioritization

| Item | Reason |
|------|--------|
| Redesigning Pack 05 section grammar | Architecture frozen; structure already good |
| Expanding Score Engine rules for prose quality | Wrong layer — use evidence/knowledge |
| Filling framework `knowledge/rule_database/01_strength/` etc. before P0 evidence | Low Narrative ROI vs Pack 04 / `20_knowledge` |
| Mass-authoring all 20 `20_knowledge` files equally | Seed high-frequency first (P0-5) |
| UI Polish / Report Engine | Separate epics; blocked on knowledge/content review |

---

## 7. Dependency graph (expansion)

```
P0-1 commercial evidence units
   ├── enables better Exec / Rec / Warning / Conclusion
   └── consumes signals from existing Analysis (no engine redesign)

P0-5 20_knowledge seeds
   └── feeds Reasoning citations (future retriever) + authoring SSOT

P1-3 orphan triage
   └── gate for P1-4 career/wealth and later marriage/children

P1-6 Canon + REF remap
   └── required before Official scholarly promotion
```

---

## 8. Effort bands (indicative)

| Tier | Indicative effort | Notes |
|------|-------------------|-------|
| P0 | Large content authoring + light wiring epic later | Highest value |
| P1 | Medium–Large | Includes governance decisions on orphans |
| P2 | Large scholarly / policy | Parallel tracks after P0/P1 stable |

Exact sprint sizing deferred until review approval.

---

## 9. Commercial readiness trajectory

| Milestone | Expected composite readiness |
|-----------|------------------------------|
| Today (post-audit) | ~35% |
| After P0 | ~55–60% |
| After P0+P1 | ~70–75% |
| After selective P2 | ~85%+ (full consultation catalog) |

These are planning estimates, not SLAs.

---

## 10. Stop line

Priority plan complete. **Do not begin P0 authoring until audit package is approved.**

---

END
