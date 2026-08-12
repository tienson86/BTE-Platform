# Alternative Analysis

| Field | Value |
|-------|-------|
| Document | ALTERNATIVE_ANALYSIS |
| Pack | PACK-01 Strength |
| Version | 1.0.0 |
| Status | DESIGN ONLY |

---

# 1. Purpose

Alternative Analysis shows which Strength class almost won, and why it lost.

Professional consultants do this.

Calculators do not.

---

# 2. Why Alternatives Are Mandatory

A single label hides uncertainty.

If the chart is Strong with a large drain, a reviewer must see that Balanced was the runner-up.

If the chart is deep Strong with no counter-evidence, the alternative may be tiny — it must still be stated or explicitly `none_plausible`.

Hiding the runner-up makes Customer Mode overconfident.

---

# 3. Visibility

| Mode | What is shown |
|------|----------------|
| Validation Mode | Class shares, reasons, near-miss rules |
| Customer Mode | At most a leak-free qualifier when the case is near a boundary |

Customers never see:

```text
Strong 92%
Balanced 8%
```

---

# 4. Primary and Alternatives

Exactly one primary class: the engine-mapped interpretation class.

Alternatives are other classes in the five-class set that remain plausible.

Typical Strength neighbors:

```text
Very Weak — Weak — Balanced — Strong — Very Strong
```

An alternative SHOULD be a neighbor unless a special exception jumps the scale.

Do not list all five classes on every case.

---

# 5. Share Model (Validation Mode)

Mode A may show percentage shares.

Rules:

1. Primary share equals Mode A confidence for the primary class, or a declared split that sums with alternatives in a documented way.
2. Alternative shares are residual plausibility, not a second scoring engine.
3. Shares are honest about uncertainty, not marketing.
4. Do not fabricate a long tail of 1% classes to look scientific.

Preferred shape:

```text
Primary:   Strong     92%
Runner-up: Balanced    8%
Others:    not plausible under current evidence
```

If two alternatives are truly live (rare):

```text
Primary:   Balanced   70%
Alt-1:     Strong     18%
Alt-2:     Weak       12%
```

Explain each.

---

# 6. Required Explanation

For each alternative:

1. Which evidence would have made it win
2. Which evidence prevented it
3. Whether missing data could revive it
4. Whether Customer Mode needs a bounded qualifier

Example (Validation Mode):

```text
Alternative: Balanced 8%
Would win if: drain were treated as equal to root support, or if one root were voided
Did not win because: season command + two roots remain dominant; level rule selected Strong
Missing data impact: none
Customer qualifier: optional mild “not extreme surplus”
```

---

# 7. When Alternative Is None

`none_plausible` is allowed when:

- required dimensions are complete
- polarities strongly agree
- no neighbor is near
- no special exception points elsewhere

Mode A must still write why alternatives are not plausible.

Silence is not allowed.

---

# 8. Special Exceptions

If a special rule overrides ordinary scoring:

- Primary = override class
- Alternative = the ordinary class that would have won without override
- Explanation must say the override is why

This is the most important alternative in Strength.

---

# 9. Customer Mode Translation

Only when Mode A says the case is near a boundary or has a material alternative.

Allowed:

> Nhật chủ thuộc nhóm Thân Vượng, nhưng không phải dạng dư lực đến mức không cần điều chỉnh.

Forbidden:

> Strong 92% Balanced 8%.
> Maybe you are actually Weak.
> The algorithm is unsure so here are three personalities.

If Mode A says `none_plausible`, Customer Mode states the class cleanly, without fake humility and without fake certainty words like “definitely destined”.

---

# 10. Forbidden Behaviors

- Changing the primary class because the alternative “sounds nicer”
- Showing alternatives that contradict the engine without labeling them as losing
- Using alternatives to smuggle Pattern or Useful God debate
- Giving the customer two contradictory life manuals
- Inventing an alternative to fill the section

---

# 11. Future Pack Reuse

Every later pack MUST show:

- one primary conclusion
- at least the strongest losing alternative, or `none_plausible` with why
- leak-free customer translation only when uncertainty is material

Examples:

| Pack | Primary | Typical alternative |
|------|---------|---------------------|
| Pattern | Follow | Reverse, if support is not extreme |
| Useful God | Wood | Fire, if temperature evidence competes |
| ShenSha | Active | Latent / not triggered |

---

END
