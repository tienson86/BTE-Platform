# Placeholder Engine

Placeholder *reference* infrastructure for Pack 03.

## Runtime modules

| Module | Role |
|--------|------|
| `resolver.py` | Resolve placeholder ids → refs + optional binding |
| `binder.py` | Bind opaque values to placeholder refs |
| `formatter.py` | Structural format (`raw` / `string` / `identity`) |
| `validator.py` | Validate refs, types, and bindings |
| `metadata.py` | Ref/value/binding/resolution models |
| `interface.py` | `PlaceholderEngineInterface` + default facade |

## Hard rules

- Only placeholder infrastructure
- No BaZi interpretation
- Context values are opaque key/value data only
