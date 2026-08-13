# THEME_MODEL

| Field | Value |
|-------|-------|
| Schema | Commercial theme V1.0 |

---

## Theme record

| Field | Rule |
|-------|------|
| `theme_id` | `SCREAMING_SNAKE` · stable public id |
| `kind` | `operating` · `overlay` · `alias` |
| `customer_name` | Vietnamese consulting name · no jargon required |
| `job` | One sentence: what this consulting class *does* for the buyer |
| `never` | One sentence: failure mode if the wrong class is used |
| `binds_from` | Published CDR / capacity / structure signals only |
| `blocks` | All 9 Layer-2 blocks required |
| `aliases` | Optional other ids that must not get a second catalog |

---

## Block record (Layer 2)

Each theme fills every block with a **stance** (reusable intent), not a finished paragraph.

| Block id | Buyer question |
|----------|----------------|
| `identity` | Who am I in this class? |
| `career` | What kind of work / decision? |
| `relationship` | How do I meet others without losing the class? |
| `growth` | What does “better” mean here (not “bigger” by default)? |
| `stress` | What happens under pressure? |
| `leadership` | What authority looks like (or confidence, if child/parent later)? |
| `environment` | Which room fits? |
| `memory` | One repeatable close |
| `action` | One weekly move + one stop |

Stances use **you / bạn** patterns. No proper names. No CASE ids. No stems as the message.

---

## Variant record (Layer 3)

| Variant | Length | Voice |
|---------|--------|-------|
| `formal` | Full consulting | Calm, precise |
| `warm` | Full, closer | Human, still consultant |
| `premium` | Dense | High-trust, fewer words |
| `short` | 1–2 sentences / block | Scan / share card |

Variant changes **dressing**, not **class**. A CONSERVING short line must still conserve.

---

## Combination rule

```
primary (exactly one operating theme)
+ overlays (0–2)
+ variant (exactly one per deliverable)
```

If two operating themes are both published → `TENSION_HOLDER` overlay; do not pick a fake winner in Memory.

---

## Empty structure

If structure is published but has no customer phrase, **do not** emit “khung đã xác định trong lá số.”  
Use STABILIZER / FOLLOW_FRAME / STANDARD hold-frame stance, or omit the structure clause.

---

END
