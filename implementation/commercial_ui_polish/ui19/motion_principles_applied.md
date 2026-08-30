# UI-19 Motion principles applied

Motion explains state. It does not decorate, slow reading, or change information.

Source: `knowledge/ui_system/09_MOTION_SYSTEM.md` + UI-13 tokens.

## What this sprint may animate

| Category | Allowed | Implemented |
|----------|---------|-------------|
| Hover | Subtle elevation / border / background | Buttons, quiet link, thumb bar, luck nodes |
| Focus | Fast focus ring | `:focus-visible` + `--focus-ring` |
| Expand / collapse | Height + opacity | Mobile `[data-mobile-body]` |
| Content reveal | 2–3 elements | Priority, insight, interpretation lead |
| Navigation | Smooth anchors unless reduced motion | `html:has(.bte-cdash)` |
| Loading | Calm skeleton | Existing UI-14 skeleton; no new architecture |
| State change | Current luck node | One-shot opacity |
| Mobile sticky | Predictable bar / safe area | Thumb bar enter + `env(safe-area-inset-bottom)` |
| Visualization | One-time bar width; current node | Existing Five Elements width; luck current |

## What this sprint must not do

- Cascade every card on load
- Bounce, spring, glow, scale, parallax, scroll hijack, section snap
- Animate BaZi, Ten Gods, or ShenSha chips
- Loop decorative motion
- Change Narrative, Presentation, Runtime, Export, adapters, or hierarchy

## Token rule

Only `--motion-fast` (120ms), `--motion-normal` (200ms), `--motion-slow` (320ms), and `--motion-ease-out`.
