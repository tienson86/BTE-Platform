# Confidence Model

Levels match the Evidence Layer (KX-1B). Propagation modes are declarative.

| Situation | Typical mode |
|-----------|----------------|
| Evidence node copies bundle confidence | `declared` |
| Inference that only restates required evidence | `inherited` |
| Alternative not taken; distant year-stem style support | `reduced` |
| Contradiction node vs final conclusion | `conflicting` |
| Final conclusion with several supporting predecessors | `combined` (conservative: min rank of supporters) |

Specification only. Future confidence scoring services MUST document any numeric formula as a new framework MINOR/MAJOR — not hide it in engine code.
