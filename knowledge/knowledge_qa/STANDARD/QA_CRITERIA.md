# QA Criteria — V1.0

| Field | Value |
|-------|-------|
| Document | QA_CRITERIA |
| Standard | Knowledge QA V1.0 |
| Criteria count | 12 (frozen) |

---

# Rule

Every Knowledge Unit review scores **all twelve criteria** (0–10) unless N/A is documented.

Future packs add **constraints**. They do not add criteria.

Scoring anchors: [QA_SCORING.md](QA_SCORING.md).

---

# 1. Professional Correctness

| Field | Content |
|-------|---------|
| **Purpose** | Ensure the claim is professionally sound and faithful to authored knowledge |
| **Definition** | The claim matches its Interpretation Knowledge source, respects class/topic ownership, and violates no banned doctrine |
| **Evaluation rules** | Compare claim to `source_document`; check class gate; check banned lists (scores, rule ids, moral ranking, medical destiny, guaranteed outcomes) |
| **Scoring guidance** | 10 = exact professional intent; 7 = minor wording drift; 5 = partial misquote; 3 = wrong class or banned doctrine; 0 = harmful or fabricated |
| **Typical failures** | Invented interpretation; upgrades Weak to Strong; dictionary definition; “Weak people fail” |

---

# 2. Evidence Compatibility

| Field | Content |
|-------|---------|
| **Purpose** | Ensure the unit can fire only when runtime facts support it |
| **Definition** | `required_facts`, `forbidden_conditions`, and `required_evidence` match what the claim actually needs |
| **Evaluation rules** | List every fact the claim implies; verify each is in schema or limitations; verify INACTIVE ≠ MISSING handling |
| **Scoring guidance** | 10 = full alignment; 7 = limitation covers gap schema misses; 5 = CLASS_ONLY but claim needs causes; 3 = requires unpublished luck/pattern; 0 = narrates missing data |
| **Typical failures** | CLASS_ONLY cluster claiming drain when drain INACTIVE; luck unit without `luck_interaction`; polarity not gated (season agree vs disagree) |

---

# 3. Domain Purity

| Field | Content |
|-------|---------|
| **Purpose** | Ensure the unit is the topic it declares |
| **Definition** | MEANING = identity; CAUSE = why; ADVANTAGE = usable capacity; CHALLENGE = cost; REC = steering; etc. |
| **Evaluation rules** | Ask: if this paragraph moved to another topic file unchanged, would it still belong? |
| **Scoring guidance** | 10 = pure topic; 7 = minor bleed with limitation; 5 = half MEANING half ADVANTAGE; 3 = wrong topic; 0 = algorithm or score explanation |
| **Typical failures** | MEANING restated as ADVANTAGE; career titles in ADVANTAGE; recommendation in MEANING; cause in MEANING |

---

# 4. Duplicate Risk

| Field | Content |
|-------|---------|
| **Purpose** | Prevent the same customer insight from printing twice |
| **Definition** | Risk that another unit (same or other topic/pack) delivers the same So what under the same conditions |
| **Evaluation rules** | Check `duplicate_cluster`; cross-check MEANING/ADV/CHAL/CAR; note undeclared overlap |
| **Scoring guidance** | 10 = NONE and no overlap; 7 = declared cluster member; 5 = undeclared near duplicate; 3 = semantic duplicate undeclared; 0 = representative conflict |
| **Typical failures** | MEAN-0006 + ADV-0014 full tank; ADV-0013 + ADV-0006 carry load; CAUS cluster + atomic causes double-print |

---

# 5. Customer Value

| Field | Content |
|-------|---------|
| **Purpose** | Ensure pay-worthy insight, not filler |
| **Definition** | If the customer heard only this sentence, they would learn something that changes understanding or decision |
| **Evaluation rules** | Apply removal test in isolation; compare to metadata `customer_value` |
| **Scoring guidance** | 10 = decisive insight; 7 = useful support; 5 = generic but true; 3 = filler; 0 = no value or harm |
| **Typical failures** | Generic praise; restated class name; optional facet printed as headline |

---

# 6. Actionability

| Field | Content |
|-------|---------|
| **Purpose** | Ensure the customer or consultant can act on the claim |
| **Definition** | Claim implies what to do, protect, choose, or avoid — not description alone |
| **Evaluation rules** | MEANING may be descriptive (≥6 acceptable); ADVANTAGE/RECOMMENDATION need steer (≥7); REC need ≥7 or FAIL |
| **Scoring guidance** | 10 = clear action path; 7 = implicit steer; 5 = descriptive only; 3 = abstract; 0 = misleading action |
| **Typical failures** | ADVANTAGE with no use context; REC without chain from challenge |

