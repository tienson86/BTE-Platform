# Future Pack Template — FROZEN V1.0

| Field | Value |
|-------|-------|
| Document | PACK_TEMPLATE |
| Status | FROZEN |

---

# 1. Reuse, do not fork

Pack 02 (Pattern), Pack 03 (Useful God), Ten Gods, ShenSha, Luck, Career, Marriage, Health:

Copy this architecture. Change only **subject-specific** catalogs.

---

# 2. Must reuse unchanged

- Dual Mode A / B
- Evidence states including `INACTIVE` vs `MISSING`
- Relevance `REL_0`–`REL_4`
- Salience `SAL_0`–`SAL_5`
- Declared duplicate clusters (new cluster ids, same mechanism)
- Conflict categories FACT / KNOWLEDGE / DOMAIN / ADVICE / CONFIDENCE
- Reason code style (add pack-prefixed codes via version bump)
- ClaimTrace chain
- Deterministic sort keys
- Four version fields
- NarrativePlan as reasoning output
- No LLM in reasoning
- Class/label lock from the **owning engine** (Pattern engine, etc.)

---

# 3. Must replace per pack

| Item | Example |
|------|---------|
| `pack` / `knowledge_id` prefix | `IK-PAT-…` |
| Fact keys | pattern name, follow flag, … |
| Purpose extras | only if freeze minor allows |
| Domain extras | only if needed |
| Default section order | Pattern-specific Why causes |
| Golden case | that pack’s CASE, not CASE-0001 Strength |

---

# 4. Must not

- Recompute another pack’s engine
- Steal Useful God into Strength (already forbidden)
- Skip Evidence Gate
- Skip Narrative Budget
- Treat “more units” as quality

---

# 5. Delivery shape for Pack N

```text
knowledge/interpretation_standard/PACK_0N_*/
knowledge/interpretation_knowledge/PACK_0N_*/
knowledge/reasoning_engine/PACK_0N_*/FREEZE/
```

Same freeze file names.

---

END
