# Test Strategy

| Field | Value |
|-------|-------|
| Document | TEST_STRATEGY |
| Version | 1.0.0 |
| Runtime now | None |

---

# 1. Future test families

| Family | Assert |
|--------|--------|
| Selection determinism | Two runs, identical NarrativePlan |
| Evidence gating | drain/luck/deep-root/class mismatch ineligible |
| Duplicate removal | synonym family → one representative |
| Conflict resolution | C1 both polarities in Why; no class flip |
| Priority | rule priority ≠ section order |
| Salience | generic persist < thin-root+control |
| Narrative budget | caps enforced; Conclusion never cut |
| Alternative analysis | shares Validation-only |
| Missing data | luck insufficient; not “no effect” |
| Claim traceability | every customer claim has ClaimTrace |
| Narrative ordering | WHY after CONCLUSION; REC has chain |

---

# 2. Fixture

CASE-0001 Strength Facts from prototype / calibration evidence.

Do not modify Golden Dataset analysis expected.

Do not add expert class to input.

---

# 3. Module tests only

When implemented: `pytest` for reasoning module only, unless the user asks for full suite.

---

END
