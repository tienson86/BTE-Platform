# Edge Cases

| Field | Value |
|-------|-------|
| Document | EDGE_CASES |
| Pack | PACK-01 Strength |
| Version | 1.0.0 |
| Status | DESIGN ONLY |

---

# 1. Purpose

This document lists Strength interpretation edge cases and the reusable handling rules for all future packs.

Edge cases are where calculators look confident and consultants become careful.

---

# 2. Global Handling Rules

For every edge case:

1. Record it in Mode A (Missing Data, Conflicts, or Alternative Analysis).
2. Do not invent data.
3. Do not silently pick the prettier class.
4. Customer Mode uses Insufficient Data or a bounded qualifier — never a fake complete story.
5. Do not skip Mode A because the case is ugly.

---

# 3. Strength Classification Edges

## 3.1 Boundary class

**Case:** Engine score or level sits near Strong/Balanced or Weak/Balanced.

**Mode A:** Lower confidence. Show neighbor alternative. Name the threshold-adjacent dimensions.

**Mode B:** Keep the engine class. Allow one leak-free qualifier that the standing is not extreme.

**Forbidden:** Flipping class to Balanced “to be safe” without engine support.

---

## 3.2 Engine has three classes, interpretation has five

**Case:** Strength Engine publishes only `strong` / `weak` / `balanced`.

**Mode A:** Map 1:1. Do not emit Very Strong / Very Weak.

**Mode B:** Same.

**Forbidden:** Upgrading Strong to Very Strong because the story feels dramatic.

---

## 3.3 Unknown or empty strength_level

**Case:** Engine failure, unmapped enum, or empty class.

**Mode A:** Final Conclusion = `unmapped`. Missing Data / error recorded.

**Mode B:** Insufficient Data for Conclusion and all dependent sections. No personality filler.

---

## 3.4 Extreme surplus or deficit

**Case:** Special exception or extreme published level = Very Strong / Very Weak.

**Mode A:** Trace the override. Alternative = ordinary class without override.

**Mode B:** Meaning and Challenges must carry the operating cost of extremity. Do not glorify or shame.

---

# 4. Evidence Edges

## 4.1 Season vs root conflict

**Case:** Đắc Lệnh supports Strong; roots support Weak (or the reverse).

**Mode A:** Conflict record. Show engine priority resolution. Confidence penalty.

**Mode B:** Narrate both lived sides without giving two classes. Example direction: real force exists, but it is not free — structure also leaks or lacks ground.

**Forbidden:** Picking only the side that matches a marketing tone.

---

## 4.2 Support and drain both large

**Case:** High support and high drain.

**Mode A:** Both polarities listed. Alternative likely Balanced. Boundary penalty.

**Mode B:** Meaning = force with leak. Recommendations = pacing, not “you are both Strong and Weak”.

---

## 4.3 No activated rules

**Case:** Matcher returns empty.

**Mode A:** Missing Data / engine empty evidence. Confidence experimental/low. Do not invent STR-IDs.

**Mode B:** Insufficient Data. Do not write a generic Strong/Weak essay.

---

## 4.4 Special exception vs ordinary scoring

**Case:** Special rule overrides level.

**Mode A:** Override trace is mandatory. Alternative = pre-override class.

**Mode B:** Explain the unusual operating mode in human language without saying “special exception rule fired”.

---

## 4.5 Void, clash, combination as strength factors

**Case:** A combination or void changes rooting or support.

**Mode A:** Show as strength influence, not as a Pattern conclusion.

**Mode B:** Describe the lived effect (support cancelled, force unstable). Do not start a Pattern lecture.

PACK-01 must not determine Pattern.

---

# 5. Missing Data Edges

## 5.1 Missing hour pillar

**Effect:** Hidden stems / some rooting / luck start may be incomplete.

**Mode A:** List `hour_pillar` missing. State whether natal class still stands.

