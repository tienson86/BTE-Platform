# ROOTING_DIAGNOSTIC

**Sprint:** PILOT-1H  
**Sources:** context_builder `_compute_root`, `02_root_rules.csv`

## Distinctions

| Distinction | Currently distinguished? | How |
|---|---|---|
| direct root | PARTIAL | hidden stem element match per branch counted |
| hidden root | PARTIAL | `Thong can tang can` if flat hidden only |
| multiple roots | YES | 1 / 2 / 3+ chi ladder |
| weak root | PARTIAL | only via lower ladder / tang can / vo can |
| seasonal root | NO separate | season scored apart from root |
| remote support | NO | not modeled as rooting |

## Loss

Which branches provide root is not published. Day-branch vs month-branch rooting is not separated. Root destroyed (xung) label exists in control rules but is rarely set by builder.

## Design implication

Profile should expose `rooting_state` with count, loci, and quality — without rewriting score in this sprint.