---

# 7. Readability

| Field | Content |
|-------|---------|
| **Purpose** | Ensure Composer-ready natural language |
| **Definition** | One claim, clear sentences, supporting points belong to same claim |
| **Evaluation rules** | Count independent claims; check supporting_points polarity; check sentence length |
| **Scoring guidance** | 10 = atomic clear claim; 7 = dense but one claim; 5 = two claims in one unit; 3 = confusing; 0 = unreadable |
| **Typical failures** | Supporting point states the blind spot; semicolon list dump; meta-instruction (“Sell capacity…”) |

---

# 8. Explainability

| Field | Content |
|-------|---------|
| **Purpose** | Ensure the unit earns its place in the narrative |
| **Definition** | Passes removal test: without this unit, customer loses important insight **in this narrative context** |
| **Evaluation rules** | Simulate narrative with/without unit; check OPTIONAL/DETAIL metadata |
| **Scoring guidance** | 10 = essential; 7 = valuable support; 5 = LOW EXPLAINABILITY optional; 3 = redundant; 0 = pure duplicate |
| **Typical failures** | Optional adaptability when headline facets kept; taxonomy intro + atomic units |

Detail: [EXPLAINABILITY_STANDARD.md](EXPLAINABILITY_STANDARD.md).

---

# 9. Commercial Quality

| Field | Content |
|-------|---------|
| **Purpose** | Ensure consultant-grade, paid-session language |
| **Definition** | A professional consultant would say this to a paying client; not textbook, not engine dump |
| **Evaluation rules** | Read aloud; check for So what; check banned consumer-widget tone |
| **Scoring guidance** | 10 = consultant-native; 7 = usable with light edit; 5 = textbook; 3 = engine leak; 0 = unacceptable |
| **Typical failures** | Rule IDs; score numbers; “Strong means Day Master is strong”; marketing hype |

Detail: [COMMERCIAL_QUALITY_STANDARD.md](COMMERCIAL_QUALITY_STANDARD.md).

---

# 10. Cross-Pack Dependency

| Field | Content |
|-------|---------|
| **Purpose** | Ensure Strength-only units do not require other packs |
| **Definition** | Unit is selectable with owning pack published facts only; no hidden Pattern/UG/Ten Gods/Luck/Marriage need |
| **Evaluation rules** | List every noun/implication requiring another pack; soft Career examples = flag, not auto-FAIL |
| **Scoring guidance** | 10 = fully isolated; 8 = soft example bleed; 5 = implied other pack; 3 = requires unpublished pack; 0 = hard dependency |
| **Typical failures** | “Useful God says use Water”; Pattern name as cause; luck decade guarantee |

Detail: [CROSS_PACK_POLICY.md](CROSS_PACK_POLICY.md).

---

# 11. Consistency

| Field | Content |
|-------|---------|
| **Purpose** | Align unit with Reasoning, Narrative, and Customer Mode policy |
| **Definition** | Metadata matches claim; limitations match Reasoning gates; mode flags match use |
| **Evaluation rules** | Cross-check `customer_mode`, `priority`, `narrative_weight`, golden plan if exists |
| **Scoring guidance** | 10 = full alignment; 7 = minor metadata drift; 5 = limitation contradicts schema; 3 = golden conflict; 0 = unsafe Customer leak |
| **Typical failures** | customer_mode ALLOWED but limitation forbids Customer; governance unit in Customer headline |

Detail: [CONSISTENCY_STANDARD.md](CONSISTENCY_STANDARD.md).

---

# 12. Traceability

| Field | Content |
|-------|---------|
| **Purpose** | Enable audit from customer claim back to source and facts |
| **Definition** | Complete chain: knowledge_id → claim → source_document → (Reasoning) facts |
| **Evaluation rules** | Verify `source_document` exact filename; claim traceable to paragraph; no orphan units |
| **Scoring guidance** | 10 = full chain; 7 = source ok, fact chain in limitations only; 5 = vague source; 3 = untraceable paraphrase; 0 = no source |
| **Typical failures** | Missing source_document; claim not in cited file; composite claim from multiple files without split |

Detail: [TRACEABILITY_STANDARD.md](TRACEABILITY_STANDARD.md).

---

END