**Mode B:** Keep natal class if engine published it without hour. Luck section likely Insufficient Data. Do not guess the hour.

---

## 5.2 Missing timezone / true solar time

**Effect:** Month or hour boundary may be wrong upstream. Interpretation does not “fix” calendar.

**Mode A:** Record upstream uncertainty if published. If not published, do not invent a calendar warning.

**Mode B:** Do not scare the customer with unverified time-boundary folklore.

---

## 5.3 Missing luck set

**Effect:** Section 7 cannot be filled.

**Mode A:** Missing Data for luck interaction. Natal confidence unchanged.

**Mode B:** Luck section = Insufficient Data. Other sections remain.

---

## 5.4 Missing temperature result

**Effect:** Temperature adjustment influence absent.

**Mode A:** Dimension `not_applicable` or `missing`.

**Mode B:** Do not discuss hot/cold as if known. Never leak token `hot`.

---

## 5.5 Gender or similar runtime attributes

**Case:** A downstream rule used gender internally.

**Mode A:** May list the field if it affected a published result.

**Mode B:** Never print `male` / `female` as raw tokens. Grammar may inflect. Strength class is not assigned by gender.

---

# 6. Luck Interaction Edges

## 6.1 Luck supports an already Strong Day Master

**Risk:** Overdrive, over-commitment, low receptivity increases.

**Mode B:** Advantages of the period + the avoid (do not take every load).

## 6.2 Luck weakens a Strong Day Master

**Meaning:** Correction period, not identity loss.

**Mode B:** You do not become a different person; you need more pacing and feedback.

## 6.3 Luck supports a Weak Day Master

**Meaning:** External feed; growth window.

**Mode B:** Use support. Do not assume the natal deficit vanished forever.

## 6.4 Luck weakens a Weak Day Master

**Meaning:** Protection of energy; environment choice matters more.

**Mode B:** No doom prophecy. Practical conservation and support-seeking.

## 6.5 Luck vs Useful God confusion

**Forbidden in PACK-01:** Treating “luck supports Day Master” as “luck is Useful God”.

Useful God is a later pack.

---

# 7. Language and Leak Edges

## 7.1 Internal token in a source sentence

If upstream interpretation text contains `strong`, Rule IDs, or dumps, Customer Mode must not pass them through.

Mode A may show the raw source as a contamination note.

## 7.2 Dictionary temptation

When authors do not know the person-specific meaning, they write definitions.

That is a defect, not an edge-case allowance.

## 7.3 Dual language residue

English labels inside Vietnamese customer body are defects.

---

# 8. Cross-Pack Boundary Edges

## 8.1 Strength wants to mention Useful God

Only if Useful God is already a published fact from its own engine.

PACK-01 may describe interaction (“this surplus needs a drain direction”) without naming an unpublished Useful God.

If Useful God is not published, do not name an element to “use”.

## 8.2 Strength wants to mention Pattern

Same rule. No Pattern determination inside PACK-01.

## 8.3 Report asks for one paragraph covering everything

Refuse at design level. Strength interpretation stays in its nine customer sections. Report may layout them; it may not collapse them into a fact label.

---

# 9. Reusable Edge Catalog for Future Packs

Every later pack MUST handle:

| Edge | Handling |
|------|----------|
| Boundary conclusion | Alternative + lower confidence |
| Empty matches | Insufficient Data |
| Override vs ordinary | Trace override; show pre-override alternative |
| Missing required field | Missing Data; no invention |
| Conflicting dimensions | Conflict record; leak-free lived synthesis |
| Missing time/luck | Block time section only when possible |
| Leak in upstream text | Strip for Mode B; note in Mode A |
| Cross-domain temptation | Do not determine other domains |

---

# 10. Non-Edges

These are not excuses to skip interpretation:

- “The customer is a beginner”
- “PDF space is small”
- “We already printed Strong in the header”
- “Validation Mode is too long”
- “AI can fill the gaps”

---

END
